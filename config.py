
import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-please')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:Pavan143@localhost:3306/flipkart_support')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
