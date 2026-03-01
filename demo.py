#!/usr/bin/env python
"""Quick demo launcher for PlayStation Store Tracker.

Run this script to instantly preview the dashboard with synthetic data.
No setup or credentials needed!

Usage:
    python demo.py
    # or
    ./demo.py (if executable)
"""

import sys
import os
import subprocess
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent.absolute()
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SRC_DIR = PROJECT_ROOT / "src"

# Add to path
sys.path.insert(0, str(SRC_DIR))

print("🎮 PlayStation Store Tracker Demo")
print("=" * 50)

# Generate demo data
print("\nGenerating sample data...")
try:
    from ps_store_tracker.storage import init_db, load_purchases
    
    # Check if data already exists
    init_db()
    df = load_purchases()
    
    if df.empty or len(df) < 20:
        print("   Creating 25 sample PlayStation purchases...")
        # Import and run the data generator
        from scripts.generate_demo_data import generate_demo_purchases
        generate_demo_purchases(25)
    else:
        print(f"   ✓ Found {len(df)} existing demo purchases")

except Exception as e:
    print(f"   ⚠️  Error generating data: {e}")
    print("   Continuing anyway...")

# Run Streamlit with demo mode
print("\n🚀 Launching dashboard...")
print("=" * 50)
print("\nThe dashboard will open at http://localhost:8501")
print("Click 'View Demo' to see the sample data!\n")

# Set demo environment variable and run streamlit
env = os.environ.copy()
env["DEMO"] = "true"  # Enable demo mode

try:
    subprocess.run(
        ["streamlit", "run", str(SRC_DIR / "ps_store_tracker" / "app.py")],
        env=env,
        cwd=str(PROJECT_ROOT)
    )
except KeyboardInterrupt:
    print("\n\n👋 Demo closed")
except FileNotFoundError:
    print("\n❌ Streamlit not found. Install with: pip install streamlit")
    sys.exit(1)
