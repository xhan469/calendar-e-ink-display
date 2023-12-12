import exception
import calendar

from uuid import getnode as get_mac

import gpsoauth
import requests
from datetime import date, datetime, timedelta

email = 'hanxiaoyu0628@gmail.com'
password = 'lxjldcndhfogsrml'
dict_event = {}
Calendar = ""
session = requests.Session()

def send(**req_kwargs):
    """Send an authenticated request to a Google API.

    Args:
        **req_kwargs: Arbitrary keyword arguments to pass to Requests.

    Return:
        requests.Response: The raw response.

    Raises:
        LoginException: If :py:meth:`login` has not been called.
    """
    # Bail if we don't have an OAuth token.
    auth_token = login()   #"['Auth']"
    if auth_token is None:
        raise exception.LoginException("Not logged in")

    # Add the token to the request.
    req_kwargs.setdefault("headers", {"Authorization": "OAuth " + auth_token})
    #print(req_kwargs)
    request = session.request(**req_kwargs)

    return request


def login():
    android_id = get_mac()

    master_response = gpsoauth.perform_master_login(email, password, android_id)
    master_token = master_response['Token']

    auth_response = gpsoauth.perform_oauth(
        email, master_token, android_id,
        service="oauth2:https://www.googleapis.com/auth/calendar", app='com.google.android.calendar',
        client_sig="38918a453d07199354f8b19af05ec6562ced5788")
    if "Auth" not in auth_response:
        if "Token" not in auth_response:
            raise exception.LoginException(auth_response.get("Error"))
    token = auth_response['Auth']


    #print(auth_response)
    #print(token)

    return token




def formatCalendar():
    Calendar = ""

    current_time = datetime.now()
    start_date = (current_time - timedelta(days=7)).isoformat() + 'Z'
    API_URL = "https://www.googleapis.com/calendar/v3/calendars/" + email + "/events"
    params = {
        "calendarId": 'primary',
        "timeMin": start_date,
        "maxResults": 10,
        "singleEvents": True,
    }

    request = send(url=API_URL, method="GET", allow_redirects=False, params=params)
    events_result = request.json()


    events = events_result.get('items', [])

    if not events:
        Calendar += 'No upcoming events found.'
        return

    # Create a table to display events
    month = datetime.now().month
    year = datetime.now().year
    cal = calendar.monthcalendar(year, month)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Print month and weekdays as column names
    '''
    print(calendar.month_name[month], year)
    for day in weekdays:
        Calendar += day + "\t"
    print()
    '''

    weekday = datetime.now().strftime('%a')
    int_weekday = weekdays.index(weekday)
    # print(int_weekday)

    # Determine the range of weeks to display
    current_week_index = -1
    for i, week in enumerate(cal):
        if datetime.now().day in week:
            current_week_index = i
            break

    # Calculate the range of dates for the four weeks
    start_date = datetime.now() - timedelta(days=current_week_index * 7 + int_weekday)
    end_date = start_date + timedelta(days=27)

    # Print dates and corresponding events for the four weeks
    date_range = []
    current_date = start_date.date()
    while current_date <= end_date.date():
        date_range.append(current_date)
        current_date += timedelta(days=1)

    count = 0
    for date in date_range:
        Calendar += str(date.day) + "\t"

        event_found = False
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            event_date = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').date()
            if event_date == date:
                event_time = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M:%S')

                if dict_event.get(date.day) == None:
                    dict_event[date.day] = []
                    dict_event[date.day].append(str(event_time) + " " + event['summary'])
                else:
                    dict_event[date.day].append(str(event_time) + " " + event['summary'])
                # print(event_time, event['summary'], end=" ")
                event_found = True

        # print("", end="\t")

        count += 1
        if count % 7 == 0 and count != 0:
            Calendar += "\n"


    return dict_event, Calendar




dict_event, Calendar = formatCalendar()
print(dict_event[4])
print(Calendar)