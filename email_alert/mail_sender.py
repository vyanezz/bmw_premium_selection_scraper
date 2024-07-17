import smtplib


class mail:
    def __init__(self, gmail_user, gmail_password, sender=None, receiver=None, message=None):
        self.server = smtplib.SMTP('smtp.gmail.com', 587)

        self.gmail_user = gmail_user
        self.gmail_password = gmail_password

        self.sender = sender
        self.receiver = receiver
        self.message = message

    def login(self):
        self.server.starttls()
        check = self.server.login(self.gmail_user, self.gmail_password)
        return check

    def sendMessage(self):
        self.server.sendmail(self.sender, self.receiver, self.message.as_string())

