# ============================================================================
# Example: Using the CFPB Consumer Complaint Database
# ============================================================================
#
# This file demonstrates how to load and analyze CFPB complaint data
# using the updated data.R script.
#
# Updated: December 2025
# ============================================================================

# Required packages
# install.packages(c("readr", "dplyr", "ggplot2"))
library(readr)
library(dplyr)
library(ggplot2)

# ----------------------------------------------------------------------------
# Method 1: Load the complete dataset using data.R
# ----------------------------------------------------------------------------

source("data.R")

# The 'df' variable now contains all CFPB complaints
# Let's explore the data:

# View first few rows
head(df)

# Summary statistics
summary(df)

# Check column names
colnames(df)


# ----------------------------------------------------------------------------
# Method 2: Load a subset using the API (faster for testing)
# ----------------------------------------------------------------------------

library(httr)

# API endpoint
api_url <- "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"

# Example 1: Get recent complaints as CSV
response <- GET(api_url, query = list(
  format = "csv",
  size = 1000,                      # Get 1000 complaints
  date_received_min = "2024-01-01", # From 2024 onwards
  no_aggs = "true"                  # Skip aggregations for speed
))

# Read the CSV data
df_recent <- read.csv(text = content(response, "text", encoding = "UTF-8"))

cat(sprintf("Loaded %d recent complaints\n", nrow(df_recent)))


# Example 2: Filter by product type
response_mortgage <- GET(api_url, query = list(
  format = "csv",
  size = 500,
  product = "Mortgage",
  date_received_min = "2024-01-01",
  no_aggs = "true"
))

df_mortgage <- read.csv(text = content(response, "text", encoding = "UTF-8"))
cat(sprintf("Loaded %d mortgage complaints\n", nrow(df_mortgage)))


# ----------------------------------------------------------------------------
# Example Analysis: Top complaint products
# ----------------------------------------------------------------------------

# Count complaints by product
product_counts <- df_recent %>%
  count(Product, sort = TRUE) %>%
  head(10)

print(product_counts)

# Visualize top products
ggplot(product_counts, aes(x = reorder(Product, n), y = n)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(
    title = "Top 10 Products by Complaint Count (2024)",
    x = "Product",
    y = "Number of Complaints"
  ) +
  theme_minimal()


# ----------------------------------------------------------------------------
# Example Analysis: Complaints by state
# ----------------------------------------------------------------------------

state_counts <- df_recent %>%
  filter(!is.na(State)) %>%
  count(State, sort = TRUE) %>%
  head(10)

ggplot(state_counts, aes(x = reorder(State, n), y = n)) +
  geom_col(fill = "coral") +
  coord_flip() +
  labs(
    title = "Top 10 States by Complaint Count (2024)",
    x = "State",
    y = "Number of Complaints"
  ) +
  theme_minimal()


# ----------------------------------------------------------------------------
# Example Analysis: Timely response rate
# ----------------------------------------------------------------------------

response_summary <- df_recent %>%
  count(`Timely.response.`) %>%
  mutate(percentage = n / sum(n) * 100)

print("Timely Response Summary:")
print(response_summary)


# ----------------------------------------------------------------------------
# Using with the Socrata Data Analyzer (ui.R + server.R)
# ----------------------------------------------------------------------------
#
# The ui.R and server.R files create an interactive Shiny app for exploring
# any CSV data from Socrata or similar sources.
#
# To use with CFPB data:
#
# 1. Save a subset of complaints to CSV:
#    write.csv(df_recent, "cfpb_complaints_sample.csv", row.names = FALSE)
#
# 2. Host the CSV file on a web server or use a local file path
#
# 3. Run the Shiny app:
#    shiny::runApp()
#
# 4. Enter the CSV URL or use the CFPB API endpoint directly:
#    https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?format=csv&size=1000&no_aggs=true
#
# Note: The Shiny app (ui.R/server.R) can work with the API CSV output
# by using the API URL directly in the "URL to CSV" field.
#
# ============================================================================
