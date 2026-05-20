import re
import json
import time
import asyncio

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================================================
# TELEGRAM CONFIG
# =========================================================

BOT_TOKEN = "8861101348:AAHGUGNG0HxhQG7JYgNDd-l-duWtZJZw88o"
# PERSONAL CHAT ID OR CHANNEL ID
# Example:
# CHAT_ID = 123456789
# CHAT_ID = "@movie_channel"

CHAT_ID = 987654321

# =========================================================
# WEBSITE URL
# =========================================================

URL = "https://www.1tamilmv.futbol/"

# =========================================================
# STORAGE FILE
# =========================================================

DATA_FILE = "movies.json"

# =========================================================
# LOAD OLD MOVIES
# =========================================================

def load_movies():

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return []

# =========================================================
# SAVE MOVIES
# =========================================================

def save_movies(movies):

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            movies,
            file,
            indent=4,
            ensure_ascii=False
        )

# =========================================================
# SCRAPE MOVIES
# =========================================================

def scrape_movies():

    options = Options()


    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    options.add_argument(
        "--disable-blink-features=AutomationControlled"
    )

    options.add_argument(
        "user-agent=Mozilla/5.0"
    )

    driver = webdriver.Chrome(
        options=options
    )

    print("Opening website...")

    driver.get(URL)

    # WAIT FOR PAGE LOAD
    time.sleep(10)

    html = driver.page_source

    # DEBUG HTML
    with open(
        "debug.html",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    driver.quit()

    movies = []

    seen = set()

    posts = soup.find_all("a")

    print("TOTAL TAGS:", len(posts))

    for post in posts:

        title = post.get_text(strip=True)

        href = post.get("href")

        if not href:
            continue

        # ONLY MOVIE POSTS
        if "/forums/topic/" not in href:
            continue

        # SKIP PAGINATION
        if "page" in href:
            continue

        if len(title) < 20:
            continue

        keywords = [
            "Tamil",
            "Telugu",
            "Hindi",
            "Malayalam",
            "WEB-DL",
            "HDRip",
            "BluRay",
            "1080p",
            "720p",
            "480p"
        ]

        if not any(
            keyword.lower() in title.lower()
            for keyword in keywords
        ):
            continue

        key = title.lower()

        if key in seen:
            continue

        seen.add(key)

        qualities = re.findall(
            r'(\d{3,4}p|WEB-DL|HDRip|BluRay|HDTC|HQ)',
            title,
            re.IGNORECASE
        )

        movie = {
            "title": title,
            "qualities": list(set(qualities)),
            "url": href
        }

        movies.append(movie)

    print("MOVIES FOUND:", len(movies))

    return movies

# =========================================================
# START COMMAND
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = """
🎬 CinePulse Bot Started

Available Commands:

/latest
/search movie_name
/tamil
/help
"""

    await update.message.reply_text(message)

# =========================================================
# HELP COMMAND
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = """
📌 Available Commands

/latest
→ Latest movies

/search leo
→ Search movie

/tamil
→ Tamil movies only

/help
→ Show commands
"""

    await update.message.reply_text(message)

# =========================================================
# LATEST MOVIES
# =========================================================

async def latest(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "🔍 Fetching latest movies..."
    )

    movies = scrape_movies()

    if len(movies) == 0:

        await update.message.reply_text(
            "❌ No movies found"
        )

        return

    message = "🔥 Latest Movies\n\n"

    for movie in movies[:10]:

        quality_text = ", ".join(
            movie["qualities"]
        )

        if quality_text == "":
            quality_text = "Unknown"

        message += (
            f"🎥 {movie['title']}\n"
            f"📀 Quality: {quality_text}\n"
            f"🔗 {movie['url']}\n\n"
        )

    await update.message.reply_text(message)

# =========================================================
# SEARCH MOVIES
# =========================================================

async def search(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if len(context.args) == 0:

        await update.message.reply_text(
            "Usage:\n/search leo"
        )

        return

    query = " ".join(context.args)

    movies = scrape_movies()

    results = []

    for movie in movies:

        if query.lower() in movie["title"].lower():

            results.append(movie)

    if len(results) == 0:

        await update.message.reply_text(
            "❌ Movie not found"
        )

        return

    message = f"🎬 Search Results for '{query}'\n\n"

    for movie in results[:10]:

        quality_text = ", ".join(
            movie["qualities"]
        )

        if quality_text == "":
            quality_text = "Unknown"

        message += (
            f"🎥 {movie['title']}\n"
            f"📀 Quality: {quality_text}\n"
            f"🔗 {movie['url']}\n\n"
        )

    await update.message.reply_text(message)

# =========================================================
# TAMIL MOVIES
# =========================================================

async def tamil(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    movies = scrape_movies()

    tamil_movies = []

    for movie in movies:

        if "Tamil" in movie["title"]:

            tamil_movies.append(movie)

    if len(tamil_movies) == 0:

        await update.message.reply_text(
            "❌ No Tamil movies found"
        )

        return

    message = "🔥 Tamil Movies\n\n"

    for movie in tamil_movies[:10]:

        quality_text = ", ".join(
            movie["qualities"]
        )

        if quality_text == "":
            quality_text = "Unknown"

        message += (
            f"🎥 {movie['title']}\n"
            f"📀 Quality: {quality_text}\n"
            f"🔗 {movie['url']}\n\n"
        )

    await update.message.reply_text(message)

# =========================================================
# NORMAL MESSAGE
# =========================================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    await update.message.reply_text(
        f"""
You said:

{text}

Use /help for commands.
"""
    )

# =========================================================
# AUTO NOTIFICATION
# =========================================================

async def send_notifications(app):

    print("Checking for new movies...")

    old_movies = load_movies()

    current_movies = scrape_movies()

    old_titles = [
        movie["title"]
        for movie in old_movies
    ]

    new_movies = []

    for movie in current_movies:

        if movie["title"] not in old_titles:

            new_movies.append(movie)

    if len(new_movies) == 0:

        print("No new movies found")

        return

    print("NEW MOVIES:", len(new_movies))

    for movie in new_movies[:10]:

        quality_text = ", ".join(
            movie["qualities"]
        )

        if quality_text == "":
            quality_text = "Unknown"

        message = (
            f"🎬 New Movie Added\n\n"
            f"🎥 {movie['title']}\n"
            f"📀 Quality: {quality_text}\n"
            f"🔗 {movie['url']}"
        )

        try:

            await app.bot.send_message(
                chat_id=CHAT_ID,
                text=message
            )

            print("Notification Sent")

        except Exception as e:

            print("Telegram Error:", e)

    save_movies(current_movies)

# =========================================================
# AUTO CHECK LOOP
# =========================================================

async def auto_check(app):

    while True:

        try:

            await send_notifications(app)

        except Exception as e:

            print("Auto Check Error:", e)

        # 15 MINUTES
        await asyncio.sleep(900)

# =========================================================
# MAIN
# =========================================================

async def main():

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    # COMMANDS

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("latest", latest)
    )

    app.add_handler(
        CommandHandler("search", search)
    )

    app.add_handler(
        CommandHandler("tamil", tamil)
    )

    # NORMAL MESSAGES

    app.add_handler(
        MessageHandler(
            filters.TEXT,
            handle_message
        )
    )

    print("🎬 CinePulse Bot Started")

    # START AUTO CHECK
    asyncio.create_task(
        auto_check(app)
    )

    await app.initialize()

    await app.start()

    await app.updater.start_polling()

    print("Bot Running Successfully")

    while True:

        await asyncio.sleep(1)

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    asyncio.run(main())