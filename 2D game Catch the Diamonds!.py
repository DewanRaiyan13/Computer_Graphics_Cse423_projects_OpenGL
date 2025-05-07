from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys
import time


win_width, win_height = 800, 600
player_x = 0
player_y = -win_height // 2 + 50
player_width = 100
player_height = 20
player_speed = 20

dia_a = random.randint(-win_width // 2 + 30, win_width // 2 - 30)
dia_b = win_height // 2 - 30
dia_size = 20
dia_speed = 3.5
dia_color = (1.0, 1.0, 1.0)

score = 0
game_over = False
paused = False

def draw_midpointLine(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        glVertex2f(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_catcher():
    glColor3f(1.0, 1.0, 1.0) if not game_over else glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    top_left_x = player_x - player_width // 1.5
    top_right_x = player_x + player_width // 1.5
    bottom_left_x = player_x - player_width // 1.5 + 20
    bottom_right_x = player_x + player_width // 1.5 - 20
    top_y = player_y + player_height
    bottom_y = player_y
    draw_midpointLine(bottom_left_x, bottom_y, bottom_right_x, bottom_y)  
    draw_midpointLine(bottom_left_x, bottom_y, top_left_x, top_y)       
    draw_midpointLine(bottom_right_x, bottom_y, top_right_x, top_y)      
    draw_midpointLine(top_left_x, top_y, top_right_x, top_y)        
    glEnd()

def draw_diamond():
    glColor3f(*dia_color)
    glBegin(GL_POINTS)
    draw_midpointLine(dia_a, dia_b, dia_a - dia_size // 2, dia_b - dia_size // 2)
    draw_midpointLine(dia_a, dia_b, dia_a + dia_size // 2, dia_b - dia_size // 2)
    draw_midpointLine(dia_a - dia_size // 2, dia_b - dia_size // 2, dia_a, dia_b - dia_size)
    draw_midpointLine(dia_a + dia_size // 2, dia_b - dia_size // 2, dia_a, dia_b - dia_size)
    glEnd()

def draw_buttons():
    button_y = win_height // 2 - 50
    button_spacing = 100

    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    draw_midpointLine(-button_spacing + 50, button_y, -button_spacing - 30, button_y)
    draw_midpointLine(-button_spacing - 30, button_y - 10, -button_spacing - 50, button_y)
    draw_midpointLine(-button_spacing - 30, button_y + 10, -button_spacing - 50, button_y)
    draw_midpointLine(-button_spacing - 30, button_y - 10, -button_spacing - 30, button_y + 10)
    glEnd()

    glColor3f(1.0, 0.5, 0.0)
    glBegin(GL_POINTS)
    if paused:
        draw_midpointLine(-10, button_y + 20, -10, button_y - 20)
        draw_midpointLine(10, button_y + 20, 10, button_y - 20)
    else:
        draw_midpointLine(-10, button_y + 20, -10, button_y - 20)
        draw_midpointLine(-10, button_y - 20, 20, button_y)
        draw_midpointLine(20, button_y, -10, button_y + 20)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    draw_midpointLine(button_spacing - 20, button_y - 20, button_spacing + 20, button_y + 20)
    draw_midpointLine(button_spacing - 20, button_y + 20, button_spacing + 20, button_y - 20)
    glEnd()

def update(value):
    global dia_b, dia_a, dia_color, dia_speed, score, game_over

    if not game_over and not paused:
        dia_b -= dia_speed

        if (player_x - player_width // 2 < dia_a < player_x + player_width // 2 and
                player_y < dia_b < player_y + player_height):
            score += 1
            print(f"Score: {score}")
            reset_diamond()

        if dia_b < -win_height // 2:
            game_over = True
            print(f"Game Over! Final score: {score}")

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

def reset_diamond():
    global dia_a, dia_b, dia_color, dia_speed
    dia_a = random.randint(-win_width // 2 + 30, win_width // 2 - 30)
    dia_b = win_height // 2 - 30
    dia_color = (random.random(), random.random(), random.random())
    dia_speed += 0.4  

def reset_game():
    global player_x, dia_a, dia_b, dia_color, dia_speed, score, game_over, paused
    player_x = 0
    dia_a = random.randint(-win_width // 2 + 30, win_width // 2 - 30)
    dia_b = win_height // 2 - 30
    dia_color = (random.random(), random.random(), random.random())
    dia_speed = 3.5
    score = 0
    game_over = False
    paused = False
    print("Starting Over")

def keyboard(key, x, y):
    global player_x, paused, game_over

    if key == GLUT_KEY_LEFT and not game_over and not paused:  
        player_x = max(player_x - player_speed, -win_width // 2 + player_width // 2)
    elif key == GLUT_KEY_RIGHT and not game_over and not paused:  
        player_x = min(player_x + player_speed, win_width // 2 - player_width // 2)

def mouse(button, state, x, y):
    global paused, game_over

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gl_x = x - win_width // 2
        gl_y = win_height // 2 - y

        if -150 <= gl_x <= -50: 
            reset_game()
        elif -50 <= gl_x <= 50:  
            paused = not paused
        elif 50 <= gl_x <= 150:  
            print(f"Goodbye! Final score: {score}")
            glutLeaveMainLoop()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_buttons()
    draw_catcher()
    draw_diamond()
    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-win_width // 2, win_width // 2, -win_height // 2, win_height // 2)

def run():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(win_width, win_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Catch the Diamonds!")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(30, update, 0)
    glutMainLoop()

run()