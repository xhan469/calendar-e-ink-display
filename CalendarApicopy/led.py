import time
import board
import neopixel
from datetime import datetime


def blink_leds(pixels, color_code, blink_duration=0.5, blink_count=10, off_duration=None):
    """
    Make the LED strip blink in a given color.

    Parameters:
    - pixels: The initialized NeoPixel object representing the LED strip.
    - color_code: The RGB color code for the blink.
    - blink_duration: Duration for which the LEDs stay ON during each blink.
    - blink_count: Number of times the LED strip should blink.
    - off_duration: Duration for which the LEDs stay OFF between blinks. If None, it will be the same as blink_duration.
    """
    if off_duration is None:
        off_duration = blink_duration

    for _ in range(blink_count):
        pixels.fill(color_code)
        time.sleep(blink_duration)
        pixels.fill((0, 0, 0))
        time.sleep(off_duration)

    # Keep the LED on with the specified color after blinking
    pixels.fill(color_code)

def turn_on_leds(pixels, color_code):
    """
    Turn on the LEDs with the given color.

    Parameters:
    - pixels: The initialized NeoPixel object representing the LED strip.
    - color_code: The RGB color code to turn the LEDs on.
    """
    pixels.fill(color_code)


def turn_off_leds(pixels):
    """
    Turn off all the LEDs.

    Parameters:
    - pixels: The initialized NeoPixel object representing the LED strip.
    """
    pixels.fill((0, 0, 0))



if __name__ == "__main__":
    # Initialize the LED strip. Adjust the number of LEDs and GPIO pin as needed.
    num_leds = 55  # Change this to the number of LEDs on your strip
    pixels = neopixel.NeoPixel(board.D18, num_leds, brightness=0.5)

    # Blink the LEDs in blue color
    '''
    color_code = (0, 0, 255)
    blink_leds(pixels, color_code)'''

    time_string = "15:10:45"
    # Convert the time string to a datetime.time object
    check_time = datetime.strptime(time_string, "%H:%M:%S").time()

    now = datetime.now().time()


        # print(check_time, r, g, b)
    #blink_leds(pixels, (0, 0, 255))

    # Turn off all LEDs at the end
    pixels.fill((0, 0, 0))
    #turn_off_leds(pixels)



