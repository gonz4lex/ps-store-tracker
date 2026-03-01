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
    
    # Combine all item pools and shuffle to avoid duplicates
    all_items = [(name, price_range) for name, price_range in [
        *[(game, (29.99, 79.99)) for game in SAMPLE_GAMES],
        *[(pass_name, (9.99, 19.99)) for pass_name in SEASON_PASSES],
        *[(dlc, (4.99, 24.99)) for dlc in DLC_CONTENT],
    ]]
    
    # Shuffle and limit to num_purchases to avoid duplicates
    random.shuffle(all_items)
    selected_items = all_items[:min(num_purchases, len(all_items))]
    
    # Generate dates spread over the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    for i, (item_name, price_range) in enumerate(selected_items, start=1):
        # Random date within the range
        random_days = random.randint(0, 730)
        purchase_date = start_date + timedelta(days=random_days)
        date_str = purchase_date.strftime("%d/%m/%Y")
        
        # Random price within the range for this item type
        price = round(random.uniform(price_range[0], price_range[1]), 2)
        
        # Create purchase record
        purchase = {
            "order_number": f"PSN-{1000000 + i}",
            "date": date_str,
            "total": price,
            "items": [
                {"name": item_name, "price": price}
            ]
        }
        
        store_purchase(purchase, source="demo")
        print(f"  ✓ {purchase['order_number']}: {item_name} - €{price:.2f} ({date_str})")
    
    print(f"\n✅ Successfully generated {len(selected_items)} demo purchases!")
    print("Run the app with DEMO=true to use this data.")


if __name__ == "__main__":
    # Optional: accept number of purchases as argument
    num = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    generate_demo_purchases(num)
