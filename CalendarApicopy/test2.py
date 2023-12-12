from gCalendarApi import Calendar
import gkeepapi
from datetime import datetime, timedelta
import socket
import os

email = ['hanxiaoyu0628@googlemail.com', '1527846269@qq.com']
password = ['lxjldcndhfogsrml', 'vxghgxadilojawvr']

'''
email = ['hanxiaoyu0628@googlemail.com']
password = ['lxjldcndhfogsrml']'''

nested_events = {}
for i in range(len(email)):
    calendar = Calendar()
    calendar.login(email[i], password[i])
    single_account_events = calendar.get_all()

    #nested_events.update(single_account_events)

    for key in single_account_events:
        if key in nested_events:
            for event in single_account_events[key]:
                nested_events[key].append(event)
        else:
            for event in single_account_events[key]:
                nested_events[key] = single_account_events[key]


print(nested_events)

# events_summary = get_event_summary(events)



