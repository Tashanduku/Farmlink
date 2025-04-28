import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:your_password@localhost/farmlink'
    SQLALCHEMY_TRACK_MODIFICATIONS = False