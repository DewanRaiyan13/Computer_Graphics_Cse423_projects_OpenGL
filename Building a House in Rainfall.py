#Task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w, h = 800, 600   
drops = []
bright = 0.8
t_bright = 0.8  
tilt = 0  

def init_drops():
    global drops
    drops = []
    for i in range(100):
        x = random.randint(0, w)
        y = random.randint(h // 2, h)
        drops.append((x, y, random.uniform(2, 4)))

def draw_bg():
    glColor3f(bright, bright, bright)
    glBegin(GL_TRIANGLES)                    #sky
    glVertex2f(0, h)
    glVertex2f(w, h)
    glVertex2f(0, h * 0.5)   
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(w, h)
    glVertex2f(w, h * 0.5)
    glVertex2f(0, h * 0.5)
    glEnd()

    glColor3f(0.0, 0.5, 0.0)  
    glBegin(GL_TRIANGLES)
    glVertex2f(0, h * 0.5)    #ground
    glVertex2f(w, h * 0.5)
    glVertex2f(0, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(w, h * 0.5)
    glVertex2f(w, 0)
    glVertex2f(0, 0)
    glEnd()

def draw_house():
    glColor3f(0.9, 0.2, 0.8)  
    glBegin(GL_TRIANGLES)
    glVertex2f(200, 250)     # Roof
    glVertex2f(600, 250)
    glVertex2f(400, 400)
    glEnd()
    
    glColor3f(1 ,1 ,0)  
    glBegin(GL_TRIANGLES)
    glVertex2f(220, 50)
    glVertex2f(580, 50)       # House
    glVertex2f(220, 250)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(580, 50)
    glVertex2f(580, 250)
    glVertex2f(220, 250)
    glEnd()

    glColor3f(0.93, 0.6, 0.4)  
    glBegin(GL_TRIANGLES)
    glVertex2f(360, 50)      # Door
    glVertex2f(440, 50)
    glVertex2f(360, 150)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(440, 50)
    glVertex2f(440, 150)
    glVertex2f(360, 150)
    glEnd()

    win_color = (0.8, 0.6, 0.4) 
    glColor3f(win_color[0], win_color[1], win_color[2])
    glBegin(GL_LINES)
    glVertex2f(260, 180)
    glVertex2f(300, 180)
    glVertex2f(300, 180)
    glVertex2f(300, 220)
    glVertex2f(300, 220)    # Window
    glVertex2f(260, 220)
    glVertex2f(260, 220)
    glVertex2f(260, 180)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(500, 180)
    glVertex2f(540, 180)    # Window
    glVertex2f(540, 180)
    glVertex2f(540, 220)
    glVertex2f(540, 220)
    glVertex2f(500, 220)
    glVertex2f(500, 220)
    glVertex2f(500, 180)
    glEnd()

def draw_rain_drop(x, y, speed):
    if bright < 0.5 :
        rain_color = (1.0, 1.0, 1.0) 
    else: rain_color = (0.0, 0.0, 0.0)

    glColor3f(*rain_color)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(x, y)
    glVertex2f(x + tilt * 0.5, y - 10)
    glEnd()
    glLineWidth(1)

def update_drops():
    global drops
    new_drops = []
    for x, y, speed in drops:
        y -= speed
        x += tilt * 0.5  
        if y < 0:
            y = h
        if x < 0:
            x = w
        elif x > w:
            x = 0
        new_drops.append((x, y, speed))
    drops = new_drops

def update_bright():
    global bright, t_bright
    if bright < t_bright:
        bright = min(bright + 0.01, t_bright)
    elif bright > t_bright:
        bright = max(bright - 0.01, t_bright)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    
    draw_bg()
    draw_house()
    
    for rain in drops:
        draw_rain_drop(rain[0], rain[1], rain[2])
    
    glutSwapBuffers()

def animate():
    update_drops()
    update_bright()
    glutPostRedisplay()

def specialkey_control(key, x, y):
    global tilt
    if key == GLUT_KEY_RIGHT:
        tilt = min(10, tilt + 1)
        print("Tilt Right")
    if key == GLUT_KEY_LEFT:
        tilt = max(-10, tilt - 1)
        print("Tilt Left")
    
    glutPostRedisplay()

def key_control(key, x, y):
    global t_bright
    if key == b'n':
        t_bright = max(0.0, t_bright - 0.1) 
    if key == b'm':
        t_bright = min(1.0, t_bright + 0.1)   
    glutPostRedisplay()

def iterate():
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    init_drops()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(w, h)
glutInitWindowPosition(0, 0)
glutCreateWindow(b" Raiyan House in Rain")
init()
glutDisplayFunc(display)
glutKeyboardFunc(key_control)
glutIdleFunc(animate)
glutSpecialFunc(specialkey_control)
glutMainLoop()



