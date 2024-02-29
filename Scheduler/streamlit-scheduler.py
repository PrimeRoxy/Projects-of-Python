import datetime
import os.path
import pickle
import streamlit as st
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

class MeetingScheduler:
    # Initialize class variables to store meeting details and Google Calendar service.
    def __init__(self):
        self.meeting_start_time = None
        self.meeting_end_time = None
        self.meeting_date = None
        self.attendee_email = None
        self.service = None

    def get_meeting_details(self, date_str, start_time_hour, start_time_minute, end_time_hour, end_time_minute, attendee_email):
        # Parse and validate meeting details such as date, start time, end time, and attendee email.
       
        try:
            year, month, day = map(int, date_str.split('-'))
            self.meeting_date = datetime.date(year, month, day)
        except ValueError:
            raise ValueError("Invalid date format. Please enter a date in YYYY-MM-DD format.")

        try:
            start_hour = int(start_time_hour)
            start_minute = int(start_time_minute)
            end_hour = int(end_time_hour)
            end_minute = int(end_time_minute)

            local_timezone = pytz.timezone('Asia/Kolkata')
            self.meeting_start_time = local_timezone.localize(datetime.datetime(self.meeting_date.year, self.meeting_date.month, self.meeting_date.day, start_hour, start_minute))
            self.meeting_end_time = local_timezone.localize(datetime.datetime(self.meeting_date.year, self.meeting_date.month, self.meeting_date.day, end_hour, end_minute))
        except ValueError:
            raise ValueError("Invalid time format.")

        self.attendee_email = attendee_email

    def generate_meeting_link(self):
        # Generate a Google Calendar event and print the meeting link.
        
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
            st.success(f"Meeting scheduled: {event['htmlLink']}")
        except Exception as e:
            st.error(f"An error occurred while scheduling the meeting: {e}")

    def finish_meeting(self, event_id):
        # Finish the meeting by deleting the specified event from Google Calendar.

        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            st.info(f"Meeting with attendee {self.attendee_email} finished.")
        except Exception as e:
            st.error(f"An error occurred while finishing the meeting: {e}")

    def fetch_conflicting_meetings(self, time_min, time_max):
        # Fetch events from Google Calendar that conflict with the specified time range.
        # and check if there is an existing meeting for the same day and time.

        events_result = self.service.events().list(calendarId='primary', timeMin=time_min,
                                                   timeMax=time_max, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def fetch_existing_meeting(self):
        # Fetch the upcoming events from Google Calendar

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        return events_result.get('items', [])

    def print_event_details(self, event):
        # Print details of a Google Calendar event.

        st.write(f"Event summary: {event['summary']}")
        st.write(f"Start time: {event['start']['dateTime']}")
        st.write(f"End time: {event['end']['dateTime']}")
        st.write(f"Attendees: {[attendee['email'] for attendee in event.get('attendees', [])]}")
        st.write("---")

    def schedule_meeting(self, date_str, start_time_hour, start_time_minute, end_time_hour, end_time_minute, attendee_email):
        # Main function to schedule a meeting, check for conflicts, and handle existing meetings.

        # Initialize Google Calendar API service
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

        # Gather and validate meeting details from the user
        self.get_meeting_details(date_str, start_time_hour, start_time_minute, end_time_hour, end_time_minute, attendee_email)
        if not self.meeting_date or not self.meeting_start_time or not self.meeting_end_time or not self.attendee_email:
            st.error("Invalid meeting details. Please provide valid date, start time, end time, and email.")
            return

        start_datetime = self.meeting_start_time.isoformat()
        end_datetime = self.meeting_end_time.isoformat()

        try:
            # Check for existing meeting with the same attendee
            existing_meetings = self.fetch_existing_meeting()

            for event in existing_meetings:
                attendees = [attendee['email'] for attendee in event.get('attendees', [])]
                if self.attendee_email in attendees:
                    st.warning(f"Meeting with attendee {self.attendee_email} already scheduled:")
                    st.write("Finish this meeting first")
                    self.print_event_details(event)
                    st.write("Meeting not scheduled.")
                    return

            # Check for conflicts with other meetings.
            events_conflict = self.fetch_conflicting_meetings(start_datetime, end_datetime)

            if events_conflict:
                st.warning("Conflict! Meetings already scheduled in this time range:")
                for event in events_conflict:
                    self.print_event_details(event)
                    st.write("Meeting not scheduled.")
                    return
                
            # Schedule the new meeting and print details.
            self.generate_meeting_link()

            # Print all events again after scheduling the new meeting
            events_all = self.fetch_existing_meeting()
            for event in events_all:
                self.print_event_details(event)

        except Exception as e:
            st.error(f"An error occurred while fetching events: {e}")

# Create Streamlit app UI
def main():
    st.title("Meeting Scheduler")

    scheduler = MeetingScheduler()

    date_str = st.date_input("Meeting Date")
    
    start_time_hour = st.selectbox("Start Hour", list(range(0, 24)), format_func=lambda x: f"{x:02d}")
    start_time_minute = st.selectbox("Start Minute", list(range(0, 60)), format_func=lambda x: f"{x:02d}")

    end_time_hour = st.selectbox("End Hour", list(range(0, 24)), format_func=lambda x: f"{x:02d}")
    end_time_minute = st.selectbox("End Minute", list(range(0, 60)), format_func=lambda x: f"{x:02d}")

    attendee_email = st.text_input("Attendee Email")

    if st.button("Schedule Meeting"):
        scheduler.schedule_meeting(str(date_str), start_time_hour, start_time_minute, end_time_hour, end_time_minute, attendee_email)

if __name__ == "__main__":
    main()
