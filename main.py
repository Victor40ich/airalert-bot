import asyncio
import requests
from aiogram import Bot
import os

# Читаємо змінні оточення з Railway (вони задані у вкладці Variables)
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_TOKEN = os.getenv("API_TOKEN")
TARGET_DISTRICT = "Прилуцький район"

bot = Bot(token=TOKEN)
previous_alert = None

async def check_alerts():
    global previous_alert
    url = f"https://api.alerts.in.ua/v1/alerts/active.json?token={API_TOKEN}"

    while True:
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            # Шукаємо потрібний район у Чернігівській області
            pryluky = next(
                (a for a in data if 
                 a.get("region") == "Чернігівська область" and 
                 a.get("district") == TARGET_DISTRICT),
                None
            )

            if not pryluky:
                print(f"[WARN] {TARGET_DISTRICT} не знайдено у відповіді API")
                await asyncio.sleep(30)
                continue

            alert = pryluky.get("alert", False)

            # Якщо стан змінився — шлемо повідомлення
            if alert != previous_alert:
                previous_alert = alert
                if alert:
                    text = f"🚨 Повітряна тривога у {TARGET_DISTRICT}!"
                else:
                    text = f"✅ Відбій у {TARGET_DISTRICT}!"
                await bot.send_message(CHAT_ID, text)
                print(f"[INFO] {text}")

        except Exception as e:
            print(f"[ERROR] {e}")

        await asyncio.sleep(30)  # перевірка кожні 30 секунд

async def main():
    await check_alerts()

if __name__ == "__main__":
    asyncio.run(main())
