# PlayStation Store Purchase Tracker

A Python tool to automatically fetch your PlayStation Store receipts, store purchase data, and visualize spending trends via a Streamlit dashboard. Fully Dockerized with secure ephemeral credentials.

---

## Features

- Connects to your Gmail using app passwords (2FA compatible)
- Automatically fetches PlayStation purchase receipts
- Extracts structured data: purchase date, game title, price, and currency
- Stores purchases in a local SQLite database
- Provides analytics:
  - Monthly and yearly spend
  - Average spend per purchase
  - Most expensive games
  - Cumulative spending trends
- Interactive Streamlit dashboard with login
- Dockerized for easy deployment and sharing

---

## Quick Start (Demo)

Try the dashboard instantly with sample data - **no setup required**!

```bash
# Install dependencies (one time)
pip install -e .

# Run the demo
python demo.py
```

Then click "View Demo" when the dashboard opens. Perfect for screenshots and testing!

**Docker:**
```bash
docker compose up ps_store_tracker_demo
```
Open http://localhost:8502

---

## Setup (Real Data)

1. **Clone the repo**

```bash
git clone https://github.com/Gonz4lex/ps_store_tracker.git
cd ps_store_tracker
```

2. **Configure Gmail**

Get an app password from [Google Account Settings](https://myaccount.google.com/apppasswords):
- Click "Select app" → "Mail"
- Click "Select device" → "Windows Computer" (or your device)
- Generate the password
- Copy it to `.env`:

```bash
cp .env.example .env
# Edit .env and paste your Gmail app password
```

3. **Run the app**

```bash
pip install -e .
streamlit run src/ps_store_tracker/app.py
```

Open http://localhost:8501 and log in with your email and app password.

**Docker:**
```bash
docker compose up ps_store_tracker
```

---

## Security

- Your email and app password are **never stored**. They are only used for the current session to fetch emails.
- Use a **Gmail app password** if your account has 2FA enabled.
- The demo mode uses synthetic data - no real credentials needed.


### Project Structure

```
ps_store_tracker/
├── README.md
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── CODE_OF_CONDUCT.md     # Community standards
├── SECURITY.md            # Security policy
├── CHANGELOG.md           # Version history
├── pyproject.toml         # Project configuration
├── uv.lock                # Dependency lock file
├── Dockerfile             # Container build
├── docker-compose.yml     # Multi-container setup
├── .env.example           # Environment template
├── data/                  # SQLite database (gitignored)
├── scripts/
│   ├── fetch_and_store.py     # CLI script to fetch emails
│   └── generate_demo_data.py   # Generate sample purchase data
├── .github/
│   ├── ISSUE_TEMPLATE/         # GitHub issue templates
│   └── PULL_REQUEST_TEMPLATE/  # PR template
├── demo.py                      # Quick demo launcher
└── src/ps_store_tracker/
    ├── app.py             # Streamlit dashboard app
    ├── fetch_email.py     # Gmail IMAP connection
    ├── parser.py          # Email receipt parsing
    ├── storage.py         # SQLite database operations
    ├── analytics.py       # Spending analytics
    ├── config.py          # Configuration & environment
    └── __init__.py
```

### Dependencies

- Python 3.10+
- `pandas`, `beautifulsoup4`, `lxml`, `streamlit`, `plotly`
- `imaplib` (standard library)
- `uv` for dependency management


### Notes

- The SQLite database is persisted via Docker volume (./data)
- Streamlit login credentials are ephemeral and not stored
- Modify parser.py if PlayStation changes the receipt email format
