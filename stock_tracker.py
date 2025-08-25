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
    'TMC':  {'Shares
