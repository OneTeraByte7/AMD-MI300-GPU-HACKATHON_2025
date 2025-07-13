from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from datetime import datetime, timezone
import pytz, os, json

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_service(user_email: str):
    token_path = f"./Keys/{user_email.split('@')[0]}.token"
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    return build("calendar", "v3", credentials=creds, cache_discovery=False)

def freebusy(email_list, time_min, time_max, tz="UTC"):
    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "timeZone": tz,
        "items": [{"id": e} for e in email_list],
    }
    service = get_service(email_list[0])  # any authorized user
    resp = service.freebusy().query(body=body).execute()
    return resp["calendars"]
