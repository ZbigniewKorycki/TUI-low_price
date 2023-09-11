import os
from email.message import EmailMessage
import ssl
import smtplib



def start_sender():
    email_sender = os.environ.get("EMAIL_SENDER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_receiver = os.environ.get("EMAIL_RECEIVER")

    subject = "Latest TUI Offers"
    body = "Body"

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content("Below are attached TUI Last Minute offers.")

    context = ssl.create_default_context()

    try:
        with open("Offers_under_1500_TUI.csv", "rb") as Offers_under_1500_TUI:
            em.add_attachment(
                Offers_under_1500_TUI.read(),
                maintype="application",
                subtype="octet-stream",
                filename=Offers_under_1500_TUI.name,
            )
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            try:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, msg=em.as_string())
                print("Message sent.")
            except Exception as e:
                print(f"An error occurred: {e}")
    except FileNotFoundError:
        print("File not found.")



