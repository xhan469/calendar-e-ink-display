import logging
import re
import time
import random
from datetime import date, datetime, timedelta
import json

from uuid import getnode as get_mac
from gCalendarApi import exception

import gpsoauth
import requests


logger = logging.getLogger(__name__)

try:
    Pattern = re._pattern_type  # pylint: disable=protected-access
except AttributeError:
    Pattern = re.Pattern  # pylint: disable=no-member



class APIAuth(object):
    """Authentication token manager"""

    def __init__(self, scopes):
        self._master_token = None
        self._auth_token = None
        self._email = None
        self._device_id = None
        self._scopes = scopes

    def login(self, email, password, device_id):
        """Authenticate to Google with the provided credentials.

        Args:
            email (str): The account to use.
            password (str): The account password.
            device_id (str): An identifier for this client.

        Raises:
            LoginException: If there was a problem logging in.
        """
        self._email = email
        self._device_id = device_id

        # Obtain a master token.
        res = gpsoauth.perform_master_login(self._email, password, self._device_id)

        # Bail if browser login is required.
        if res.get("Error") == "NeedsBrowser":
            raise exception.BrowserLoginRequiredException(res.get("Url"))

        # Bail if no token was returned.
        if "Token" not in res:
            raise exception.LoginException(res.get("Error"), res.get("ErrorDetail"))

        self._master_token = res["Token"]
        #print(self._master_token)

        # Obtain an OAuth token.
        res = self.refresh()
        #print(res)
        return True

    def getMasterToken(self):
        return self._master_token

    def setMasterToken(self, master_token):
        self._master_token = master_token

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getDeviceId(self):
        return self._device_id

    def setDeviceId(self, device_id):
        self._device_id = device_id

    def getAuthToken(self):
        return self._auth_token

    def setAuthToken(self, auth_token):
        self._auth_token = auth_token

    def refresh(self):
        """Refresh the OAuth token.

        Returns:
            string: The auth token.

        Raises:
            LoginException: If there was a problem refreshing the OAuth token.
        """
        # Obtain an OAuth token with the necessary scopes by pretending to be
        # the keep android client.
        res = gpsoauth.perform_oauth(
            self._email,
            self._master_token,
            self._device_id,
            service=self._scopes,
            app='com.google.android.calendar',
            client_sig="38918a453d07199354f8b19af05ec6562ced5788",
        )
        # Bail if no token was returned.
        if "Auth" not in res:
            if "Token" not in res:
                raise exception.LoginException(res.get("Error"))

        self._auth_token = res["Auth"]
        return self._auth_token

    def logout(self):
        """Log out of the account."""
        self._master_token = None
        self._auth_token = None
        self._email = None
        self._device_id = None



class API(object):
    """Base API wrapper"""

    RETRY_CNT = 2

    def __init__(self, auth=None):
        self._session = requests.Session()
        self._auth = auth

    def getAuth(self):
        return self._auth

    def setAuth(self, auth):
        self._auth = auth

    def send(self, **req_kwargs):
        """Send an authenticated request to a Google API.
        Automatically retries if the access token has expired.

        Args:
            **req_kwargs: Arbitrary keyword arguments to pass to Requests.

        Return:
            dict: The parsed JSON response.

        Raises:
            APIException: If the server returns an error.
            LoginException: If :py:meth:`login` has not been called.
        """
        # Send a request to the API servers, with retry handling. OAuth tokens
        # are valid for several hours (as of this comment).
        i = 0
        while True:
            # Send off the request. If there was no error, we're good.
            response = self._send(**req_kwargs).json()
            if "error" not in response:
                break

            # Otherwise, check if it was a non-401 response code. These aren't
            # handled, so bail.
            error = response["error"]
            if error["code"] != 401:
                raise exception.APIException(error["code"], error)

            # If we've exceeded the retry limit, also bail.
            if i >= self.RETRY_CNT:
                raise exception.APIException(error["code"], error)

            # Otherwise, try requesting a new OAuth token.
            logger.info("Refreshing access token")
            self._auth.refresh()
            i += 1

        return response

    def _send(self, **req_kwargs):
        """Send an authenticated request to a Google API.

        Args:
            **req_kwargs: Arbitrary keyword arguments to pass to Requests.

        Return:
            requests.Response: The raw response.

        Raises:
            LoginException: If :py:meth:`login` has not been called.
        """
        # Bail if we don't have an OAuth token.
        auth_token = self._auth.getAuthToken()
        if auth_token is None:
            raise exception.LoginException("Not logged in")

        # Add the token to the request.
        req_kwargs.setdefault("headers", {"Authorization": "OAuth " + auth_token})

        return self._session.request(**req_kwargs)


    def get(self):
        email = self._auth.getEmail()

        current_time = datetime.now()
        start = (current_time - timedelta(days=current_time.weekday() + 7)).isoformat() + "+12:00"
        end = (current_time - timedelta(days=current_time.weekday() - 21)).isoformat() + "+12:00"

        #print("start time: " + start)
        #print("end time: " + end)


        #start_date = (current_time - timedelta(days=7)).isoformat() + 'Z'
        API_URL = "https://www.googleapis.com/calendar/v3/calendars/" + email + "/events"

        params = {
            "calendarId": 'primary',
            "timeMin": start,
            "timeMax": end,
            #"maxResults": 10,
            "singleEvents": True,
        }

        request = self.send(url=API_URL, method="GET", allow_redirects=False, params=params)
        #events_result = request.json()
        events = request.get('items', [])
        output_dict = {}
        for event in events:
            #print(event)
            start = event['start'].get('dateTime', event['start'].get('date'))
            #print(start)

            event_dates = start.split('T')[0][5:]
            #print(event_dates)
            # output_dict[int(date_key)] = event['summary']
            #event_date = str(datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').date())[-2:]
            event_time = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M:%S')

            #key = int(event_date)

            # print(event['summary'])

            if output_dict.get(event_dates) == None:
                output_dict[event_dates] = []
                if 'summary' not in event.keys():
                    output_dict[event_dates].append(str(event_time)[:5] + " (No Title)")
                else:
                    #output_dict[event_dates].append(str(event_time)[:5] + " " + json.dumps(event))
                    output_dict[event_dates].append(str(event_time)[:5] + " " + event['summary'])
            else:
                if 'summary' not in event.keys():
                    output_dict[event_dates].append(str(event_time)[:5] + " (No Title)")
                else:
                    #output_dict[event_dates].append(str(event_time)[:5] + " " + json.dumps(event))
                    output_dict[event_dates].append(str(event_time)[:5] + " " + event['summary'])

        return output_dict

    def get_all(self):
        email = self._auth.getEmail()

        current_time = datetime.now()
        start = (current_time - timedelta(days=current_time.weekday() + 8)).isoformat() + "+12:00"
        end = (current_time - timedelta(days=current_time.weekday() - 21)).isoformat() + "+12:00"

        print("start time: " + start)
        print("end time: " + end)


        #start_date = (current_time - timedelta(days=7)).isoformat() + 'Z'
        API_URL = "https://www.googleapis.com/calendar/v3/calendars/" + email + "/events"

        params = {
            "calendarId": 'primary',
            "timeMin": start,
            "timeMax": end,
            #"maxResults": 10,
            "singleEvents": True,
        }

        request = self.send(url=API_URL, method="GET", allow_redirects=False, params=params)
        #events_result = request.json()
        events = request.get('items', [])
        output_dict = {}
        for event in events:
            #print(event)

            start = event['start'].get('dateTime', event['start'].get('date'))


            event_dates = start.split('T')[0][5:]

            if output_dict.get(event_dates) == None:
                output_dict[event_dates] = []
                output_dict[event_dates].append(event)

            else:
                output_dict[event_dates].append(event)


        return output_dict




class Calendar(object):
    OAUTH_SCOPES = "oauth2:https://www.googleapis.com/auth/calendar"

    def __init__(self):
        self._auth = None
        self._calendar_api = API(self._auth)

    def login(
        self,
        email,
        password,
        device_id=None,
    ):
        """Authenticate to Google with the provided credentials & sync.

        Args:
            email (str): The account to use.
            password (str): The account password.
            device_id (str): Override for device ID

        Raises:
            LoginException: If there was a problem logging in.
        """
        auth = APIAuth(self.OAUTH_SCOPES)
        if device_id is None:
            device_id = get_mac()

        ret = auth.login(email, password, device_id)
        self._auth = auth
        return ret, auth

    def get(self):
        self._calendar_api.setAuth(self._auth)
        result = self._calendar_api.get()

        return result

    def get_all(self):
        self._calendar_api.setAuth(self._auth)
        result = self._calendar_api.get_all()
        return result





