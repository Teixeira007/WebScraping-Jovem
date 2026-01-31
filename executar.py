import subprocess
import sys
import os
import time
from dotenv import load_dotenv

def run_check(origin, destination, start, end, token=None, chat_id=None):
    """
    Runs main.py for a specific route and date range.
    """
    cmd = [
        sys.executable, "main.py",
        "--origin", origin,
        "--destination", destination,
        "--start", start,
        "--end", end,
        "--once"
    ]
    
    if token:
        cmd.extend(["--telegram-token", token])
    
    if chat_id:
        cmd.extend(["--telegram-chat-id", chat_id])
        
    print(f"--- Running check: {origin} -> {destination} ({start} to {end}) ---")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        sys.exit(1)

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Retrieve Telegram credentials from environment variables if available
    # You can also hardcode them here if prefered, but environment variables are safer.
    # On Windows PowerShell: $env:TELEGRAM_TOKEN="your_token"; python executar.py
    telegram_token = os.environ.get("TELEGRAM_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not telegram_token:
        print("Warning: TELEGRAM_TOKEN not found in environment variables. Notifications might not work.")
    if not telegram_chat_id:
        print("Warning: TELEGRAM_CHAT_ID not found in environment variables.")

    # Define the checks to run
    checks = [
        {
            "origin": "Joao Pessoa - PB",
            "destination": "Irece - BA",
            "start": "2026-02-20",
            "end": "2026-04-13"
        },
        {
            "origin": "Irece - BA",
            "destination": "Joao Pessoa - PB",
            "start": "2026-03-01",
            "end": "2026-04-20" # Adjusted end date based on user request "2026-04-20"
        }
    ]

    print("Starting batch checks...")
    
    for i, check in enumerate(checks):
        run_check(
            origin=check["origin"],
            destination=check["destination"],
            start=check["start"],
            end=check["end"],
            token=telegram_token,
            chat_id=telegram_chat_id
        )
        
        # Add a small delay between checks to be nice to the API/system
        if i < len(checks) - 1:
            print("Waiting 5 seconds before next check...")
            time.sleep(5)
            
    print("All checks completed.")

if __name__ == "__main__":
    main()
