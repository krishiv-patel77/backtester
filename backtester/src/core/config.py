from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str
    DATABASE_URL: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        env_file = "../../../.env"

settings = Settings()