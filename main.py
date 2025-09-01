import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_TOKEN = os.getenv("API_TOKEN")

print("===== DEBUG VARIABLES =====")
print("BOT_TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)
print("API_TOKEN:", API_TOKEN)
print("============================")