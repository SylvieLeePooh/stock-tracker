# Stock Tracker (GitHub Actions)

這個專案會在 **美股收盤後**（UTC 22:10；台灣大約早上 06:10）自動：
1. 抓取你的持股＋追蹤清單的最新收盤價
2. 計算損益（僅對持股）
3. 將結果 **append** 到 `stock_data.csv`
4. （可選）寄 Email 給你，或把 CSV 以 **artifact** 方式附在 Actions

## 使用方式（完全用 GitHub 網站即可）
1. 新增一個 Repo（例如 `stock-tracker`）
2. 在 Repo 裡建立以下檔案：
   - `stock_tracker.py`（本程式）
   - `requirements.txt`
   - `.github/workflows/stock.yml`
3. 進入 **Actions** 分頁 → 第一次會看到 workflow，允許它執行
4. （可選）到 **Settings → Actions → General → Workflow permissions** 設定為 **Read and write**，確保能 push CSV
5. （可選）在 **Settings → Secrets and variables → Actions** 新增：
   - `EMAIL_USER`：你的 Gmail
   - `EMAIL_PASS`：Gmail **應用程式密碼**
   - `EMAIL_TO`：收件人（通常是你自己）

## 修改清單
打開 `stock_tracker.py` 裡的 `portfolio` 字典，增刪 tickers、股數、均價。

## 手動執行
在 Actions 頁面點「Run workflow」。

## Cron 時間說明
GitHub 使用 **UTC**。設定為 `22:10 UTC`，可確保無論美國是否夏令時，都在收盤後執行。
