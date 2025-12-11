"""
CFPB Consumer Complaint Database Data Loader
Python implementation

This module provides functions to load and process the CFPB Consumer Complaint
Database using current official data sources.

Data Source: https://www.consumerfinance.gov/data-research/consumer-complaints/
Updated: December 2025
"""

import pandas as pd
import requests
from io import BytesIO, StringIO
from zipfile import ZipFile
from typing import Optional, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Option 1: Direct CSV Download (RECOMMENDED for complete dataset)
# =============================================================================

def load_cfpb_data(cache: bool = True) -> pd.DataFrame:
    """
    Load the complete CFPB Consumer Complaint Database from official CSV file.

    The CFPB provides a complete dataset as a zipped CSV file, updated daily.
    This is the most straightforward method for getting all complaint data.

    Args:
        cache: If True, cache the downloaded data (default: True)

    Returns:
        pandas DataFrame containing all CFPB complaints

    Note:
        This file is large (typically 100+ MB compressed, 500+ MB uncompressed).
        Download may take several minutes depending on connection speed.

    Example:
        >>> df = load_cfpb_data()
        >>> print(f"Total complaints: {len(df):,}")
        >>> print(f"Date range: {df['Date received'].min()} to {df['Date received'].max()}")
    """
    url = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"

    logger.info("Downloading CFPB Consumer Complaint Database...")
    logger.info(f"URL: {url}")

    try:
        response = requests.get(url, timeout=300)  # 5 minute timeout
        response.raise_for_status()

        logger.info(f"Downloaded {len(response.content):,} bytes")
        logger.info("Extracting CSV from ZIP file...")

        # Extract and read CSV from ZIP
        with ZipFile(BytesIO(response.content)) as zip_file:
            # Get the CSV filename (should be complaints.csv)
            csv_filename = zip_file.namelist()[0]
            logger.info(f"Reading {csv_filename}...")

            with zip_file.open(csv_filename) as csv_file:
                df = pd.read_csv(csv_file)

        logger.info(f"✓ Successfully loaded {len(df):,} complaints")
        logger.info(f"✓ Columns: {len(df.columns)}")
        logger.info(f"✓ Date range: {df['Date received'].min()} to {df['Date received'].max()}")

        return df

    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading data: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise


# =============================================================================
# Option 2: REST API (RECOMMENDED for filtered queries)
# =============================================================================

def load_cfpb_api(
    size: int = 1000,
    format: str = 'csv',
    date_received_min: Optional[str] = None,
    date_received_max: Optional[str] = None,
    product: Optional[str] = None,
    company: Optional[str] = None,
    state: Optional[str] = None,
    **kwargs: Any
) -> pd.DataFrame:
    """
    Load CFPB complaints data using the REST API with optional filters.

    The CFPB provides a REST API for more targeted queries. This is much faster
    than downloading the complete dataset when you only need filtered data.

    Args:
        size: Number of records to retrieve (max varies by API)
        format: Response format ('csv' or 'json'), csv recommended
        date_received_min: Minimum date (YYYY-MM-DD format)
        date_received_max: Maximum date (YYYY-MM-DD format)
        product: Filter by product type (e.g., "Credit card", "Mortgage")
        company: Filter by company name
        state: Filter by state abbreviation (e.g., "CA", "NY")
        **kwargs: Additional API parameters

    Returns:
        pandas DataFrame containing filtered complaints

    Example:
        >>> # Get recent credit card complaints
        >>> df = load_cfpb_api(
        ...     size=1000,
        ...     product="Credit card",
        ...     date_received_min="2024-01-01"
        ... )
        >>> print(df['Product'].value_counts())

        >>> # Get complaints from California
        >>> df = load_cfpb_api(size=500, state="CA")

    API Documentation:
        https://cfpb.github.io/api/ccdb/
        https://cfpb.github.io/ccdb5-api/
    """
    api_url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

    # Build query parameters
    params = {
        'format': format,
        'size': size,
        'no_aggs': 'true'  # Skip aggregations for faster response
    }

    # Add optional filters
    if date_received_min:
        params['date_received_min'] = date_received_min
    if date_received_max:
        params['date_received_max'] = date_received_max
    if product:
        params['product'] = product
    if company:
        params['company'] = company
    if state:
        params['state'] = state

    # Add any additional parameters
    params.update(kwargs)

    logger.info(f"Fetching {size} complaints from CFPB API...")
    logger.info(f"Filters: {', '.join(f'{k}={v}' for k, v in params.items() if k not in ['format', 'size', 'no_aggs'])}")

    try:
        response = requests.get(api_url, params=params, timeout=60)
        response.raise_for_status()

        if format == 'csv':
            df = pd.read_csv(StringIO(response.text))
        else:  # json
            data = response.json()
            # API returns data in hits.hits structure
            if 'hits' in data and 'hits' in data['hits']:
                df = pd.json_normalize(data['hits']['hits'])
            else:
                df = pd.DataFrame(data)

        logger.info(f"✓ Successfully loaded {len(df):,} complaints")

        return df

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from API: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing API response: {e}")
        raise


# =============================================================================
# Data Processing Utilities
# =============================================================================

def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get a summary of the CFPB complaints data.

    Args:
        df: DataFrame containing CFPB complaints

    Returns:
        Dictionary with summary statistics

    Example:
        >>> df = load_cfpb_api(size=1000)
        >>> summary = get_data_summary(df)
        >>> print(f"Total complaints: {summary['total_complaints']:,}")
    """
    summary = {
        'total_complaints': len(df),
        'date_range': (
            df['Date received'].min() if 'Date received' in df.columns else None,
            df['Date received'].max() if 'Date received' in df.columns else None
        ),
        'num_columns': len(df.columns),
        'top_products': df['Product'].value_counts().head(5).to_dict() if 'Product' in df.columns else {},
        'top_states': df['State'].value_counts().head(5).to_dict() if 'State' in df.columns else {},
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
    }

    return summary


def filter_complaints(
    df: pd.DataFrame,
    product: Optional[str] = None,
    state: Optional[str] = None,
    date_start: Optional[str] = None,
    date_end: Optional[str] = None,
    timely_response: Optional[bool] = None
) -> pd.DataFrame:
    """
    Filter CFPB complaints DataFrame based on various criteria.

    Args:
        df: DataFrame containing CFPB complaints
        product: Filter by product type
        state: Filter by state
        date_start: Start date (YYYY-MM-DD)
        date_end: End date (YYYY-MM-DD)
        timely_response: Filter by timely response (True/False)

    Returns:
        Filtered DataFrame

    Example:
        >>> df = load_cfpb_data()
        >>> filtered = filter_complaints(
        ...     df,
        ...     product="Credit card",
        ...     state="CA",
        ...     date_start="2024-01-01"
        ... )
    """
    result = df.copy()

    if product and 'Product' in result.columns:
        result = result[result['Product'] == product]

    if state and 'State' in result.columns:
        result = result[result['State'] == state]

    if date_start and 'Date received' in result.columns:
        result['Date received'] = pd.to_datetime(result['Date received'])
        result = result[result['Date received'] >= date_start]

    if date_end and 'Date received' in result.columns:
        result['Date received'] = pd.to_datetime(result['Date received'])
        result = result[result['Date received'] <= date_end]

    if timely_response is not None and 'Timely response?' in result.columns:
        result = result[result['Timely response?'] == ('Yes' if timely_response else 'No')]

    logger.info(f"Filtered from {len(df):,} to {len(result):,} complaints")

    return result


# =============================================================================
# Column Information
# =============================================================================

COLUMN_DESCRIPTIONS = {
    'Date received': 'Date the CFPB received the complaint',
    'Product': 'Type of product (Credit card, Mortgage, etc.)',
    'Sub-product': 'More specific product category',
    'Issue': 'The issue the consumer identified',
    'Sub-issue': 'More specific issue category',
    'Consumer complaint narrative': "Consumer's description (if consented)",
    'Company public response': "Company's optional public-facing response",
    'Company': 'Company complaint was sent to',
    'State': "Consumer's state",
    'ZIP code': "Consumer's ZIP code",
    'Tags': 'Special designations (Older American, Servicemember, etc.)',
    'Consumer consent provided?': 'Whether consumer agreed to publish narrative',
    'Submitted via': 'How complaint was submitted (Web, Referral, etc.)',
    'Date sent to company': 'Date CFPB sent to company',
    'Company response to consumer': 'How company responded',
    'Timely response?': 'Whether company responded in timely manner',
    'Consumer disputed?': "Whether consumer disputed company's response",
    'Complaint ID': 'Unique identifier'
}


def print_column_info():
    """Print information about available columns in the dataset."""
    print("CFPB Consumer Complaints Database - Column Descriptions")
    print("=" * 80)
    for col, desc in COLUMN_DESCRIPTIONS.items():
        print(f"\n{col}")
        print(f"  {desc}")


# =============================================================================
# Main - Example Usage
# =============================================================================

if __name__ == "__main__":
    print("CFPB Consumer Complaint Database Data Loader\n")

    # Example 1: Load recent data via API
    print("=" * 80)
    print("Example 1: Loading recent complaints via API...")
    print("=" * 80)
    df_recent = load_cfpb_api(
        size=100,
        date_received_min="2024-01-01"
    )
    print(f"\nLoaded {len(df_recent)} complaints")
    print("\nTop 5 products:")
    print(df_recent['Product'].value_counts().head())

    # Example 2: Load filtered data
    print("\n" + "=" * 80)
    print("Example 2: Loading credit card complaints...")
    print("=" * 80)
    df_credit = load_cfpb_api(
        size=50,
        product="Credit card",
        date_received_min="2024-01-01"
    )
    print(f"\nLoaded {len(df_credit)} credit card complaints")

    # Example 3: Get data summary
    print("\n" + "=" * 80)
    print("Example 3: Data summary...")
    print("=" * 80)
    summary = get_data_summary(df_recent)
    print(f"\nTotal complaints: {summary['total_complaints']:,}")
    print(f"Date range: {summary['date_range'][0]} to {summary['date_range'][1]}")
    print(f"Memory usage: {summary['memory_usage_mb']:.2f} MB")

    # Print column information
    print("\n" + "=" * 80)
    print_column_info()
