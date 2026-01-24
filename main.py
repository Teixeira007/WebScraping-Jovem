import time
import logging
from datetime import datetime
import argparse
from monitor import Monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Main")

def main():
    parser = argparse.ArgumentParser(description="Monitor ID Jovem Tickets")
    parser.add_argument("--origin", type=str, default="Joao Pessoa - PB", help="Origin city")
    parser.add_argument("--destination", type=str, default="Irece - BA", help="Destination city")
    parser.add_argument("--start", type=str, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--interval", type=int, default=15, help="Check interval in minutes")
    parser.add_argument("--once", action="store_true", help="Run only once and exit")
    
    parser.add_argument("--telegram-token", type=str, help="Telegram Bot Token")
    parser.add_argument("--telegram-chat-id", type=str, help="Telegram Chat ID")
    
    args = parser.parse_args()
    
    # Pass telegram credentials if they exist
    monitor = Monitor(telegram_token=args.telegram_token, telegram_chat_id=args.telegram_chat_id)
    
    logger.info("="*60)
    logger.info("ID JOVEM MONITOR STARTED")
    logger.info(f"Route: {args.origin} -> {args.destination}")
    logger.info(f"Period: {args.start} to {args.end}")
    logger.info(f"Interval: {args.interval} minutes")
    
    if args.telegram_token:
        logger.info("Telegram notification ENABLED")
    else:
        logger.info("Telegram notification DISABLED (no token provided)")
        
    logger.info("="*60)
    
    while True:
        try:
            logger.info("Starting check cycle...")
            start_time = time.time()
            
            # Run the check
            results = monitor.run_check_cycle(args.origin, args.destination, args.start, args.end)
            
            # Notification logic (placeholder for now)
            if results:
                logger.info(f"!!! FOUND {len(results)} TICKETS !!!")
                for ticket in results:
                    print(f"  >> {ticket['date']} | {ticket['benefit']} | {ticket['origin']} -> {ticket['destination']} | R$ {ticket['price']}")
                # Here we would send the Telegram message
            
            elapsed = time.time() - start_time
            logger.info(f"Check cycle finished in {elapsed:.2f} seconds.")
            
            if args.once:
                logger.info("One-time run check completed. Exiting.")
                break
                
            # Wait for next cycle
            logger.info(f"Waiting {args.interval} minutes for next check...")
            time.sleep(args.interval * 60)
            
        except KeyboardInterrupt:
            logger.info("Stopping monitor...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)

            if args.once:
                logger.info("Error occurred during one-time run. Exiting.")
                break

            time.sleep(60) 

if __name__ == "__main__":
    main()
