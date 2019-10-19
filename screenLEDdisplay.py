'''A simple graphics example constructs a face from basic shapes.
'''

from graphics import *


def main():
    win = GraphWin('Face', 1300, 500) # give title and dimensions

    for a in range(128):
        LEDs = {}
        LEDs[a] = yellow

    for i in range(17):
        one = Circle(Point(250 + 50*i,100), 25) # set center and radius
        one.setFill("yellow")
        one.draw(win)

    for j in range(18):
        two = Circle(Point(225 + 50*j,150), 25) # set center and radius
        two.setFill("yellow")
        two.draw(win)

    for k in range(19):
        two = Circle(Point(200 + 50*k,200), 25) # set center and radius
        two.setFill("yellow")
        two.draw(win)

    for l in range(20):
        two = Circle(Point(175 + 50*l,250), 25) # set center and radius
        two.setFill("yellow")
        two.draw(win)

    for m in range(19):
        one = Circle(Point(200 + 50*m,300), 25) # set center and radius
        one.setFill("yellow")
        one.draw(win)

    for n in range(18):
        two = Circle(Point(225 + 50*n,350), 25) # set center and radius
        two.setFill("yellow")
        two.draw(win)

    for k in range(17):
        two = Circle(Point(250 + 50*k,400), 25) # set center and radius
        two.setFill("yellow")
        two.draw(win)


    message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')
    message.draw(win)
    win.getMouse()
    win.close()

main()
