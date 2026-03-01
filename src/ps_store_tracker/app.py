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
from ps_store_tracker.storage import init_db, store_purchase, load_purchases, load_orders
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

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
        if st.button("View Demo", width="stretch", type="primary"):
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
        if st.button("Login", width="stretch"):
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
        # Create centered spinner message
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            with st.spinner(""):
                st.markdown("""
                <div style="text-align: center; padding: 60px 20px;">
                    <h2 style="font-size: 2.5em; margin-bottom: 30px;">🔄</h2>
                    <h1 style="font-size: 2em; color: #1f77b4; margin-bottom: 20px;">Crunching your numbers...</h1>
                    <p style="font-size: 1.1em; color: #666;">Fetching and parsing PlayStation receipts...</p>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    # Connect to Gmail
                    mail = connect_gmail(st.session_state['email'], st.session_state['password'])
                    
                    # Fetch all emails
                    emails = fetch_emails(mail)
                    total_emails = len(emails)
                    new_count = 0

                    for idx, email_msg in enumerate(emails, start=1):
                        content = get_email_body(email_msg)
                        purchase = parse(content)
                        if purchase:
                            store_purchase(purchase, source="real")
                            new_count += 1

                    st.session_state['fetched'] = True
                    st.success(f"✅ Fetched {new_count} new purchases!")
                    st.rerun()

                except Exception as e:
                    st.session_state['fetched'] = True
                    st.error(f"Failed to fetch emails: {e}")
                    st.rerun()
    
    # Mark as fetched in demo mode
    if st.session_state['demo_mode']:
        st.session_state['fetched'] = True
        if st.session_state.get('first_demo_load', True):
            st.info("📊 **Demo Mode** - Viewing sample PlayStation Store purchase data")
            st.session_state['first_demo_load'] = False

    # Load purchases and orders from DB (use demo or real data based on mode)
    data_source = "demo" if st.session_state['demo_mode'] else "real"
    df_items = load_purchases(source=data_source)  # For raw data table (unique items)
    df_orders = load_orders(source=data_source)    # For analytics (spending calculations)
    
    if df_items.empty or df_orders.empty:
        st.warning("No purchases found. Click refresh or add some data first.")
    else:
        # Raw Data Table & Stats in side-by-side columns (at the top)
        col_table, col_stats = st.columns(2)

        with col_table:
            with st.expander("📊 Raw Data Table", expanded=False):
                st.dataframe(
                    df_items[['item_name', 'date', 'item_price']].rename(
                        columns={'item_name': 'Game', 'date': 'Date', 'item_price': 'Price (€)'}
                    ),
                    width="stretch",
                    hide_index=True
                )

        with col_stats:
            with st.expander("🎮 Purchase Statistics", expanded=False):
                # Sort items by date for first/latest
                df_sorted = df_items.copy()
                df_sorted['date'] = pd.to_datetime(df_sorted['date'], dayfirst=True, errors='coerce')
                df_sorted = df_sorted.dropna(subset=['date'])
                df_sorted = df_sorted.sort_values('date')

                # Most Expensive Item
                st.subheader("💰 Most Expensive Purchase")
                most_exp = df_items.nlargest(1, 'item_price').iloc[0]
                st.write(f"**{most_exp['item_name']}**")
                st.write(f"€{most_exp['item_price']:.2f}")

                # Cheapest Item
                st.subheader("💳 Cheapest Purchase")
                cheapest = df_items[df_items['item_price'] > 0].nsmallest(1, 'item_price').iloc[0]
                st.write(f"**{cheapest['item_name']}**")
                st.write(f"€{cheapest['item_price']:.2f}")

                # First Purchase
                st.subheader("🚀 First Purchase")
                first = df_sorted.iloc[0]
                st.write(f"**{first['item_name']}**")
                st.write(f"€{first['item_price']:.2f} ({first['date'].strftime('%d/%m/%Y')})")

                # Latest Purchase
                st.subheader("⏰ Latest Purchase")
                latest = df_sorted.iloc[-1]
                st.write(f"**{latest['item_name']}**")
                st.write(f"€{latest['item_price']:.2f} ({latest['date'].strftime('%d/%m/%Y')})")

        st.header("Summary")
        
        avg_per_purchase, avg_monthly, avg_yearly = compute_kpis(df_orders)

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
            month_df = monthly_spending(df_orders).reset_index()
            month_df['date'] = month_df['date'].dt.to_timestamp()
            st.bar_chart(
                month_df.rename(columns={'date':'Month', 'total':'Total'}).set_index('Month')
            )

        with c5:
            st.header("Yearly Spending")
            year_df = yearly_spending(df_orders).reset_index()
            st.bar_chart(
                year_df.rename(columns={'date':'Year', 'total':'Total'}).set_index('Year')
            )

        # st.header("Most Expensive Games")
        # st.dataframe(most_expensive_games(df_items))

        st.header("Cumulative Spending Over Time")
        cum_df = cumulative_spending(df_orders)

        # Ensure 'date' is datetime
        cum_df['date'] = pd.to_datetime(cum_df['date'], dayfirst=True, errors='coerce')
        cum_df = cum_df.dropna(subset=['date', 'cumulative'])

        # Keep only the columns we want
        plot_df = cum_df[['date', 'cumulative']].rename(columns={'date': 'Date', 'cumulative': 'Total'})
        plot_df = plot_df.set_index('Date')

        st.line_chart(plot_df)
