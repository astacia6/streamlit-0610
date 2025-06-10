import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime, timedelta

# 페이지 제목
st.title("📈 글로벌 시총 TOP 10 기업 - 최근 3년 주가 변화")

# 시총 상위 10개 기업 티커
tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 거래소
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta": "META",
    "Tesla": "TSLA",
    "TSMC": "TSM"
}

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365 * 3)

# 주가 데이터 수집
@st.cache_data(show_spinner=False)
def load_data(ticker):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df["Close"]

# 데이터프레임 구성
all_data = pd.DataFrame()
for name, ticker in tickers.items():
    data = load_data(ticker)
    all_data[name] = data

# 그래프 그리기
fig = go.Figure()
for name in all_data.columns:
    fig.add_trace(go.Scatter(x=all_data.index, y=all_data[name], mode='lines', name=name))

fig.update_layout(
    title="시가총액 상위 10개 기업의 최근 3년간 종가 변화",
    xaxis_title="날짜",
    yaxis_title="주가 (USD 또는 해당 통화)",
    legend_title="기업명",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# 주의 문구
st.caption("※ 일부 해외 거래소(예: 사우디)의 경우 주가 데이터가 제한될 수 있습니다.")
