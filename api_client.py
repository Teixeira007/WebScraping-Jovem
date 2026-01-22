import requests
import json
from datetime import datetime
import logging

# Configure basic logging logic is removed from library
logger = logging.getLogger(__name__)

class GuanabaraAPI:
    BASE_URL = "https://arara-core-proxy.gipsyy.com.br/app/sale/trips"
    
    # Headers default (extracted from test_api.py)
    DEFAULT_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1laWQiOiIzN2EyOTRmZS0zZjFiLTRhZjEtYjdjOS01NjM4ZDY2ZDEzMzkiLCJ1bmlxdWVfbmFtZSI6IklOVEVSIiwiSWRVc2VyIjoiMjUxNCIsIlRlbmFudCI6InNtYXJ0YnVzLWdhdGV3YXkiLCJDb21wYW5pZXMiOiIxfHIsMnxyLDN8ciw1fHIsNnxyLDR8ciwxMHxyLDEzfHIsMTF8ciwxNXx3LDE0fHciLCJuYmYiOjE3NjkwMDQyNzQsImV4cCI6MTgwMDU0MDI3NCwiaWF0IjoxNzY5MDA0Mjc0fQ.H1wHvKB0WZNoJmyrVeWcGy-yYKk3FTN1mGscBlTo4WQ",
        "content-type": "application/json",
        "identifierworkstation": "306C3125-CF50-40BA-AB8B-C2C2736E1629",
        "iduser": "2514",
        "origin": "https://www.viajeguanabara.com.br",
        "productid": "487a774c-0485-401f-84d2-61ed508becc3",
        "referer": "https://www.viajeguanabara.com.br/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def get_trips(self, origin, destination, date, seats=1):
        """
        Fetches trips for a given route and date.
        
        Args:
            origin (str): Origin city name (e.g., "Joao Pessoa - PB")
            destination (str): Destination city name (e.g., "Irece - BA")
            date (str): Date in ISO format (YYYY-MM-DD) or (YYYY-MM-DDT00:00:00.000Z)
            seats (int): Number of seats to search for.
            
        Returns:
            dict: JSON response from the API or None if failed.
        """
        # Ensure date format is correct for the API
        if "T" not in date:
            date = f"{date}T00:00:00.000Z"

        payload = {
            "departureLocationName": origin,
            "arrivalLocationName": destination,
            "isReturn": False,
            "departureDate": date,
            "seats": str(seats),
            "idBookingCouponRevalidation": None,
            "searchType": 2,
            "discountType": None,
            "isOpen": False,
            "passengers": [
                {
                    "idPassengerClassification": 13,
                    "quantity": seats
                }
            ]
        }
        
        logger.info(f"Searching trips: {origin} -> {destination} on {date}")
        
        try:
            response = self.session.post(self.BASE_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info("Request successful")
                return response.json()
            else:
                logger.error(f"Request failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {e}")
            return None
