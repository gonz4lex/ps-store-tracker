"""PlayStation Store receipt email parser.

This module parses HTML emails from PlayStation Store receipts and extracts
structured purchase data including order number, date, items, and total price.
"""

from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Any
import re


def parse(body: str) -> Optional[Dict[str, Any]]:
    """Parse PlayStation Store email HTML into structured purchase data.
    
    Extracts order number, purchase date, item details, and total price from
    the HTML body of a PlayStation Store receipt email.
    
    Args:
        body: HTML email body as a string.
        
    Returns:
        Dictionary containing:
            - order_number: Unique order identifier
            - date: Purchase date (format: dd/mm/yyyy)
            - items: List of dicts with 'name' and 'price' keys
            - total: Total purchase amount in EUR
        Returns None if parsing fails or required fields are missing.
        
    Note:
        This parser is designed for PlayStation Store emails in Spanish.
        It may need updates if the email format changes.
    """
    if not body:
        return None

    soup = BeautifulSoup(body, "html.parser")

    # --- Order number ---
    order_number = None
    order_div = soup.find(lambda tag: tag.name == "div" and "Número de pedido" in tag.get_text())
    if order_div:
        match = re.search(r"(\d+)", order_div.get_text())
        if match:
            order_number = match.group(1)

    # --- Date ---
    date = None
    date_div = soup.find(lambda tag: tag.name == "div" and "Fecha de compra" in tag.get_text())
    if date_div:
        match = re.search(r"Fecha de compra:\s*([\d/]+)", date_div.get_text())
        if match:
            date = match.group(1)

    # --- Items ---
    items: List[Dict] = []
    # Find the table with items (has header "Detalles" and "Precio")
    for table in soup.find_all("table"):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if "Detalles" in headers and "Precio" in headers:
            for row in table.find_all("tr"):
                # Skip header row
                if row.find("th"):
                    continue
                cols = row.find_all("td")
                if len(cols) < 3:
                    continue
                name = cols[0].get_text(strip=True)
                # Skip subtotal/other info rows
                if not name or any(x in name for x in ["Subtotal", "Total", "Impuestos"]):
                    continue
                # Price is empty in the product row; set None
                items.append({"name": name, "price": None})
            break

    # --- Total ---
    total = None
    total_span = soup.find(lambda tag: tag.name == "span" and "Total" in tag.get_text())
    if total_span:
        match = re.search(r"([\d.,]+)\s*€", total_span.get_text())
        if match:
            total = float(match.group(1).replace(".", "").replace(",", "."))

    if total is not None and len(items) == 1:
        items[0]["price"] = total

    if not order_number or not items:
        return None

    return {
        "order_number": order_number,
        "date": date,
        "items": items,
        "total": total,
    }
