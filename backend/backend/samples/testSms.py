# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="This is a message sent with CareTakerAI where we take care of you.",
    from_="+19789694707",
    to="+15483337532"
    # scheduleType="fixed",
    # sendAt=datetime(2024, 11, 23, 23, 55, 27),
)

print(message.body)