"""
CFPB Consumer Complaints Database - Interactive Explorer
Python/Streamlit Application

This app provides an interactive interface for exploring and analyzing the
Consumer Financial Protection Bureau's consumer complaints database.

Data Source: https://www.consumerfinance.gov/data-research/consumer-complaints/
Updated: December 2025
"""

import streamlit as st
import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from cfpb_data import load_cfpb_api, get_data_summary
from cfpb_analysis import (
    analyze_top_products,
    analyze_by_state,
    analyze_response_rates,
    analyze_trends_over_time,
    analyze_product_issues,
    visualize_top_products,
    visualize_state_distribution,
    visualize_response_breakdown,
    visualize_trends
)

# Page configuration
st.set_page_config(
    page_title="CFPB Complaints Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS block removed for security reasons.
# The app now uses st.title and st.metric for display, which are safer alternatives.


@st.cache_data(ttl=3600)
def load_data(size, date_min, product_filter, state_filter):
    """Load data with caching (1 hour TTL)"""
    return load_cfpb_api(
        size=size,
        date_received_min=date_min,
        product=product_filter if product_filter != "All" else None,
        state=state_filter if state_filter != "All" else None
    )


def main():
    # Header
    st.title("📊 CFPB Consumer Complaints Explorer")

    st.markdown("""
    Explore and analyze consumer complaints submitted to the **Consumer Financial Protection Bureau (CFPB)**.
    This interactive dashboard provides insights into complaint patterns, company responses, and trends over time.
    """)

    # Sidebar - Data Loading Controls
    st.sidebar.header("⚙️ Data Controls")

    # Initialize session state for loading and filters
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    if 'filters' not in st.session_state:
        st.session_state.filters = {}

    # Callback to manage loading state
    def handle_load_data_click():
        st.session_state.loading = True
        st.session_state.filters = current_filters  # Update filters on load
        st.cache_data.clear()

    # Date range
    default_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    date_min = st.sidebar.date_input(
        "From Date",
        value=datetime.strptime(default_date, "%Y-%m-%d"),
        max_value=datetime.now()
    ).strftime("%Y-%m-%d")

    # Sample size
    sample_size = st.sidebar.select_slider(
        "Sample Size",
        options=[100, 500, 1000, 2000, 5000, 10000],
        value=1000,
        help="Number of complaints to load (larger = slower)"
    )

    # Filters
    st.sidebar.markdown("### 🔍 Filters")
    product_filter = st.sidebar.selectbox(
        "Product",
        ["All", "Credit card", "Mortgage", "Bank account or service",
         "Credit reporting", "Student loan", "Debt collection"],
        help="Filter by product type"
    )

    state_filter = st.sidebar.selectbox(
        "State",
        ["All", "CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"],
        help="Filter by state"
    )

    # Store current filter values
    current_filters = {
        "date_min": date_min,
        "sample_size": sample_size,
        "product_filter": product_filter,
        "state_filter": state_filter,
    }

    # Initialize session state with the first set of filters
    if not st.session_state.filters:
        st.session_state.filters = current_filters

    # Detect if filters have changed
    filters_changed = st.session_state.filters != current_filters

    # Load data button
    button_label = "Loading..." if st.session_state.loading else "🔄 Load Data"
    st.sidebar.button(
        button_label,
        type="primary",
        on_click=handle_load_data_click,
        disabled=st.session_state.loading,
        help="Click to fetch the latest data. The button is disabled while data is loading."
    )

    # Show a notification if filters have changed
    if filters_changed:
        st.sidebar.info("Filters have changed. Click 'Load Data' to apply.")

    # Load data and manage loading state
    try:
        with st.spinner("Loading CFPB complaint data..."):
            df = load_data(sample_size, date_min, product_filter, state_filter)

            if len(df) == 0:
                st.error("No data found with the selected filters. Try adjusting your criteria.")
                st.stop()  # Use st.stop() for a cleaner exit

    except Exception as e:
        logging.error(f"An error occurred during data loading: {e}", exc_info=True)
        st.error("An unexpected error occurred while loading the data.")
        st.info("The data source may be temporarily unavailable. Please try again later.")
        st.stop()
    finally:
        # Reset loading state at the end of every run
        st.session_state.loading = False

    # Data Summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Data Summary")
    st.sidebar.metric("Total Complaints", f"{len(df):,}")

    if 'Date received' in df.columns:
        date_range = f"{df['Date received'].min()} to {df['Date received'].max()}"
        st.sidebar.caption(f"📅 {date_range}")

    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "🏢 Products & Issues",
        "🗺️ Geographic",
        "📈 Trends",
        "📋 Raw Data"
    ])

    # TAB 1: Overview
    with tab1:
        st.header("Overview")

        # Key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Complaints", f"{len(df):,}")

        with col2:
            if 'Product' in df.columns:
                unique_products = df['Product'].nunique()
                st.metric("Product Types", f"{unique_products}")

        with col3:
            if 'Company' in df.columns:
                unique_companies = df['Company'].nunique()
                st.metric("Companies", f"{unique_companies}")

        with col4:
            if 'Timely response?' in df.columns:
                timely_pct = (df['Timely response?'] == 'Yes').sum() / len(df) * 100
                st.metric("Timely Response", f"{timely_pct:.1f}%")

        st.markdown("---")

        # Top products
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Products")
            if 'Product' in df.columns:
                fig = visualize_top_products(df, top_n=10)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Company Response Breakdown")
            if 'Company response to consumer' in df.columns:
                try:
                    fig = visualize_response_breakdown(df)
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.info("Not enough data for response breakdown")

        # Response statistics
        st.subheader("Response Statistics")
        response_stats = analyze_response_rates(df)

        if not response_stats.empty:
            cols = st.columns(len(response_stats.columns))
            for idx, col_name in enumerate(response_stats.columns):
                with cols[idx]:
                    value = response_stats[col_name].iloc[0]
                    if isinstance(value, (int, float)):
                        st.metric(col_name, f"{value:.1f}%")
                    else:
                        st.metric(col_name, value)

    # TAB 2: Products & Issues
    with tab2:
        st.header("Products & Issues Analysis")

        # Top products table
        st.subheader("Top Complaint Products")
        top_products = analyze_top_products(df, top_n=15)
        st.dataframe(top_products, use_container_width=True, hide_index=True)

        # Product-specific analysis
        st.markdown("---")
        st.subheader("Product Deep Dive")

        if 'Product' in df.columns:
            available_products = df['Product'].value_counts().head(10).index.tolist()
            selected_product = st.selectbox(
                "Select a product to analyze",
                available_products
            )

            if selected_product and 'Issue' in df.columns:
                col1, col2 = st.columns([2, 1])

                with col1:
                    issues = analyze_product_issues(df, selected_product, top_n=10)
                    if not issues.empty:
                        fig = px.bar(
                            issues,
                            x='Count',
                            y='Issue',
                            orientation='h',
                            title=f'Top Issues for {selected_product}',
                            text='Count',
                            color='Count',
                            color_continuous_scale='Reds'
                        )
                        fig.update_layout(
                            yaxis={'categoryorder': 'total ascending'},
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("#### Issue Statistics")
                    if not issues.empty:
                        for _, row in issues.head(5).iterrows():
                            st.metric(
                                row['Issue'][:30] + "..." if len(row['Issue']) > 30 else row['Issue'],
                                f"{row['Count']:,}",
                                f"{row['Percentage']:.1f}%"
                            )

    # TAB 3: Geographic
    with tab3:
        st.header("Geographic Distribution")

        if 'State' in df.columns:
            # Map
            st.subheader("Complaints by State")
            try:
                fig = visualize_state_distribution(df)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.info("Map visualization unavailable")

            # Top states
            col1, col2 = st.columns([2, 1])

            with col1:
                state_data = analyze_by_state(df, top_n=20)
                fig = px.bar(
                    state_data,
                    x='Count',
                    y='State',
                    orientation='h',
                    title='Top 20 States by Complaint Count',
                    text='Count',
                    color='Count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("#### Top States")
                st.dataframe(state_data.head(10), use_container_width=True, hide_index=True)

    # TAB 4: Trends
    with tab4:
        st.header("Trends Over Time")

        if 'Date received' in df.columns:
            # Frequency selector
            freq = st.radio(
                "Grouping",
                options=['D', 'W', 'M'],
                format_func=lambda x: {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly'}[x],
                horizontal=True
            )

            # Trend chart
            try:
                fig = visualize_trends(df, freq=freq)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                logging.error(f"Error creating trend chart: {e}", exc_info=True)
                st.error("An error occurred while creating the trend chart.")

            # Summary statistics
            st.subheader("Trend Statistics")
            trends = analyze_trends_over_time(df, freq=freq)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average per Period", f"{trends['Count'].mean():.0f}")
            with col2:
                st.metric("Peak Period", f"{trends['Count'].max():,}")
            with col3:
                st.metric("Data Points", f"{len(trends)}")

    # TAB 5: Raw Data
    with tab5:
        st.header("Raw Data")

        # Column selector
        if st.checkbox("Select specific columns"):
            available_cols = df.columns.tolist()
            selected_cols = st.multiselect(
                "Choose columns to display",
                available_cols,
                default=available_cols[:10] if len(available_cols) > 10 else available_cols
            )
            display_df = df[selected_cols] if selected_cols else df
        else:
            display_df = df

        # Display data
        st.dataframe(display_df, use_container_width=True)

        # Download button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"cfpb_complaints_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        # Data info
        with st.expander("📊 Data Information"):
            st.write(f"**Shape:** {display_df.shape[0]:,} rows × {display_df.shape[1]} columns")
            st.write(f"**Memory Usage:** {display_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            st.write("**Columns:**")
            st.write(display_df.dtypes)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About

    This app provides interactive analysis of the CFPB Consumer Complaints Database.

    **Data Source:** [CFPB](https://www.consumerfinance.gov/data-research/consumer-complaints/)

    **Updates:** Daily

    **Data Range:** 2011 - Present
    """)

    st.sidebar.info("""
    💡 **Tip:** Use filters to narrow down specific products, states, or time periods.
    Data is cached for 1 hour for better performance.
    """)


if __name__ == "__main__":
    main()
