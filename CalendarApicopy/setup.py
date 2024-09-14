from gCalendarApi import Calendar
import gkeepapi
from datetime import datetime, timedelta
import socket
import led
import neopixel
import board
import os




script_dir = os.path.dirname(os.path.abspath(__file__))

email = []
password = []
mode = ''
brightness = 0

mode_file_path = os.path.join(script_dir, "setting/mode.txt")
try:
    with open(mode_file_path, "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            mode = lines[0]
except FileNotFoundError:
    print("mode.txt not found")


password_file_path = os.path.join(script_dir, "setting/password.txt")
print(password_file_path)

try:
    with open(password_file_path, "r") as f:
        lines = f.readlines()

        for i in range(0, len(lines), 2):
            email.append(lines[i].strip())  # First line is the account, remove any trailing newline or spaces
            password.append(lines[i+1].strip())  # Second line is the password, remove any trailing newline or spaces
            print(email)
            print(password)
except:
    print("The file password.txt does not exist.")
    print(password_file_path)


brightness_file_path = os.path.join(script_dir, "setting/brightness.txt")
try:
    with open(brightness_file_path, "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            brightness = float(lines[0])
except FileNotFoundError:
    print("brightness.txt not found")





class LedSetting:
    def __init__(self):
        self.__led_on_time = None
        self.__led_off_time = None
        self.__led_blink_time = None
        self.__has_blinked = False
        self.__color_code = None

    def reset(self):
        self.__led_on_time = None
        self.__led_off_time = None
        self.__led_blink_time = None
        self.__has_blinked = False
        self.__color_code = None

    def set_led_time(self, on, off):
        self.__led_on_time = on
        self.__led_off_time = off

    def has_blinked(self):
        return self.__has_blinked

    def set_led_blink(self, blink):
        self.__led_blink_time = blink

    def blink(self):
        num_leds = 55
        pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=brightness)
        now = datetime.now().time()

        if (self.__has_blinked == False):

            if ((now.hour, now.minute) > (self.__led_blink_time.hour, self.__led_blink_time.minute) and (now.hour, now.minute) < (self.__led_off_time.hour, self.__led_off_time.minute)):
                led.blink_leds(pixels, self.__color_code)
                #print("blink_color", self.__color_code)
                #print("blinked")
                self.__has_blinked = True


    def get_next_entry(self, entries):
        now = datetime.now().time()
        two_hours_later = (datetime.combine(datetime.today(), now) + timedelta(minutes=120)).time()

        # Filter out past entries and entries more than 2 hours ahead
        valid_entries = [entry for entry in entries if now < entry[0] <= two_hours_later]

        # Sort the valid entries by time and return the first one
        return sorted(valid_entries, key=lambda x: x[0])[0] if valid_entries else None


    def is_blink_event(self):
        if self.__led_on_time == None:
            return False
        else:
            return True


    def turn_led_on(self, time_and_colorCode):
        print(time_and_colorCode)
        events = get_next_entry(time_and_colorCode)
        num_leds = 55
        pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=brightness)

        if events != None:
            check_time, r, g, b = events
            color_code = (r, g, b)

            event_datetime = datetime.combine(datetime.today(), check_time)
            led_on_datetime = event_datetime - timedelta(minutes=120)
            blink_datetime = event_datetime - timedelta(minutes=10)
            led_on_time = led_on_datetime.time()
            led_blink_time = blink_datetime.time()

            led_off_datetime = event_datetime
            led_off_time = led_off_datetime.time()

            print("led blink", led_blink_time)
            print("led on", led_on_time)
            print("led off", led_off_time)
            print("color code", color_code)

            now = datetime.now().time()

            self.__led_on_time = led_on_time
            self.__led_off_time = led_off_time
            self.__led_blink_time = led_blink_time
            self.__color_code = color_code

            if ((now.hour, now.minute) > (led_on_time.hour, led_on_time.minute)) and (
                    (now.hour, now.minute) < (led_off_time.hour, led_off_time.minute)):
                led.turn_on_leds(pixels, color_code)
                print("on")
            elif ((now.hour, now.minute) >= (led_off_time.hour, led_off_time.minute)):
                led.turn_off_leds(pixels)
                print("off")

        else:
            led.turn_off_leds(pixels)
            print("off")



def check_today(date):
    today = datetime.today()
    today = str(today).split()[0]
    today = today[-5:]

    if today == date:
        return True
    return False

def convert_to_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

def set_led_blink_time(dict_event_with_time, nested_event):
    output = []
    for date in dict_event_with_time:
        events = dict_event_with_time[date]
        now = datetime.now().time()
        #print(now_temp)

        for event in events:
            #color_id = get_color_id(event)
            #print(color_id)
            #print(event[0])

            if 'T' in event[1]:
                time_string = event[1].split('T')[1][:5]
                event_time = convert_to_time(time_string)
                #print(date)
                if check_today(date):
                    id = event[0]
                    summary, colorId = find_event_summary_by_id(id, nested_event)
                    #print(summary, colorId)

                    red, green, blue = led_color_code(colorId)

                    #print(event_time)
                    event_datetime = datetime.combine(datetime.today(), event_time)
                    blink_datetime = event_datetime
                    #blink_datetime = event_datetime - timedelta(minutes=10)
                    blink_time = blink_datetime.time()
                    #print(blink_time)
                    #print(type(now))
                    output.append((blink_time, red, green, blue))
    return output


def get_next_entry(entries):
    now = datetime.now().time()
    two_hours_later = (datetime.combine(datetime.today(), now) + timedelta(minutes=120)).time()

    # Filter out past entries and entries more than 2 hours ahead
    valid_entries = [entry for entry in entries if now < entry[0] <= two_hours_later]

    # Sort the valid entries by time and return the first one
    return sorted(valid_entries, key=lambda x: x[0])[0] if valid_entries else None




def turn_led_on(time_and_colorCode):
    print(time_and_colorCode)
    events = get_next_entry(time_and_colorCode)
    num_leds = 55
    pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=brightness)

    if events != None:
        check_time, r, g, b = events
        color_code = (r, g, b)

        event_datetime = datetime.combine(datetime.today(), check_time)
        led_on_datetime = event_datetime - timedelta(minutes=120)
        led_on_time = led_on_datetime.time()

        led_off_datetime = event_datetime
        led_off_time = led_off_datetime.time()

        print("led on", led_on_time)
        print("led off", led_off_time)
        now = datetime.now().time()

        if ((now.hour, now.minute) > (led_on_time.hour, led_on_time.minute)) and ((now.hour, now.minute) < (led_off_time.hour, led_off_time.minute)):
            led.turn_on_leds(pixels, color_code)
            print("on")
        elif ((now.hour, now.minute) >= (led_off_time.hour, led_off_time.minute)):
            led.turn_off_leds(pixels)
            print("off")
    else:
        led.turn_off_leds(pixels)
        print("off")





def set_led_blink(time_and_colorCode):
    num_leds = 55
    pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=brightness)
    for event in time_and_colorCode:
        #print(event)
        check_time, r, g, b = event
        color_code = (r, g, b)

        event_datetime = datetime.combine(datetime.today(), check_time)
        led_blink_datetime = event_datetime - timedelta(minutes=10)
        led_blink_time = led_blink_datetime.time()

        print("blink time", led_blink_time)

        #time_string = "14:51:45"
        # Convert the time string to a datetime.time object
        #parsed_time = datetime.strptime(time_string, "%H:%M:%S").time()

        now = datetime.now().time()

        if ((now.hour, now.minute) == (check_time.hour, check_time.minute)):
            led.blink_leds(pixels, color_code)
            print("blink", color_code)




def led_color_code(id):
    if id == "":
        return 255, 255, 255  #white
    if id == "5" or id == "6":
        return 255, 128, 0 #orange
    if id == "11" or id == "4":
        return 255, 0, 0    #red
    if id == "2" or id == "10":
        return 0, 255, 0 #green
    if id == "9":
        return 0, 0, 255
    return 255, 255, 255


def check_time(dict_event_with_time):
    output = {}
    for date in dict_event_with_time:
        events = dict_event_with_time[date]
        now = datetime.now().time()
        #print(now_temp)

        for event in events:
            #print(event)
            if 'T' in event[1]:
                time_string = event[1].split('T')[1][:5]
                event_time = convert_to_time(time_string)
                #print(date)
                if check_today(date):
                    if event_time > now:
                    #print(time_string)

                        if output.get(date) == None:
                            output[date] = []
                            output[date].append(event[0])
                        else:
                            output[date].append(event[0])
                            output[date] = (output[date])[:4]

            else:
                #print(date)
                if check_today(date):
                    if output.get(date) == None:
                        output[date] = []
                        output[date].append(event[0])
                    else:
                        output[date].insert(0, event[0])
                        output[date] = (output[date])[:4]

        if date in output:
            while len(output[date]) < 4:
                output[date].append("")


    return output





def max_four_event(dict_event):
    output = {}
    for key in dict_event.keys():
        events = dict_event[key]

        output[key] = (events)[:4]
        while len(output[key]) < 4:
            output[key].append("")
    return output




def login(email, password):
    gkeepapi.node.DEBUG = True
    keep = gkeepapi.Keep()
    keep.login(email, password)   #'something@googlemail.com', '<your generated app password from google>'

    return keep

def get_note(keep):
    gnotes = keep.all()
    gnotes = gnotes[:3]

    result= ""
    for i in gnotes:
        result +=(str(i)) + "\n"
    return gnotes

def refresh(email, password):
    nested_events = {}
    result = []

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

        #events_summary = get_event_summary(events)

        keep = login(email[i], password[i])
        single_account_result = get_note(keep)

        for note in single_account_result:
            result.append(note)
        #print(result)
        print(nested_events)


    return nested_events, result[:3]



def show_today_date():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%B %d")
    #print("Today's date:", formatted_date)
    return formatted_date

def get_month_and_year():
    current_date = datetime.now()
    formatted_month = current_date.strftime("%B")
    formatted_year = current_date.strftime("%Y")
    return formatted_month, formatted_year

#print(events.keys())
#print(events['07-04'])




def get_event_summary(nested_dict):
    output = {}
    for date in nested_dict:
        for event in (nested_dict[date]):
            if output.get(date) == None:
                output[date] = []
                if event.get("summary") != None:
                    output[date].append(event['summary'])
                else:
                    output[date].append('(No Title)')
            else:
                if event.get("summary") != None:
                    output[date].append(event['summary'])
                else:
                    output[date].append('(No Title)')
    return output

def get_event_id(event_dict):
    output = {}
    for date in event_dict:
        output[date] = [item[0] for item in event_dict[date]]
        #print(output[date])

    return output


def sort_event(nested_dict):
    output = {}
    for date in nested_dict:
        for event in (nested_dict[date]):
            if output.get(date) == None:
                output[date] = []
                if "dateTime" in event['start']:
                    output[date].append((event['id'], event['start']['dateTime']))
                else:
                    output[date].append((event['id'], event['start']['date']))
            else:
                if "dateTime" in event['start']:
                    output[date].append((event['id'], event['start']['dateTime']))
                else:
                    output[date].append((event['id'], event['start']['date']))
        output[date] = sorted(output[date], key=lambda x: x[1])
        #print(output[date])
        #output[date] = [item[0] for item in output[date]]
        # print(output[date])

    return output


def find_event_summary_by_id(id, nested_dict):
    summary = ""
    colorId = ""
    for date in nested_dict:
        for event in nested_dict[date]:
            if id == event['id']:
                date_format = '%Y-%m-%d'
                date_format2 = '%Y-%m-%dT%H:%M:%S%z'
                event_time = ""


                start = event['start'].get('dateTime', event['start'].get('date'))

                try:
                    # Parse the date string using the specified format
                    event_time = (datetime.strptime(start, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M:%S'))[:6]
                except ValueError as e:
                    pass
                try:
                    event_time = str(datetime.strptime(start, date_format))[5:10]
                except ValueError as e:
                    pass

                if 'summary' in event.keys():
                    #print(event['summary'])
                    summary = str(event_time) + " " + event['summary']
                else:
                    summary = str(event_time) + " (No Title)"
                if 'colorId' in event.keys():
                    #print(event['colorId'])
                    colorId = event['colorId']
    return summary, colorId



def get_color_id(event):
    if event.get("colorId") != None:
        return event["colorId"]
    else:
        return None

def color_id_to_color(id):
    #print(id)
    if id == "" and mode == 'light':
        return None, "black"
    if id == "":
        return None, "white"


    if id == "5" or id == "6":
        return "#ff8000", "white" #orange
    if id == "11" or id == "4":
        return "red", "white"
    if id == "2" or id == "10":
        return "#00ff00", "black" #green
    if id == "9":
        return "blue", "white"
    return None, "white"



def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a remote server (Google's public DNS server)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address of the machine
        local_ip = s.getsockname()[0]

        # Close the socket
        s.close()

        return local_ip
    except socket.error:
        return None





