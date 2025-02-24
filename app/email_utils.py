"""
NASTAVENÍ EMAILŮ Z POPTÁVKOVÉHO FORMULÁŘE
"""

import os
import smtplib
from email.mime.text import MIMEText
from flask import flash
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))  # Defaultní hodnota pro SMTP port
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_TO = os.getenv('EMAIL_TO', '')  # Např. mail majitele

def send_email(subject, body, recipient=None, send_to_owner=False):
    """
    Odešle e-mail s daným předmětem a tělem na zadanou adresu.
    Pokud je send_to_owner=True, pošle se na EMAIL_TO (tj. majitel).
    """
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

def send_owner_email(full_name, email, message):
    """
    Odešle e-mail majiteli s informacemi z formuláře.
    """
    subject_owner = "Nová poptávka z webu"
    email_body_owner = (
        f"Jméno: {full_name}\n"
        f"Email: {email}\n"
        f"Zpráva:\n{message}"
    )
    send_email(subject_owner, email_body_owner, send_to_owner=True)

def send_customer_email(full_name, email, message):
    """
    Odešle potvrzovací e-mail zákazníkovi.
    """
    subject_customer = "Potvrzení poptávky"
    email_body_customer = (
        "Dobrý den,\n\n"
        "děkujeme za Vaši poptávku. Toto je potvrzení, že jsme ji úspěšně obdrželi.\n\n"
        f"Jméno: {full_name}\n"
        f"E-mail: {email}\n"
        f"Zpráva:\n{message}\n\n"
        "Ozveme se Vám co nejdříve.\n\n"
        "S pozdravem,\nTým Autoservis Mogy-tech"
    )
    send_email(subject_customer, email_body_customer, recipient=email)