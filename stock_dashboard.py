import yfinance as yf
import pandas as pd
import streamlit as st
from ta.trend import EMAIndicator, ADXIndicator
from ta.momentum import RSIIndicator

st.set_page_config(page_title="Trending Stocks Finder", layout="wide")
st.title("📈 Trending Stocks for Positional Trading")

# Define stock list (Nifty 500 from NSE)
nifty500 = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "LT.NS", "SBIN.NS", "KOTAKBANK.NS",
    "ASIANPAINT.NS", "ITC.NS", "HINDUNILVR.NS", "ULTRACEMCO.NS", "ADANIGREEN.NS", "BHARTIARTL.NS",
    "ADANIPORTS.NS", "BAJFINANCE.NS", "MARUTI.NS", "AXISBANK.NS", "HCLTECH.NS", "DMART.NS", "BAJAJ-AUTO.NS",
    "DIVISLAB.NS", "EICHERMOT.NS", "GRASIM.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "JSWSTEEL.NS", "LTI.NS",
    "M&M.NS", "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS", "SBILIFE.NS", "SUNPHARMA.NS", "TATAMOTORS.NS",
    "TATASTEEL.NS", "TECHM.NS", "TITAN.NS", "UPL.NS", "WIPRO.NS", "ZEEL.NS", "AMBUJACEM.NS", "AUROPHARMA.NS",
    "BANDHANBNK.NS", "BERGEPAINT.NS", "BIOCON.NS", "CANBK.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS",
    "DABUR.NS", "GAIL.NS", "GODREJCP.NS", "ICICIPRULI.NS", "IDFCFIRSTB.NS", "INDUSINDBK.NS", "INDUSTOWER.NS",
    "IOC.NS", "IRCTC.NS", "JUBLFOOD.NS", "LICI.NS", "MRF.NS", "PIDILITIND.NS", "PIIND.NS", "POLYCAB.NS",
    "RECLTD.NS", "SHREECEM.NS", "SIEMENS.NS", "SRF.NS", "TRENT.NS", "TVSMOTOR.NS", "VOLTAS.NS", "ZOMATO.NS"
    # You can add the rest of Nifty 500 stocks here or load from a CSV/API for full automation
]

# Sidebar options
st.sidebar.header("Filter Settings")
ema_fast = st.sidebar.slider("Fast EMA (short-term)", 10, 50, 20)
ema_slow = st.sidebar.slider("Slow EMA (medium-term)", 30, 100, 50)
ema_long = st.sidebar.slider("Long EMA (trend confirm)", 100, 300, 200)
rsi_max = st.sidebar.slider("Max RSI (avoid overbought)", 60, 90, 70)
adx_min = st.sidebar.slider("Min ADX (trend strength)", 10, 40, 20)

# Function to check if stock is trending
def is_trending(ticker):
    try:
        data = yf.download(ticker, period="6mo", interval="1d")
        data.dropna(inplace=True)

        data['EMA_fast'] = EMAIndicator(data['Close'], window=ema_fast).ema_indicator()
        data['EMA_slow'] = EMAIndicator(data['Close'], window=ema_slow).ema_indicator()
        data['EMA_long'] = EMAIndicator(data['Close'], window=ema_long).ema_indicator()
        data['RSI'] = RSIIndicator(data['Close'], window=14).rsi()
        data['ADX'] = ADXIndicator(data['High'], data['Low'], data['Close'], window=14).adx()

        latest = data.iloc[-1]

        if (
            latest['EMA_fast'] > latest['EMA_slow'] > latest['EMA_long'] and
            latest['Close'] > latest['EMA_long'] and
            latest['RSI'] < rsi_max and
            latest['ADX'] > adx_min
        ):
            return True, latest
    except:
        return False, None

    return False, None

# Scan stocks
results = []
progress = st.progress(0)
for i, stock in enumerate(nifty500):
    trending, latest_data = is_trending(stock)
    if trending:
        results.append((stock, latest_data['Close'], latest_data['RSI'], latest_data['ADX']))
    progress.progress((i + 1) / len(nifty500))

# Show results
st.success(f"✅ {len(results)} trending stocks found")

if results:
    df = pd.DataFrame(results, columns=["Ticker", "Close Price", "RSI", "ADX"])
    st.dataframe(df.set_index("Ticker"))
else:
    st.warning("No trending stocks found based on current filter settings.")
