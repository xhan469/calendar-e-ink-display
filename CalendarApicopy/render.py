from apscheduler.schedulers.blocking import BlockingScheduler
from display import display
from display import eBookInterface
import CalendarDates
import os
from setup import LedSetting
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def are_lists_not_equal(list1, list2):
    if len(list1) != len(list2):
        return True

    for i in range(len(list1)):
        if str(list1[i]) != str(list2[i]):
            return True
    return False


def are_nested_dict_not_same(dict1, dict2):
    for key in dict1:
        # Check if the key exists in both dictionaries
        if key not in dict2:
            return True

        # Check if the lists of dictionaries are not the same
        if len(dict1[key]) != len(dict2[key]):
            return True

        # Compare each dictionary in the lists
        for d1, d2 in zip(dict1[key], dict2[key]):
            # Check if the dictionaries are not the same
            if d1 != d2:
                return True

    return False


def are_dicts_not_same(dict1, dict2):
    # Check if the length of both dictionaries is different
    if len(dict1) != len(dict2):
        return True

    # Compare the key-value pairs in both dictionaries
    for key in dict1:
        if key not in dict2 or dict1[key] != dict2[key]:
            return True
    return False


old_dict_event, old_today_event, old_keep_result, old_led_blink_info = eBookInterface.generate_calendar()


my_led = LedSetting()
my_led.turn_led_on(old_led_blink_info)
if (my_led.is_blink_event()):
    my_led.blink()

show = display.Display()
show.run()


old_days = CalendarDates.get_days()


def rewake():
    global old_dict_event, old_today_event, old_keep_result, old_days, old_led_blink_info, my_led

    days = CalendarDates.get_days()
    dict_event, today_event, keep_result, led_blink_info= eBookInterface.generate_calendar()
    #print(old_dict_event)
    #print(dict_event)

    print("\n")
    #print(my_led.has_blinked())
    my_led.turn_led_on(led_blink_info)
    if (my_led.is_blink_event()):
        my_led.blink()
        #print(my_led.has_blinked())

    '''
    if dict_event != old_dict_event or today_event != old_today_event\
            or keep_result != old_keep_result or days != old_days:

        show.run()'''


    if are_lists_not_equal(old_days, days) or are_lists_not_equal(old_keep_result, keep_result)\
        or are_nested_dict_not_same(old_dict_event, dict_event)\
            or are_dicts_not_same(old_today_event, today_event):
        show.run()

    if are_lists_not_equal(old_led_blink_info, led_blink_info):
        my_led.reset()
        print("reset")


    # Update the old values with the new ones for the next iteration
    old_dict_event = dict_event
    old_today_event = today_event
    old_keep_result = keep_result
    old_days = days
    old_led_blink_info = led_blink_info

scheduler = BlockingScheduler()
scheduler.add_job(rewake, 'interval', seconds=15) #adjust rewake time
scheduler.start()
