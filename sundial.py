#!/usr/bin/env python3
# sundial - LED sunrise alarm clock
# made by Ian K. Bania, June 2019

import datetime
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
#zero_0 = [33,36,72,75,109,108,77,69,38,32]
zero_0 = []
zero_1 = [32,38,70,77,108]
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
one_0 = [28,29,42,65,81,104,105,79,68,40]
one_1 = [28,42,66,81,104]
one_2 = [29,28,40,67,66,81,104,105]
one_3 = [29,28,42,67,66,81,104,105]
one_4 = [29,41,66,67,68,81,103,105,79]
one_5 = [29,28,42,67,66,79,104,105]
one_6 = [29,28,42,67,66,79,104,105,40]
one_7 = [29,41,66,81,103,104,105]
one_8 = [29,28,42,67,66,79,104,105,40,81]
one_9 = [29,41,67,66,79,104,105,81]
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
two_9 = [85,99,98,87,61,60,23,47]
two = [two_0,two_1,two_2,two_3,two_4,two_5,two_6,two_7,two_8,two_9]

#fourth position
three_0 = [18,19,50,52,58,55,91,89,95,94]
three_1 = [18,52,56,91,94]
three_2 = [18,19,50,57,56,91,94,95]
three_3 = [95,94,91,56,57,52,18,19]
three_4 = [19,51,56,91,93,57,58,89,95]
three_5 = [94,95,89,57,56,52,18,19]
three_6 = [94,95,89,57,56,52,18,19,50]
three_7 = [19,51,56,91,93,94,95]
three_8 = [94,89,57,56,52,18,19,91,95,50]
three_9 = [94,89,57,56,51,19,95,91]
three = [three_0,three_1,three_2,three_3,three_4,three_5,three_6,three_7,three_8,three_9]

############
# END DATA #
############

def display(strip, colorfg, colorbg, digit0, digit1, digit2, digit3):
    """takes 2 colors and 4 digits, then displays them on the panel"""

    # concatinate the digit lists (such as zero_3[] which resides inside the positon list zero[]) into a foreground list
    # allow to colon to be shown on even seconds, blink effect
    if datetime.datetime.now().second % 2 == 0:
        foreground = zero[digit0] + one[digit1] + colon + two[digit2] + three[digit3]
    else:
        foreground = zero[digit0] + one[digit1] + two[digit2] + three[digit3]

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
    """takes colors in final form, and calls the display to print the time"""

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

    digit2 = datetime.datetime.now().minute // 10
    digit3 = datetime.datetime.now().minute % 10

    if datetime.datetime.now().hour >= 12:
        PM = 1
        hour12pm = datetime.datetime.now().hour - 12
        if hour12pm == 0:
            digit0 = 1
            digit1 = 2
        else:
            digit0 = hour12pm // 10
            digit1 = hour12pm % 10
    else:
        PM = 0
        if datetime.datetime.now().hour == 0:
            digit0 = 1
            digit1 = 2
        else:
            digit0 = datetime.datetime.now().hour // 10
            digit1 = datetime.datetime.now().hour % 10

    display(strip, colorfg, colorbg, digit0, digit1, digit2, digit3)


########
# MAIN #
########

if __name__ == '__main__':
    # create NeoPixel object with appropriate configuration
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # intialize the library (must be called once before other functions)
    strip.begin()
    # brightness setting
    BRIGHTfg = 1
    BRIGHTbg = 1
    # initialize lists
    fg = [0, 0, 0]
    bg = [0, 0, 0]
    # color setting
    #RAWbg = [226./255., 201./255., 1.] #skyblue
    RAWbg = [1,1,1] #overcast
    #RAWbg = [39./255., 171./255., 79./255.]
    RAWfg = [1. - RAWbg[0], 1. - RAWbg[1], 1. - RAWbg[2]]
    print(RAWbg)
    print(RAWfg)
    # mix the values with the brightness multipler
    for m in range(3):
        fg[m] = int(RAWfg[m] * 255 * BRIGHTfg)
        bg[m] = int(BRIGHTbg * 255 * RAWbg[m])
    # call clock function with the calculated colors
    print(bg)
    print(fg)
    while True:
        timedisplay(strip, Color(fg[0], fg[1], fg[2]), Color(bg[0], bg[1], bg[2]))
