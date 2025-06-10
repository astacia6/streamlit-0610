import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def app():
    st.title("글로벌 시가총액 탑 10 기업의 주가 변화 (최근 3년)")

    # Top 10 global companies by market cap (as of June 2025, using common tickers)
    # Using a list based on the search results, ensuring valid yfinance tickers
    tickers = {
        "Microsoft": "MSFT",
        "Nvidia": "NVDA",
        "Apple": "AAPL",
        "Amazon": "AMZN",
        "Alphabet (Google)": "GOOGL",
        "Meta Platforms": "META",
        "Broadcom": "AVGO",
        "TSMC": "TSM",
        "Berkshire Hathaway": "BRK-B",
        "Tesla": "TSLA"
    }

    selected_company_name = st.selectbox("기업을 선택하세요:", list(tickers.keys()))
    selected_ticker = tickers[selected_company_name]

    end_date = datetime.now()
    start_date = end_date - timedelta(days=3 * 365) # Last 3 years

    st.subheader(f"{selected_company_name} ({selected_ticker}) 주가 변화")

    @st.cache_data
    def get_stock_data(ticker, start, end):
        try:
            data = yf.download(ticker, start=start, end=end)
            if data.empty:
                st.error(f"데이터를 가져오지 못했습니다: {ticker}. 티커를 확인해주세요.")
                return None
            return data
        except Exception as e:
            st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {ticker} - {e}")
            return None

    stock_data = get_stock_data(selected_ticker, start_date, end_date)

    if stock_data is not None:
        # Reset index to use 'Date' as a column for Plotly
        stock_data = stock_data.reset_index()

        # Create interactive plot using Plotly Express
        fig = px.line(stock_data, x="Date", y="Close", title=f"{selected_company_name} ({selected_ticker}) 주가",
                      labels={"Close": "종가 (USD)", "Date": "날짜"},
                      hover_data={"Date": "|%Y-%m-%d", "Close": ":.2f"})
        
        fig.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.update_layout(
            hovermode="x unified",
            xaxis_rangeslider_visible=True,
            title_font_size=20,
            title_x=0.5
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("데이터 미리보기")
        st.dataframe(stock_data.tail())

if __name__ == '__main__':
    app()
