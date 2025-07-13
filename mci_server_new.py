import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import pandas as pd
from openbb import obb
from transformers import pipeline
import plotly.graph_objects as go
from jinja2 import Environment, FileSystemLoader
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Initialize sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Jinja2 environment for HTML reporting
env = Environment(loader=FileSystemLoader('.'))

# --- Pydantic Models ---

class TickerRequest(BaseModel):
    tickers: List[str] = Field(..., example=["BEF.SG", "AUR.AX"])
    days: int = 30

class Sentiment(BaseModel):
    label: str
    score: float

class KpiData(BaseModel):
    average_price: float
    volatility: float
    price_change_percentage: float
    average_volume: float
    sharpe_ratio: float

class TickerData(BaseModel):
    kpis: KpiData
    sentiment: Dict[str, List[Sentiment]]
    news: List[Dict[str, Any]]

class CompetitiveAnalysisResponse(BaseModel):
    data: Dict[str, TickerData]
    benchmark: Dict[str, Dict[str, Any]]
    chart: Dict
    report_filename: str

class DashboardResponse(BaseModel):
    data: Dict[str, KpiData]
    chart: Dict

# --- Helper Functions ---

def fetch_stock_data(tickers: List[str], days: int) -> Dict[str, pd.DataFrame]:
    """Fetches historical stock data for a list of tickers."""
    data = {}
    for ticker in tickers:
        try:
            df = obb.stocks.price.historical(ticker, start_date=(pd.Timestamp.now() - pd.Timedelta(days=days)).strftime('%Y-%m-%d')).to_df()
            if df.empty:
                logger.warning(f"No data found for ticker: {ticker}")
                continue
            df.sort_index(ascending=True, inplace=True)
            data[ticker] = df
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to fetch data for {ticker}")
    return data

def calculate_kpis(df: pd.DataFrame) -> KpiData:
    """Calculates key performance indicators from stock data."""
    avg_price = df['close'].mean()
    volatility = df['close'].std()
    price_change = (df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0] * 100
    avg_volume = df['volume'].mean()

    # Calculate Sharpe Ratio
    daily_returns = df['close'].pct_change().dropna()
    sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252) if daily_returns.std() != 0 else 0

    return KpiData(
        average_price=avg_price,
        volatility=volatility,
        price_change_percentage=price_change,
        average_volume=avg_volume,
        sharpe_ratio=sharpe_ratio
    )

def get_sentiment(texts: List[str]) -> List[Sentiment]:
    """Analyzes sentiment of a list of texts."""
    try:
        sentiments = sentiment_pipeline(texts)
        return [Sentiment(label=s['label'], score=s['score']) for s in sentiments]
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return []

def fetch_news_and_sentiment(ticker: str) -> (List[Dict[str, Any]], List[Sentiment]):
    """Fetches news and analyzes sentiment."""
    try:
        news_data = obb.news.company(symbol=ticker, limit=5).to_df()
        news_list = news_data[['created', 'title']].to_dict('records')
        sentiments = get_sentiment([news['title'] for news in news_list])
        return news_list, sentiments
    except Exception as e:
        logger.error(f"Failed to fetch news for {ticker}: {e}")
        return [], []

def generate_plotly_chart(stock_data: Dict[str, pd.DataFrame], kpis: Dict[str, KpiData]) -> Dict:
    """Generates a Plotly chart of stock prices."""
    fig = go.Figure()
    for ticker, df in stock_data.items():
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['close'],
            mode='lines',
            name=ticker,
            hovertemplate=f"<b>{ticker}</b><br>Price: %{{y:.2f}}<br>Sharpe Ratio: {kpis[ticker].sharpe_ratio:.2f}<extra></extra>"
        ))
    fig.update_layout(
        title="Competitive Stock Price Analysis",
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        hovermode="x unified"
    )
    return fig.to_json()

def generate_html_report(data: Dict, benchmark: Dict, filename: str):
    """Generates an HTML report from analysis data."""
    template = env.get_template('report_template.html')
    html_content = template.render(data=data, benchmark=benchmark)
    with open(filename, 'w') as f:
        f.write(html_content)

# --- API Endpoints ---

@app.post("/competitive_analysis", response_model=CompetitiveAnalysisResponse)
def competitive_analysis(request: TickerRequest):
    """
    Performs competitive analysis on a list of stock tickers.
    """
    stock_data = fetch_stock_data(request.tickers, request.days)
    if not stock_data:
        raise HTTPException(status_code=404, detail="No valid data found for any of the tickers.")

    analysis_results = {}
    kpi_results = {}

    for ticker, df in stock_data.items():
        kpis = calculate_kpis(df)
        kpi_results[ticker] = kpis

        # News and Sentiment
        news, news_sentiments = fetch_news_and_sentiment(ticker)

        # Mock X posts
        mock_x_posts = [f"{ticker} stock is gaining traction!", f"Positive outlook for {ticker}", f"Is {ticker} the next big thing?"]
        x_sentiments = get_sentiment(mock_x_posts)

        analysis_results[ticker] = TickerData(
            kpis=kpis,
            sentiment={"news": news_sentiments, "x_posts": x_sentiments},
            news=news
        )

    # Generate benchmark table
    benchmark = pd.DataFrame({ticker: kpi.dict() for ticker, kpi in kpi_results.items()}).T.to_dict('index')

    # Generate chart and report
    chart_json = generate_plotly_chart(stock_data, kpi_results)
    report_filename = f"competitive_report_{'_'.join(request.tickers)}.html"
    generate_html_report(analysis_results, benchmark, report_filename)

    return CompetitiveAnalysisResponse(
        data=analysis_results,
        benchmark=benchmark,
        chart=chart_json,
        report_filename=report_filename
    )

@app.get("/dashboard/competitive/{tickers}", response_model=DashboardResponse)
def get_dashboard_data(tickers: str, days: int = 30):
    """
    Provides data for the competitive analysis dashboard.
    """
    ticker_list = [ticker.strip() for ticker in tickers.split(',')]
    stock_data = fetch_stock_data(ticker_list, days)
    if not stock_data:
        raise HTTPException(status_code=404, detail="No valid data found for any of the tickers.")

    kpi_results = {ticker: calculate_kpis(df) for ticker, df in stock_data.items()}
    chart_json = generate_plotly_chart(stock_data, kpi_results)

    return DashboardResponse(
        data={ticker: kpi.dict() for ticker, kpi in kpi_results.items()},
        chart=chart_json
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
