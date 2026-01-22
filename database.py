import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name="tickets.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize the database with the necessary table."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS found_tickets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        origin TEXT,
                        destination TEXT,
                        price REAL,
                        benefit TEXT,
                        found_at DATETIME
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")

    def is_ticket_processed(self, date, origin, destination, price):
        """
        Check if a ticket with the same details has already been processed.
        Returns True if it exists, False otherwise.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 1 FROM found_tickets 
                    WHERE date = ? AND origin = ? AND destination = ? AND price = ?
                """, (date, origin, destination, price))
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            logger.error(f"Error checking ticket existence: {e}")
            return False

    def add_ticket(self, date, origin, destination, price, benefit):
        """Add a new ticket to the database."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                found_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO found_tickets (date, origin, destination, price, benefit, found_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (date, origin, destination, price, benefit, found_at))
                conn.commit()
                logger.info(f"Ticket saved to DB: {date} - {benefit}")
        except sqlite3.Error as e:
            logger.error(f"Error adding ticket: {e}")
