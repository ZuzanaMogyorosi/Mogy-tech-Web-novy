# NASTAVENÍ EMAILŮ Z POPTÁVKOVÉHO FORMULÁŘE

import os
import smtplib
from email.mime.text import MIMEText
from flask import flash
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_TO = os.getenv('EMAIL_TO', '')  # Např. mail majitele

def send_email(subject, body, recipient=None, send_to_owner=False):
    #===============================================================
    # Odešle e-mail s daným předmětem a tělem na zadanou adresu.
    # Pokud je send_to_owner=True, pošle se na EMAIL_TO (tj. majitel).
    #===============================================================
    try:
        to_addr = EMAIL_TO if send_to_owner else recipient
        if not to_addr:
            return  # Není co posílat

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_addr

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, [to_addr], msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(f"Chyba při odesílání emailu: {e}")
        flash("Nepodařilo se odeslat e-mail.")
