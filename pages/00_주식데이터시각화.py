import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def app():
    st.title("글로벌 시가총액 탑 10 기업의 주가 변화 (최근 3년)")

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

        # --- 디버깅 라인 시작 ---
        st.write("--- 디버그 정보: stock_data ---")
        st.write("컬럼:", stock_data.columns.tolist())
        st.write("데이터 타입:", stock_data.dtypes)
        st.write("'Date' 컬럼 존재 여부:", "Date" in stock_data.columns)
        st.write("'Close' 컬럼 존재 여부:", "Close" in stock_data.columns)
        if 'Date' in stock_data.columns and 'Close' in stock_data.columns:
            st.write("처음 5행 (Date, Close):", stock_data[['Date', 'Close']].head())
        st.write("stock_data 비어있는가?", stock_data.empty)
        st.write("stock_data 형태 (rows, columns):", stock_data.shape)
        st.write("--- 디버그 정보 끝 ---")
        
        # Plotly Express 호출 전에 필수 컬럼 존재 여부 재확인
        if "Date" not in stock_data.columns or "Close" not in stock_data.columns:
            st.error("오류: 주식 데이터에 'Date' 또는 'Close' 컬럼이 없습니다. 티커나 데이터 소스를 확인해주세요.")
            return # 필수 컬럼이 없으면 함수를 종료합니다.

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
