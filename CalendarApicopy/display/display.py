import sys
import os


from waveshare_epd import epd7in3f
import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
logging.basicConfig(level=logging.DEBUG)

class Display:
    def __init__(self):
        self._epd = epd7in3f.EPD()
        self._epd.init()

    def run(self):
        self._epd.Clear()

        logging.info("read calendar.png file")
        Himage = Image.open('calendar.png')
        self._epd.display(self._epd.getbuffer(Himage))
        time.sleep(10)



'''
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in3f
import logging
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)                           #Enable log-information for debbuging

try:
    epd = epd7in3f.EPD()
    epd.init()
    epd.Clear()

    logging.info("read calendar.png file")
    Himage = Image.open(picdir + 'calendar.png')
    epd.display(epd.getbuffer(Himage))
    time.sleep(10)


except IOError as e:
    logging.info(e)
'''
