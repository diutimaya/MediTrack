import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///medicine_reminder.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_FROM    = os.environ.get("MAIL_FROM", os.environ.get("MAIL_USERNAME"))

    LOW_STOCK_CHECK_INTERVAL_MINUTES = 60
    REMINDER_CHECK_INTERVAL_SECONDS  = 60