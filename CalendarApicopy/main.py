from tkinter import *
import setup
import CalendarDates
from tkinter.font import Font
from PIL import ImageGrab
from datetime import datetime

#dict_event = setup.check_time(setup.events)
dict_event = setup.max_four_event(setup.events)
today_event = setup.check_time(setup.events)
keep_result = setup.result
event_len = 0

days = CalendarDates.get_days()

week_font = ('Arial Rounded MT Bold', 12, "bold")


window = Tk()
window.title("Calendar")
window.geometry("800x480")
window.overrideredirect(True)

#window.wm_attributes('-transparentcolor', window['bg'])

weekdays_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
#window.geometry('{}x{}'.format(300, 300))

#Fonts
title_font = Font(family='Helvetica', size=14, weight='bold')
big_font = Font(family='Helvetica', size=14)
small_font = Font(family='Helvetica', size=12)

container_frame3= Frame(window, highlightbackground="gray80", highlightcolor="gray80", highlightthickness=1,bd=0)
container_frame3.grid(row=0,sticky="nsew")

container_note= Frame(window, highlightbackground="gray80", highlightcolor="gray80", highlightthickness=0,bd=0)
container_note.grid(row=1,sticky="nsew")


is_today = None

count = 0
for row in range(5):
    for col in range(7):
        if setup.check_today(days[count]):
            is_today = 'yellow'

            if today_event.get(days[count]) != None:
                event_len = len(today_event[days[count]])
        else:
            is_today = None
            if dict_event.get(days[count]) != None:
                event_len = len(dict_event[days[count]])

        if row == 0:
            weeklabel = Label(container_frame3, text=weekdays_list[col], font=title_font,width=13,justify=CENTER)
            weeklabel.grid(row=row, column=col)
        else:
            bglabel = Label(container_frame3, text="", width=13, height=5, font=big_font,
                              bg=is_today, anchor='n',borderwidth=1, relief="solid")
            bglabel.grid(sticky="nsew", row=row, column=col)



            day = str(days[count])[-2:]
            datalabel= Label(container_frame3, text="{}".format(day),font=big_font, bg=is_today, anchor='n')
            datalabel.grid(sticky="n",row=row, column=col, padx=5, pady=2)



            if dict_event.get(days[count]) == None:
                eventlabel = Label(container_frame3, text='', font=small_font, bg=is_today)
                eventlabel.grid(row=row, column=col)
            else:
                if setup.check_today(days[count]):
                    msg = today_event[days[count]]
                else:
                    msg = dict_event[days[count]]
                msg = "\n".join(msg)

                if event_len == 4:
                    eventlabel= Label(container_frame3, text=msg, font=small_font, bg=is_today, width=12, height=5,justify="left", anchor="sw")
                    eventlabel.grid(sticky="s", row=row, column=col, padx=5, pady=2)
                else:
                    eventlabel = Label(container_frame3, text=msg, font=small_font, bg=is_today, width=12, height=5,
                                       justify="left", anchor="w")
                    eventlabel.grid(row=row, column=col, padx=5, pady=2)

            eventlabel.lower(datalabel)


            count += 1
'''
note_label = Label(window, text="Notes: " + keep_result, wraplength=700, justify=LEFT)
note_label.grid(row=7, column=0, columnspan=7, padx=10, pady=15)  # Grid placement for note label

'''
for i in range(3):
    #print(str(keep_result[i]))
    note_label = Label(container_note, text="Notes"+str(i+1)+": " + (str(keep_result[i])[:150]).strip(), justify=LEFT, wraplength=230, anchor="nw")
    note_label.grid(sticky = "nw", row = 7, column=i, padx=10, pady=15)  # Grid placement for note label

window.update()  # Ensure widgets are updated before capturing the window

# Capture the content of the Tkinter window
x = window.winfo_rootx()
y = window.winfo_rooty()
width = window.winfo_reqwidth()
height = window.winfo_reqheight()
image = ImageGrab.grab((x, y, x + 800, y + 480))

# Save the image as a file (e.g., 'output.png')
image.save("output.png")

window.mainloop()
