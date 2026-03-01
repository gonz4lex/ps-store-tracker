import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ps_store_tracker.fetch_email import connect_gmail, fetch_emails, get_email_body
from ps_store_tracker.parser import parse
from ps_store_tracker.storage import init_db, store_purchase
from ps_store_tracker.config import EMAIL_ADDRESS, APP_PASSWORD

def main():
    if not EMAIL_ADDRESS or not APP_PASSWORD:
        raise ValueError("EMAIL_ADDRESS and APP_PASSWORD must be set in .env file")
    
    init_db()
    
    imap_conn = connect_gmail(EMAIL_ADDRESS, APP_PASSWORD)
    emails = fetch_emails(imap_conn, label='"[Gmail]/All Mail"')  # Include archived
    
    for msg in emails:
        body = get_email_body(msg)
        purchase = parse(body)
        if purchase:
            store_purchase(purchase)
            print(f"Stored order {purchase['order_number']}")

    imap_conn.logout()

if __name__ == "__main__":
    main()
