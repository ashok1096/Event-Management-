"""Email service for sending asynchronous background emails."""

import os
import smtplib
from email.message import EmailMessage
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_registration_email(to_email: str, attendee_name: str, event_title: str, ticket_id: str):
        """
        Sends a registration confirmation email.
        This function runs in the background.
        """
        from dotenv import load_dotenv
        load_dotenv()
        
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        msg = EmailMessage()
        msg['Subject'] = f"Registration Confirmed: {event_title}"
        msg['From'] = smtp_user or "noreply@eventpulse.com"
        msg['To'] = to_email

        content = f"""
        Hi {attendee_name},

        You have successfully registered for {event_title}!
        
        Your Ticket ID is: {ticket_id}
        
        Please save this email. You can present this Ticket ID at the venue for check-in.

        Best regards,
        The EventPulse Team
        """
        msg.set_content(content)

        # If SMTP credentials aren't configured, we just simulate sending it.
        # This is great for local development without spamming real emails.
        if not smtp_user or not smtp_password:
            logger.info(f"📩 [SIMULATED EMAIL] Sent to {to_email} for event '{event_title}'. Ticket ID: {ticket_id}")
            print(f"📩 [SIMULATED EMAIL] Sent to {to_email} for event '{event_title}'. Ticket ID: {ticket_id}")
            return

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                logger.info(f"✅ Email successfully sent to {to_email}")
        except Exception as e:
            logger.error(f"❌ Failed to send email to {to_email}: {str(e)}")
