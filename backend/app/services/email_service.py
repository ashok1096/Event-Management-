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

        import io
        import qrcode

        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(ticket_id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_data = img_byte_arr.getvalue()

        msg = EmailMessage()
        msg['Subject'] = f"Registration Confirmed: {event_title}"
        msg['From'] = smtp_user or "noreply@eventpulse.com"
        msg['To'] = to_email

        # Set the plain text fallback
        text_content = f"""
        Hi {attendee_name},

        You have successfully registered for {event_title}!
        
        Your Ticket ID is: {ticket_id}
        
        Please save this email. You can present this Ticket ID or the attached QR Code at the venue for check-in.

        Best regards,
        The EventPulse Team
        """
        msg.set_content(text_content)

        # Add beautiful HTML version
        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #4F46E5;">Registration Confirmed! 🎉</h2>
            <p>Hi <strong>{attendee_name}</strong>,</p>
            <p>You have successfully registered for <strong>{event_title}</strong>!</p>
            <div style="background-color: #F3F4F6; padding: 20px; border-radius: 8px; text-align: center; margin: 25px 0;">
                <p style="margin: 0; color: #6B7280; font-size: 14px; text-transform: uppercase; font-weight: bold;">Your Ticket ID</p>
                <h1 style="margin: 5px 0 0 0; color: #111827; letter-spacing: 3px; font-family: monospace;">{ticket_id}</h1>
            </div>
            <p>Please save this email. You can present the attached <strong>QR Code</strong> at the venue for quick and contactless check-in.</p>
            <br>
            <p>Best regards,<br><strong>The EventPulse Team</strong></p>
          </body>
        </html>
        """
        msg.add_alternative(html_content, subtype='html')

        # Attach the QR code image
        msg.add_attachment(img_data, maintype='image', subtype='png', filename=f'ticket_{ticket_id}.png')

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
