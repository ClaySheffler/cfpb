# CFPB Consumer Complaints Database - Analysis Tools

Python-based tools for downloading, analyzing, and visualizing the Consumer Financial Protection Bureau's consumer complaints database.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the interactive web application
streamlit run app.py

# Or use the data tools directly in Python
python cfpb_data.py
python cfpb_analysis.py
```

## 📊 What This Does

This project provides comprehensive tools for analyzing consumer financial complaints submitted to the CFPB:

- **📈 Interactive Dashboard**: Streamlit web app for exploring complaints data
- **🔍 Data Loading**: Functions to download from official CFPB sources (CSV or API)
- **📊 Analysis Tools**: Pre-built analyses for products, geography, trends, and responses
- **🎨 Visualizations**: Interactive charts with Plotly for data exploration
- **💾 Export**: Download filtered datasets as CSV

## 🏗️ Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    CFPB Data Sources                         │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │  Official CSV        │    │  REST API            │      │
│  │  (Complete Dataset)  │    │  (Filtered Queries)  │      │
│  └──────────────────────┘    └──────────────────────┘      │
└─────────────────┬────────────────────┬───────────────────────┘
                  │                    │
                  ▼                    ▼
         ┌─────────────────────────────────────┐
         │      cfpb_data.py                   │
         │  ┌────────────────────────────┐    │
         │  │ load_cfpb_data()           │    │ Download & Parse
         │  │ load_cfpb_api()            │    │
         │  │ filter_complaints()        │    │ Clean & Filter
         │  └────────────────────────────┘    │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      cfpb_analysis.py               │
         │  ┌────────────────────────────┐    │
         │  │ analyze_top_products()     │    │ Aggregate
         │  │ analyze_by_state()         │    │
         │  │ analyze_response_rates()   │    │ Calculate
         │  │ analyze_trends_over_time() │    │
         │  │ analyze_product_issues()   │    │ Transform
         │  └────────────────────────────┘    │
         └──────────────┬──────────────────────┘
                        │
                        ▼
         ┌─────────────────────────────────────┐
         │      app.py (Streamlit)             │
         │  ┌────────────────────────────┐    │
         │  │ Interactive Dashboard      │    │ Visualize
         │  │ - Overview Tab             │    │
         │  │ - Products & Issues Tab    │    │ Interact
         │  │ - Geographic Tab           │    │
         │  │ - Trends Tab               │    │ Explore
         │  │ - Raw Data Tab             │    │
         │  └────────────────────────────┘    │
         └─────────────────────────────────────┘
```

### Data Pipeline

1. **Source Selection**
   - **Complete Dataset**: 100+ MB ZIP file with all complaints (1.8M+ records)
   - **API Endpoint**: Filtered queries for specific subsets

2. **Download & Extract**
   ```python
   # Option 1: Complete dataset
   response = requests.get("https://files.consumerfinance.gov/ccdb/complaints.csv.zip")
   with ZipFile(BytesIO(response.content)) as zip_file:
       df = pd.read_csv(zip_file.open("complaints.csv"))

   # Option 2: API with filters
   response = requests.get(api_url, params={'product': 'Credit card', 'size': 1000})
   df = pd.read_csv(StringIO(response.text))
   ```

3. **Processing & Analysis**
   - Clean data (handle nulls, parse dates)
   - Aggregate by dimensions (product, state, company, date)
   - Calculate metrics (response rates, trends, distributions)

4. **Visualization**
   - Interactive Plotly charts (bar, line, choropleth, pie)
   - Drill-down capabilities
   - Export functionality

## 📁 Project Structure

```
cfpb/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
│
├── app.py                      # 🎨 Interactive Streamlit dashboard
├── cfpb_data.py               # 📥 Data loading utilities
├── cfpb_analysis.py           # 📊 Analysis functions
│
├── .gitignore                 # Git ignore rules
│
└── archive/
    └── r/                     # Historical R/Shiny implementations
        ├── app.R              # Original Shiny apps
        ├── data.R             # R data loading
        └── [other R files]    # Legacy code
```

## 🔧 Components

### 1. Interactive Dashboard (`app.py`)

Full-featured Streamlit web application with:

**Features:**
- 📊 **Overview Tab**: Key metrics, top products, response breakdown
- 🏢 **Products & Issues**: Product analysis with drill-down capabilities
- 🗺️ **Geographic**: State-level choropleth maps and distributions
- 📈 **Trends**: Time series analysis (daily/weekly/monthly)
- 📋 **Raw Data**: Browse and download filtered datasets

**Controls:**
- Date range filtering
- Sample size selection (100 - 10,000 records)
- Product and state filters
- Dynamic data refresh

### 2. Data Loading (`cfpb_data.py`)

#### Functions

**`load_cfpb_data()`**
- Downloads complete CFPB dataset from official ZIP file
- ~500 MB uncompressed, 1.8M+ complaints
- Recommended for comprehensive analysis
- Cached to avoid repeated downloads

**`load_cfpb_api(size, date_received_min, product, state, ...)`**
- Queries CFPB REST API with filters
- Much faster for targeted analysis
- Supports all CFPB API parameters
- Returns filtered DataFrame

**`filter_complaints(df, product, state, date_start, date_end, ...)`**
- Post-load filtering for already-loaded data
- Multiple filter criteria support
- Efficient pandas-based filtering

**`get_data_summary(df)`**
- Returns summary statistics dictionary
- Date ranges, top products/states
- Memory usage information

### 3. Analysis Tools (`cfpb_analysis.py`)

#### Product Analysis
```python
from cfpb_analysis import analyze_top_products, analyze_product_issues

# Top complained-about products
top_products = analyze_top_products(df, top_n=10)

# Issues for specific product
credit_issues = analyze_product_issues(df, "Credit card", top_n=10)
```

#### Geographic Analysis
```python
from cfpb_analysis import analyze_by_state, visualize_state_distribution

# State-level counts
state_counts = analyze_by_state(df, top_n=20)

# Interactive choropleth map
fig = visualize_state_distribution(df)
fig.show()
```

#### Response Analysis
```python
from cfpb_analysis import analyze_response_rates

# Calculate timely response rate, dispute rate, etc.
response_stats = analyze_response_rates(df)
```

#### Time Series Analysis
```python
from cfpb_analysis import analyze_trends_over_time, visualize_trends

# Monthly trend data
trends = analyze_trends_over_time(df, freq='M')

# Interactive line chart
fig = visualize_trends(df, freq='M')
fig.show()
```

## 📊 CFPB Database Information

### Data Source

- **Official Page**: https://www.consumerfinance.gov/data-research/consumer-complaints/
- **Updates**: Daily (new complaints added continuously)
- **Data Range**: 2011 - Present
- **Current Size**: 1.8+ million complaints (as of December 2025)
- **Formats**: CSV, JSON, XML, Excel

### Data Schema

| Column | Description |
|--------|-------------|
| `Date received` | Date CFPB received the complaint |
| `Product` | Financial product type (Credit card, Mortgage, etc.) |
| `Sub-product` | More specific product category |
| `Issue` | Main issue identified by consumer |
| `Sub-issue` | More specific issue category |
| `Consumer complaint narrative` | Consumer's description (if consented) |
| `Company` | Company the complaint is about |
| `State` | Consumer's state |
| `ZIP code` | Consumer's ZIP code |
| `Company response to consumer` | How company responded |
| `Timely response?` | Whether company responded in timely manner |
| `Consumer disputed?` | Whether consumer disputed the response |
| `Complaint ID` | Unique identifier |

### Access Methods

#### Method 1: Direct CSV Download
**Best for:** Complete dataset analysis, offline work

```python
from cfpb_data import load_cfpb_data

df = load_cfpb_data()
# Downloads entire database (~500 MB)
```

**URL:** https://files.consumerfinance.gov/ccdb/complaints.csv.zip

#### Method 2: REST API
**Best for:** Filtered queries, specific analysis, faster loading

```python
from cfpb_data import load_cfpb_api

# Example: Recent credit card complaints from California
df = load_cfpb_api(
    size=1000,
    product="Credit card",
    state="CA",
    date_received_min="2024-01-01"
)
```

**Endpoint:** https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/

**API Parameters:**
- `size`: Number of records (default: 1000)
- `format`: Response format ('csv' or 'json')
- `date_received_min/max`: Date range (YYYY-MM-DD)
- `product`: Product type filter
- `company`: Company name filter
- `state`: State abbreviation (e.g., 'CA', 'NY')
- `no_aggs`: Skip aggregations for faster response

### API Documentation

- **Main API Docs**: https://cfpb.github.io/api/ccdb/
- **Search API**: https://cfpb.github.io/ccdb5-api/
- **Data.gov Catalog**: https://catalog.data.gov/dataset/consumer-complaint-database

## 💻 Usage Examples

### Example 1: Load and Explore Data

```python
from cfpb_data import load_cfpb_api

# Load recent complaints
df = load_cfpb_api(
    size=1000,
    date_received_min="2024-01-01"
)

# Basic exploration
print(f"Total complaints: {len(df):,}")
print("\nTop 5 products:")
print(df['Product'].value_counts().head())

print("\nTop 5 states:")
print(df['State'].value_counts().head())
```

### Example 2: Product Analysis

```python
from cfpb_data import load_cfpb_api
from cfpb_analysis import analyze_product_issues, visualize_top_products

# Load data
df = load_cfpb_api(size=5000)

# Analyze top products
fig = visualize_top_products(df, top_n=10)
fig.show()

# Deep dive into credit card complaints
credit_issues = analyze_product_issues(df, "Credit card")
print(credit_issues)
```

### Example 3: Geographic Analysis

```python
from cfpb_data import load_cfpb_api
from cfpb_analysis import visualize_state_distribution

# Load data
df = load_cfpb_api(size=2000, date_received_min="2024-01-01")

# Create interactive map
fig = visualize_state_distribution(df)
fig.show()
```

### Example 4: Trend Analysis

```python
from cfpb_data import load_cfpb_api
from cfpb_analysis import analyze_trends_over_time, visualize_trends

# Load data with date range
df = load_cfpb_api(
    size=10000,
    date_received_min="2023-01-01"
)

# Monthly trends
trends = analyze_trends_over_time(df, freq='M')
print(trends)

# Visualize
fig = visualize_trends(df, freq='M')
fig.show()
```

### Example 5: Company Response Analysis

```python
from cfpb_data import load_cfpb_api
from cfpb_analysis import analyze_response_rates, visualize_response_breakdown

# Load data
df = load_cfpb_api(size=1000)

# Response statistics
stats = analyze_response_rates(df)
print(stats)

# Response breakdown chart
fig = visualize_response_breakdown(df)
fig.show()
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cfpb
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - Or navigate manually to the URL shown in the terminal

### Dependencies

```
streamlit>=1.28.0    # Web application framework
pandas>=2.0.0        # Data manipulation
numpy>=1.24.0        # Numerical operations
plotly>=5.17.0       # Interactive visualizations
requests>=2.31.0     # HTTP requests
openpyxl>=3.1.0      # Excel file support (optional)
```

## 🎨 Visualization Examples

The tools generate several types of interactive visualizations:

- **Bar Charts**: Top products, states, issues
- **Pie/Donut Charts**: Response type breakdowns
- **Line Charts**: Trends over time
- **Choropleth Maps**: Geographic distribution
- **Tables**: Sortable, filterable data views

All visualizations are interactive (zoom, pan, hover) and exportable as PNG/SVG.

## 📦 Deployment

### Streamlit Cloud

```bash
# Deploy to Streamlit Cloud (free)
# 1. Push to GitHub
# 2. Visit https://streamlit.io/cloud
# 3. Connect your repository
# 4. Select app.py as main file
```

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t cfpb-app .
docker run -p 8501:8501 cfpb-app
```

### Local Production

```bash
# Run with production settings
streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true
```

## 🔍 Common Use Cases

### 1. Regulatory Compliance Monitoring
Track complaint volumes and response rates for your organization

### 2. Market Research
Analyze competitor complaint patterns and customer issues

### 3. Product Development
Identify common pain points and areas for improvement

### 4. Risk Assessment
Monitor trends in specific product categories or geographic regions

### 5. Academic Research
Study consumer financial behavior and regulatory effectiveness

## 📝 Project History

- **2016-2017**: Initial R/Shiny implementation with Socrata API
- **2018**: Added general-purpose Socrata data explorer
- **December 2025**:
  - Updated to current CFPB official data sources
  - Migrated from R/Shiny to Python/Streamlit
  - Enhanced with comprehensive analysis tools
  - Added interactive dashboard with multiple views
  - Improved documentation and examples

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional analysis functions
- More visualization types
- Performance optimizations
- Unit tests
- Additional data sources

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Resources

- **CFPB Consumer Complaints**: https://www.consumerfinance.gov/data-research/consumer-complaints/
- **CFPB API Docs**: https://cfpb.github.io/api/ccdb/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Plotly Docs**: https://plotly.com/python/
- **Pandas Docs**: https://pandas.pydata.org/docs/

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Last Updated**: December 2025
**Maintainer**: sheffler
**Language**: Python 3.8+
**Framework**: Streamlit
