import os
from dotenv import load_dotenv

load_dotenv()


def get_env_variable(var_name: str, default=None, required=True):
    value = os.getenv(var_name, default)
    if required and value is None:
        raise ValueError(f"Missing required environment variable: {var_name}")
    return value
# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# JWT and authentication config
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Email configuration (using SMTP for email sending)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_email_password")
EMAIL_USE_TLS = get_env_variable("EMAIL_USE_TLS", "True", required=False).lower() == "true"
EMAIL_USE_SSL = get_env_variable("EMAIL_USE_SSL", "False", required=False).lower() == "true"