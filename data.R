library("RSocrata")

url <- "https://data.consumerfinance.gov/resource/jhzv-w97w?$$app_token=Q1VMXVriKOA9ySDVQkn5Lssfm"
df <- read.socrata(url)