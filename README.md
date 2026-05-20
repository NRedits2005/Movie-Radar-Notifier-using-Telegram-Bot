# 🎬 NR Movie Radar Bot

NR Movie Radar Bot is an automated Telegram movie notification bot built using Python, Selenium, BeautifulSoup, and Telegram Bot API.

The bot:
- Scrapes latest movie posts
- Detects movie quality formats
- Sends Telegram notifications automatically
- Supports movie search commands
- Filters Tamil movies
- Runs continuously on Railway

---

# 🚀 Features

✅ Automatic movie notifications  
✅ Telegram bot commands  
✅ Selenium anti-block scraping  
✅ Detects:
- 480p
- 720p
- 1080p
- WEB-DL
- HDRip
- BluRay

✅ Search movies from Telegram  
✅ Tamil movie filtering  
✅ Duplicate prevention  
✅ Railway deployment support

---

# 🛠 Tech Stack

- Python
- Selenium
- BeautifulSoup
- Telegram Bot API
- Railway
- Chrome Headless Browser

---

# 📂 Project Structure

```bash
movie-notifier/
│
├── movie_notifier.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── nixpacks.toml
├── movies.json
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPO
cd movie-notifier
```

---

## 2. Install Packages

```bash
pip install -r requirements.txt
```

---

# 📦 requirements.txt

```txt
python-telegram-bot
selenium
webdriver-manager
beautifulsoup4
```

---

# 🤖 Create Telegram Bot

1. Open Telegram
2. Search:

```txt
@BotFather
```

3. Create bot:

```txt
/newbot
```

4. Copy BOT TOKEN

Example:

```txt
123456789:ABCXYZ
```

---

# 💬 Get Telegram Chat ID

Send message to your bot:

```txt
/start
```

Then open:

```txt
https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
```

Find:

```json
"chat": {
    "id": 123456789
}
```

Copy:

```txt
123456789
```

---

# 🔐 Environment Variables

Never hardcode secrets.

Use environment variables.

---

## BOT TOKEN

```env
BOT_TOKEN=YOUR_BOT_TOKEN
```

---

## CHAT ID

```env
CHAT_ID=123456789
```

---

# ▶️ Run Locally

```bash
python movie_notifier.py
```

Expected Output:

```txt
🎬 NR Movie Radar Bot Started
Opening website...
MOVIES FOUND: 42
Notification Sent
```

---

# 📱 Telegram Commands

## Start Bot

```txt
/start
```

---

## Help

```txt
/help
```

---

## Latest Movies

```txt
/latest
```

---

## Search Movie

```txt
/search leo
```

---

## Tamil Movies Only

```txt
/tamil
```

---

# 🔍 Supported Quality Detection

The bot automatically extracts:

- 480p
- 720p
- 1080p
- WEB-DL
- HDRip
- BluRay
- HQ
- HDTC

---

# 🚫 Duplicate Prevention

The bot stores old movie titles inside:

```txt
movies.json
```

This prevents repeated notifications.

---

# ☁️ Railway Deployment

## 1. Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial Commit"
git push
```

---

## 2. Create Railway Project

Open:

https://railway.app

Create:

```txt
New Project
→ Deploy from GitHub Repo
```

---

## 3. Add Variables

Railway Dashboard → Variables

Add:

| KEY | VALUE |
|---|---|
| BOT_TOKEN | your bot token |
| CHAT_ID | your telegram id |

---

# 📄 Procfile

Create file:

```txt
Procfile
```

Content:

```txt
worker: python movie_notifier.py
```

---

# 🐍 runtime.txt

```txt
python-3.11.9
```

---

# ⚙️ nixpacks.toml

```toml
[phases.setup]
nixPkgs = ["google-chrome"]
```

---

# 🧠 Selenium Setup

The bot uses headless Chrome.

Chrome options:

```python
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
```

---

# 🔄 Auto Notification System

The bot automatically:

1. Scrapes website
2. Detects new posts
3. Sends Telegram notification
4. Sleeps for 15 minutes
5. Repeats forever

---

# 🛡 Filtering System

The bot removes unwanted posts:

- Movie Explain
- Video Songs
- FLAC
- Trailers
- Glimpses

---

# 📌 Example Notification

```txt
🎬 New Movie Added

🎥 Coolie (2026) Tamil WEB-DL 1080p

📀 Quality: WEB-DL, 1080p

🔗 https://example.com/movie
```

---

# ⚠️ Important Notes

- Website structure may change
- Selenium is required due to anti-bot protection
- Avoid aggressive scraping intervals
- Recommended interval: 15–30 minutes

---

# 🧹 Recommended Optimization

Current recommended interval:

```python
await asyncio.sleep(1800)
```

30 minutes is safer and reduces blocking risk.

---

# 🐞 Debugging

## Check Generated HTML

```txt
debug.html
```

---

## Telegram Error

```txt
Forbidden: the bot can't send messages to the bot
```

Fix:
- Use numeric chat ID
- NOT bot username

---

# 📜 License

This project is for educational and automation purposes only.

---

# ❤️ Credits

Built using:
- Python
- Telegram Bot API
- Selenium
- BeautifulSoup

---

# 🎬 CinePulse

Automated movie notifications directly to Telegram.

Because manually refreshing movie forums every hour is apparently how humans chose to spend their finite lifespan.
