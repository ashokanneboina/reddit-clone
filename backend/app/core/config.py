from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Reddit Clone API"
    API_V1_STR: str = "/api/v1"
    
    # SQLite for local development
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./reddit_clone.db"
    
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_ME_IN_PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        case_sensitive = True

settings = Settings()
