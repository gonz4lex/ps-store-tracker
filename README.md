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

## Security

- Your email and app password are **never stored**. They are only used for the current session to fetch emails.
- Use a **Gmail app password** if your account has 2FA enabled.

---

## Setup

1. **Clone the repo**

```bash
git clone <repo_url>
cd ps_store_tracker
```

2. **Build the Docker image**

```bash
docker build -t ps_store_tracker .
```

3. **Run the container**

```bash
docker run -p 8501:8501 -v $(pwd)/data:/app/data ps_store_tracker
```

4. **Access the dashboard**

Open http://localhost:8501 and log in with your email and app password. Credentials are never saved.


### Project Structure

```
ps_store_tracker/
├── README.md
├── pyproject.toml
├── uv.lock
├── data/                  # SQLite DB
├── scripts/               
├── src/ps_store_tracker/  
│   ├── app.py             # Streamlit app
│   ├── email.py           # Email fetching
│   ├── parser.py          # Receipt parsing
│   ├── storage.py         # SQLite storage
│   ├── analytics.py       # Spending analysis
│   └── config.py          
└── tests/
```

### Dependencies

- Python 3.12

- `pandas`, `beautifulsoup4`, `lxml`, `streamlit`, `plotly`

- `imaplib` (standard library)

- `uv` for dependency management


### Notes

- The SQLite database is persisted via Docker volume (./data)
- Streamlit login credentials are ephemeral and not stored
- Modify parser.py if PlayStation changes the receipt email format
