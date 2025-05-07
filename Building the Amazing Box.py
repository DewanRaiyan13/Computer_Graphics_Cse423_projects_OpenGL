#Task2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w, h = 800, 600
point = []
dir = []
color = []
speed = 0.1
blink_stat = 'off'
blink_flag = 'no'
paused = False

class Point:
    def __init__(self, x, y, dx, dy, color):
        self.x = x        # x and y coordinates of point
        self.y = y 
        self.dx = dx      # dx and dy direction of point
        self.dy = dy
        self.color = color
        self.original_color = color

def draw_point(x, y, color):
    glPointSize(13)
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def create_point(x, y):
    global point, dir, color
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])
    color = [random.random(), random.random(), random.random()]
    p = Point(x, y, dx, dy, color)
    point.append(p)
    dir.append([dx, dy])
    color.append(color)

def blink(value):
    global blink_stat
    if blink_stat == 'off':
        blink_stat = 'on'
    elif blink_stat == 'on':
        blink_stat = 'off'
    if blink_flag == 'yes':
        glutTimerFunc(500, blink, 0)

def speed_control(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed += 0.05
    elif key == GLUT_KEY_DOWN:
        speed = max(0.05, speed - 0.05)

def keyboard_control(key, x, y):
    global paused
    if key == b' ':
        paused = not paused

def mouse_control(button, state, x, y):
    global blink_flag
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        create_point(x, h - y)
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if blink_flag == 'no':
            blink_flag = 'yes'
            blink(0)
        else:
            blink_flag = 'no'

def update_points():
    global point, dir, color, speed, blink_stat, paused
    if not paused:
        for i in range(len(point)):
            point[i].x += point[i].dx * speed
            point[i].y += point[i].dy * speed
            if point[i].x <= 0 or point[i].x >= w:
                point[i].dx *= -1
            if point[i].y <= 0 or point[i].y >= h:
                point[i].dy *= -1
        glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for i in range(len(point)):
        if blink_stat == 'on' and blink_flag == 'yes':
            continue
        draw_point(point[i].x, point[i].y, point[i].color)
    glutSwapBuffers()

def iterate():
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, w, 0.0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
glutCreateWindow(b" Raiyan Amazing Box")
glutDisplayFunc(display)
glutIdleFunc(update_points)
glutSpecialFunc(speed_control)
glutKeyboardFunc(keyboard_control)
glutMouseFunc(mouse_control)
iterate()
glutMainLoop()