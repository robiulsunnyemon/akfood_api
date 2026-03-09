from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    
    # JWT Settings
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expire_days: int = Field(default=7, env="JWT_EXPIRE_DAYS")
    otp_expire_minutes: int = Field(default=5, env="OTP_EXPIRE_MINUTES")

    # Email / SMTP Settings
    smtp_user: str = Field(..., env="SMTP_USER")
    smtp_pass: str = Field(..., env="SMTP_PASS")
    email_from: str = Field(..., env="EMAIL_FROM")
    smtp_port: int = Field(default=465, env="SMTP_PORT")
    smtp_host: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    mail_starttls: bool = Field(default=False)
    mail_ssl_tls: bool = Field(default=True)
    use_credentials: bool = Field(default=True)
    validate_certs: bool = Field(default=True)

    # Cloudinary Config (if needed)
    cloudinary_cloud_name: str | None = Field(default=None, env="CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key: str | None = Field(default=None, env="CLOUDINARY_API_KEY")
    cloudinary_api_secret: str | None = Field(default=None, env="CLOUDINARY_API_SECRET")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
