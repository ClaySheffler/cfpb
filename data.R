# ============================================================================
# CFPB Consumer Complaint Database Data Loader
# Updated: December 2025
# ============================================================================
#
# This script loads the CFPB Consumer Complaint Database using the current
# official data sources. The old Socrata API endpoint is no longer available.
#
# Data Source: https://www.consumerfinance.gov/data-research/consumer-complaints/
# ============================================================================

# Option 1: Download from official CSV file (RECOMMENDED)
# -------------------------------------------------------
# The CFPB provides a complete dataset as a zipped CSV file, updated daily.
# This is the most straightforward method for getting all complaint data.

library(readr)

# Direct download URL for the complete complaints dataset (updated daily)
url <- "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"

# Download and read the data
# Note: This file is large (typically 100+ MB compressed, 500+ MB uncompressed)
temp_file <- tempfile(fileext = ".zip")
download.file(url, temp_file, mode = "wb")

# Read the CSV from the zip file
df <- read_csv(unz(temp_file, "complaints.csv"))

# Clean up temp file
unlink(temp_file)

# View basic info about the dataset
cat("CFPB Consumer Complaint Database loaded successfully!\n")
cat(sprintf("Total complaints: %s\n", format(nrow(df), big.mark = ",")))
cat(sprintf("Date range: %s to %s\n",
            min(df$`Date received`, na.rm = TRUE),
            max(df$`Date received`, na.rm = TRUE)))
cat(sprintf("Number of columns: %d\n", ncol(df)))


# Option 2: Use the CFPB API (for filtered queries)
# -------------------------------------------------
# The CFPB also provides a REST API for more targeted queries.
# API Documentation: https://cfpb.github.io/api/ccdb/
#
# Example API usage (requires httr and jsonlite packages):
#
# library(httr)
# library(jsonlite)
#
# api_url <- "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
#
# # Example: Get 100 recent complaints in JSON format
# response <- GET(api_url, query = list(
#   format = "json",
#   size = 100,
#   sort = "created_date_desc"
# ))
#
# df_api <- fromJSON(content(response, "text"))$hits$hits
#
# # For CSV format:
# response_csv <- GET(api_url, query = list(
#   format = "csv",
#   size = 100,
#   date_received_min = "2024-01-01",
#   no_aggs = "true"
# ))
# df_csv <- read.csv(text = content(response_csv, "text"))


# Option 3: Data.gov Catalog
# --------------------------
# The dataset is also available on data.gov:
# https://catalog.data.gov/dataset/consumer-complaint-database
#
# This provides additional metadata and alternative access methods.


# ============================================================================
# Column Descriptions (as of 2024)
# ============================================================================
# Date received: Date the CFPB received the complaint
# Product: Type of product (Credit card, Mortgage, etc.)
# Sub-product: More specific product category
# Issue: The issue the consumer identified
# Sub-issue: More specific issue category
# Consumer complaint narrative: Consumer's description (if consented)
# Company public response: Company's optional public-facing response
# Company: Company complaint was sent to
# State: Consumer's state
# ZIP code: Consumer's ZIP code
# Tags: Special designations (Older American, Servicemember, etc.)
# Consumer consent provided?: Whether consumer agreed to publish narrative
# Submitted via: How complaint was submitted (Web, Referral, etc.)
# Date sent to company: Date CFPB sent to company
# Company response to consumer: How company responded
# Timely response?: Whether company responded in timely manner
# Consumer disputed?: Whether consumer disputed company's response
# Complaint ID: Unique identifier
# ============================================================================
