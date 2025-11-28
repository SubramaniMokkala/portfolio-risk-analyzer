# Portfolio Risk Analyzer Web Interface Using Streamlit

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Importing data collection module
from src.data_collection import get_stock_data, get_stock_info, validate_ticker

# Page Configuration
st.set_page_config(
    page_title="Portfolio Risk Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# custom css
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Helper functions

def plot_stock_chart(data, ticker_symbol):
    """Create an interactive candlestick chart"""
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name=ticker_symbol
    )])
    
    fig.update_layout(
        title=f'{ticker_symbol} Stock Price',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        template='plotly_white',
        height=500,
        hovermode='x unified'
    )
    
    return fig


def calculate_basic_metrics(data):
    """Calculate basic stock metrics"""
    metrics = {}
    metrics['current_price'] = data['Close'].iloc[-1]
    metrics['price_change'] = data['Close'].iloc[-1] - data['Close'].iloc[0]
    metrics['price_change_pct'] = (metrics['price_change'] / data['Close'].iloc[0]) * 100
    metrics['period_high'] = data['High'].max()
    metrics['period_low'] = data['Low'].min()
    metrics['avg_volume'] = data['Volume'].mean()
    return metrics

# Main app

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Portfolio Risk Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Analyze stocks with real-time data from Yahoo Finance")
    st.markdown("---")
    
    # Side bar for user inputs
    st.sidebar.header("🔧 Configuration")
    
    # Stock ticker input
    ticker_input = st.sidebar.text_input(
        "Enter Stock Ticker Symbol",
        value="AAPL",
        help="Examples: AAPL (Apple), GOOGL (Google), MSFT (Microsoft), RELIANCE.NS (Reliance India)"
    ).upper()
    
    # Date range selection
    st.sidebar.subheader("📅 Date Range")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        default_start = datetime.now() - timedelta(days=90)
        start_date = st.date_input(
            "Start Date",
            value=default_start,
            max_value=datetime.now()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    # Fetch button
    fetch_button = st.sidebar.button("📈 Fetch Data", type="primary", use_container_width=True)
    
    # Info section
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **💡 Tips:**
    - US stocks: AAPL, GOOGL, TSLA
    - Indian stocks: Add .NS (RELIANCE.NS)
    - Date range: Up to 5 years of data
    """)
    
    # Will fetch the data once button ic clicked
    
    if fetch_button:
        # Validate ticker first
        with st.spinner(f"🔍 Validating ticker {ticker_input}..."):
            if not validate_ticker(ticker_input):
                st.error(f"❌ Invalid ticker symbol: **{ticker_input}**")
                st.info("💡 Make sure you're using the correct format (e.g., AAPL, GOOGL, RELIANCE.NS)")
                st.stop()  # Use st.stop() instead of return
        
        # Fetch stock data
        with st.spinner(f"📡 Fetching data for {ticker_input}..."):
            data = get_stock_data(ticker_input, start_date, end_date)
            
            if data is None or data.empty:
                st.error(f"❌ No data found for {ticker_input} in the selected date range")
                st.info("💡 Try a different date range or check the ticker symbol")
                st.stop()
            
            # Store in session state
            st.session_state['stock_data'] = data
            st.session_state['ticker_symbol'] = ticker_input
            
            # Fetch company info
            with st.spinner("📋 Fetching company information..."):
                info = get_stock_info(ticker_input)
                st.session_state['stock_info'] = info
        
        st.success(f"✅ Successfully fetched {len(data)} days of data for **{ticker_input}**!")
    
    # Display if data available
    
    if 'stock_data' in st.session_state:
        data = st.session_state['stock_data']
        ticker = st.session_state['ticker_symbol']
        info = st.session_state.get('stock_info', {})
        
        # Company Info Header
        if info:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"## {info.get('longName', ticker)}")
                st.caption(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
            with col2:
                st.metric("Symbol", ticker)
            with col3:
                if 'marketCap' in info:
                    market_cap = info['marketCap'] / 1e9
                    st.metric("Market Cap", f"${market_cap:.2f}B")
        
        st.markdown("---")
        
        # Calculate and display metrics
        metrics = calculate_basic_metrics(data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current Price",
                f"${metrics['current_price']:.2f}",
                f"{metrics['price_change']:+.2f} ({metrics['price_change_pct']:+.2f}%)"
            )
        
        with col2:
            st.metric("Period High", f"${metrics['period_high']:.2f}")
        
        with col3:
            st.metric("Period Low", f"${metrics['period_low']:.2f}")
        
        with col4:
            st.metric("Avg Volume", f"{metrics['avg_volume']:,.0f}")
        
        st.markdown("---")
        
        # Plot chart
        st.subheader("📈 Price Chart")
        fig = plot_stock_chart(data, ticker)
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        st.subheader("📋 Raw Data")
        show_all = st.checkbox("Show all data", value=False)
        
        if show_all:
            st.dataframe(data, use_container_width=True)
        else:
            st.dataframe(data.tail(10), use_container_width=True)
            st.caption(f"Showing last 10 rows. Total: {len(data)} rows")
        
        # Download button
        csv = data.to_csv()
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"{ticker}_data_{start_date}_{end_date}.csv",
            mime="text/csv"
        )
    
    else:
        # Show welcome message when no data is loaded
        st.info("""
        👈 **Get Started:**
        1. Enter a stock ticker symbol in the sidebar
        2. Select your date range
        3. Click "Fetch Data" to analyze
        
        **Popular Tickers to Try:**
        - 🍎 AAPL (Apple)
        - 🔍 GOOGL (Google)
        - ⚡ TSLA (Tesla)
        - 💼 MSFT (Microsoft)
        - 🇮🇳 RELIANCE.NS (Reliance India)
        """)
        
        st.markdown("### 📊 Your chart will appear here")
        st.image("https://via.placeholder.com/800x400?text=Stock+Chart+Will+Appear+Here", use_column_width=True)


# Run app
if __name__ == "__main__":
    main()