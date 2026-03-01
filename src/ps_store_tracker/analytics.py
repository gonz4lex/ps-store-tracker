import pandas as pd

def monthly_spending(df):
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    return df.groupby(df['date'].dt.to_period('M'))['price'].sum()

def yearly_spending(df):
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    return df.groupby(df['date'].dt.year)['price'].sum()

def average_spend(df):
    return df['price'].mean()

def most_expensive_games(df, top_n=5):
    return df.sort_values(by='price', ascending=False).head(top_n)

def cumulative_spending(df: pd.DataFrame, rolling_window: int = 3) -> pd.DataFrame:
    """Return cumulative spending with optional rolling smoothing."""
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df.dropna(subset=['date', 'price'])
    df = df.sort_values('date').copy()
    df['cumulative'] = df['price'].cumsum()
    df['cumulative_smooth'] = df['cumulative'].rolling(rolling_window, min_periods=1).mean()
    return df

def compute_kpis(df: pd.DataFrame):
    """Return average per purchase, monthly spend, yearly spend."""
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['date', 'price'])
    total_spent = df['price'].sum()
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
