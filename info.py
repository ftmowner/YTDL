import os

SESSION = "my_bot"
API_ID = int(os.getenv("API_ID", "80122"))
API_HASH = os.getenv("API_HASH", "171")
BOT_TOKEN = os.getenv("BOT_TOKEN", "80759xZZnChpX5srczTxgxz5YmHQ8")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002284232975"))
DUMP_CHANNEL = int(os.getenv("DUMP_CHANNEL", "-1002284232975"))
PORT = int(os.getenv("PORT", "8080"))
FORCE_CHANNEL = int(os.getenv("FORCE_CHANNEL", "-1002379643238"))
HTTP_PROXY = ''
MONGO_URI = os.getenv("MONGO_URI", "hhh")
MONGO_NAME = os.getenv("MONGO_NAME", "YouTubeDL")
ADMINS = [5660839376]
DAILY_LIMITS = 10 
