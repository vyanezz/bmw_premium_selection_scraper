from email_alert.mail_sender import mail
from dotenv import load_dotenv
import os


def prepareMail(message):
    load_dotenv("email_alert/mail_user_data.env")


    email = os.getenv("mail_smtp")
    passw = os.getenv("pass_smtp")

    sender_email = os.getenv("sender_email")
    receiver_emails = os.getenv("receiver_emails")
    return sendMail(email, passw, sender_email, receiver_emails,
                    message)


def sendMail(email, passw, sender_email, receiver_emails, message):
    mailData = mail(gmail_user=email, gmail_password=passw, sender=sender_email, receiver=receiver_emails,
                    message=message)

    mailData.login()
    mailData.sendMessage()


