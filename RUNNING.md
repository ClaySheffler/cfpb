# Running the CFPB Consumer Complaints Explorer

This guide shows you how to run the CFPB dashboard application locally or deploy it online.

## 🚀 Option 1: Run Locally (Recommended for Testing)

### Step 1: Install Dependencies

```bash
cd /home/user/cfpb
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install streamlit pandas plotly requests numpy
```

### Step 2: Run the App

```bash
streamlit run app.py
```

### Step 3: View in Browser

- Streamlit will automatically open your browser to `http://localhost:8501`
- If it doesn't auto-open, manually navigate to that URL
- You'll see the CFPB Consumer Complaints Explorer dashboard

### Tips for Local Use

- The app will hot-reload when you save changes to `app.py`
- Press `Ctrl+C` in terminal to stop the server
- First load may take a moment while fetching data from CFPB API
- Data is cached for 1 hour to improve performance

### Quick Test Command

Want to test immediately? Run this all-in-one command:

```bash
cd /home/user/cfpb && \
pip install streamlit pandas plotly requests numpy && \
streamlit run app.py
```

---

## ☁️ Option 2: Deploy to Streamlit Cloud (Free!)

To make your app accessible online for anyone with the URL:

### Step 1: Ensure Code is on GitHub

Your code should already be pushed to GitHub. If not:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Visit **https://streamlit.io/cloud**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Configure deployment:
   - **Repository**: `ClaySheffler/cfpb`
   - **Branch**: `main` (or `claude/repo-overview-01B3kzjkijEWwjffqWycAo1z`)
   - **Main file path**: `app.py`
5. Click **"Deploy"**

### Step 3: Access Your Live App

Your app will be live at a URL like:
```
https://your-app-name.streamlit.app
```

### Benefits of Streamlit Cloud

- ✅ Free hosting
- ✅ Automatic HTTPS
- ✅ Updates automatically when you push to GitHub
- ✅ Easy sharing with others
- ✅ No server maintenance required

---

## 🐳 Option 3: Deploy with Docker

Perfect for production deployments or running in containers.

### Step 1: Create Dockerfile

Create a file named `Dockerfile` in the project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

### Step 2: Build Docker Image

```bash
docker build -t cfpb-app .
```

### Step 3: Run Docker Container

```bash
docker run -p 8501:8501 cfpb-app
```

### Step 4: Access the App

Open your browser to `http://localhost:8501`

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  cfpb-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

---

## 🎯 What to Expect When Running

### Initial Screen

When the app loads, you'll see:

1. **Header**: "📊 CFPB Consumer Complaints Explorer"
2. **Brief Description**: Explanation of the tool
3. **Sidebar Controls** (left side):
   - 📅 Date range picker (default: last 1 year)
   - 🎚️ Sample size slider (100-10,000 records)
   - 🔍 Product filter dropdown
   - 🗺️ State filter dropdown
   - 🔄 "Load Data" button

### Main Content Tabs

After loading data, explore 5 interactive tabs:

1. **📊 Overview**
   - Key metrics (total complaints, products, companies, response rate)
   - Top products bar chart
   - Company response breakdown pie chart
   - Response statistics

2. **🏢 Products & Issues**
   - Top 15 products table
   - Product selector for deep dive
   - Top 10 issues for selected product
   - Interactive visualizations

3. **🗺️ Geographic**
   - Interactive US choropleth map
   - Top 20 states bar chart
   - State-level statistics table

4. **📈 Trends**
   - Time series line chart
   - Daily/Weekly/Monthly grouping options
   - Trend statistics (average, peak, data points)

5. **📋 Raw Data**
   - Full dataset table (sortable, filterable)
   - Column selector
   - CSV download button
   - Data information (shape, memory usage, dtypes)

### First Use Instructions

1. **Select Filters** (in sidebar):
   - Choose date range (e.g., from 2024-01-01)
   - Select sample size (start with 1000 for quick testing)
   - Optionally filter by product or state

2. **Click "🔄 Load Data"**
   - Wait 5-10 seconds while data loads from CFPB API
   - Loading spinner will show progress

3. **Explore the Data**:
   - Navigate between tabs
   - Hover over charts for details
   - Click and drag to zoom
   - Use dropdowns to drill down

4. **Export Results**:
   - Go to "Raw Data" tab
   - Click "📥 Download as CSV"

---

## 🔧 Troubleshooting

### Import Errors

If you get errors like `ModuleNotFoundError`:

```bash
pip install --upgrade streamlit pandas plotly requests numpy openpyxl
```

### Port Already in Use

If port 8501 is already taken:

```bash
streamlit run app.py --server.port=8502
```

Then visit `http://localhost:8502`

### Slow Data Loading

If the CFPB API is slow or timing out:

- **Reduce sample size** to 100-500 records
- **Use filters** (product/state) to narrow the data
- **Wait longer** - first load can take 30-60 seconds
- **Check internet connection** - app requires API access

### Data Not Loading

If you see "Error loading data":

- The CFPB API may be temporarily unavailable
- Check your internet connection
- Try again in a few minutes
- Try with different date ranges or smaller sample sizes

### Memory Issues

If the app crashes with large datasets:

- Reduce sample size (don't exceed 10,000 for API calls)
- Clear cache: Click "🔄 Load Data" button to refresh
- Restart the Streamlit server

### Blank Visualizations

If charts don't display:

- Ensure data loaded successfully (check sidebar metrics)
- Try selecting different filters
- Check browser console for JavaScript errors
- Try a different browser (Chrome/Firefox recommended)

---

## 🌐 Running on a Remote Server

### Using SSH Tunnel

If running on a remote server, create an SSH tunnel:

```bash
ssh -L 8501:localhost:8501 user@remote-server
```

Then run the app on the remote server and access locally at `http://localhost:8501`

### Production Settings

For production deployment:

```bash
streamlit run app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=true
```

### Using systemd (Linux)

Create `/etc/systemd/system/cfpb-app.service`:

```ini
[Unit]
Description=CFPB Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/cfpb
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable cfpb-app
sudo systemctl start cfpb-app
sudo systemctl status cfpb-app
```

---

## 📊 Usage Tips

### Performance Optimization

1. **Start Small**: Begin with 100-500 records to test filters
2. **Use Filters**: Product/state filters reduce data volume
3. **Cache Benefit**: Second load is instant (1-hour cache)
4. **Date Ranges**: Shorter ranges = faster loading

### Best Practices

1. **Explore Incrementally**:
   - Start with Overview tab to understand the data
   - Use filters to narrow focus
   - Deep dive into specific products/states

2. **Export for Further Analysis**:
   - Download filtered datasets as CSV
   - Open in Excel/Pandas for custom analysis
   - Share specific views with stakeholders

3. **Regular Monitoring**:
   - Check daily for new complaints
   - Set up scheduled reports
   - Track trends over time

### Common Workflows

**Workflow 1: Product Analysis**
1. Filter by specific product (e.g., "Credit card")
2. Load 1,000-2,000 records
3. Check Products & Issues tab
4. Identify top complaint issues
5. Export data for deeper analysis

**Workflow 2: Geographic Research**
1. Filter by state (e.g., "CA")
2. Load 1,000 records
3. View Geographic tab
4. Compare with other states
5. Analyze regional patterns

**Workflow 3: Trend Monitoring**
1. Set date range (e.g., last 6 months)
2. Load 5,000+ records
3. View Trends tab
4. Toggle between Daily/Weekly/Monthly
5. Identify spikes or anomalies

---

## 🔐 Environment Variables (Optional)

For advanced configurations, create a `.streamlit/config.toml` file:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[browser]
gatherUsageStats = false
```

---

## 📞 Getting Help

### Common Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **CFPB API Docs**: https://cfpb.github.io/api/ccdb/
- **Project README**: See `README.md` for detailed documentation

### Reporting Issues

If you encounter problems:

1. Check this troubleshooting guide
2. Review the main README.md
3. Check Streamlit logs in terminal
4. Open a GitHub issue with:
   - Error message
   - Steps to reproduce
   - System information (OS, Python version)

---

## 🎉 You're Ready!

Choose your preferred method and start exploring CFPB consumer complaints data:

- **Quick Local Test**: `streamlit run app.py`
- **Online Deployment**: Streamlit Cloud (free)
- **Production**: Docker or systemd

Enjoy your data exploration! 📊

---

**Last Updated**: December 2025
**Requires**: Python 3.8+, Internet connection for CFPB API access
