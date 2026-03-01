import sys
from pathlib import Path

# Ensure "src" is in sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from ps_store_tracker.storage import init_db, store_purchase, load_purchases
from ps_store_tracker.analytics import (
    monthly_spending,
    yearly_spending,
    most_expensive_games,
    cumulative_spending,
    compute_kpis
)
from ps_store_tracker.fetch_email import connect_gmail, fetch_emails, get_email_body
from ps_store_tracker.parser import parse

# Initialize DB
init_db()

st.set_page_config(
    page_title="PlayStation Spending Tracker",
    page_icon=":video_game:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlit login
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("Login to PlayStation Tracker")
    st.info(
        "Enter your email and app password. "
        "If you don't have one, create it at https://myaccount.google.com/apppasswords."
    )
    username_input = st.text_input("Email")
    password_input = st.text_input("App Password", type="password")
    if st.button("Login"):
        if username_input and password_input:
            st.session_state['authenticated'] = True
            st.session_state['email'] = username_input
            st.session_state['password'] = password_input
            st.rerun()
        else:
            st.error("Please enter both email and password")
else:
    st.title("🎮 PlayStation Store Spending Tracker")

    # Auto-fetch emails once per session
    if 'fetched' not in st.session_state:
        try:
            # Connect to Gmail
            mail = connect_gmail(st.session_state['email'], st.session_state['password'])
            
            # Fetch all emails
            emails = fetch_emails(mail)
            total_emails = len(emails)
            new_count = 0

            progress_text = "Fetching and parsing PlayStation receipts..."
            progress_bar = st.progress(0, text=progress_text)

            for idx, email_msg in enumerate(emails, start=1):
                if idx > 2:
                    break
                print(f"Parsing {idx} of {total_emails} receipts...")
                content = get_email_body(email_msg)
                purchase = parse(content)
                if purchase:
                    print(f"Storing {idx}")
                    store_purchase(purchase)
                    new_count += 1
                
                # Update progress bar
                progress_bar.progress(idx / total_emails, text=f"{progress_text} ({idx}/{total_emails})")

            progress_bar.empty()  # clear bar once done
            st.session_state['fetched'] = True
            st.success(f"Fetched {new_count} new purchases!")

        except Exception as e:
            st.error(f"Failed to fetch emails: {e}")

    # Load purchases from DB
    df = load_purchases()
    if df.empty:
        st.warning("No purchases found.")
    else:
        st.header("Summary")
        
        avg_per_purchase, avg_monthly, avg_yearly = compute_kpis(df)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Monthly Average", f"${avg_monthly:.2f}")
        with c2:
            st.metric("Yearly Average", f"${avg_yearly:.2f}")
        with c3:
            st.metric("Average per Purchase", f"${avg_per_purchase:.2f}")

        c4, c5 = st.columns(2)

        with c4:
            st.header("Monthly Spending")
            month_df = monthly_spending(df).reset_index()
            month_df['date'] = month_df['date'].dt.to_timestamp()
            st.bar_chart(
                month_df.rename(columns={'date':'Month', 'price':'Total'}).set_index('Month')
            )

        with c5:
            st.header("Yearly Spending")
            year_df = yearly_spending(df).reset_index()
            st.bar_chart(
                year_df.rename(columns={'date':'Year', 'price':'Total'}).set_index('Year')
            )

        # st.header("Most Expensive Games")
        # st.dataframe(most_expensive_games(df))

        st.header("Cumulative Spending Over Time")
        cum_df = cumulative_spending(df)

        # Ensure 'date' is datetime
        cum_df['date'] = pd.to_datetime(cum_df['date'], dayfirst=True, errors='coerce')
        cum_df = cum_df.dropna(subset=['date', 'cumulative'])

        # Keep only the columns we want
        plot_df = cum_df[['date', 'cumulative']].rename(columns={'date': 'Date', 'cumulative': 'Total'})
        plot_df = plot_df.set_index('Date')

        st.line_chart(plot_df, )
