import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import MACD

st.set_page_config(page_title="Intraday AI Trader", layout="centered")
st.title("📈 Intraday AI Trading Assistant")
st.markdown("Enter a stock symbol (e.g. `TCS.NS`, `INFY.NS`) to get intraday prediction using RSI & MACD.")

# Input
symbol = st.text_input("Enter Stock Symbol", value="INFY.NS")

if st.button("Predict Now"):
    # Download real-time 5-minute interval data for the last 1 day
    data = yf.download(symbol, interval="5m", period="1d")

    if data.empty:
        st.error("❌ No data found for this symbol.")
    else:
        data.reset_index(inplace=True)

        # Handle 'Close' safely
        close_prices = data['Close']
        if isinstance(close_prices, pd.DataFrame):
            close_prices = close_prices.squeeze()

        # Calculate RSI and MACD indicators
        try:
            rsi_series = RSIIndicator(close_prices).rsi()
            macd_series = MACD(close_prices).macd_diff()

            data['rsi'] = rsi_series
            data['macd_diff'] = macd_series

            # Get last non-null values
            rsi_value = rsi_series.dropna().iloc[-1] if not rsi_series.dropna().empty else None
            macd_value = macd_series.dropna().iloc[-1] if not macd_series.dropna().empty else None

            # Plot chart
            fig, ax = plt.subplots()
            data['Close'].plot(ax=ax, title=f"{symbol} - 5min Chart", color="black")
            st.pyplot(fig)

            # Show values and decision
            if rsi_value is not None and macd_value is not None:
                st.write(f"**RSI:** {rsi_value:.2f}")
                st.write(f"**MACD Diff:** {macd_value:.2f}")

                # AI Decision Logic
                if rsi_value < 30 and macd_value > 0:
                    st.success("🔼 Suggestion: BUY")
                elif rsi_value > 70 and macd_value < 0:
                    st.error("🔽 Suggestion: SELL")
                else:
                    st.info("⏸️ Suggestion: HOLD")
            else:
                st.warning("⚠️ Not enough data to calculate RSI or MACD. Try a different stock or wait for more candles.")

        except Exception as e:
            st.error(f"⚠️ Error calculating indicators: {str(e)}")

