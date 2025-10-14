import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://dev.ishgo.uz")
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "93 505 20 25")
