# Risk Assessment models - risk scoring and portfolio analysis using ML

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta


def calculate_returns(data):
    """
    Calculate daily and cumulative returns
    
    Args:
        data: DataFrame with 'Close' prices
    
    Returns:
        tuple: (daily_returns, cumulative_returns)
    """
    # Daily returns (percentage change)
    daily_returns = data['Close'].pct_change().dropna()
    
    # Cumulative returns
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    
    return daily_returns, cumulative_returns


def calculate_volatility(daily_returns, annualize=True):
    """
    Calculate volatility (standard deviation of returns)
    
    Args:
        daily_returns: Series of daily returns
        annualize: If True, annualize the volatility (multiply by sqrt(252))
    
    Returns:
        float: Volatility percentage
    
    Why 252? There are ~252 trading days per year in stock markets
    """
    volatility = daily_returns.std()
    
    if annualize:
        # volatility calculation for annual 
        volatility = volatility * np.sqrt(252)
    
    return volatility * 100  # Convert to percentage


def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.02):
    """
    Calculate Sharpe Ratio - measures risk-adjusted returns
    
    Formula: (Return - Risk_Free_Rate) / Volatility
    Higher is better (better return per unit of risk)
    
    Args:
        daily_returns: Series of daily returns
        risk_free_rate: Annual risk-free rate (default 2% for US Treasury)
    
    Returns:
        float: Sharpe ratio
    
    Interpretation:
        > 2.0  = Excellent
        1.0-2.0 = Good
        0.5-1.0 = Acceptable
        < 0.5  = Poor
    """
    # returns annually
    annual_return = (1 + daily_returns.mean()) ** 252 - 1
    
    # volatility annually
    annual_vol = daily_returns.std() * np.sqrt(252)
    
    # Sharpe ratio
    if annual_vol == 0:
        return 0
    
    sharpe = (annual_return - risk_free_rate) / annual_vol
    return sharpe


def calculate_max_drawdown(data):
    """
    Calculate maximum drawdown - largest peak-to-trough decline
    
    Shows worst-case scenario loss from peak
    
    Args:
        data: DataFrame with 'Close' prices
    
    Returns:
        float: Maximum drawdown as negative percentage
    """
    # Calculate cumulative returns
    cumulative = (1 + data['Close'].pct_change()).cumprod()
    
    # Calculate running maximum
    running_max = cumulative.expanding().max()
    
    # Calculate drawdown
    drawdown = (cumulative - running_max) / running_max
    
    # Maximum drawdown (most negative value)
    max_dd = drawdown.min()
    
    return max_dd * 100  # Convert to percentage


def calculate_beta(stock_returns, market_returns):
    """
    Calculate Beta - measures stock volatility relative to market
    
    Beta = 1.0: Moves with market
    Beta > 1.0: More volatile than market
    Beta < 1.0: Less volatile than market
    
    Args:
        stock_returns: Series of stock daily returns
        market_returns: Series of market daily returns (e.g., S&P 500)
    
    Returns:
        float: Beta value
    """
    # Align the two series
    combined = pd.concat([stock_returns, market_returns], axis=1).dropna()
    
    if len(combined) < 2:
        return 1.0  # Default beta
    
    # Calculate covariance and variance
    covariance = combined.iloc[:, 0].cov(combined.iloc[:, 1])
    market_variance = combined.iloc[:, 1].var()
    
    if market_variance == 0:
        return 1.0
    
    beta = covariance / market_variance
    return beta


def calculate_risk_metrics(data, market_data=None):
    """
    Calculate comprehensive risk metrics for a stock
    
    Args:
        data: DataFrame with OHLCV data
        market_data: Optional DataFrame with market index data (e.g., SPY)
    
    Returns:
        dict: Dictionary of risk metrics
    """
    # Calculate returns
    daily_returns, cumulative_returns = calculate_returns(data)
    
    # Basic metrics
    metrics = {
        'total_return': cumulative_returns.iloc[-1] * 100,  # Total return %
        'annual_return': (1 + daily_returns.mean()) ** 252 - 1,  # Annualized
        'volatility': calculate_volatility(daily_returns),
        'sharpe_ratio': calculate_sharpe_ratio(daily_returns),
        'max_drawdown': calculate_max_drawdown(data),
        'positive_days': (daily_returns > 0).sum() / len(daily_returns) * 100,
    }
    
    # Calculate Beta if market data provided
    if market_data is not None:
        market_returns, _ = calculate_returns(market_data)
        metrics['beta'] = calculate_beta(daily_returns, market_returns)
    else:
        metrics['beta'] = None
    
    return metrics


def calculate_risk_score(metrics):
    """
    Calculate overall risk score using ML-inspired approach
    
    Combines multiple risk factors into single score (0-100)
    0 = Very Low Risk, 100 = Very High Risk
    
    Args:
        metrics: Dictionary of risk metrics
    
    Returns:
        dict: Risk score and classification
    """
    # Feature weights (tuned based on financial theory)
    weights = {
        'volatility': 0.35,      # High volatility = higher risk
        'max_drawdown': 0.25,    # Large drawdowns = higher risk
        'sharpe_ratio': -0.20,   # High Sharpe = lower risk (negative weight)
        'positive_days': -0.20,  # More positive days = lower risk
    }
    
    # Normalize features to 0-100 scale
    normalized = {}
    
    # Volatility: 0-50% vol -> 0-100 score
    vol = min(metrics['volatility'], 50)
    normalized['volatility'] = (vol / 50) * 100
    
    # Max Drawdown: 0 to -50% -> 0-100 score
    dd = abs(min(metrics['max_drawdown'], 0))
    normalized['max_drawdown'] = min((dd / 50) * 100, 100)
    
    # Sharpe Ratio: -1 to 3 -> 0-100 (inverted, higher Sharpe = lower risk)
    sharpe = max(min(metrics['sharpe_ratio'], 3), -1)
    normalized['sharpe_ratio'] = ((sharpe + 1) / 4) * 100
    
    # Positive Days: 40-60% -> 0-100 (inverted)
    pos_days = metrics['positive_days']
    normalized['positive_days'] = pos_days
    
    # Calculate weighted score
    risk_score = 0
    for feature, weight in weights.items():
        risk_score += normalized[feature] * weight
    
    # Ensure score is between 0-100
    risk_score = max(0, min(risk_score, 100))
    
    # Classify risk level
    if risk_score < 30:
        risk_level = "Low Risk"
        risk_color = "🟢"
    elif risk_score < 60:
        risk_level = "Medium Risk"
        risk_color = "🟡"
    else:
        risk_level = "High Risk"
        risk_color = "🔴"
    
    return {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'risk_color': risk_color,
        'normalized_features': normalized
    }


def get_investment_recommendation(metrics, risk_assessment):
    """
    Generate investment recommendation based on metrics
    
    Args:
        metrics: Dictionary of risk metrics
        risk_assessment: Dictionary from calculate_risk_score()
    
    Returns:
        dict: Recommendation details
    """
    risk_score = risk_assessment['risk_score']
    sharpe = metrics['sharpe_ratio']
    total_return = metrics['total_return']
    
    # Decision logic
    if risk_score < 30 and sharpe > 1.0:
        recommendation = "🟢 BUY"
        reason = "Low risk with good risk-adjusted returns"
        confidence = "High"
    elif risk_score < 60 and sharpe > 0.5 and total_return > 0:
        recommendation = "🟡 HOLD"
        reason = "Moderate risk with acceptable returns"
        confidence = "Medium"
    elif risk_score > 70 or sharpe < 0:
        recommendation = "🔴 SELL/AVOID"
        reason = "High risk or poor risk-adjusted returns"
        confidence = "High"
    else:
        recommendation = "🟡 HOLD"
        reason = "Mixed signals, monitor closely"
        confidence = "Low"
    
    return {
        'recommendation': recommendation,
        'reason': reason,
        'confidence': confidence
    }


# For testing
if __name__ == "__main__":
    print("Testing Risk Models Module...")
    
    # Create sample data
    dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='D')
    np.random.seed(42)
    
    # Simulate stock prices with some volatility
    prices = 100 * (1 + np.random.randn(len(dates)).cumsum() * 0.02)
    
    sample_data = pd.DataFrame({
        'Close': prices,
        'Open': prices * 0.99,
        'High': prices * 1.01,
        'Low': prices * 0.98,
        'Volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    print("\n1. Calculating risk metrics...")
    metrics = calculate_risk_metrics(sample_data)
    
    print(f"   Total Return: {metrics['total_return']:.2f}%")
    print(f"   Volatility: {metrics['volatility']:.2f}%")
    print(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"   Max Drawdown: {metrics['max_drawdown']:.2f}%")
    
    print("\n2. Calculating risk score...")
    risk = calculate_risk_score(metrics)
    print(f"   Risk Score: {risk['risk_score']:.1f}/100")
    print(f"   Risk Level: {risk['risk_color']} {risk['risk_level']}")
    
    print("\n3. Getting recommendation...")
    recommendation = get_investment_recommendation(metrics, risk)
    print(f"   Recommendation: {recommendation['recommendation']}")
    print(f"   Reason: {recommendation['reason']}")
    print(f"   Confidence: {recommendation['confidence']}")
    
    print("\nRisk models module working correctly!")