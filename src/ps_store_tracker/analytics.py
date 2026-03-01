"""Spending analytics for PlayStation Store purchases.

This module provides functions to analyze purchase data including monthly/yearly
spending, averages, and cumulative trends.
"""

from typing import Tuple
import pandas as pd


def monthly_spending(df: pd.DataFrame) -> pd.Series:
    """Calculate total spending per month.
    
    Args:
        df: DataFrame with 'date' and 'total' columns (from load_orders).
        
    Returns:
        Series with month periods as index and total spending as values.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    return df.groupby(df['date'].dt.to_period('M'))['total'].sum()


def yearly_spending(df: pd.DataFrame) -> pd.Series:
    """Calculate total spending per year.
    
    Args:
        df: DataFrame with 'date' and 'total' columns (from load_orders).
        
    Returns:
        Series with years as index and total spending as values.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    return df.groupby(df['date'].dt.year)['total'].sum()


def average_spend(df: pd.DataFrame) -> float:
    """Calculate average spending per purchase.
    
    Args:
        df: DataFrame with 'price' column.
        
    Returns:
        Average price per transaction.
    """
    return df['price'].mean()


def most_expensive_games(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Get the most expensive items/games purchased.
    
    Args:
        df: DataFrame with 'item_price' column.
        top_n: Number of top items to return. Default is 5.
        
    Returns:
        DataFrame sorted by item_price (descending) with top_n rows.
    """
    return df.sort_values(by='item_price', ascending=False).head(top_n)


def cumulative_spending(df: pd.DataFrame, rolling_window: int = 3) -> pd.DataFrame:
    """Calculate cumulative spending with optional rolling average smoothing.
    
    Args:
        df: DataFrame with 'date' and 'total' columns (from load_orders).
        rolling_window: Window size for rolling average smoothing. Default is 3.
        
    Returns:
        DataFrame with added 'cumulative' and 'cumulative_smooth' columns.
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['total'] = pd.to_numeric(df['total'], errors='coerce')
    df = df.dropna(subset=['date', 'total'])
    df = df.sort_values('date')
    df['cumulative'] = df['total'].cumsum()
    df['cumulative_smooth'] = df['cumulative'].rolling(rolling_window, min_periods=1).mean()
    return df


def compute_kpis(df: pd.DataFrame) -> Tuple[float, float, float]:
    """Compute key performance indicators for spending analysis.
    
    Args:
        df: DataFrame with 'date' and 'total' columns (from load_orders).
        
    Returns:
        Tuple of (avg_per_purchase, avg_monthly, avg_yearly).
    """
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['date', 'total'])
    total_spent = df['total'].sum()
    total_purchases = len(df)
    avg_per_purchase = total_spent / total_purchases if total_purchases else 0

    if df.empty:
        return avg_per_purchase, 0, 0

    first_date, last_date = df['date'].min(), df['date'].max()
    total_days = (last_date - first_date).days + 1
    total_months = total_days / 30.44
    total_years = total_days / 365.25

    avg_monthly = total_spent / total_months if total_months > 0 else 0
    avg_yearly = total_spent / total_years if total_years > 0 else 0

    return avg_per_purchase, avg_monthly, avg_yearly
