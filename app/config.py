from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: str
    DATABASE_URL_FOR_ALEMBIC: str

    class Config:
        env_file = ".env"
        from_attributes = True


settings = Settings()
