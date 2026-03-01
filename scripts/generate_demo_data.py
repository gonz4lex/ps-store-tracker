"""Generate sample PlayStation Store purchase data for demo purposes.

This script creates realistic synthetic purchase data for the dashboard demo.
No real credentials or personal data are used.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add src to path
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from ps_store_tracker.storage import init_db, store_purchase

# Sample PlayStation games commonly purchased
SAMPLE_GAMES = [
    "Elden Ring",
    "Final Fantasy XVI",
    "Street Fighter 6",
    "Baldur's Gate 3",
    "Starfield",
    "Call of Duty: Modern Warfare III",
    "Hogwarts Legacy",
    "S.T.A.L.K.E.R. 2",
    "Dragon Age: The Veilguard",
    "Black Myth: Wukong",
    "Dragon's Dogma 2",
    "Tekken 8",
    "Like a Dragon: Infinite Wealth",
    "Metaphor: ReFantazio",
    "Star Wars Outlaws",
    "Indiana Jones and the Great Circle",
    "Alan Wake 2",
    "Cyberpunk 2077: Phantom Liberty",
]

SEASON_PASSES = [
    "Battle Pass - Season 1",
    "Battle Pass - Season 2",
    "Premium Season Pass",
    "Annual Pass",
]

DLC_CONTENT = [
    "Expansion Pack",
    "DLC Bundle",
    "Character Pack",
    "Cosmetic Bundle",
    "Soundtrack",
]


def generate_demo_purchases(num_purchases: int = 25) -> None:
    """Generate sample purchase data for dashboard demo.
    
    Args:
        num_purchases: Number of purchase orders to generate (default: 25).
    """
    print(f"Initializing database...")
    init_db()
    
    print(f"Generating {num_purchases} sample purchases...")
    
    # Generate dates spread over the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    for i in range(1, num_purchases + 1):
        # Random date within the range
        random_days = random.randint(0, 730)
        purchase_date = start_date + timedelta(days=random_days)
        date_str = purchase_date.strftime("%d/%m/%Y")
        
        # 70% chance of game purchase, 20% season pass, 10% DLC
        random_type = random.random()
        if random_type < 0.70:
            item_name = random.choice(SAMPLE_GAMES)
            price = round(random.uniform(29.99, 79.99), 2)
        elif random_type < 0.90:
            item_name = random.choice(SEASON_PASSES)
            price = round(random.uniform(9.99, 19.99), 2)
        else:
            item_name = random.choice(DLC_CONTENT)
            price = round(random.uniform(4.99, 24.99), 2)
        
        # Create purchase record
        purchase = {
            "order_number": f"PSN-{1000000 + i}",
            "date": date_str,
            "total": price,
            "items": [
                {"name": item_name, "price": price}
            ]
        }
        
        store_purchase(purchase)
        print(f"  ✓ {purchase['order_number']}: {item_name} - €{price:.2f} ({date_str})")
    
    print(f"\n✅ Successfully generated {num_purchases} demo purchases!")
    print("Run the app with DEMO=true to use this data.")


if __name__ == "__main__":
    # Optional: accept number of purchases as argument
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    generate_demo_purchases(num)
