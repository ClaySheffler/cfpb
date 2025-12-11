# CFPB Data Visualization & Analysis Tools

This repository contains data visualization and analysis applications for government open data sources, including the CFPB Consumer Complaints Database and U.S. birth data patterns.

## 🚀 Quick Start

### Python Application (Current)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Friday 13th visualization app
streamlit run app.py

# Or use the CFPB data tools
python cfpb_data.py
```

### R Applications (Archived)

The original R/Shiny applications are available in `archive/r/`. See the [R Documentation](#r-applications-archived) section below.

## 📊 Current Applications

### Friday the 13th Effect Visualizer

An interactive web application exploring whether there's a statistically significant difference in U.S. births on Friday the 13th compared to other days.

**Features:**
- Interactive visualizations with multiple plot types (scatter, bar, line)
- Year range filtering (1969-1988)
- Multiple theme options for customization
- Real-time data filtering and calculation

### CFPB Consumer Complaints Analyzer

Tools for downloading, analyzing, and visualizing the Consumer Financial Protection Bureau's consumer complaints database.

**Features:**
- Direct CSV download (1.8+ million complaints)
- REST API integration for filtered queries
- Example analyses and visualizations
- Daily updated data

## 🔬 How It Works

### Friday the 13th Effect Application

#### Data Source
- **Dataset**: U.S. birth data from 1969-1988
- **Source**: CDC/NCHS and Social Security Administration
- **Fields**: Date, day of week, number of births

#### Algorithm

1. **Data Filtering**
   - Filter data by user-selected year range
   - Extract births on the 6th, 13th, and 20th of each month
   - These three dates provide statistical comparison (13th vs. control dates)

2. **Calculation**
   ```python
   # For each day of the week:
   avg_13th = mean(births on 13th)
   avg_control = mean(births on 6th and 20th)
   difference_ppt = ((avg_13th - avg_control) / avg_control) * 100
   ```

3. **Visualization**
   - Plot the percentage point difference by day of week
   - Highlight Friday to see if there's a "Friday the 13th effect"
   - Allow users to switch between scatter, bar, and line charts
   - Apply different themes for visual customization

#### Expected Results
Research has shown that births on Friday the 13th are typically lower than expected, possibly due to:
- Planned C-sections being scheduled on different dates
- Psychological factors affecting reported birth times
- Statistical variation in birth scheduling

### CFPB Data Tools

#### Data Pipeline

1. **Download**
   ```
   CFPB API/CSV → Download → Decompress → Parse
   ```

2. **Processing**
   - Clean and normalize data fields
   - Handle missing values
   - Parse dates and categorical variables

3. **Analysis Options**
   - Aggregate by product type, company, state
   - Time series analysis of complaint trends
   - Response rate and timeliness metrics
   - Geographic distribution visualization

#### API Integration

```python
# Fetch filtered data
response = requests.get(
    "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/",
    params={
        'format': 'csv',
        'size': 1000,
        'date_received_min': '2024-01-01',
        'product': 'Credit card'
    }
)
```

#### Data Schema
- **Date received**: When CFPB received the complaint
- **Product**: Type of financial product (Credit card, Mortgage, etc.)
- **Issue**: Consumer's main complaint
- **Company**: Company the complaint is about
- **State**: Consumer's state
- **Company response**: How company responded
- **Timely response?**: Whether response was timely
- **Consumer disputed?**: Whether consumer disputed the response

## 📁 Repository Structure

```
cfpb/
├── app.py                      # Main Streamlit application (Python)
├── cfpb_data.py                # CFPB data loading utilities (Python)
├── cfpb_analysis.py            # Analysis examples (Python)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── archive/
    └── r/                      # Archived R applications
        ├── app.R               # Friday 13th Shiny app
        ├── ui.R                # Socrata analyzer UI
        ├── server.R            # Socrata analyzer server
        ├── data.R              # CFPB data loader (R)
        ├── example_usage.R     # R usage examples
        ├── deployApp.R         # Deployment script
        ├── rbokeh.Rmd          # rbokeh experiments
        ├── rbokeh.nb.html      # Rendered notebook
        ├── cfpb.Rproj          # RStudio project
        └── rsconnect/          # Shiny deployment config
```

## 🐍 Python Implementation Details

### Technology Stack

- **Streamlit**: Web application framework (similar to Shiny)
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations (similar to Highcharter)
- **Requests**: HTTP library for API calls

### Why Python?

- **Broader ecosystem**: More data science and ML libraries
- **Easier deployment**: Better support for modern cloud platforms
- **Performance**: Faster for large datasets
- **Community**: Larger data science community
- **Integration**: Easier to integrate with other tools and APIs

### Differences from R Version

| Feature | R (Shiny) | Python (Streamlit) |
|---------|-----------|-------------------|
| Framework | Shiny | Streamlit |
| Charts | Highcharter | Plotly |
| Data manipulation | dplyr/tidyr | Pandas |
| Deployment | shinyapps.io | Streamlit Cloud, Docker, etc. |
| Syntax | Reactive programming | Top-to-bottom script |

## 📚 CFPB Consumer Complaints Database

### Data Source

The CFPB Consumer Complaints Database contains complaints about consumer financial products and services submitted to the Consumer Financial Protection Bureau.

- **Official Page**: https://www.consumerfinance.gov/data-research/consumer-complaints/
- **Updates**: Daily
- **Data Range**: 2011 - Present (2024-2025 data available)
- **Size**: 1.8+ million complaints (as of 2024-2025)
- **Format**: CSV, JSON, XML, Excel

### Accessing the Data

#### Option 1: Direct CSV Download (Recommended for bulk access)
```python
import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile

url = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"
response = requests.get(url)
with ZipFile(BytesIO(response.content)) as zip_file:
    with zip_file.open("complaints.csv") as csv_file:
        df = pd.read_csv(csv_file)
```

#### Option 2: REST API (Recommended for filtered queries)
```python
import requests
import pandas as pd

api_url = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
response = requests.get(api_url, params={
    'format': 'csv',
    'size': 1000,
    'date_received_min': '2024-01-01',
    'no_aggs': 'true'
})
df = pd.read_csv(pd.io.common.StringIO(response.text))
```

### API Documentation

- Main API Docs: https://cfpb.github.io/api/ccdb/
- API Search Interface: https://cfpb.github.io/ccdb5-api/
- Data.gov Catalog: https://catalog.data.gov/dataset/consumer-complaint-database

### Example Analyses

The `cfpb_analysis.py` file includes:
- Top complaint products and issues
- Geographic distribution by state
- Company response rates and timeliness
- Time series trend analysis
- Product-specific deep dives

## 🔧 Requirements

### Python
```bash
pip install streamlit pandas plotly requests numpy
```

See `requirements.txt` for specific versions.

### R (for archived apps)
```r
install.packages(c("shiny", "shinythemes", "ggplot2", "highcharter",
                   "tidyr", "dplyr", "readr", "httr"))
```

## 🎯 Usage Examples

### Running the Friday 13th App

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Analyzing CFPB Data

```python
from cfpb_data import load_cfpb_data, load_cfpb_api

# Load full dataset (large)
df = load_cfpb_data()

# Or load filtered subset via API
df = load_cfpb_api(
    size=1000,
    product="Credit card",
    date_min="2024-01-01"
)

# Analyze
print(df['Product'].value_counts())
print(df.groupby('State').size().sort_values(ascending=False))
```

## 📈 Project History

1. **2016-2017**: Started as CFPB consumer complaints analyzer using Socrata API
2. **2017**: Evolved into general-purpose Socrata data exploration tool
3. **2018**: Added Friday the 13th birth data visualization (deployed to shinyapps.io)
4. **December 2025**:
   - Updated CFPB data access to use current official sources
   - Migrated from R/Shiny to Python/Streamlit
   - Archived original R code in `archive/r/`
   - Enhanced documentation with "How It Works" section

## 🔗 Deployment

### Original R/Shiny App
The original app is deployed at: https://sheffler.shinyapps.io/cfpb/

### Python/Streamlit App
Deploy to Streamlit Cloud, Heroku, or any Python hosting platform:

```bash
# Streamlit Cloud - just connect your GitHub repo
# or deploy locally/docker
streamlit run app.py
```

## R Applications (Archived)

The original R/Shiny applications have been moved to `archive/r/` but are fully functional.

### Files
- **app.R** - Friday the 13th Effect Shiny app
- **ui.R + server.R** - Interactive Socrata data analyzer
- **data.R** - CFPB data loading utilities
- **example_usage.R** - Complete usage examples

### Running R Apps
```r
# From archive/r/ directory
setwd("archive/r")
shiny::runApp("app.R")
```

## 📄 License

This is a personal learning/demo project exploring data visualization and government open data.

## 🤝 Contributing

Feel free to fork, experiment, and submit pull requests!

---

**Last Updated**: December 2025
**Maintainer**: sheffler
**Languages**: Python (current), R (archived)
