#!/usr/bin/env python3
# sundial - LED sunrise alarm clock
# made by Ian K. Bania, June 2019

import datetime
currentDT = datetime.datetime.now()
import time
import subprocess
from neopixel import *

# LED strip configuration:
LED_COUNT      = 129      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# define the LEDs to be illuminated to render to the digits
# first position
zero_0 = []
zero_1 = [33,37,71,76,109]
zero_2 = []
zero_3 = []
zero_4 = []
zero_5 = []
zero_6 = []
zero_7 = []
zero_8 = []
zero_9 = []
zero = [zero_0,zero_1,zero_2,zero_3,zero_4,zero_5,zero_6,zero_7,zero_8,zero_9]

# second position
one_0 = []
one_1 = []
one_2 = [29,28,40,67,66,81,104,105]
one_3 = []
one_4 = []
one_5 = []
one_6 = []
one_7 = []
one_8 = []
one_9 = []
one = [one_0,one_1,one_2,one_3,one_4,one_5,one_6,one_7,one_8,one_9]

# colon
colon = [44,83]

# third position
two_0 = [46,85,99,98,87,62,59,48,23,22]
two_1 = [22,48,60,87,98]
two_2 = [22,23,60,61,87,98,99,46]
two_3 = [23,22,99,98,60,61,87,48]
two_4 = [23,47,60,87,97,99,85,61,62]
two_5 = [85,99,98,61,60,48,23,22]
two_6 = [46,85,99,98,22,23,48,61,60]
two_7 = [23,47,60,87,97,98,99]
two_8 = [46,85,99,98,87,61,60,48,23,22]
two_9 = [85,99,98,87,61,60,48,23,22]
two = [two_0,two_1,two_2,two_3,two_4,two_5,two_6,two_7,two_8,two_9]

#fourth position
three_0 = []
three_1 = [18,52,56,91,94]
three_2 = []
three_3 = []
three_4 = []
three_5 = []
three_6 = []
three_7 = []
three_8 = []
three_9 = []
three = [three_0,three_1,three_2,three_3,three_4,three_5,three_6,three_7,three_8,three_9]

def display(strip, colorfg, colorbg, digit0, digit1, digit2, digit3):
    """takes 2 colors and 4 digits, then displays them on the panel"""

    # concatinate the digit lists (such as zero_3[] which resides inside the positon list zero[]) into a foreground list
    foreground = zero[digit0] + one[digit1] + colon + two[digit2] + three[digit3]

    # check to see if an LED is in the foreground, if not, add to background list
    background = []
    for a in range(128):
        if a not in foreground:
            background.append(a)

    # show fore and background on pannel in respective colors
    for b in foreground:
        strip.setPixelColor(b, colorfg)
    for c in background:
        strip.setPixelColor(c, colorbg)
    strip.show()

def timedisplay(strip, colorfg, colorbg):
    # file = open(".alarm", "r")
    # alarm0 = file.readline(1)
    # alarm1 = file.readline(2)
    # alarm2 = file.readline(3)
    # alarm3 = file.readline(4)
    # alarmPM = file.readline(5)
    #
    # file = open(".sunrise", "r")
    # buffer = readline(1)
    #
    # file = open(".sound", "r")
    # sound = readline(1)

    digit2 = currentDT.minute // 10
    digit3 = currentDT.minute % 10

    if currentDT.hour >= 12:
        PM = 1
        hour12pm = currentDT.hour - 12
        if hour12pm == 0:
            digit0 = 1
            digit1 = 2
        else:
            digit0 = hour12pm // 10
            digit1 = hour12pm % 10
    else:
        PM = 0
        if currentDT.hour == 0:
            digit0 = 1
            digit1 = 2
        else:
            digit0 =  currentDT.hour // 10
            digit1 = currentDT.hour % 10

    display(strip, colorfg, colorbg, digit0, digit1, digit2, digit3)
#    if digit0 == alarm0 and digit1 == alarm1 and digit2 == alarm2 and digit3 == alarm3 and PM = alarmPM:


if __name__ == '__main__':
    # create NeoPixel object with appropriate configuration
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # intialize the library (must be called once before other functions)
    strip.begin()

    fG = .05
    fB = .7
    fR = 1
    bG = 1
    bB = .3
    bR = .3
    fgbright = 1
    bgbright = .07
    abs_fG = int(256 * fG * fgbright)
    abs_fB = int(256 * fB * fgbright)
    abs_fR = int(256 * fR * fgbright)
    abs_bG = int(256 * bG * bgbright)
    abs_bB = int(256 * bB * bgbright)
    abs_bR = int(256 * bR * bgbright)

    while True:
        timedisplay(strip, Color(abs_fG, abs_fB, abs_fR), Color(abs_bG, abs_bB, abs_bR))
        time.sleep(0.5)
