#!/usr/bin/env python3
# sundial - LED sunrise alarm clock
# made by Ian K. Bania, June 2019

import time
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



# define functions which animate LEDs in various ways
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# def theaterChase(strip, color, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     for j in range(iterations):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, color)
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)
#
# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)
#
# def rainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i+j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
#
# def rainbowCycle(strip, wait_ms=20, iterations=5):
#     """Draw rainbow that uniformly distributes itself across all pixels."""
#     for j in range(256*iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
#         strip.show()
#         time.sleep(wait_ms/1000.0)
#
# def theaterChaseRainbow(strip, wait_ms=50):
#     """Rainbow movie theater light style chaser animation."""
#     for j in range(256):
#         for q in range(3):
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, wheel((i+j) % 255))
#             strip.show()
#             time.sleep(wait_ms/1000.0)
#             for i in range(0, strip.numPixels(), 3):
#                 strip.setPixelColor(i+q, 0)

# define the LEDs to be illuminated to render to the digits
# first position
zero_0 = []
zero_1=[33,37,71,76,109]
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
one_0=[]
one_1=[]
one_2=[29,28,40,67,66,81,104,105]
one_3=[]
one_4=[]
one_5=[]
one_6=[]
one_7=[]
one_8=[]
one_9=[]
one = [one_0,one_1,one_2,one_3,one_4,one_5,one_6,one_7,one_8,one_9]

# colon
colon=[44,83]

# third position
two_0=[46,85,99,98,87,62,59,48,23,22]
two_1=[22,48,60,87,98]
two_2=[22,23,60,61,87,98,99,46]
two_3=[23,22,99,98,60,61,87,48]
two_4=[23,47,60,87,97,99,85,61,62]
two_5=[85,99,98,61,60,48,23,22]
two_6=[46,85,99,98,22,23,48,61,60]
two_7=[23,47,60,87,97,98,99]
two_8=[46,85,99,98,87,61,60,48,23,22]
two_9=[85,99,98,87,61,60,48,23,22]
two = [two_0,two_1,two_2,two_3,two_4,two_5,two_6,two_7,two_8,two_9]

#fourth position
three_0=[]
three_1=[18,52,56,91,94]
three_2=[]
three_3=[]
three_4=[]
three_5=[]
three_6=[]
three_7=[]
three_8=[]
three_9=[]
three = [three_0,three_1,three_2,three_3,three_4,three_5,three_6,three_7,three_8,three_9]

def display(strip, colorfg, colorbg, digit0, digit1, digit2, digit3):
    """takes 2 colors and 4 digits, then displays them on the panel"""
    #colorWipe(strip, Color(0,59,0))

    for a in zero[digit0]:
        strip.setPixelColor(a, colorfg)
        strip.show()

    for b in one[digit1]:
        strip.setPixelColor(b, colorfg)
        strip.show()

    for c in colon:
        strip.setPixelColor(c, colorfg)
        strip.show()

    for d in two[digit2]:
        strip.setPixelColor(d, colorfg)
        strip.show()

    for e in three[digit3]:
        strip.setPixelColor(e, colorfg)
        strip.show()


if __name__ == '__main__':
    # create NeoPixel object with appropriate configuration
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # intialize the library (must be called once before other functions)
    strip.begin()
    # exit conditon
    print ('Press Ctrl-C to quit.')

    try:
        while True:
            display(strip, Color(5,100,177), Color(23,5,6), 1, 2, 9, 1)
    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 10)
