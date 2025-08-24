import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf
import pandas_market_calendars as mcal
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib

# ===== Portfolio (持股 + 追蹤) =====
portfolio = {
    # 已持有
    'SMR':  {'Shares': 10,  'Avg Buy Price': 44.363},
    'SNOW': {'Shares': 4,   'Avg Buy Price': 196.3525},
    'UAMY': {'Shares': 50,  'Avg Buy Price': 4.034},
    'UEC':  {'Shares': 20,  'Avg Buy Price': 9.3295},
    'UUUU': {'Shares': 50,  'Avg Buy Price': 8.2982},
    'AMPX': {'Shares': 100, 'Avg Buy Price': 7.8979},
    'RCAT': {'Shares': 70,  'Avg Buy Price': 9.320857},
    'TMC':  {'Shares': 80,  'Avg Buy Price': 5.31525},
    'CRML': {'Shares': 50,  'Avg Buy Price': 3.50},
    # 追蹤名單
    'AREC': {'Shares': 0, 'Avg Buy Price': None},
    'USAR': {'Shares': 0, 'Avg Buy Price': None},
    'PPTA': {'Shares': 0, 'Avg Buy Price': None},
    'LEU':  {'Shares': 0, 'Avg Buy Price': None},
    'OKLO': {'Shares': 0, 'Avg Buy Price': None},
    'AMZN': {'Shares': 0, 'Avg Buy Price': None},
    'ALB':  {'Shares': 0, 'Avg Buy Price': None},
    'LAC':  {'Shares': 0, 'Avg Buy Price': None},
    'PLL':  {'Shares': 0, 'Avg Buy Price': None},
    'MP':   {'Shares': 0, 'Avg Buy Price': None},
    'CCJ':  {'Shares': 0, 'Avg Buy Price': None},
    'URG':  {'Shares': 0, 'Avg Buy Price': None},
}

CSV_FILE = "stock_data.csv"

def is_trading_day(date=None) -> bool:
    """Return True if NYSE is open on given date (America/New_York)."""
    nyse = mcal.get_calendar('NYSE')
    ny_date = pd.Timestamp(date or datetime.now(ZoneInfo('America/New_York')).date(), tz='America/New_York')
    sched = nyse.schedule(start_date=ny_date, end_date=ny_date)
    return not sched.empty

def fetch_stock_data() -> pd.DataFrame:
    rows = []
    ny_now = datetime.now(ZoneInfo("America/New_York"))
    trade_date = ny_now.strftime("%Y-%m-%d")

    for ticker, info in portfolio.items():
        try:
            hist = yf.Ticker(ticker).history(period='5d')
            if hist.empty:
                print(f"[WARN] No data for {ticker}")
                continue
            latest_close = float(hist['Close'].dropna().iloc[-1])
            avg = info['Avg Buy Price']
            pl = None if not avg else (latest_close - avg) / avg * 100.0

            rows.append({
                "Date": trade_date,
                "Ticker": ticker,
                "Shares": info['Shares'],
                "Avg Buy Price": avg,
                "Latest Close": round(latest_close, 4),
                "P/L (%)": None if pl is None else round(pl, 2),
            })
        except Exception as e:
            print(f"[ERROR] {ticker}: {e}")

    df = pd.DataFrame(rows, columns=["Date","Ticker","Shares","Avg Buy Price","Latest Close","P/L (%)"])
    if df.empty:
        print("[WARN] DataFrame empty; skip writing.")
        return df

    # append long/tidy table
    write_header = not os.path.exists(CSV_FILE)
    df.to_csv(CSV_FILE, mode="a", header=write_header, index=False, encoding="utf-8")
    print(f"[OK] Appended {len(df)} rows to {CSV_FILE}")
    return df

def send_email_if_configured(file_path: str):
    """Send the CSV via Gmail SMTP if EMAIL_USER/EMAIL_PASS/EMAIL_TO are set."""
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")
    if not (sender and password and receiver):
        print("[INFO] Email env not set; skip emailing.")
        return

    msg = MIMEMultipart()
    msg['Subject'] = "每日股票報表"
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText("附上最新的股票追蹤報表。", "plain", "utf-8"))

    with open(file_path, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
    print("[OK] Email sent.")

def main():
    if is_trading_day():
        df = fetch_stock_data()
        if not df.empty:
            send_email_if_configured(CSV_FILE)
    else:
        print("不是交易日，跳過。")

if __name__ == "__main__":
    main()
