from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from openai import OpenAI
import sys
import os
from datetime import datetime, timedelta
import json
import logging
import dateutil.parser
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Agent.meeting_agent import MeetingAgent
from config import BASE_URL, MODEL_PATH, OPENAI_API_KEY, GOOGLE_SCOPES, KEYS_DIR
import glob
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)
agent = MeetingAgent(client, MODEL_PATH)

# Setup logging
logging.basicConfig(
    filename="scheduler.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s"
)
app = Flask(__name__)

# Helper to fetch calendar events for a user
def retrive_calendar_events(user_email, start, end):
    events_list = []
    # Use correct token file naming: userone.amd.token
    token_path = os.path.join(KEYS_DIR, user_email.split("@")[0]+".amd.token")
    token_files = glob.glob(os.path.join(KEYS_DIR, '*.token'))
    if not os.path.exists(token_path):
        if token_files:
            token_path = token_files[0]
        else:
            logging.warning(f"No token file found for {user_email}. Returning empty events.")
            return []
    user_creds = Credentials.from_authorized_user_file(token_path)
    calendar_service = build("calendar", "v3", credentials=user_creds)
    events_result = calendar_service.events().list(calendarId='primary', timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        attendee_list = []
        try:
            for attendee in event.get("attendees", []):
                attendee_list.append(attendee['email'])
        except:
            attendee_list.append("SELF")
        start_time = event["start"]["dateTime"]
        end_time = event["end"]["dateTime"]
        events_list.append({
            "StartTime": start_time,
            "EndTime": end_time,
            "NumAttendees": len(set(attendee_list)),
            "Attendees": list(set(attendee_list)),
            "Summary": event.get("summary", "")
        })
    logging.info(f"Fetched events for {user_email}: {json.dumps(events_list, indent=2)}")
    return events_list
# Add a route for direct calendar event debugging
@app.route("/calendar_events", methods=["GET"])
def calendar_events():
    user = request.args.get("user")
    start = request.args.get("start")
    end = request.args.get("end")
    if not user or not start or not end:
        return jsonify({"error": "Missing user, start, or end parameter"}), 400
    events = retrive_calendar_events(user, start, end)
    return jsonify({"user": user, "start": start, "end": end, "events": events})

# Main scheduling endpoint
@app.route("/schedule", methods=["POST"])
def schedule():
    data = request.get_json(force=True)
    # Extract required fields
    request_id = data.get("Request_id")
    datetime_str = data.get("Datetime")
    location = data.get("Location", "")
    sender = data.get("From")
    attendees = data.get("Attendees", [])
    subject = data.get("Subject", "")
    email_content = data.get("EmailContent", "")

    # Use today's date if not provided
    if not datetime_str:
        datetime_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    else:
        # Convert 'DD-MM-YYYY' to 'YYYY-MM-DD' if needed
        date_part, time_part = datetime_str.split('T')
        if '-' in date_part and len(date_part.split('-')[0]) == 2:
            # Assume format is 'DD-MM-YYYY', convert to 'YYYY-MM-DD'
            day, month, year = date_part.split('-')
            date_only = f"{year}-{month}-{day}"
            datetime_str = f"{date_only}T{time_part}"
        else:
            date_only = date_part

    # Set scheduling window (full day)
    start = f"{date_only}T00:00:00+05:30"
    end = f"{date_only}T23:59:59+05:30"

    # Get events for all participants
    all_attendees = [sender] + [a["email"] for a in attendees]
    attendees_with_events = []
    attendee_busy_dict = {}
    for email in all_attendees:
        events = retrive_calendar_events(email, start, end)
        attendees_with_events.append({"email": email, "events": events})
        busy_slots = []
        for event in events:
            busy_slots.append({
                "start": event["StartTime"],
                "end": event["EndTime"]
            })
        attendee_busy_dict[email] = {"busy": busy_slots}
        logging.debug(f"Busy slots for {email}: {json.dumps(busy_slots, indent=2)}")

    # Call agent to resolve and schedule
    constraints = agent.parse_meeting_request(data)
    logging.info(f"Parsed constraints from LLM: {json.dumps(constraints, indent=2)}")
    # Fallback for missing duration
    duration = int(constraints.get("duration_minutes", data.get("Duration_mins", 30)))

    llm_payload = {
        "duration_minutes": duration,
        "start_window": start,
        "end_window": end,
        "timezone": "Asia/Kolkata",
        "requested_start": datetime_str
    }
    logging.info(f"Passing to agent.resolve_conflicts_and_schedule: busy_dict={json.dumps(attendee_busy_dict, indent=2)}, constraints={json.dumps(llm_payload, indent=2)}")

    scheduled = agent.resolve_conflicts_and_schedule(
        attendee_busy_dict,
        llm_payload
    )
    logging.info(f"Agent scheduling response: {json.dumps(scheduled, indent=2)}")

    # Build output
    if scheduled.get("start") and scheduled.get("end"):
        confirmed_subject = f"Confirmed: {subject}"
        confirmed_email = (
            f"Hi team, after checking everyone's calendar, this time was selected and confirmed. "
            f"Looking forward to seeing you all!\n\nDetails:\nDate & Time: {scheduled.get('start')} to {scheduled.get('end')}\nLocation: {location}"
        )
        output = {
            "Request_id": request_id,
            "Datetime": datetime_str,
            "Location": location,
            "From": sender,
            "Attendees": attendees_with_events,
            "Subject": confirmed_subject,
            "EmailContent": confirmed_email,
            "EventStart": scheduled.get("start"),
            "EventEnd": scheduled.get("end"),
            "Duration_mins": str(duration),
            "MetaData": {}
        }
    else:
        polite_fail = (
            f"Hi team, unfortunately, no common slot was found for all participants. "
            f"Please suggest alternative times or check your calendars."
        )
        output = {
            "Request_id": request_id,
            "Datetime": datetime_str,
            "Location": location,
            "From": sender,
            "Attendees": attendees_with_events,
            "Subject": f"Could not schedule: {subject}",
            "EmailContent": polite_fail,
            "EventStart": None,
            "EventEnd": None,
            "Duration_mins": str(duration),
            "MetaData": {}
        }
    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)