import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(
    recipient_email: str,
    subject: str,
    body: str,
    sender_email: str,
    smtp_password: str,
    html: bool = False,
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 587
) -> bool:
    """
    Send an email using SMTP.

    Args:
        recipient_email (str): Email address of the recipient
        subject (str): Subject of the email
        body (str): Content of the email
        sender_email (str): Sender's email address
        smtp_password (str): SMTP password or app-specific password
        html (bool): If True, sends email as HTML. Defaults to False
        smtp_server (str): SMTP server address. Defaults to Gmail's SMTP
        smtp_port (int): SMTP port number. Defaults to 587 (TLS)

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Create message container
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email

        # Create the body of the message
        content_type = 'html' if html else 'plain'
        mime_text = MIMEText(body, content_type)
        message.attach(mime_text)

        # Create SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Enable TLS
            server.login(sender_email, smtp_password)

            # Send email
            server.send_message(message)

        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    # Plain text emailI'
    success = send_email(
        recipient_email="caretaker.sentinel@gmail.com",
        subject="URGENT MESSAGE",
        body="Syke. Not that urgent.",
        sender_email="caretaker.sentinel@gmail.com",
        smtp_password="xotqszzwyrrqjvee"
    )
