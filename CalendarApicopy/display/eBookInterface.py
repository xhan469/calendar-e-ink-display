import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont
import setup
import CalendarDates
import os
from setup import LedSetting



def generate_calendar():
    mode = ''
    my_led = LedSetting()




    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)

    print(parent_dir)

    mode_file_path = os.path.join(parent_dir, "setting/mode.txt")
    with open(mode_file_path, "r") as f:
        lines = f.readlines()
        if len(lines) == 1:
            mode = lines[0]

    print("detected mode", mode)


    nested_events, result = setup.refresh(setup.email, setup.password)
    events_with_time = setup.sort_event(nested_events)
    events = setup.get_event_id(events_with_time)
    print(nested_events)
    #print(events)

    dict_event = setup.max_four_event(events)
    today_event = setup.check_time(events_with_time)

    led_blink_info = setup.set_led_blink_time(events_with_time, nested_events)
    #print(led_blink)

    setup.set_led_blink(led_blink_info)
    next_event = setup.get_next_entry(led_blink_info)

    #print(next_event)




    #today_event = setup.max_four_event(events)
    keep_result = result

    event_len = 0

    days = CalendarDates.get_days()

    im = Image.new('RGB', (800, 480), '#000000')
    if mode == 'light':
        im = Image.new('RGB', (800, 480), '#ffffff')


    #im = Image.open("bg.png")

    # Draw line
    draw = ImageDraw.Draw(im)
    #im.show()

    month, year = setup.get_month_and_year()

    font_month = ImageFont.truetype(script_dir + "/Arial_Bold.ttf", 20)
    font_year = ImageFont.truetype(script_dir + "/Arial_Bold.ttf", 16)

    draw.text((5, 5), month, fill='white', font=font_month)
    draw.text((740, 10), year, fill='white', font=font_year)
    if mode == 'light':
        draw.text((5, 5), month, fill='black', font=font_month)
        draw.text((740, 10), year, fill='black', font=font_year)



    margin = 30
    weekdays_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    color_list = [None, None, None, None, None, "red", "red"]
    fill_list = ["white", "white", "white", "white", "white", "white", "white"]

    if mode == 'light':
        weekdays_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        color_list = [None, None, None, None, None, "red", "red"]
        fill_list = ["black", "black", "black", "black", "black", "white", "white"]

    # Define the coordinates of the rectangle's top-left and bottom-right corners
    x0, y0 = 5, 5 + margin
    x1, y1 = 115, 75 + margin



    # Define the border color and width
    border_color = 'white'

    if mode == 'light':
        border_color = 'black'
    border_width = 1
    font = ImageFont.truetype(script_dir + "/Arial.ttf", 13)
    weekdays_font =ImageFont.truetype(script_dir + "/Arial_Bold.ttf", 16)
    small_font = ImageFont.truetype(script_dir + "/Arial.ttf", 10)


    row0_y0, row0_y1 = 5 + margin, 35 + margin
    for column in range(7):

        draw.rectangle(((x0, row0_y0), (x1, row0_y1)), outline='white', width=border_width, fill=color_list[column])
        if mode == 'light':
            draw.rectangle(((x0, row0_y0), (x1, row0_y1)), outline='black', width=border_width, fill=color_list[column])
        draw.text((x0 + 2, row0_y0 + 1), weekdays_list[column], fill=fill_list[column], font=weekdays_font)
        x0 = x0 + 110
        x1 = x1 + 110

    y0, y1 = 35 + margin, 105 + margin

    # Draw the rectangle with border
    count = 0
    for row in range(4):
        x0, x1 = 5, 115
        for column in range(7):
            if setup.check_today(days[count]):
                is_today = 'YELLOW'

                if today_event.get(days[count]) != None:
                    event_len = len(today_event[days[count]])
            else:
                is_today = 'black'
                if dict_event.get(days[count]) != None:
                    event_len = len(dict_event[days[count]])
            day = str(days[count])[-2:]


            draw.rounded_rectangle(((x0, y0), (x1, y1)), outline=border_color,width=border_width, fill='black')

            if mode == 'light':
                draw.rounded_rectangle(((x0, y0), (x1, y1)), outline=border_color, width=border_width, fill='white')

            if setup.check_today(days[count]):
                draw.rounded_rectangle(((x0 + 1, y0 + 1), (x1 - 1, y0 + 15)), fill='yellow')
                draw.text((x0 + 2, y0 + 1), text=day, font=font, fill='black')
            else:
                draw.text((x0 + 2, y0 + 1), text=day, font=font, fill='white')
                if mode == 'light':
                    draw.text((x0 + 2, y0 + 1), text=day, font=font, fill='black')

            msg = ["", "", "", ""]
            colorId_list = ['BLACK', 'BLACK', 'BLACK', 'BLACK']



            foregd_list = ['BLACK', 'BLACK', 'BLACK', 'BLACK']



            if dict_event.get(days[count]) != None:
                if setup.check_today(days[count]):
                    if today_event.get(days[count]) != None:
                        msg = today_event[days[count]]
                else:
                    msg = dict_event[days[count]]
                #msg = "\n".join(line[:20] for line in msg)



                summary_list = []
                temp = 0
                for id in msg:
                    summary, colorId = setup.find_event_summary_by_id(id, nested_events)
                    #print(id)
                    summary_list.append(summary)
                    color, forecolor = setup.color_id_to_color(colorId)
                    colorId_list[temp] = color
                    foregd_list[temp] = forecolor
                    temp += 1
                #msg = "\n".join(summary_list)
                #print(msg)
                #msg = "\n".join(line[:22] for line in summary_list)


                draw.rounded_rectangle(((x0+2, y0+15), (x1-3, y0+28)), fill = colorId_list[0], outline='black')
                draw.rounded_rectangle(((x0 + 2, y0 + 28), (x1 - 3, y0+41)), fill=colorId_list[1], outline='black')
                draw.rounded_rectangle(((x0 + 2, y0 + 41), (x1 - 3, y0 + 55)), fill=colorId_list[2], outline='black')
                draw.rounded_rectangle(((x0 + 2, y0 + 55), (x1 - 3, y0 + 68)), fill=colorId_list[3], outline='black')

                if mode == 'light':
                    draw.rounded_rectangle(((x0 + 2, y0 + 15), (x1 - 3, y0 + 28)), fill=colorId_list[0],
                                           outline='white')
                    draw.rounded_rectangle(((x0 + 2, y0 + 28), (x1 - 3, y0 + 41)), fill=colorId_list[1],
                                           outline='white')
                    draw.rounded_rectangle(((x0 + 2, y0 + 41), (x1 - 3, y0 + 55)), fill=colorId_list[2],
                                           outline='white')
                    draw.rounded_rectangle(((x0 + 2, y0 + 55), (x1 - 3, y0 + 68)), fill=colorId_list[3],
                                           outline='white')



                draw.text((x0 + 2, y0 + 16), text=summary_list[0], font=small_font, fill=foregd_list[0])
                draw.text((x0 + 2, y0 + 29), text=summary_list[1], font=small_font, fill=foregd_list[1])
                draw.text((x0 + 2, y0 + 42), text=summary_list[2], font=small_font, fill=foregd_list[2])
                draw.text((x0 + 2, y0 + 56), text=summary_list[3], font=small_font, fill=foregd_list[3])


                summary_list = ["", "", "", ""]
                #foregd_list = ['white', 'white', 'white', 'white']
                foregd_list = ['BLACK', 'BLACK', 'BLACK', 'BLACK']


            #draw.text((x0 + 2, y0 + 16), text=msg, font=small_font, fill='BLACK')


            x0 = x0 + 110
            x1 = x1 + 110
            draw.rounded_rectangle(((x0 + 1, y0), (x1, y1)), width=border_width, fill='black')
            if mode == 'light':
                draw.rounded_rectangle(((x0 + 1, y0), (x1, y1)), width=border_width, fill='white')

            count += 1


        y0 = y0 + 70
        y1 = y1 + 70
    # Save or display the image
    # im.save('rectangle_with_border.png')

    max_width = 230

    x0, x1 = 5, 115
    for i in range(len(keep_result)):

        msg = "Notes" + str(i + 1) + ": " + (str(keep_result[i])[:150]).strip()

        # Implement the text wrapping logic using textwrap
        wrapped_msg = "\n".join(textwrap.wrap(msg, width=40))

        # Draw the wrapped text on the image
        x, y = x0 + 2, y0 + 1
        for line in wrapped_msg.split('\n'):
            draw.text((x, y), line, font=font, fill="white")

            if mode == "light":
                draw.text((x, y), line, font=font, fill="black")
            y += 12  # Move to the next line

        x0 = x0 + 260
        x1 = x1 + 260

    #im.show()
    draw.text((700, 460), text=setup.get_local_ip(), font=small_font, fill='white')

    im.save('calendar.png')

    #print(nested_events)
    return nested_events, today_event, keep_result, led_blink_info


generate_calendar()




