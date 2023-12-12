import socket
import subprocess
import sys
import os


from waveshare_epd import epd7in3g
import logging
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
logging.basicConfig(level=logging.DEBUG)


def check_wifi_connected():
    try:
        # Run a command to get the WiFi status
        output = subprocess.check_output(["iwgetid"]).decode("utf-8")
        if "ESSID" in output:
            return True
    except subprocess.CalledProcessError:
        pass
    return False

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to a remote server (Google's public DNS server)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address of the machine
        ip_address = s.getsockname()[0]

        # Close the socket
        s.close()
        return ip_address
    except socket.gaierror:
        return None

# Function to get the current WiFi SSID
def get_ssid():
    try:
        ssid = subprocess.check_output(['iwgetid', '-r']).decode().strip()
        return ssid
    except subprocess.CalledProcessError:
        return None

if __name__ == "__main__":
    if check_wifi_connected():
        ip_address = get_ip_address()
        ssid = get_ssid()

        if ip_address and ssid:
            print(f"Connected to WiFi. IP address: {ip_address}")

            message = 'http://' + ip_address + ':5000'


            epd = epd7in3g.EPD()
            logging.info("init and Clear")
            epd.init()
            epd.Clear()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            arial_path = os.path.join(script_dir, "Arial.ttf")
            print(arial_path)

            font24 = ImageFont.truetype(arial_path, 24)

            Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
            draw = ImageDraw.Draw(Himage)
            draw.text((400, 0), message, font=font24, fill=epd.RED)
            draw.text((400, 30), ssid, font=font24, fill=epd.RED)
            epd.display(epd.getbuffer(Himage))
            time.sleep(3)

        else:
            print("Connected to WiFi, but could not get IP address.")


    else:
        print("Not connected to WiFi. Please connect to the default WiFi settings.")
        message = "Not connected to WiFi. Please connect to the default WiFi settings."


        epd = epd7in3g.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        arial_path = os.path.join(script_dir, "Arial.ttf")
        print(arial_path)

        font24 = ImageFont.truetype(arial_path, 24)

        Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        draw.text((0, 0), message, font=font24, fill=epd.RED)
        epd.display(epd.getbuffer(Himage))
        time.sleep(3)
