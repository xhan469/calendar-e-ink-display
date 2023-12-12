import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont
import setup
import CalendarDates

import sys
import os

from waveshare_epd import epd7in3f
import logging
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)


def generate_calendar():
    epd = epd7in3f.EPD()
    epd.init()

    epd.Clear()

    dict_event = setup.max_four_event(setup.events)
    today_event = setup.check_time(setup.events)
    keep_result = setup.result

    event_len = 0

    days = CalendarDates.get_days()

    im = Image.new('RGB', (epd.width, epd.height), epd.WHITE)

    draw = ImageDraw.Draw(im)
    weekdays_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    # Define the coordinates of the rectangle's top-left and bottom-right corners
    x0, y0 = 5, 5
    x1, y1 = 115, 75

    # Define the border color and width
    border_color = epd.BLACK
    border_width = 1
    font = ImageFont.truetype("Arial.ttf", 13)
    small_font = ImageFont.truetype("Arial.ttf", 10)


    row0_y0, row0_y1 = 5, 35
    for column in range(7):
        draw.text((x0+ 2, row0_y0 + 1), weekdays_list[column], fill=epd.BLACK, font = font)
        draw.rectangle(((x0, row0_y0), (x1, row0_y1)), outline=border_color, width=border_width)
        x0 = x0 + 110
        x1 = x1 + 110

    y0, y1 = 35, 105

    # Draw the rectangle with border
    count = 0
    for row in range(4):
        x0, x1 = 5, 115
        for column in range(7):
            if setup.check_today(days[count]):
                is_today = epd.YELLOW

                if today_event.get(days[count]) != None:
                    event_len = len(today_event[days[count]])
            else:
                is_today = None
                if dict_event.get(days[count]) != None:
                    event_len = len(dict_event[days[count]])
            day = str(days[count])[-2:]


            draw.rectangle(((x0, y0), (x1, y1)), outline=border_color,width=border_width, fill=is_today)
            draw.text((x0 + 2, y0 + 1), text=day, font=font, fill=epd.BLACK)

            msg = ""
            #print(setup.check_today('07-22'))
            #print(today_event.get('07-22'))
            if dict_event.get(days[count]) != None:
                if setup.check_today(days[count]):
                    if today_event.get(days[count]) != None:
                        msg = today_event[days[count]]
                else:
                    msg = dict_event[days[count]]
                msg = "\n".join(msg)
            draw.text((x0 + 2, y0 + 16), text=msg, font=small_font, fill=epd.BLACK)


            x0 = x0 + 110
            x1 = x1 + 110

            count += 1


        y0 = y0 + 70
        y1 = y1 + 70
    # Save or display the image
    # im.save('rectangle_with_border.png')

    max_width = 230

    x0, x1 = 5, 115
    for i in range(3):
        msg = "Notes" + str(i + 1) + ": " + (str(keep_result[i])[:150]).strip()

        # Implement the text wrapping logic using textwrap
        wrapped_msg = "\n".join(textwrap.wrap(msg, width=40))

        # Draw the wrapped text on the image
        x, y = x0 + 2, y0 + 1
        for line in wrapped_msg.split('\n'):
            draw.text((x, y), line, font=font, fill=epd.BLACK)
            y += 12  # Move to the next line

        x0 = x0 + 260
        x1 = x1 + 260

    #im.show()
    epd.display(epd.getbuffer(im))
    #im.save('calendar.png')

generate_calendar()

'''
show = display.Display()
#show.init()
show.run()
'''
