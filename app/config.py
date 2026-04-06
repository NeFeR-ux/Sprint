import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST = os.getenv("FSTR_DB_HOST", "localhost")
    DB_PORT = os.getenv("FSTR_DB_PORT", "5432")
    DB_LOGIN = os.getenv("FSTR_DB_LOGIN", "postgres")
    DB_PASS = os.getenv("FSTR_DB_PASS", "")
    DB_NAME = os.getenv("FSTR_DB_NAME", "fstr_db")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_LOGIN}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()