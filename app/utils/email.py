from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_user,
    MAIL_PASSWORD=settings.smtp_pass,
    MAIL_FROM=settings.email_from,
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_host,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=settings.use_credentials,
    VALIDATE_CERTS=settings.validate_certs,
)

async def send_otp_email(email: EmailStr, otp: str):
    """Sends a 6-digit OTP code to the specified email."""
    
    html = f"""
    <h3>Password Recovery</h3>
    <p>Your verification code is: <strong>{otp}</strong></p>
    <p>This code will expire in 5 minutes.</p>
    <br>
    <p>If you did not request this, please ignore this email.</p>
    """

    message = MessageSchema(
        subject="Password Recovery OTP - AK Food",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info(f"OTP email successfully sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}. Error: {e}")
        # Reraise or handle based on app requirements. For now, log it.
