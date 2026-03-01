from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

RECEIPT_SENDER = "do-not-reply@playstation.com"
RECEIPT_SUBJECT_KEYWORDS = ["Gracias por su compra"]

