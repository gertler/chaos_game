#!/usr/bin/env python3

from graphics import *
from random import *
from time import *

rules = "(1)\tPure random point (No modifier)\n"
rules += "(2)\tDon't repeat previous point\n"
rules += "(3)\tDon't choose the point directly counterclockwise to the previous point\n"
rules += "(4)\tDon't choose the point 2 away from the previous point\n"
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']


def normal_rule():
    return randint(0, num_points - 1)


def no_imm_repeat(old):
    choice = randint(0, num_points - 1)
    while old == choice:
        choice = randint(0, num_points - 1)
    return choice


def no_cclock(old):
    choice = randint(0, num_points - 1)
    while choice == (old + 1) % num_points:
        choice = randint(0, num_points - 1)
    return choice


def no_2_away(old):
    choice = randint(0, num_points - 1)
    while choice == (old + 2) % num_points:
        choice = randint(0, num_points - 1)
    return choice


# Get initial information about the program
num_points = 3
iterations = 2000
delta = 0.5
rule = 1
np = input("Enter the number of points (Enter nothing for default) (3-6 suggested): ")
if np != '':
    num_points = int(np)
    iterations = int(input("Enter the number of iterations you'd like to see (4000-6000 suggested): "))
    delta = float(input("Enter the fraction of distance travelled each time (0.5-0.75 suggested): "))
    rule = int(input(rules + "Enter the rule modifier: "))

# Create the window and message
win = GraphWin('Chaos Game!', 725, 725)
win.setBackground('black')
message = Text(Point(win.getWidth() / 2, 20), 'Click on ' + str(num_points) + '  points')
message.setTextColor('white')
message.setSize(13)
message.draw(win)

# Get and draw three vertices of triangle
vertices = []
for i in range(num_points):
    point = win.getMouse()
    point.setOutline('white')
    point.draw(win)
    vertices += [point]

message.setText('Click a starting point')
curr_point = win.getMouse()

curr_x_y = curr_point.getX(), curr_point.getY()
win.plot(curr_x_y[0], curr_x_y[1], 'white')

# -----------------
# Run the algorithm
# -----------------
new_choice = -1
old_choice = -1
division = iterations / 50
for j in range(iterations):
    if win.isClosed():
        break

    # Update the iteration count
    if j % division == 0:
        message.setText('Iteration: ' + str(j) + ' / ' + str(iterations))

    # Choose next vertex using rule
    if rule == 1:
        new_choice = normal_rule()
    elif rule == 2:
        new_choice = no_imm_repeat(old_choice)
    elif rule == 3:
        new_choice = no_cclock(old_choice)
    else:
        new_choice = no_2_away(old_choice)

    point = vertices[new_choice]
    old_choice = new_choice

    # Find the distance to travel
    dx = (point.getX() - curr_x_y[0]) * delta
    dy = (point.getY() - curr_x_y[1]) * delta

    curr_x_y = curr_x_y[0] + dx, curr_x_y[1] + dy
    win.plot(curr_x_y[0], curr_x_y[1], colors[j%len(colors)])
    # Comment below line to choose fast-mode
    sleep(0.5**(j/(0.0075*iterations)))

if not win.isClosed():
    message.setText('Click anywhere to quit')  # change text message
    win.getMouse()
    win.close()
