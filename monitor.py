from datetime import datetime, timedelta
import logging
from api_client import GuanabaraAPI
from database import Database
from notifier import TelegramNotifier
import time

logger = logging.getLogger(__name__)

class Monitor:
    def __init__(self, telegram_token=None, telegram_chat_id=None):
        self.api = GuanabaraAPI()
        self.db = Database()
        self.notifier = TelegramNotifier(telegram_token, telegram_chat_id)

    def generate_dates(self, start_date_str, end_date_str):
        """
        Generates a list of dates between start and end date (inclusive).
        Dates must be in 'YYYY-MM-DD' format.
        """
        start = datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        date_list = []
        current = start
        while current <= end:
            date_list.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        
        return date_list

    def check_availability(self, origin, destination, dates):
        """
        Checks for ID Jovem availability for a list of dates.
        Returns a list of NEW found opportunities (not previously detected).
        """
        new_opportunities = []
        
        logger.info(f"Checking availability for {len(dates)} dates...")
        
        for date in dates:
            trips_data = self.api.get_trips(origin, destination, date)
            
            # Check if trips key exists AND is not None
            if not trips_data or "trips" not in trips_data or trips_data["trips"] is None:
                logger.warning(f"No data for {date}")
                continue
                
            for trip in trips_data["trips"]:
                price = trip.get('price')
                original_price = trip.get('originalPrice')
                
                if price is not None and original_price:
                    # Calculate discount
                    # Sometimes price can be 0 (100% discount)
                    try:
                        discount = ((original_price - price) / original_price) * 100
                    except ZeroDivisionError:
                        discount = 0

                    is_id_jovem = False
                    benefit_type = None

                    if discount >= 95:
                        is_id_jovem = True
                        benefit_type = "100%"
                    elif discount >= 45 and discount <= 55:
                        is_id_jovem = True
                        benefit_type = "50%"
                    
                    if is_id_jovem:
                        # CHECK DUPLICATES
                        dep_date = trip.get('departureDateTime')
                        if not self.db.is_ticket_processed(dep_date, origin, destination, price):
                            opp = {
                                "date": dep_date,
                                "origin": trip.get('departureLocationName'),
                                "destination": trip.get('arrivalLocationName'),
                                "price": price,
                                "original_price": original_price,
                                "benefit": benefit_type,
                                "seats": trip.get('availableSeats')
                            }
                            new_opportunities.append(opp)
                            self.db.add_ticket(opp['date'], opp['origin'], opp['destination'], opp['price'], opp['benefit'])
                            logger.info(f"FOUND NEW! {opp['date']} - {opp['benefit']} - R$ {opp['price']}")
                        else:
                            logger.debug(f"Skipping duplicate: {dep_date}")
            
            # Simple rate limiting
            time.sleep(1) 
            
        return new_opportunities

    def run_check_cycle(self, origin, destination, start_date, end_date):
        """
        Runs a full check cycle, prints results, and sends notifications.
        """
        dates = self.generate_dates(start_date, end_date)
        new_tickets = self.check_availability(origin, destination, dates)
        
        if new_tickets:
            logger.info(f"Cycle complete. found {len(new_tickets)} NEW tickets.")
            
            # Prepare and send notification
            msg = f"🚌 *ID JOVEM ENCONTRADO!* ({len(new_tickets)} novas)\n\n"
            for t in new_tickets:
                # Parse date for better reading
                dt_obj = datetime.strptime(t['date'], "%Y-%m-%dT%H:%M:%S")
                fmt_date = dt_obj.strftime("%d/%m %H:%M")
                
                msg += f"📅 *{fmt_date}*\n"
                msg += f"🚩 {t['origin']} -> {t['destination']}\n"
                msg += f"🎫 Desconto: *{t['benefit']}*\n"
                msg += f"💰 Preço: R$ {t['price']:.2f}\n"
                msg += "----------------\n"
            
            self.notifier.send_message(msg)
            
        else:
            logger.info("Cycle complete. No new tickets found.")
            
        return new_tickets
