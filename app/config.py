from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # We kept MAIL_FROM, removed the SMTP stuff, and added the Brevo Key
    MAIL_FROM: str
    BREVO_API_KEY: str  
    
    FRONTEND_URL: str = "https://tayorasustain.vercel.app"

    class Config:
        env_file = ".env"

settings = Settings()

