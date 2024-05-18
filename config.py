import os
from dotenv import load_dotenv

load_dotenv()


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TOKEN = os.getenv("TOKEN")
DB_NAME = os.getenv("DB_NAME")
MONGO = os.getenv("MONGO")
GOKIL = ". ! ? / , - +"
PREFIX = GOKIL.split()
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "97429043").split()))
