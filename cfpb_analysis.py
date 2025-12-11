"""
CFPB Consumer Complaints - Analysis Examples
Python implementation

This module demonstrates various analyses you can perform on the CFPB
Consumer Complaint Database.

Updated: December 2025
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from cfpb_data import load_cfpb_api, get_data_summary, filter_complaints
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Analysis 1: Top Products and Issues
# =============================================================================

def analyze_top_products(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Analyze the most complained-about products.

    Args:
        df: DataFrame containing CFPB complaints
        top_n: Number of top products to return

    Returns:
        DataFrame with product counts

    Example:
        >>> df = load_cfpb_api(size=1000)
        >>> top_products = analyze_top_products(df)
        >>> print(top_products)
    """
    if 'Product' not in df.columns:
        raise ValueError("DataFrame must contain 'Product' column")

    product_counts = df['Product'].value_counts().head(top_n).reset_index()
    product_counts.columns = ['Product', 'Count']
    product_counts['Percentage'] = (product_counts['Count'] / len(df) * 100).round(2)

    return product_counts


def visualize_top_products(df: pd.DataFrame, top_n: int = 10):
    """
    Create a bar chart of top products.

    Args:
        df: DataFrame containing CFPB complaints
        top_n: Number of top products to display

    Returns:
        Plotly figure object
    """
    product_counts = analyze_top_products(df, top_n)

    fig = px.bar(
        product_counts,
        x='Count',
        y='Product',
        orientation='h',
        title=f'Top {top_n} Products by Complaint Count',
        labels={'Count': 'Number of Complaints', 'Product': ''},
        text='Count',
        color='Count',
        color_continuous_scale='Blues'
    )

    fig.update_layout(
        height=500,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )

    fig.update_traces(texttemplate='%{text:,}', textposition='outside')

    return fig


# =============================================================================
# Analysis 2: Geographic Distribution
# =============================================================================

def analyze_by_state(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Analyze complaints by state.

    Args:
        df: DataFrame containing CFPB complaints
        top_n: Number of top states to return

    Returns:
        DataFrame with state counts

    Example:
        >>> df = load_cfpb_api(size=1000)
        >>> state_analysis = analyze_by_state(df)
        >>> print(state_analysis)
    """
    if 'State' not in df.columns:
        raise ValueError("DataFrame must contain 'State' column")

    # Remove null states
    df_states = df[df['State'].notna()]

    state_counts = df_states['State'].value_counts().head(top_n).reset_index()
    state_counts.columns = ['State', 'Count']
    state_counts['Percentage'] = (state_counts['Count'] / len(df_states) * 100).round(2)

    return state_counts


def visualize_state_distribution(df: pd.DataFrame):
    """
    Create a choropleth map of complaints by state.

    Args:
        df: DataFrame containing CFPB complaints

    Returns:
        Plotly figure object
    """
    if 'State' not in df.columns:
        raise ValueError("DataFrame must contain 'State' column")

    # Count by state
    state_counts = df[df['State'].notna()]['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']

    fig = px.choropleth(
        state_counts,
        locations='State',
        locationmode='USA-states',
        color='Count',
        scope='usa',
        title='Consumer Complaints by State',
        labels={'Count': 'Number of Complaints'},
        color_continuous_scale='Reds'
    )

    fig.update_layout(
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        height=500
    )

    return fig


# =============================================================================
# Analysis 3: Company Response Analysis
# =============================================================================

def analyze_response_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze company response rates and timeliness.

    Args:
        df: DataFrame containing CFPB complaints

    Returns:
        DataFrame with response statistics

    Example:
        >>> df = load_cfpb_api(size=1000)
        >>> response_stats = analyze_response_rates(df)
        >>> print(response_stats)
    """
    stats = {}

    if 'Timely response?' in df.columns:
        timely = df['Timely response?'].value_counts()
        stats['Timely Response Rate'] = (
            timely.get('Yes', 0) / len(df) * 100
        )

    if 'Consumer disputed?' in df.columns:
        disputed = df['Consumer disputed?'].value_counts()
        stats['Dispute Rate'] = (
            disputed.get('Yes', 0) / len(df) * 100
        )

    if 'Company response to consumer' in df.columns:
        response_types = df['Company response to consumer'].value_counts()
        stats['Most Common Response'] = response_types.index[0] if len(response_types) > 0 else None

    return pd.DataFrame([stats])


def visualize_response_breakdown(df: pd.DataFrame):
    """
    Create a pie chart of company response types.

    Args:
        df: DataFrame containing CFPB complaints

    Returns:
        Plotly figure object
    """
    if 'Company response to consumer' not in df.columns:
        raise ValueError("DataFrame must contain 'Company response to consumer' column")

    response_counts = df['Company response to consumer'].value_counts()

    fig = px.pie(
        values=response_counts.values,
        names=response_counts.index,
        title='Company Response Breakdown',
        hole=0.3  # Donut chart
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)

    return fig


# =============================================================================
# Analysis 4: Time Series Analysis
# =============================================================================

def analyze_trends_over_time(df: pd.DataFrame, freq: str = 'M') -> pd.DataFrame:
    """
    Analyze complaint trends over time.

    Args:
        df: DataFrame containing CFPB complaints
        freq: Frequency for grouping ('D'=daily, 'W'=weekly, 'M'=monthly, 'Y'=yearly)

    Returns:
        DataFrame with time series data

    Example:
        >>> df = load_cfpb_api(size=5000, date_received_min="2023-01-01")
        >>> trends = analyze_trends_over_time(df, freq='M')
        >>> print(trends)
    """
    if 'Date received' not in df.columns:
        raise ValueError("DataFrame must contain 'Date received' column")

    df['Date received'] = pd.to_datetime(df['Date received'])

    # Group by time period
    time_series = df.groupby(pd.Grouper(key='Date received', freq=freq)).size()
    time_series = time_series.reset_index()
    time_series.columns = ['Date', 'Count']

    return time_series


def visualize_trends(df: pd.DataFrame, freq: str = 'M'):
    """
    Create a line chart of complaint trends over time.

    Args:
        df: DataFrame containing CFPB complaints
        freq: Frequency for grouping

    Returns:
        Plotly figure object
    """
    trends = analyze_trends_over_time(df, freq)

    freq_labels = {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly', 'Y': 'Yearly'}

    fig = px.line(
        trends,
        x='Date',
        y='Count',
        title=f'Complaint Trends Over Time ({freq_labels.get(freq, freq)})',
        labels={'Count': 'Number of Complaints', 'Date': ''}
    )

    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    return fig


# =============================================================================
# Analysis 5: Product-Specific Deep Dive
# =============================================================================

def analyze_product_issues(df: pd.DataFrame, product: str, top_n: int = 10) -> pd.DataFrame:
    """
    Analyze top issues for a specific product.

    Args:
        df: DataFrame containing CFPB complaints
        product: Product name to analyze
        top_n: Number of top issues to return

    Returns:
        DataFrame with issue counts for the product

    Example:
        >>> df = load_cfpb_api(size=1000)
        >>> credit_card_issues = analyze_product_issues(df, "Credit card")
        >>> print(credit_card_issues)
    """
    if 'Product' not in df.columns or 'Issue' not in df.columns:
        raise ValueError("DataFrame must contain 'Product' and 'Issue' columns")

    # Filter to specific product
    product_df = df[df['Product'] == product]

    if len(product_df) == 0:
        logger.warning(f"No complaints found for product: {product}")
        return pd.DataFrame()

    # Count issues
    issue_counts = product_df['Issue'].value_counts().head(top_n).reset_index()
    issue_counts.columns = ['Issue', 'Count']
    issue_counts['Percentage'] = (issue_counts['Count'] / len(product_df) * 100).round(2)

    return issue_counts


def compare_products(df: pd.DataFrame, products: list, metric: str = 'timely_response') -> pd.DataFrame:
    """
    Compare metrics across multiple products.

    Args:
        df: DataFrame containing CFPB complaints
        products: List of product names to compare
        metric: Metric to compare ('timely_response', 'dispute_rate', 'count')

    Returns:
        DataFrame with comparison data

    Example:
        >>> df = load_cfpb_api(size=5000)
        >>> comparison = compare_products(
        ...     df,
        ...     ["Credit card", "Mortgage", "Bank account or service"]
        ... )
        >>> print(comparison)
    """
    results = []

    for product in products:
        product_df = df[df['Product'] == product]

        if len(product_df) == 0:
            continue

        row = {'Product': product, 'Count': len(product_df)}

        if metric == 'timely_response' and 'Timely response?' in df.columns:
            timely = (product_df['Timely response?'] == 'Yes').sum()
            row['Timely Response Rate (%)'] = (timely / len(product_df) * 100).round(2)

        if metric == 'dispute_rate' and 'Consumer disputed?' in df.columns:
            disputed = (product_df['Consumer disputed?'] == 'Yes').sum()
            row['Dispute Rate (%)'] = (disputed / len(product_df) * 100).round(2)

        results.append(row)

    return pd.DataFrame(results)


# =============================================================================
# Main - Example Usage
# =============================================================================

if __name__ == "__main__":
    print("CFPB Consumer Complaints - Analysis Examples\n")

    # Load sample data
    print("Loading data from CFPB API...")
    df = load_cfpb_api(size=2000, date_received_min="2024-01-01")
    print(f"Loaded {len(df):,} complaints\n")

    # Analysis 1: Top Products
    print("=" * 80)
    print("Analysis 1: Top Products")
    print("=" * 80)
    top_products = analyze_top_products(df, top_n=5)
    print(top_products.to_string(index=False))

    # Analysis 2: State Distribution
    print("\n" + "=" * 80)
    print("Analysis 2: Top States")
    print("=" * 80)
    top_states = analyze_by_state(df, top_n=5)
    print(top_states.to_string(index=False))

    # Analysis 3: Response Rates
    print("\n" + "=" * 80)
    print("Analysis 3: Response Statistics")
    print("=" * 80)
    response_stats = analyze_response_rates(df)
    print(response_stats.to_string(index=False))

    # Analysis 4: Trends
    print("\n" + "=" * 80)
    print("Analysis 4: Monthly Trends")
    print("=" * 80)
    trends = analyze_trends_over_time(df, freq='M')
    print(f"Data points: {len(trends)}")
    print(trends.head(10).to_string(index=False))

    # Analysis 5: Product-specific
    print("\n" + "=" * 80)
    print("Analysis 5: Credit Card Issues")
    print("=" * 80)
    if 'Credit card' in df['Product'].values:
        credit_issues = analyze_product_issues(df, "Credit card", top_n=5)
        if not credit_issues.empty:
            print(credit_issues.to_string(index=False))
    else:
        print("No credit card complaints in this sample")

    print("\n" + "=" * 80)
    print("Analysis complete!")
    print("=" * 80)
