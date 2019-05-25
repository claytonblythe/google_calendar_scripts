from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime


def get_payday_dates():
    year = "2019"
    with open \
                (
                f"/Users/claytonb/github/google_calendar_scripts/data/{year}_zillow.txt") as f:
        lines = f.readlines()
        pay_dates = []
        for line in lines:
            pay_date = line.split()[3]
            month, day, year = map(int, pay_date.split("/"))
            pay_dates.append((month, day, year))
        return pay_dates


def get_api_service():
    SCOPES = 'https://www.googleapis.com/auth/calendar.events'
    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service


def add_paydate_events(dates, service):
    for date in dates:
        month, day, year = date
        date_obj = datetime(year, month, day)
        date_string = date_obj.strftime("%Y-%m-%d") + "T06:00:00-07:00"

        event = {
            'summary': f"Payday",
            'location': '',
            'description': 'Zillow Payday',
            'start': {
                'dateTime': date_string,
                'timeZone': 'America/Los_Angeles',
            },
            "end" : {
            "dateTime" : date_string,
            "timeZone" : "America/Los_Angeles"
        }
        }

        event = service.events().insert(calendarId='primary',
                                        body=event).execute()
        print(event)


def main():
    service = get_api_service()
    pay_dates = get_payday_dates()
    add_paydate_events(pay_dates, service)


if __name__ == "__main__":
    main()
