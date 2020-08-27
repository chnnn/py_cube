#Partially referended/modiedfied from the pygames's example code and OpenGL example code. 
import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

EdgeLength_of_the_Regular_Hexahedron=1 
l=EdgeLength_of_the_Regular_Hexahedron/2
#define vertices from D to U, F to B, L to R
verticies=(
        (-l,-l,-l), (l,-l,-l),
        (l,l,-l), (-l,l,-l),
        (-l,-l,l), (l,-l,l),
        (l,l,l), (-l,l,l),
    )
edges=(
        (0,1), (0,3),
        (0,4), (2,1),
        (2,3), (2,6),
        (5,1), (5,4),
        (5,6), (7,3),
        (7,4), (7,6)
    )
##D U F B L R
faces=(
        (0,1,2,3), (4,5,6,7),
        (0,1,5,4), (3,2,6,7),
        (0,3,7,4), (1,2,6,5)
    )
colors=(
        (1,0,0), (0,1,0),
        (0,0,1), (1,1,0),
        (1,0,1), (0,1,1)
    )

def cubies():
    glBegin(GL_QUADS)
    faces_and_colors=list(zip(faces, colors))
    for face_and_color in faces_and_colors:
        color=face_and_color[1]
        face=face_and_color[0]
        glColor3fv(color)
        for vertex_index in face:
            glVertex3fv(verticies[vertex_index])
    glEnd()
    glBegin(GL_LINES)
    for edge in edges:
        for vertex_index in edge:
            glColor3f(0,0,0)
            glVertex3fv(verticies[vertex_index])
    glEnd()

def init_gl_stuff(display):
    glEnable(GL_DEPTH_TEST)        #use pygame zbuffer

    aspect_ratio=display[0]/display[1]
    field_of_view_Angle=60
    zNear=0.1
    zFar=100
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(field_of_view_Angle, aspect_ratio,zNear,zFar)
    glTranslatef(0.0, 0.0, -3.0)                 #object move away from the screen
    glRotatef(25, 1, 1, 0)                       #object rotate cc 25 deg around (1,1,0)
    gluLookAt(-1,0.1,0, 0,0,-3, 0,1,0)           #cameramove left

def main():
    pygame.init()
    display=(800,600)
    isfullscreen=False
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    init_gl_stuff(display)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_f:
                    if isfullscreen==False:
                        print("Changing to FULLSCREEN")
                        pygame.display.set_mode(display, OPENGL | DOUBLEBUF | FULLSCREEN)
                        isfullscreen=True
                    else:
                        print("Changing to windowed mode")
                        pygame.display.set_mode(display, OPENGL | DOUBLEBUF)
                        isfullscreen=False
                    init_gl_stuff(display)

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #orbit camera around by 1 degree
        glRotatef(1, 1, 1, 1)
        cubies()
        pygame.display.flip()
        pygame.time.wait(10)
       
main()
