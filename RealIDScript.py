import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
import re

# Email configuration
EMAIL_SENDER = "hanishmutyala@gmail.com"
EMAIL_PASSWORD = "nfbfluyiincnlwip"
EMAIL_RECEIVER = "hanishmutyala@gmail.com"

# Target URL
URL = "https://telegov.njportal.com/njmvc/AppointmentWizard/16"

def check_appointments():
    print("Checking for appointments...")
    response = requests.get(URL)
    
    if response.status_code != 200:
        print("Failed to fetch the page.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()

    # Look for text like "123 Appointments Available"
    matches = re.findall(r"\b\d+\s+Appointments Available\b", page_text)

    if matches:
        print(f"Appointments found: {matches}")
        send_email()
    else:
        print("No appointments available.")

def send_email():
    subject = "🎉 NJ MVC Appointment Available!"
    body = f"Appointments may be available at {URL}"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule the job every hour
schedule.every(1).hours.do(check_appointments)

# Run the script continuously
if __name__ == "__main__":
    print("Starting appointment checker...")
    check_appointments()  # Run immediately
    while True:
        schedule.run_pending()
        time.sleep(60)
