import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nfe.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom