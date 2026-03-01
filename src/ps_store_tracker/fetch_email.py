import imaplib
import email
from email.header import decode_header
from typing import List

import base64

IMAP_SERVER = "imap.gmail.com"

def connect_gmail(user: str, app_password: str):
    """Connect to Gmail via IMAP."""
    imap_conn = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap_conn.login(user, app_password)
    print("Email client successfully authenticated!")
    return imap_conn

def fetch_emails(imap_conn, label: str = '"[Gmail]/All Mail"', limit: int = None):
    """Fetch emails from a given label/folder, optionally limited to the latest `limit` messages."""
    status, _ = imap_conn.select(label)
    if status != "OK":
        raise Exception(f"Failed to select mailbox {label}")

    status, messages = imap_conn.search(None, 'FROM "PlayStation" SUBJECT "Gracias"')
    email_list = []

    if status != "OK":
        print("No messages found!")
        return email_list

    msg_nums = messages[0].split()
    
    # Take only the last `limit` messages if specified
    if limit is not None:
        msg_nums = msg_nums[-limit:]

    for num in msg_nums:
        status, msg_data = imap_conn.fetch(num, "(RFC822)")
        if status != "OK":
            continue
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        email_list.append(msg)

    print(f"Fetched {len(email_list)} purchase receipts.")
    return email_list

def get_email_body(msg) -> str:
    """Return the HTML or plain text content of an email, properly decoded."""
    html = None
    plain = None

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            charset = part.get_content_charset() or "utf-8"
            payload = part.get_payload(decode=True)

            if not payload:
                continue

            # Gmail sometimes sends base64 even if decode=True returns bytes
            cte = part.get("Content-Transfer-Encoding", "").lower()
            if cte == "base64":
                try:
                    payload = base64.b64decode(payload)
                except Exception:
                    pass

            try:
                text = payload.decode(charset, errors="ignore")
            except Exception:
                text = payload.decode("utf-8", errors="ignore")

            if ctype == "text/html":
                html = text
            elif ctype == "text/plain":
                plain = text
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            try:
                text = payload.decode(charset, errors="ignore")
            except Exception:
                text = payload.decode("utf-8", errors="ignore")
            html = text

    return html or plain


