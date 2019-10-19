#!/usr/bin/env python3
# sundial - WS2812 LED sunrise alarm clock to run on raspberry pi zero w/ photoresitor for active brightness adjustment
# hardware:
# made by ian k. bania, jun' 19, for emmayln's clock
# general foss etiquette applies here

import datetime
import time
import subprocess
#from neopixel import *
from spidev import SpiDev
from graphics import *

# LED strip configuration:
LED_COUNT      = 129      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# define the LEDs to be illuminated to render to the digits
# first position
#zero_0 = [33,36,72,75,109,108,77,69,38,32]
zero_0 = [32,33,38,36,69,72,77,75,108,109]
zero_1 = [32,38,70,77,108]
global zero
zero = [zero_0,zero_1]

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
global one
one = [one_0,one_1,one_2,one_3,one_4,one_5,one_6,one_7,one_8,one_9]

# colon
global colon
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
global two
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
global three
three = [three_0,three_1,three_2,three_3,three_4,three_5,three_6,three_7,three_8,three_9]

############################
# END DATA BEGIN FUNCTIONS #
############################

def LEDlistcreate(digit0, digit1, digit2, digit3):
    """uses 4 digits passed in and the system clock to determine exactly what leds should be on or off to form the digits"""
# clear lists
    backgroundLEDs = []
    foregroundLEDs = []
# concatinate the digit lists (such as zero_3[] which resides inside the positon list zero[]) into a foreground list, allow to colon to be shown on even seconds, blink effect
    if datetime.datetime.now().second % 2 == 0:
        foregroundLEDs = zero[digit0] + one[digit1] + colon + two[digit2] + three[digit3]
    else:
        foregroundLEDs = zero[digit0] + one[digit1] + two[digit2] + three[digit3]
# check to see if an LED is in the foreground, if not, add to background list
    backgroundLEDs = []
    for a in range(0,128,1):
        if a not in foregroundLEDs:
            backgroundLEDs.append(a)
    return backgroundLEDs, foregroundLEDs;

def display(strip, colorfg, colorbg, backgroundLEDs, foregroundLEDs):
    """takes 2 colors and the back and foreground led lists, then displays them on the panel"""
# show fore and background on pannel in respective colors
    for u in foregroundLEDs:
        strip.setPixelColor(u, colorfg)
    for w in backgroundLEDs:
        strip.setPixelColor(w, colorbg)
    strip.show()

def rgb2hex(r,g,b):
    """converts r g and b values into hexidecimal"""
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def graphicaldisplay(backgroundLEDs, foregroundLEDs, prebrightBG, prebrightFG):
    """takes lists of fore and background LEDs, as well as prebirghtness rgb values, displays in a window"""
# convert background color to hexidecimal
    hexBG = rgb2hex(int(prebrightBG[0]), int(prebrightBG[1]), int(prebrightBG[2]))
# convert foreground color to hexidecimal
    hexFG = rgb2hex(int(prebrightFG[0]), int(prebrightFG[1]), int(prebrightFG[2]))

# TOP ROW
    for i in range(112,129,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgcircles = Circle(Point(1050 + -50*(i-112),100), 25) # set center and radius
                fgcircles.setFill(hexFG)
                fgcircles.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgcircles = Circle(Point(1050 + -50*(i-112),100), 25) # set center and radius
                bgcircles.setFill(hexBG)
                bgcircles.draw(win)
# SECOND ROW
    for i in range(94,112,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgpixels = Circle(Point(225 + 50*(i-94),150), 25) # set center and radius
                fgpixels.setFill(hexFG)
                fgpixels.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgpixels = Circle(Point(225 + 50*(i-94),150), 25) # set center and radius
                bgpixels.setFill(hexBG)
                bgpixels.draw(win)
# THIRD ROW
    for i in range(75,94,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgpixels = Circle(Point(200 + 50*(i-75),200), 25) # set center and radius
                fgpixels.setFill(hexFG)
                fgpixels.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgpixels = Circle(Point(200 + 50*(i-75),200), 25) # set center and radius
                bgpixels.setFill(hexBG)
                bgpixels.draw(win)
# FORTH ROW
    for i in range(55,75,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgpixels = Circle(Point(1125 - 50*(i-55),250), 25) # set center and radius
                fgpixels.setFill(hexFG)
                fgpixels.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgpixels = Circle(Point(1125 - 50*(i-55),250), 25) # set center and radius
                bgpixels.setFill(hexBG)
                bgpixels.draw(win)
# FHITH ROW
    for i in range(36,55,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgpixels = Circle(Point(200 + 50*(i-36),300), 25) # set center and radius
                fgpixels.setFill(hexFG)
                fgpixels.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgpixels = Circle(Point(200 + 50*(i-36),300), 25) # set center and radius
                bgpixels.setFill(hexBG)
                bgpixels.draw(win)
# SIXTH ROW
    for i in range(18,36,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgpixels = Circle(Point(1075 - 50*(i-18),350), 25) # set center and radius
                fgpixels.setFill(hexFG)
                fgpixels.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgpixels = Circle(Point(1075 - 50*(i-18),350), 25) # set center and radius
                bgpixels.setFill(hexBG)
                bgpixels.draw(win)
# SEVENTH ROW
    for i in range(1,18,1):
        for x in foregroundLEDs:
            if i == (x+1):
                fgpixels = Circle(Point(200 + 50*i,400), 25) # set center and radius
                fgpixels.setFill(hexFG)
                fgpixels.draw(win)
        for y in backgroundLEDs:
            if i == (y+1):
                bgpixels = Circle(Point(200 + 50*i,400), 25) # set center and radius
                bgpixels.setFill(hexBG)
                bgpixels.draw(win)

def timedigits():
    """uses the system clock to seperate the current time out into it's four digits, returns a list of 4 digits"""
    digits = [0,0,0,0]
    digits[2] = datetime.datetime.now().minute // 10
    digits[3] = datetime.datetime.now().minute % 10
    if datetime.datetime.now().hour >= 12:
        PM = 1
        hour12pm = datetime.datetime.now().hour - 12
        if hour12pm == 0:
            digits[0] = 1
            digits[1] = 2
        else:
            digits[0] = hour12pm // 10
            digits[1] = hour12pm % 10
    else:
        PM = 0
        if datetime.datetime.now().hour == 0:
            digits[0] = 1
            digits[1] = 2
        else:
            digits[0] = datetime.datetime.now().hour // 10
            digits[1] = datetime.datetime.now().hour % 10
    return digits

def getbrightness(alarmtime_hour, alarmtime_min, alarmduration):
    """takes details about the sunrise and calculates the right brightness based on time and photoresitor input"""
    alarmtime_rawmin = alarmtime_hour*60 + alarmtime_min
    nowtime_hour = datetime.datetime.now().hour
    nowtime_min = datetime.datetime.now().minute
    nowtime_sec = datetime.datetime.now().second
    nowtime_rawmin = nowtime_hour*60 + nowtime_min
    sunrisestart_rawmin = alarmtime_rawmin - alarmduration
    max = 1
    offset = .25
    progress = 0
    brightnessBG = max - offset
    brightnessFG = max
    ### DELETE THIS ^, put photoresitor code right here
    #getphotoresistor()
# preprescribed brightness for the sunrise duration
    if (nowtime_rawmin >= sunrisestart_rawmin) and (nowtime_rawmin <= alarmtime_rawmin):
        progress = ((nowtime_rawmin - sunrisestart_rawmin)*60 + nowtime_sec) / (alarmduration*60) #seconds elapsed since alarm started / total seconds in alarm
        brightnessBG = (max - offset)*progress
        brightnessFG = offset + brightnessBG
    if (nowtime_rawmin > alarmtime_rawmin) and (nowtime_rawmin < (alarmtime_rawmin + 15)):
        progress = ((nowtime_rawmin - sunrisestart_rawmin)*60 + nowtime_sec) / (alarmduration*60) #seconds elapsed since alarm started / total seconds in alarm
        brightnessBG = max - offset
        brightnessFG = max
    return brightnessBG, brightnessFG;

def readsettings():
    """reads various files with alarm and color settings, these files need to be in the directory sundial is run in. they are created/edited with bash scripts"""
    file1 = open("alarmtimehour", "r")
    file2 = open("alarmduration", "r")
    file3 = open("colorsetting", "r")
    file4 = open("graphicalsetting", "r")
    file6 = open("alarmtimemin", "r")
    if file1.mode == 'r':
        alarmtime_hour = file1.read()
    if file6.mode == 'r':
        alarmtime_min = file6.read()
    if file2.mode == 'r':
        alarmduration = file2.read()
    if file3.mode == 'r':
        colorsetting = file3.read()
    if file4.mode == 'r':
        graphicalon = file4.read()
    return int(alarmtime_hour), int(alarmtime_min), int(alarmduration), colorsetting, graphicalon;

def getcolor(colorsetting, alarmtime_hour, alarmtime_min, alarmduration):
    """ uses alarm details, the current time and color settings to determine the proper colores in rgb format"""
# default colors
    prebrightBG = [150,25,199]
    prebrightFG = [10,132,10]
# sunrise color determination happ[ens here
    alarmtime_rawmin = alarmtime_hour*60 + alarmtime_min
    nowtime_hour = datetime.datetime.now().hour
    nowtime_min = datetime.datetime.now().minute
    nowtime_sec = datetime.datetime.now().second
    nowtime_rawmin = nowtime_hour*60 + nowtime_min
    sunrisestart_rawmin = alarmtime_rawmin - alarmduration
    progress = 0
    sp = 0
# pre sunrise
    if nowtime_rawmin == sunrisestart_rawmin - 2:
        initialBG = [prebrightBG[0],prebrightBG[1],prebrightBG[2]]
        initialFG = [prebrightFG[0],prebrightFG[1],prebrightFG[2]]
        i = nowtime_sec / 60
        prebrightFG = [(initialFG[0] - i*initialFG[0]),(initialFG[1] - i*initialFG[1]),(initialFG[2] - i*initialFG[2])]
        prebrightBG = [(initialBG[0] - i*initialBG[0]),(initialBG[1] - i*initialBG[1]),(initialBG[2] - i*initialBG[2])]
    if nowtime_rawmin == sunrisestart_rawmin - 1:
        i = nowtime_sec / 60
        prebrightBG = [0,0,(128*i)]
        prebrightFG = [(63*i),0,(255*i)]
# during the sunrise
    if (nowtime_rawmin >= sunrisestart_rawmin) and (nowtime_rawmin < alarmtime_rawmin):
        progress = ((nowtime_rawmin - sunrisestart_rawmin)*60 + nowtime_sec) / (alarmduration*60) #seconds elapsed since alarm started / total seconds in alarm

# !!! sunrise staging is fucked up rn, going 1,2,3,4,1,2,3,4 etc
# FIRST SUNRISE STAGE
        if (progress < 0.14):
            sp = progress / 0.14
            prebrightBG = [(63*sp),0,(128 + 127*sp)] #iterate to 63,0,255 INDIGO
            prebrightFG = [(63 + 64*sp),0,255] #iterate to 127,0,255 VIOLET TEXT
            print("stage1")
# SECOND SUNRISE STAGE
        if (progress >= 0.14) and (progress < 0.28):
            sp = (progress - 0.14) / 0.14
            prebrightBG = [(63 + 64*sp),0,255] #iterate to 127,0,255 VIOLET
            prebrightFG = [(127 + 126*sp),(0 + 192*sp),(255 - 52*sp)] #iterate to 255,192,203 PINK TEXT
            print("stage2")
# THIRD SUNRISE STAGE
        if (progress >= 0.28) and (progress < 0.42):
            sp = (progress - 0.28) / 0.14
            prebrightBG = [(127 + 126*sp),(0 + 192*sp),(255 - 52*sp)] #iterate to 255,192,203 PINK
            prebrightFG = [255,(192 - 65*sp),(203 - 203*sp)] #iterate to 255,127,0 ORANGE NUMBERS
            print("stage3")
# FOURTH SUNRISE STAGE
        if (progress >= 0.42) and (progress < 0.56):
            sp = (progress - 0.42) / 0.14
            prebrightBG = [255,(192 - 65*sp),(203 - 203*sp)] #iterate to 255,127,0 ORANGE
            prebrightFG = [255,(127 + 88*sp),0] #iterate to 255,215,0 GOLD NUMBERS
            print("stage4")
# FHITH SUNRISE STAGE
        if (progress >= 0.56) and (progress < 0.70):
            sp = (progress - 0.56) / 0.14
            prebrightBG = [255,(127 + 88*sp),0] #iterate to 255,215,0 GOLD
            prebrightFG = [255,(215 + 40*sp),0] #iterate to 255,255,0 YELLOW NUMBERS
            print("stage5")
# SIXTH SUNRISE STAGE
        if (progress >= 0.70) and (progress < 0.84):
            sp = (progress - 0.70) / 0.14
            prebrightBG = [255,(215 + 40*sp),0] #iterate to 255,255,0 YELLOW
            prebrightFG = [255,255,(0 + 204*sp)] #iterate to 255,255,204 LIGHT YELLOW NUMBERS
            print("stage6")
# FINAL SUNRISE STAGE
        if (progress >= 0.84) and (progress <= 1 ):
            sp = (progress - 0.84) / 0.14
            prebrightBG = [255,255,(0 + 204*sp)] #iterate to 255,255,204 LIGHT YELLOW
            prebrightFG = [(255 - 82*sp),(255 - 39*sp),(204 + 26*sp)] #iterate to 173,216,230 LIGHT BLUE NUMBERS
            print("stage7")
# post sunrise
    if (nowtime_rawmin >= alarmtime_rawmin) and (nowtime_rawmin < (alarmtime_rawmin + 15)):
        prebrightBG = [255,255,204]
        prebrightFG = [173,216,230]
    if nowtime_rawmin == alarmtime_rawmin + 15:
        initialBG = [prebrightBG[0],prebrightBG[1],prebrightBG[2]]
        initialFG = [prebrightFG[0],prebrightFG[1],prebrightFG[2]]
        i = nowtime_sec / 60
        prebrightFG = [(initialFG[0] - i*initialFG[0]),(initialFG[1] - i*initialFG[1]),(initialFG[2] - i*initialFG[2])]
        prebrightBG = [(initialBG[0] - i*initialBG[0]),(initialBG[1] - i*initialBG[1]),(initialBG[2] - i*initialBG[2])]
    if nowtime_rawmin == alarmtime_rawmin + 16:
        i = nowtime_sec / 60
        prebrightBG = [(150*i),(25*i),(199*i)]
        prebrightFG = [(10*i),(132*i),(10*i)]
# debuging
    # print("*****")
    # print(progress, "progress")
    # print(sp, "stage progress")
    # print(nowtime_min, "min")
    # print(nowtime_sec, "sec")
    # print(prebrightBG,prebrightFG)
    return prebrightBG, prebrightFG;

def applybrightness(prebrightBG, prebrightFG, brightnessBG, brightnessFG):
    """ takes the brightnesses and the rbg colors and mixes them, returning the rgb values with brightness applied"""
    postbrightBG = [i * brightnessBG for i in prebrightBG]
    postbrightFG = [j * brightnessFG for j in prebrightFG]
    return postbrightBG, postbrightFG;

def LEDreadable(postbrightBG, postbrightFG):
    """takes rgb colors and converts them to something the WS2812 can understand, honestly have no idea how the color() function works, it just do"""
    for i in postbrightBG:
        LEDreadconvertBG[i] = Color(postbrightBG[i])
    for j in postbrightFG[j]:
        LEDreadconvertFG[i] = Color(postbrightFG[j])
    return LEDreadconvertBG, LEDreadconvertFG;


########
# MAIN #
########
if __name__ == '__main__':
# create NeoPixel object with appropriate configuration
    # strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# intialize the library (must be called once before other functions)
    # strip.begin()
# initalize lists
    M_prebrightBG = [0,0,0]
    M_prebrightFG = [0,0,0]
    M_postbrightBG = [0,0,0]
    M_postbrightFG = [0,0,0]
    M_LEDreadconvertBG = [0,0,0]
    M_LEDreadconvertFG = [0,0,0]
    M_digits = [0,0,0,0]
# give title and dimensions to the onscreen display
    win = GraphWin('clock', 1300, 500)

#################
# WHILE in MAIN #
#################
    while True: #processing loop that the clock is countinously running
        M_alarmtime_hour, M_alarmtime_min, M_alarmduration, M_colorsetting, M_graphicalon = readsettings()
        M_brightnessFG, M_brightnessBG = getbrightness(M_alarmtime_hour, M_alarmtime_min, M_alarmduration)
        M_prebrightBG, M_prebrightFG = getcolor(M_colorsetting, M_alarmtime_hour, M_alarmtime_min, M_alarmduration)
        M_postbrightBG, M_postbrightFG = applybrightness(M_prebrightBG, M_prebrightFG, M_brightnessBG, M_brightnessFG)
#        LEDreadconvertBG, LEDreadconvertFG = LEDreadable(postbrightBG, postbrightFG)
        M_digits = timedigits()
        M_backgroundLEDs, M_foregroundLEDs = LEDlistcreate(M_digits[0], M_digits[1], M_digits[2], M_digits[3])
# finally, call the LED display

# also call the graphical onscreen display
        if int(M_graphicalon) == 1:
            graphicaldisplay(M_backgroundLEDs, M_foregroundLEDs, M_postbrightBG, M_postbrightFG)
# reduce thermal workload and hardware lifetime ?
        time.sleep(.25)
