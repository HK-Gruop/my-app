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
        "GODREJCP.NS": "GODREJCP",
        "NBCC.NS": "NBCC",
        "MFSL.NS": "MFSL",
        "TATACHEM.NS": "TATACHEM",
        "UNITDSPR.NS": "UNITDSPR",
        "BPCL.NS": "BPCL",
        "KALYANKJIL.NS": "KALYANKJIL",
        "JINDALSTEL.NS": "JINDALSTEL",
        "RECLTD.NS": "RECLTD",
        "NESTLEIND.NS": "NESTLEIND",
        "CROMPTON.NS": "CROMPTON",
        "TATACONSUM.NS": "TATACONSUM",
        "OBEROIRLTY.NS": "OBEROIRLTY",
        "UNOMINDA.NS": "UNOMINDA",
        "HCLTECH.NS": "HCLTECH",
        "PGEL.NS": "PGEL",
        "CONCOR.NS": "CONCOR",
        "LAURUSLABS.NS": "LAURUSLABS",
        "NTPC.NS": "NTPC",
        "TATASTEEL.NS": "TATASTEEL",
        "HINDPETRO.NS": "HINDPETRO",
        "PPLPHARMA.NS": "PPLPHARMA",
        "TECHM.NS": "TECHM",
        "GODREJPROP.NS": "GODREJPROP",
        "ICICIPRULI.NS": "ICICIPRULI",
        "FORTIS.NS": "FORTIS",
        "MAXHEALTH.NS": "MAXHEALTH",
        "PHOENIXLTD.NS": "PHOENIXLTD",
        "VOLTAS.NS": "VOLTAS",
        "HDFCLIFE.NS": "HDFCLIFE",
        "NMDC.NS": "NMDC",
        "CIPLA.NS": "CIPLA",
        "SBILIFE.NS": "SBILIFE",
        "BHARATFORG.NS": "BHARATFORG",
        "RBLBANK.NS": "RBLBANK",
        "OIL.NS": "OIL",
        "INFY.NS": "INFY",
        "ICICIBANK.NS": "ICICIBANK",
        "ASTRAL.NS": "ASTRAL",
        "NATIONALUM.NS": "NATIONALUM",
        "ADANIENSOL.NS": "ADANIENSOL",
        "SHRIRAMFIN.NS": "SHRIRAMFIN",
        "BAJAJFINSV.NS": "BAJAJFINSV",
        "INDUSTOWER.NS": "INDUSTOWER",
        "LUPIN.NS": "LUPIN",
        "VEDL.NS": "VEDL",
        "BEL.NS": "BEL",
        "HINDZINC.NS": "HINDZINC",
        "MOTHERSON.NS": "MOTHERSON",
        "SUNPHARMA.NS": "SUNPHARMA",
        "AUROPHARMA.NS": "AUROPHARMA",
        "MARICO.NS": "MARICO",
        "LICI.NS": "LICI",
        "IGL.NS": "IGL",
        "CYIENT.NS": "CYIENT",
        "AUBANK.NS": "AUBANK",
        "HDFCBANK.NS": "HDFCBANK",
        "HINDALCO.NS": "HINDALCO",
        "PAYTM.NS": "PAYTM",
        "PFC.NS": "PFC",
        "POWERGRID.NS": "POWERGRID",
        "BIOCON.NS": "BIOCON",
        "EXIDEIND.NS": "EXIDEIND",
        "ASHOKLEY.NS": "ASHOKLEY",
        "KFINTECH.NS": "KFINTECH",
        "PNB.NS": "PNB",
        "IOC.NS": "IOC",
        "CDSL.NS": "CDSL",
        "ADANIPORTS.NS": "ADANIPORTS",
        "UPL.NS": "UPL",
        "JSWSTEEL.NS": "JSWSTEEL",
        "SAMMAANCAP.NS": "SAMMAANCAP",
        "LODHA.NS": "LODHA",
        "INOXWIND.NS": "INOXWIND",
        "INDHOTEL.NS": "INDHOTEL",
        "ETERNAL.NS": "ETERNAL",
        "PATANJALI.NS": "PATANJALI",
        "CANBK.NS": "CANBK",
        "AMBUJACEM.NS": "AMBUJACEM",
        "IEX.NS": "IEX",
        "WIPRO.NS": "WIPRO",
        "TATATECH.NS": "TATATECH",
        "NYKAA.NS": "NYKAA",
        "LTF.NS": "LTF",
        "ONGC.NS": "ONGC",
        "AXISBANK.NS": "AXISBANK",
        "ICICIGI.NS": "ICICIGI"
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


