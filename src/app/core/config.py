import os

import dotenv

dotenv.load_dotenv()


class Settings:
    POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    DB_MIN_POOL_CON: int = os.getenv("DB_MIN_POOL_CON", 10)
    DB_MAX_POOL_CON: int = os.getenv("DB_MAX_POOL_CON", 80)
    DB_POOL_SIZE: int = os.getenv("DB_POOL_SIZE", 100)
    DB_POOL_OVERFLOW: int = os.getenv("DB_POOL_OVERFLOW", 20)
    DB_TIMEOUT: int = os.getenv("DB_TIMEOUT", 5)
    IS_DB_ECHO_LOG: bool = os.getenv("IS_DB_ECHO_LOG", False)
    IS_DB_EXPIRE_ON_COMMIT: bool = os.getenv("IS_DB_EXPIRE_ON_COMMIT", False)
    IS_DB_FORCE_ROLLBACK: bool = os.getenv("IS_DB_FORCE_ROLLBACK", False)


settings = Settings()
