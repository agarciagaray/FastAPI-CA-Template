from twilio.rest import Client
import os

def send_whatsapp(to_number: str, message: str):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")  # Ejemplo: 'whatsapp:+14155238886'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=f"whatsapp:{to_number}"
    )
    return message.sid