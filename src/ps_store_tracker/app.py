"""PlayStation Store Spending Tracker Dashboard.

Interactive Streamlit dashboard for analyzing PS Store purchase history.
Can run in demo mode (with synthetic data) or with real Gmail data.
"""

import sys
import os
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

# Check if running in demo mode
DEMO_MODE = os.getenv("DEMO", "false").lower() == "true"

# Streamlit login/demo
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = DEMO_MODE  # Auto-auth in demo mode

if not st.session_state['authenticated']:
    st.title("Login to PlayStation Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Try Demo")
        st.write("Preview the dashboard with sample data - no setup required!")
        if st.button("View Demo", use_container_width=True, type="primary"):
            st.session_state['authenticated'] = True
            st.session_state['demo_mode'] = True
            st.rerun()
    
    with col2:
        st.subheader("🔐 Login with Gmail")
        st.write("Connect your PlayStation Store receipt history via Gmail.")
        st.info(
            "**How to set up:**\n"
            "1. Go to https://myaccount.google.com/apppasswords\n"
            "2. Create an app password\n"
            "3. Enter your email and app password below"
        )
        username_input = st.text_input("Email")
        password_input = st.text_input("App Password", type="password")
        if st.button("Login", use_container_width=True):
            if username_input and password_input:
                st.session_state['authenticated'] = True
                st.session_state['email'] = username_input
                st.session_state['password'] = password_input
                st.session_state['demo_mode'] = False
                st.rerun()
            else:
                st.error("Please enter both email and password")

else:
    st.title("🎮 PlayStation Store Spending Tracker")
    
    # Set demo_mode if not already set
    if 'demo_mode' not in st.session_state:
        st.session_state['demo_mode'] = DEMO_MODE

    # Auto-fetch emails once per session (skip in demo mode)
    if 'fetched' not in st.session_state and not st.session_state['demo_mode']:
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
    
    # Mark as fetched in demo mode
    if st.session_state['demo_mode']:
        st.session_state['fetched'] = True
        if st.session_state.get('first_demo_load', True):
            st.info("📊 **Demo Mode** - Viewing sample PlayStation Store purchase data")
            st.session_state['first_demo_load'] = False

    # Load purchases from DB
    df = load_purchases()
    if df.empty:
        st.warning("No purchases found. Click refresh or add some data first.")
    else:
        st.header("Summary")
        
        avg_per_purchase, avg_monthly, avg_yearly = compute_kpis(df)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Monthly Average", f"€{avg_monthly:.2f}")
        with c2:
            st.metric("Yearly Average", f"€{avg_yearly:.2f}")
        with c3:
            st.metric("Average per Purchase", f"€{avg_per_purchase:.2f}")

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

        st.line_chart(plot_df)
