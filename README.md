# 📊 Portfolio Risk Analyzer

An ML-powered investment portfolio analysis tool that provides real-time risk assessment, financial metrics calculation, and data-driven investment recommendations using interactive visualizations.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

### 📈 Real-Time Data Analysis
- Fetch live stock data from Yahoo Finance
- Support for US and international markets (NSE, BSE, etc.)
- Historical data analysis with customizable date ranges
- Interactive candlestick charts with zoom and pan

### 🎯 AI-Powered Risk Assessment
- **ML-based risk scoring algorithm** (0-100 scale)
- Multi-factor risk analysis (volatility, drawdown, Sharpe ratio)
- Risk classification: Low, Medium, High
- Visual risk gauge with color-coded indicators

### 💡 Investment Recommendations
- Data-driven BUY/HOLD/SELL recommendations
- Confidence levels and reasoning
- Risk-adjusted return analysis
- Suitability assessment for different investor profiles

### 📊 Financial Metrics
- **Sharpe Ratio**: Risk-adjusted return calculation
- **Volatility**: Annualized standard deviation
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Beta**: Market correlation (when market data available)
- **Total & Annualized Returns**: Performance metrics

### 🎨 Interactive Visualizations
- Professional candlestick price charts
- Risk assessment gauge (speedometer style)
- Radar chart for risk factor breakdown
- Responsive design with dark mode support

### 📥 Data Export
- Download historical data as CSV
- Export analysis reports
- Share-ready visualizations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SubramaniMokkala/portfolio-risk-analyzer.git
cd portfolio-risk-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open in browser**
- The app will automatically open at `http://localhost:8501`
- If not, navigate to the URL shown in terminal

---

## 💻 Usage

### Basic Analysis
1. Enter a stock ticker symbol (e.g., `AAPL`, `GOOGL`, `TSLA`)
2. Select date range (default: last 3 months)
3. Click **"Fetch Data"**
4. View comprehensive risk analysis and recommendations

### Ticker Symbol Formats
- **US Stocks**: `AAPL`, `GOOGL`, `MSFT`, `TSLA`
- **Indian Stocks (NSE)**: `RELIANCE.NS`, `TCS.NS`, `INFY.NS`
- **Indian Stocks (BSE)**: `RELIANCE.BO`, `TCS.BO`

### Example Analyses

**Low Risk Stock (Coca-Cola)**
```
Ticker: KO
Expected: Low volatility, stable returns, BUY/HOLD recommendation
```

**High Risk Stock (Tesla)**
```
Ticker: TSLA
Expected: High volatility, higher returns, SELL/HOLD recommendation
```

---

##  Project Structure

```
portfolio-risk-analyzer/
├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── data_collection.py      # Yahoo Finance API integration
│   └── risk_models.py          # ML risk assessment algorithms
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── .gitignore                 # Git ignore rules
└── LICENSE                     # MIT License
```

---

## 🧮 Risk Scoring Algorithm

Our proprietary risk scoring algorithm combines multiple financial metrics:

### Feature Weights
- **Volatility** (35%): Price fluctuation magnitude
- **Maximum Drawdown** (25%): Worst-case loss scenario
- **Sharpe Ratio** (-20%): Risk-adjusted returns (inverse)
- **Positive Days** (-20%): Frequency of gains (inverse)

### Risk Classification
- **0-30**: 🟢 Low Risk (Conservative investors)
- **30-60**: 🟡 Medium Risk (Balanced approach)
- **60-100**: 🔴 High Risk (Aggressive investors)

### Calculation Process
1. **Data Collection**: Fetch historical OHLCV data
2. **Feature Engineering**: Calculate returns, volatility, drawdowns
3. **Normalization**: Scale features to 0-100 range
4. **Weighted Scoring**: Apply feature weights
5. **Classification**: Assign risk level and recommendation

---

## 📊 Technologies Used

### Backend
- **Python 3.13**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **scikit-learn**: ML preprocessing and scaling

### Data Sources
- **yfinance**: Yahoo Finance API wrapper
- Real-time and historical stock data
- No API key required

### Frontend
- **Streamlit**: Interactive web framework
- **Plotly**: Interactive visualizations (charts, gauges)
- Responsive design with custom CSS

### Version Control
- **Git**: Source control
- **GitHub**: Remote repository hosting

---

## 🎓 Key Concepts Demonstrated

### Data Science Skills
-  Feature engineering from time-series data
-  Statistical analysis (mean, std, correlation)
-  Risk metrics calculation (Sharpe, Beta, Drawdown)
-  Data normalization and scaling

### Machine Learning
-  Weighted scoring algorithm (inspired by linear models)
-  Multi-factor risk classification
-  Decision system (recommendation engine)
-  Model interpretability (explainable AI)

### Software Engineering
-  Modular code architecture
-  Separation of concerns (data, models, UI)
-  Error handling and validation
-  Documentation and comments

### Financial Domain Knowledge
-  Portfolio theory (Sharpe ratio, volatility)
-  Risk management principles
-  Investment decision frameworks
-  Market data analysis

---

## 📚 Educational Value

This project demonstrates understanding of:

1. **Quantitative Finance**: Risk metrics, portfolio theory
2. **Data Science**: Feature engineering, statistical analysis
3. **Machine Learning**: Classification, scoring algorithms
4. **Software Development**: Clean code, modularity, documentation
5. **Full-Stack Development**: Backend + Frontend integration

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Subramani Mokkala**
- GitHub: [@SubramaniMokkala](https://github.com/SubramaniMokkala)
- LinkedIn: [www.linkedin.com/in/subramani-mokkala]
- Email: [subramanimokkala@gmail.com]

---

## 🙏 Acknowledgments

- Yahoo Finance for providing free financial data API
- Streamlit for the amazing web framework
- The open-source community for inspiring this project

---

## ⚠️ Disclaimer

**This tool is for educational purposes only. Not financial advice.**

- Always do your own research before investing
- Past performance does not guarantee future results
- Consult with a qualified financial advisor for investment decisions
- The creators are not responsible for any financial losses

---

## 📞 Support

If you found this project helpful, please ⭐ star the repository!

For questions or issues, please open an issue on GitHub.

---

**Thank You**
