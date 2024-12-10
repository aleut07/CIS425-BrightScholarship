import os

class Config:
    """Base configuration class for the Flask application."""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secure_key')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///scholarship.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance

    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Your email address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Your email password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Additional Settings
    DEBUG = os.environ.get('DEBUG', True)
