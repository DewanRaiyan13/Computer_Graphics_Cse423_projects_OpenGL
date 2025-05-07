from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Camera-related variables
camera_pos = [0, 500, 500]  
camera_angle = 90 
rad = 500  
cam_z = 500
plyr_rotation = 0
plyr_life = 5
miss = 0
plyr_pos = [0, 0, 0]
score = 0

bullet_list = []
bullet_speed = 10
fovY = 120
GRID_LENGTH = 600
rand_var = 423
enemy_list = []
time = 0.0

enemy_speed = 0.1
game_over = False
first_person_mode = False

cheat_mode = False
cheat_vision = False
cheat_shoot_cooldown = 0

tile_size = 80
grid_count = 13
boun_size = (tile_size * grid_count) / 2 
boun_min = -boun_size
boun_max =  boun_size  


def reset_enemies():
    global enemy_list
    enemy_list = []
    for i in range(5):
        x = random.uniform(boun_min, boun_max)
        y = random.uniform(boun_min, boun_max)
        z = 50
        enemy_list.append([x, y, z])
reset_enemies()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    initial_x = 600
    initial_y = 600
    GRID_x = initial_x
    GRID_y = initial_y
    length = (initial_x + initial_y) / 13
    color = True
    glBegin(GL_QUADS)
    for i in range(13):
        for j in range(13):
            if not color:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1, 1, 1)
            glVertex3f(-GRID_x, GRID_y, 0)
            glVertex3f(-GRID_x + length, GRID_y, 0)
            glVertex3f(-GRID_x + length, GRID_y - length, 0)
            glVertex3f(-GRID_x, GRID_y - length, 0)
            GRID_x -= length
            color = not color
        GRID_x = initial_x
        GRID_y -= length
    glEnd()
    glBegin(GL_QUADS)
    glColor3f(0, 1, 0)
    glVertex3f(-initial_x, initial_y, 0)
    glVertex3f(-initial_x, initial_y - (13 * length), 0)
    glVertex3f(-initial_x, initial_y - (13 * length), 100)
    glVertex3f(-initial_x, initial_y, 100)
    glColor3f(0, 0, 1)
    glVertex3f(initial_x, initial_y, 0)
    glVertex3f(initial_x, initial_y - (13 * length), 0)
    glVertex3f(initial_x, initial_y - (13 * length), 100)
    glVertex3f(initial_x, initial_y, 100)
    glColor3f(67/255, 234/255, 240/255)
    glVertex3f(-initial_x, initial_y - (13 * length), 0)
    glVertex3f(-initial_x + (13 * length), initial_y - (13 * length), 0)
    glVertex3f(-initial_x + (13 * length), initial_y - (13 * length), 100)
    glVertex3f(-initial_x, initial_y - (13 * length), 100)
    glColor3f(1, 1, 1)
    glVertex3f(-initial_x, initial_y, 0)
    glVertex3f(-initial_x + (13 * length), initial_y, 0)
    glVertex3f(-initial_x + (13 * length), initial_y, 100)
    glVertex3f(-initial_x, initial_y, 100)
    glEnd()

def draw_bullets(x, y, z):
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(x, y, z)
    glutSolidCube(5)
    glPopMatrix()

def draw_enemies(x, y, z, pulse_scale):
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(x, y, z)
    glScalef(pulse_scale, pulse_scale, pulse_scale)
    gluSphere(gluNewQuadric(), 50, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(x, y, z + 25)
    glScalef(pulse_scale, pulse_scale, pulse_scale)
    gluSphere(gluNewQuadric(), 20, 10, 10)
    glPopMatrix()

def draw_player():
    global plyr_pos, plyr_rotation, game_over, plyr_life
    x, y, z = plyr_pos
    glPushMatrix()
    glTranslatef(x, y, z)
    glTranslatef(-46.1538462, 46.1538462, 0)
    glRotatef(plyr_rotation, 0, 0, 1)
    if game_over:
        glRotatef(-90, 1, 0, 0)
    glPushMatrix()
    glColor3f(50/255, 168/255, 82/255)
    glTranslatef(0, 0, 50)
    glScalef(0.7, 0.4, 1)
    glutSolidCube(50)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(10, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-10, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(247/255, 230/255, 190/255)
    glTranslatef(18, -10, 65)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 20, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(247/255, 230/255, 190/255)
    glTranslatef(-18, -10, 65)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 20, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(191/255, 191/255, 191/255)
    glTranslatef(0, -10, 65)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 35, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 85)
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()
    glPopMatrix()

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global plyr_pos, plyr_rotation, plyr_life, miss, score, game_over, cheat_mode, cheat_vision, bullet_list
    ax, ay, az = plyr_pos
    speed = 15
    angle_rad = math.radians(plyr_rotation)
    x_new, y_new = ax, ay
    # # Move forward (W key)
    if key == b'w' and not game_over:
        x_new += speed * math.sin(angle_rad)
        y_new -= speed * math.cos(angle_rad)
    # # Move backward (S key)
    if key == b's' and not game_over:
        x_new -= speed * math.sin(angle_rad)
        y_new += speed * math.cos(angle_rad)
    # # Rotate gun left (A key)
    if key == b'a' and not game_over:
        plyr_rotation += 5
    # # Rotate gun right (D key)
    if key == b'd' and not game_over:
        plyr_rotation -= 5
    x_new = max(boun_min, min(boun_max, x_new))
    y_new = max(boun_min, min(boun_max, y_new))
    plyr_pos[0], plyr_pos[1] = x_new, y_new
    # # Toggle cheat mode (C key)
    if key == b'c':
        cheat_mode = not cheat_mode
        if not cheat_mode:
            cheat_vision = False
    # # Toggle cheat vision (V key)
    if key == b'v' and cheat_mode and first_person_mode:
        cheat_vision = not cheat_vision
    # # Reset the game if R key is pressed
    if key == b'r' and game_over:
        plyr_pos[:] = [0, 0, 0]
        plyr_rotation = 0
        plyr_life = 5
        miss = 0
        score = 0
        reset_enemies()
        bullet_list.clear()
        game_over = False
        cheat_mode = False
        cheat_vision = False

def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, camera_angle, cam_z
    if not first_person_mode:
        # Move camera up (UP arrow key)
        if key == GLUT_KEY_UP and cam_z < 1000:
            cam_z += 10
        # # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN and cam_z > 10:
            cam_z -= 10
        # moving camera left (LEFT arrow key)
        if key == GLUT_KEY_LEFT:
            camera_angle += 2.86  # Approx 0.05 radians
        # moving camera right (RIGHT arrow key)
        if key == GLUT_KEY_RIGHT:
            camera_angle -= 2.86
        camera_pos[0] = rad * math.cos(math.radians(camera_angle))
        camera_pos[1] = rad * math.sin(math.radians(camera_angle))
        camera_pos[2] = cam_z

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    global first_person_mode, plyr_pos, plyr_rotation, bullet_list, game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        ax, ay, az = plyr_pos
        bullet_x = ax - 46.1538462 - (-60) * math.sin(math.radians(plyr_rotation))
        bullet_y = ay + 46.1538462 + (-60) * math.cos(math.radians(plyr_rotation))
        bullet_z = az + 65
        x_dir = math.sin(math.radians(plyr_rotation))
        y_dir = -math.cos(math.radians(plyr_rotation))
        bullet_list.append([bullet_x, bullet_y, bullet_z, x_dir, y_dir])
        print("Player Bullet Fired!")
    # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix
    # Extract camera position and look-at target
    if not first_person_mode:
        x, y, z = camera_pos
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                  0, 0, 0,  # Look-at target
                  0, 0, 1)  # Up vector (z-axis)
    else:
        ax, ay, az = plyr_pos
        x = ax - 46.1538462
        y = ay + 46.1538462
        theta = math.radians(plyr_rotation)
        forward_x = math.sin(theta)
        forward_y = -math.cos(theta)
        if cheat_mode and cheat_vision:
            distance = 200
            gluLookAt(x, y - 5, az + 100, x + forward_x * distance, y + forward_y * distance, az + 100, 0, 0, 1)
        elif cheat_mode and not cheat_vision:
            gluLookAt(x, y - 5, az + 100, x, y - 50, az + 100, 0, 0, 1)
        else:
            distance = 50
            gluLookAt(x, y - 5, az + 100, x + forward_x * distance, y + forward_y * distance, az + 100, 0, 0, 1)

def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    global plyr_life, time, enemy_list, bullet_speed, miss, bullet_list, plyr_pos, enemy_speed, score, game_over, cheat_mode, cheat_shoot_cooldown, plyr_rotation
    if game_over:
        glutPostRedisplay()
        return
    enemy_hit = 50
    player_hit = 10
    time += 0.02
    GRID_LIMIT = 600
    new_bullet_list = []
    temp_enemy_list1 = enemy_list[:]
    for bullet in bullet_list:
        x, y, z, dir_x, dir_y = bullet
        x += dir_x * bullet_speed
        y += dir_y * bullet_speed
        bullet_hit = False
        for enemy in temp_enemy_list1[:]:
            bx, by, bz = enemy
            dis = math.sqrt((x - bx) ** 2 + (y - by) ** 2)
            if dis <= enemy_hit:
                temp_enemy_list1.remove(enemy)
                bullet_hit = True
                score += 1
                new_x = random.uniform(boun_min, boun_max)
                new_y = random.uniform(boun_min, boun_max)
                temp_enemy_list1.append([new_x, new_y, 50])
                break
        if not bullet_hit and -GRID_LIMIT <= x <= GRID_LIMIT and -GRID_LIMIT <= y <= GRID_LIMIT:
            new_bullet_list.append([x, y, z, dir_x, dir_y])
        elif not bullet_hit:
            miss += 1
            print(f"Bullet Missed: {miss}")
    bullet_list[:] = new_bullet_list
    enemy_list[:] = temp_enemy_list1
    ax, ay, _ = plyr_pos
    new_enemy_list = []
    for enemy in enemy_list:
        bx, by, bz = enemy
        dis = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
        if dis > player_hit:
            dx = ax - bx
            dy = ay - by
            if dis > 0:
                dir_x = dx / dis
                dir_y = dy / dis
                bx += dir_x * enemy_speed
                by += dir_y * enemy_speed
                bx = max(boun_min, min(boun_max, bx))
                by = max(boun_min, min(boun_max, by))
                new_enemy_list.append([bx, by, bz])
        else:
            new_x = random.uniform(boun_min, boun_max)
            new_y = random.uniform(boun_min, boun_max)
            new_enemy_list.append([new_x, new_y, 50])
            plyr_life -= 1
            print(f"Remaining Player Life: {plyr_life}")
    enemy_list[:] = new_enemy_list
    if miss >= 10 or plyr_life <= 0:
        game_over = True
        print("Game Over!")
    if cheat_mode and not game_over:
        plyr_rotation = (plyr_rotation + 3) % 360
        if cheat_shoot_cooldown <= 0:
            ax, ay, az = plyr_pos
            gun_x = ax - 46.1538462 - (-60) * math.sin(math.radians(plyr_rotation))
            gun_y = ay + 46.1538462 + (-60) * math.cos(math.radians(plyr_rotation))
            gun_z = az + 65
            facing_x = math.sin(math.radians(plyr_rotation))
            facing_y = -math.cos(math.radians(plyr_rotation))
            for enemy in enemy_list:
                bx, by, bz = enemy
                to_enemy_x = bx - gun_x
                to_enemy_y = by - gun_y
                dis = math.hypot(to_enemy_x, to_enemy_y)
                if dis == 0:
                    continue
                to_enemy_x /= dis
                to_enemy_y /= dis
                dot = facing_x * to_enemy_x + facing_y * to_enemy_y
                angle = math.degrees(math.acos(max(-1.0, min(1.0, dot))))
                if angle <= 10:
                    bullet_list.append([gun_x, gun_y, gun_z, to_enemy_x, to_enemy_y])
                    print("Player Bullet Fired!")
                    cheat_shoot_cooldown = 0.15
                    break
        else:
            cheat_shoot_cooldown -= 0.02
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size
    setupCamera()  # Configure camera perspective
    draw_grid()
    draw_text(10, 770, f"Game Score: {score}")
    draw_text(10, 740, f"Player Life remaining: {plyr_life}")
    draw_text(10, 710, f"Player bullet Missed: {miss}")
    if game_over:
        draw_text(10, 680, f"GAME OVER! Your Score is: {score}", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 650, 'Press "R" to Restart', GLUT_BITMAP_HELVETICA_18)
    draw_player()
    for b in bullet_list:
        draw_bullets(b[0], b[1], b[2])
    pulse_scale = 0.8 + 0.3 * math.sin(2.0 * time)
    for enemy in enemy_list:
        draw_enemies(enemy[0], enemy[1], enemy[2], pulse_scale)
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()

def main():
    """
    Main function to set up OpenGL window and loop
    """
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    glutCreateWindow(b"3D Bullet Frenzy")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    glEnable(GL_DEPTH_TEST)
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()