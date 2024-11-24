import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(
    sender_name: str,
    recipient_name: str,
    body: str
) -> bool:
    html = False
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    subject = f"URGENT MESSAGE: {sender_name} requires assistance!"
    sender_email = "caretaker.sentinel@gmail.com"
    smtp_password ="xotqszzwyrrqjvee"
    recipient_email = "arnavnagpal@gmail.com"
    
    try:
        # Create message container
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email
        final_body = f"""
        Hi {recipient_name},
        
        You are receiving this email as {sender_name}'s registered primary caretaker and they require reported a severe issue.
        Here is what the user reported:
        {body}
        
        Please contact the individual if you think they require help.
        
        Sent with CaretakerAI
        """

        # Create the body of the message
        content_type = 'html' if html else 'plain'
        mime_text = MIMEText(final_body, content_type)
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
