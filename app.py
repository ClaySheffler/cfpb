"""
Friday the 13th Effect - Interactive Visualization
Python/Streamlit implementation

This app visualizes whether there's a significant difference in U.S. births
on the 13th of each month compared to the 6th and 20th.

Data Source: CDC/NCHS, Social Security Administration
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="The Friday the 13th Effect",
    page_icon="📅",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    """Load birth data from CSV file or generate sample data"""
    data_path = Path("data/births.csv")

    if data_path.exists():
        df = pd.read_csv(data_path)
    else:
        # Generate sample data if file doesn't exist
        st.warning("⚠️ Data file not found. Using sample data for demonstration.")
        df = generate_sample_data()

    return df


def generate_sample_data():
    """Generate sample birth data for demonstration purposes"""
    import numpy as np

    np.random.seed(42)
    years = range(1969, 1989)
    months = range(1, 13)
    days = [6, 13, 20]
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday']

    data = []
    for year in years:
        for month in months:
            for day in days:
                for dow in days_of_week:
                    # Simulate slight decrease on Friday the 13th
                    base_births = 10000
                    if dow == 'Friday' and day == 13:
                        births = int(base_births * np.random.uniform(0.85, 0.95))
                    else:
                        births = int(base_births * np.random.uniform(0.95, 1.05))

                    data.append({
                        'year': year,
                        'month': month,
                        'date_of_month': day,
                        'day_of_week': dow,
                        'births': births
                    })

    return pd.DataFrame(data)


def calculate_diff(df, year_range):
    """
    Calculate the difference between births on 13th vs average of 6th and 20th

    Args:
        df: DataFrame with birth data
        year_range: Tuple of (min_year, max_year)

    Returns:
        DataFrame with differences by day of week
    """
    # Filter by year range
    filtered = df[df['year'].between(year_range[0], year_range[1])]

    # Filter to only 6th, 13th, and 20th
    filtered = filtered[filtered['date_of_month'].isin([6, 13, 20])]

    # Create day category
    filtered['day_category'] = filtered['date_of_month'].apply(
        lambda x: 'thirteen' if x == 13 else 'not_thirteen'
    )

    # Calculate mean births by day of week and category
    grouped = filtered.groupby(['day_of_week', 'day_category'])['births'].mean().reset_index()

    # Pivot to get thirteen and not_thirteen columns
    pivoted = grouped.pivot(index='day_of_week', columns='day_category', values='births').reset_index()

    # Calculate percentage point difference
    pivoted['diff_ppt'] = ((pivoted['thirteen'] - pivoted['not_thirteen']) /
                           pivoted['not_thirteen']) * 100

    # Ensure proper day ordering
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday']
    pivoted['day_of_week'] = pd.Categorical(pivoted['day_of_week'],
                                            categories=day_order,
                                            ordered=True)
    pivoted = pivoted.sort_values('day_of_week')

    return pivoted


def create_chart(data, plot_type, theme):
    """
    Create Plotly chart based on selected type and theme

    Args:
        data: DataFrame with diff_ppt column
        plot_type: Type of chart ('scatter', 'bar', 'line')
        theme: Color theme for the chart

    Returns:
        Plotly figure object
    """
    # Theme colors
    themes = {
        'No theme': {'bg': 'white', 'color': 'royalblue', 'grid': 'lightgray'},
        'Dark': {'bg': '#1e1e1e', 'color': '#00d9ff', 'grid': '#404040'},
        'Economist': {'bg': '#d5e4eb', 'color': '#01a2d9', 'grid': '#6794a7'},
        'FiveThirtyEight': {'bg': '#f0f0f0', 'color': '#008fd5', 'grid': '#cbcbcb'},
        'Plotly': {'bg': 'white', 'color': '#636efa', 'grid': '#e5ecf6'},
        'Seaborn': {'bg': '#eaeaf2', 'color': '#4c72b0', 'grid': '#ffffff'},
    }

    theme_config = themes.get(theme, themes['No theme'])

    # Create figure based on plot type
    if plot_type == 'scatter':
        fig = go.Figure(data=go.Scatter(
            x=data['day_of_week'],
            y=data['diff_ppt'],
            mode='markers',
            marker=dict(size=12, color=theme_config['color']),
            name='Difference, in ppt',
            hovertemplate='<b>%{x}</b><br>Difference: %{y:.4f} ppt<extra></extra>'
        ))
    elif plot_type == 'bar':
        fig = go.Figure(data=go.Bar(
            x=data['day_of_week'],
            y=data['diff_ppt'],
            marker_color=theme_config['color'],
            name='Difference, in ppt',
            hovertemplate='<b>%{x}</b><br>Difference: %{y:.4f} ppt<extra></extra>'
        ))
    else:  # line
        fig = go.Figure(data=go.Scatter(
            x=data['day_of_week'],
            y=data['diff_ppt'],
            mode='lines+markers',
            line=dict(color=theme_config['color'], width=2),
            marker=dict(size=8),
            name='Difference, in ppt',
            hovertemplate='<b>%{x}</b><br>Difference: %{y:.4f} ppt<extra></extra>'
        ))

    # Update layout
    fig.update_layout(
        title={
            'text': 'The Friday the 13th Effect',
            'font': {'size': 24, 'weight': 'bold'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Day of Week',
        yaxis_title='Difference, in ppt',
        plot_bgcolor=theme_config['bg'],
        paper_bgcolor=theme_config['bg'],
        height=500,
        hovermode='closest',
        showlegend=False,
        xaxis=dict(
            gridcolor=theme_config['grid'],
            showgrid=True
        ),
        yaxis=dict(
            gridcolor=theme_config['grid'],
            showgrid=True,
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='gray'
        )
    )

    return fig


# Main app
def main():
    # Title
    st.title("📅 The Friday the 13th Effect")

    # Load data
    births = load_data()

    # Get year range from data
    years = sorted(births['year'].unique())
    min_year, max_year = int(min(years)), int(max(years))

    # Sidebar controls
    st.sidebar.header("Controls")

    year_range = st.sidebar.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    plot_type = st.sidebar.selectbox(
        "Plot Type",
        options=['scatter', 'bar', 'line'],
        format_func=lambda x: x.capitalize()
    )

    theme = st.sidebar.selectbox(
        "Theme",
        options=['No theme', 'Dark', 'Economist', 'FiveThirtyEight',
                'Plotly', 'Seaborn']
    )

    # Info section
    st.markdown(f"""
    **Difference in the share of U.S. births on the 13th of each month from the
    average of births on the 6th and 20th**

    📊 **Years**: {year_range[0]} - {year_range[1]}

    💡 **How it works**: This visualization compares birth rates on the 13th of each month
    with the average of the 6th and 20th to detect any "Friday the 13th effect" - a phenomenon
    where births may be lower on Friday the 13th due to superstition affecting scheduled
    procedures or reporting.
    """)

    # Calculate differences
    diff_data = calculate_diff(births, year_range)

    # Create and display chart
    fig = create_chart(diff_data, plot_type, theme)
    st.plotly_chart(fig, use_container_width=True)

    # Data source
    st.caption("📈 Sources: CDC/NCHS, Social Security Administration")

    # Show raw data (expandable)
    with st.expander("📊 View Calculated Data"):
        st.dataframe(
            diff_data[['day_of_week', 'thirteen', 'not_thirteen', 'diff_ppt']]
            .rename(columns={
                'day_of_week': 'Day of Week',
                'thirteen': 'Avg Births (13th)',
                'not_thirteen': 'Avg Births (6th & 20th)',
                'diff_ppt': 'Difference (ppt)'
            }),
            hide_index=True
        )

    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### About

    This app explores whether there's a measurable difference in birth rates
    on Friday the 13th compared to other days.

    **Data**: U.S. birth records from CDC/NCHS and SSA

    **Method**: Compare births on the 13th with average of 6th and 20th
    of each month to control for day-of-month effects.
    """)


if __name__ == "__main__":
    main()
