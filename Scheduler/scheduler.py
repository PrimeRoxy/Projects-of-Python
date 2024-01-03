import datetime
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

class MeetingScheduler:
    def __init__(self):
        self.meeting_start_time = None
        self.meeting_end_time = None
        self.meeting_date = None
        self.attendee_email = None
        self.service = None

    def get_meeting_details(self):
        try:
            date_entry = input("Enter a date in YYYY-MM-DD format: ")
            year, month, day = map(int, date_entry.split('-'))
            self.meeting_date = datetime.date(year, month, day)
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
            return

        try:
            start_time_entry = input("Enter a start time in HH:MM format: ")
            end_time_entry = input("Enter an end time in HH:MM format: ")

            start_hour, start_minute = map(int, start_time_entry.split(':'))
            end_hour, end_minute = map(int, end_time_entry.split(':'))

            local_timezone = pytz.timezone('Asia/Kolkata')
            self.meeting_start_time = local_timezone.localize(datetime.datetime(self.meeting_date.year, self.meeting_date.month, self.meeting_date.day, start_hour, start_minute))
            self.meeting_end_time = local_timezone.localize(datetime.datetime(self.meeting_date.year, self.meeting_date.month, self.meeting_date.day, end_hour, end_minute))
        except ValueError:
            print("Invalid time format. Please enter start and end times in HH:MM format.")
            return

        self.attendee_email = input("Enter the attendee's email: ")

    def generate_meeting_link(self):
        event = {
            'summary': 'Meeting',
            'start': {
                'dateTime': self.meeting_start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': self.meeting_end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [
                {'email': self.attendee_email},
            ],
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Meeting scheduled: {event['htmlLink']}")
        except Exception as e:
            print(f"An error occurred while scheduling the meeting: {e}")
            print(f"Error details: {e.details}")

    def finish_meeting(self, event_id):
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f"Meeting with attendee {self.attendee_email} finished.")
        except Exception as e:
            print(f"An error occurred while finishing the meeting: {e}")
            print(f"Error details: {e.details}")

    def fetch_conflicting_meetings(self, time_min, time_max):
        events_result = self.service.events().list(calendarId='primary', timeMin=time_min,
                                                   timeMax=time_max, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def fetch_existing_meeting(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def print_event_details(self, event):
        print(f"Event summary: {event['summary']}")
        print(f"Start time: {event['start']['dateTime']}")
        print(f"End time: {event['end']['dateTime']}")
        print(f"Attendees: {[attendee['email'] for attendee in event.get('attendees', [])]}")
        print("---")

    def schedule_meeting(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar'])
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('calendar', 'v3', credentials=creds)

        self.get_meeting_details()
        if not self.meeting_date or not self.meeting_start_time or not self.meeting_end_time or not self.attendee_email:
            print("Invalid meeting details. Please provide valid date, start time, end time, and email.")
            return

        start_datetime = self.meeting_start_time.isoformat()
        end_datetime = self.meeting_end_time.isoformat()

        print("Start Datetime:", start_datetime)
        print("End Datetime:", end_datetime)

        try:
            # Check for existing meeting with the same attendee
            existing_meetings = self.fetch_existing_meeting()

            for event in existing_meetings:
                attendees = [attendee['email'] for attendee in event.get('attendees', [])]
                if self.attendee_email in attendees:
                    print(f"Meeting with attendee {self.attendee_email} already scheduled:")
                    self.print_event_details(event)

                    # Optionally, ask the user if they want to finish the existing meeting
                    response = input("Do you have finish the existing meeting? (yes/no): ")
                    if response.lower() == 'yes':
                        self.finish_meeting(event['id'])
                        print("Existing meeting finished.")
                        return
                    else:
                        print("Meeting not scheduled.")
                        return

            # Check for time conflicts
            events_conflict = self.fetch_conflicting_meetings(start_datetime, end_datetime)

            if events_conflict:
                print("Conflict! Meetings already scheduled in this time range:")
                for event in events_conflict:
                    self.print_event_details(event)

                # Optionally, you can ask the user if they still want to schedule the meeting
                response = input("Do you still want to schedule the meeting? (yes/no): ")
                if response.lower() != 'yes':
                    print("Meeting not scheduled.")
                    return

            self.generate_meeting_link()

            # Print all events again after scheduling the new meeting
            print("All events after scheduling:")
            events_all = self.fetch_existing_meeting()
            for event in events_all:
                self.print_event_details(event)

        except Exception as e:
            print(f"An error occurred while fetching events: {e}")

# Create an instance of MeetingScheduler and schedule a meeting
scheduler = MeetingScheduler()
scheduler.schedule_meeting()
