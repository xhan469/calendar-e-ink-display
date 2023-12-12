import RPi.GPIO as GPIO
import os
import subprocess
import time

#script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up the GPIO pin for button input
BUTTON_PIN = 26
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def config(channel):
    print("Button pressed!")
    pressed_time = time.time()
    while GPIO.input(BUTTON_PIN) == 0:  # Wait for the button to be released
        time.sleep(0.1)
    released_time = time.time()
    elapsed_time = released_time - pressed_time
    if elapsed_time > 3:  # Change 1 to the number of seconds you consider a "long press"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Kill render.py
        render_path = os.path.join(script_dir, "show_ip.py")
        try:
            print("killing render")
            subprocess.run(["pkill", "-f", render_path])
        except Exception as e:
            print(f"Failed to kill render.py: {e}")

        subprocess.run(['wpa_cli', '-i', 'wlan0', 'reconfigure'])
        time.sleep(10)
        appfile_path = os.path.join(script_dir, "app.py")
        epd_path = os.path.join(script_dir, "show_ip.py")
        print("Running show_ip.py...")

        subprocess.run(["python3", epd_path])


        print("Long press detected! Running app.py...")

        subprocess.run(["python3", appfile_path])






    else:
        print("Short press detected. Doing nothing.")

# Detect falling edge on button press
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=config, bouncetime=200)

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()


