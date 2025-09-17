from flask import Flask
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def breakout_report():
    now = datetime.utcnow() + timedelta(hours=5, minutes=30)

    tickers = {
        "SONACOMS.NS": "SONACOMS",
        "GODREJCP.NS": "GODREJCP"
    }

    results = []
    for symbol, name in tickers.items():
        try:
            df = yf.download(symbol, period="1d", interval="15m", progress=False)
            if df.empty or len(df) < 2:
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            df.index = (df.index.tz_convert(None) + timedelta(hours=5, minutes=30))
            df = df[df.index <= now]

            first_candle = df.iloc[0]
            first_high = float(first_candle["High"])
            first_low = float(first_candle["Low"])

            if len(df) > 1:
                second_candle = df.iloc[1]
                close = float(second_candle["Close"])
                volume = int(second_candle["Volume"])

                if close > first_high:
                    results.append([
                        name,
                        "🔼 Close Above High",
                        close,
                        df.index[1].strftime("%H:%M:%S"),
                        f"{first_low:.2f}-{first_high:.2f}",
                        volume
                    ])
        except Exception as e:
            results.append([name, f"Error: {e}", "-", "-", "-", 0])

    if results:
        df_out = pd.DataFrame(results, columns=["Stock", "Status", "Price", "Time", "First15m Range", "Volume"])
        return df_out.to_html(index=False, border=1)
    else:
        return "<h2>No breakout today</h2>"
