import json
import os
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

TIMEZONE = "Europe/Lisbon"
REMINDERS_FILE = os.path.join(os.path.dirname(__file__), "reminders.json")


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        resp.read()


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    with open(REMINDERS_FILE, encoding="utf-8") as f:
        reminders = json.load(f)

    now = datetime.now(ZoneInfo(TIMEZONE))
    current_time = now.strftime("%H:%M")

    sent = 0
    for reminder in reminders:
        if reminder["time"] == current_time:
            send_telegram_message(token, chat_id, reminder["message"])
            sent += 1

    print(f"Lisbon time {current_time}: sent {sent} reminder(s)")


if __name__ == "__main__":
    main()
