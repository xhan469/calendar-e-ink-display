import calendar
import datetime

def get_days():
    # Create an empty list to store all the days
    all_days = []

    # Get the current date
    current_date = datetime.datetime.now()

    # Find the previous week's Monday
    calendar.setfirstweekday(calendar.MONDAY)  # Set Monday as the first day of the week
    start = current_date - datetime.timedelta(days=current_date.weekday() + 7)  # Subtract days to get to the start of the previous week

    calendar_days = [start + datetime.timedelta(days=i) for i in range(28)]

    for date in calendar_days:

        event_dates = str(date).split()[0][5:]
        #print(event_dates)
        all_days.append(event_dates)

    return all_days


'''
    # Find the current week's Monday
    current_week_start = current_date - datetime.timedelta(days=current_date.weekday())  # Subtract days to get to the start of the current week

    # Find the dates for the previous week
    previous_week_dates = [previous_week_start + datetime.timedelta(days=i) for i in range(7)]

    # Find the dates for the current week
    current_week_dates = [current_week_start + datetime.timedelta(days=i) for i in range(7)]

    # Find the dates for the next two weeks
    next_two_weeks_start = current_date + datetime.timedelta(days=7)  # Add 7 days to get to the start of the next week
    next_two_weeks_dates = [next_two_weeks_start + datetime.timedelta(weeks=i) + datetime.timedelta(days=j) for i in range(2) for j in range(7)]

    # Create an empty list to store all the days
    all_days = []

    # Add the dates for the previous week to the list
    for date in previous_week_dates:
        all_days.append(date.strftime("%-d"))

    # Add the dates for the current week to the list
    for date in current_week_dates:
        all_days.append(date.strftime("%-d"))

    # Add the dates for the next two weeks to the list
    for date in next_two_weeks_dates:
        all_days.append(date.strftime("%-d"))

    # Print the list of all days
    return all_days
    '''

#print(get_days())