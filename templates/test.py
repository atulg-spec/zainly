import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject

        # Add body to the message
        message.attach(MIMEText(body, 'plain'))

        # Create SMTP session for sending the mail
        server = smtplib.SMTP('cooperclinic.pk', 587)  # Use your SMTP server and port
        server.starttls()  # Enable security
        server.login(sender_email, sender_password)  # Log in to the SMTP server

        text = message.as_string()  # Convert the message to string format
        server.sendmail(sender_email, recipient_email, text)  # Send the email

        server.quit()  # Terminate the SMTP session
        print("Email successfully sent to", recipient_email)

    except Exception as e:
        print("Error occurred while sending the email:", e)


# Example usage
sender_email = 'sharif@cooperclinic.pk'
sender_password = 'Shariful2214'
recipient_email = 'atulg0736@gmail.com'  # Update the recipient email
subject = 'Test Email from Cooper Clinic'
body = ' server.'

send_email(sender_email, sender_password, recipient_email, subject, body)
