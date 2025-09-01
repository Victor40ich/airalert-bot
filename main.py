import asyncio
import aiohttp
from aiogram import Bot

# 👉 Тут впиши свої дані напряму
TOKEN = "7928801571:AAElQ_J6qieo6pvggLwinsZd4Q6YiFBpXOc"
CHAT_ID = "@ichnya"
API_TOKEN = "b173d916643516264fe848bb2b1be6a503398488ab2203"
TARGET_DISTRICT = "Прилуцький район"

bot = Bot(token=TOKEN, parse_mode="HTML")
previous_alert = None


async def check_alerts():
    global previous_alert
    url = f"https://api.alerts.in.ua/v1/alerts/active.json?token={API_TOKEN}"

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        print(f"[ERROR] HTTP {response.status}")
                        await asyncio.sleep(30)
                        continue

                    data = await response.json()

                    # Фільтруємо по Чернігівській області та Прилуцькому району
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

                    # Якщо статус змінився → надсилаємо повідомлення
                    if alert != previous_alert:
                        previous_alert = alert
                        if alert:
                            text = f"🚨 Повітряна тривога у {TARGET_DISTRICT}!"
                        else:
                            text = f"✅ Відбій у {TARGET_DISTRICT}!"
                        await bot.send_message(CHAT_ID, text)
                        print(f"[INFO] {text}")
                    else:
                        print("[INFO] Стан не змінився.")

            except Exception as e:
                print(f"[EXCEPTION] {e}")

            await asyncio.sleep(30)  # перевірка кожні 30 секунд


async def main():
    await check_alerts()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Зупинено вручну")