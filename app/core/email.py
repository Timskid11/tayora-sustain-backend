import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_email(subject: str, recipients: list, body: str):
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    # Brevo needs the emails formatted as a list of dictionaries
    to_list = [{"email": email} for email in recipients]
    
    payload = {
        "sender": {
            "email": settings.MAIL_FROM, 
            "name": "Tayora Sustain"
        },
        "to": to_list,
        "subject": subject,
        "htmlContent": body
    }
    
    # Send the email using standard HTTP (Port 443) which Render allows
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status() 
            logger.info(f"Email sent successfully to {recipients}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to send email: {e.response.text}")
            raise e
    
