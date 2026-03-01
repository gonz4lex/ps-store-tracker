"""Configuration and environment setup for PlayStation Store Tracker."""

from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

# Gmail Configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

# PlayStation Store Email Configuration
RECEIPT_SENDER = "do-not-reply@playstation.com"
RECEIPT_SUBJECT_KEYWORDS = ["Gracias por su compra"]  # Spanish: "Thank you for your purchase"


