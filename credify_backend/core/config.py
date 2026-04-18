import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = ""
    DATABASE_NAME: str = "credify_db"
    
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Email settings (Mock for now if not provided)
    EMAIL_USER: str = os.getenv("EMAIL_USER", "")
    EMAIL_PASS: str = os.getenv("EMAIL_PASS", "")
    EMAIL_HOST: str = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT", 587))
    

    # ML Model Paths
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", "ml_models/credit_score_model.pkl")
    SCALER_PATH: str = os.getenv("SCALER_PATH", "ml_models/scaler.pkl")
    
    # Agent Settings (Gemini)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    AGENT_TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    AGENT_MAX_ITERATIONS: int = int(os.getenv("AGENT_MAX_ITERATIONS", "10"))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
    RATE_LIMIT_PER_DAY: int = int(os.getenv("RATE_LIMIT_PER_DAY", "1500"))

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"

settings = Settings()
