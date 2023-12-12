# gCalendar to E-ink

This project would show events from the google calendar in four weeks, starting from the first row as previous week events. It shows a maximum of 4 events per day order by start time, but current day would show the upcoming events.
Maximum of three notes is displayed under the calendar. (These notes come from google keep api and should be plain text)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install -r requirements.txt
```

## Usage
generate your application password for the google account

further information please look at https://support.google.com/accounts/answer/185833?hl=en

Once you got your application password, open setup.py input your email and password

```bash
email = 'something@googlemail.com'
password = '<your generated app password from google>'
```

run render.py then you're all set
```bash
python3 render.py
```



----------
optional but recommended: The calendar will only refresh when updating event or notes, however to customise the refreshing time please check in render.py
```bash
scheduler.add_job(rewake, 'interval', seconds=15) #adjust rewake time
```

Note: when delete a note, you'd need to empty the bin to get rid of it.

