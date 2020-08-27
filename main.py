import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from cubies import *
import quarternion
import global_variables as g

#----draw_cubies----
#e.g. draw_cubie('DFL'), it process the cubies26_dict to OpenGL parameters 
def draw_cubies(cubies_dict):
    for key in cubies_dict:
        cubie_obj=cubies_dict[key]
        glBegin(GL_QUADS)
        for face_key in cubie_obj.faces_dict:
            face=cubie_obj.faces_dict[face_key] #e.g. (0,1,2,3)
            color=cubie_obj.faces_color_dict[face_key] #e.g. (1,0,0)
            glColor3fv(color)
            for vertex_index in face:
                glVertex3fv(cubie_obj.verticies_coordinateslist_list[vertex_index])
        glEnd()
        glBegin(GL_LINES)
        for edge in cubie_obj.edges_tuple:
            for vertex_index in edge:
                glColor3f(0,0,0) #black
                glVertex3fv(cubie_obj.verticies_coordinateslist_list[vertex_index])
        glEnd()
    return
#----select_cubies(the 9 cubies to rotate, from the total 26 cubies)----
#----use the mapping_dict {1:'UFR', 2:... 25:'D'} to perform the select----------
#----return 9 cubie_IDs ['UFR', 'R', ...]----
def select_cubies(
        key, mapping_dict = g.current_location_permutation_mapping_dict
        ):
    key = str(key) #e.g. 'U'
    cubies_selected = []
    cubies_leftovered = []
    ##---loop 26 times, the index represents 26 possible positions on the cube---
    for position_index in mapping_dict: 
        cubie_ID=mapping_dict[position_index]
        ##---use g.all_cubies[position_index] to find which "position_indexes" belong to which "face"---
        if key in g.all_cubies[position_index]: 
            cubies_selected.append(cubie_ID)
        else:
            cubies_leftovered.append(cubie_ID)
    return cubies_selected, cubies_leftovered

#----rotate: animation&coordinate_calculation----
def rotate(rotation_face, clockwise_rotation_degree, total_transition_steps):
    #push status to stack. size depends on the step, should be optimized----
    g.state_dict_stack.append(g.cubies_currentstate_dict)
    #---------------------------------------------
    rotation_face = str(rotation_face)
    cubies_selected, cubies_leftovered = select_cubies(rotation_face)
    total_transition_steps = float(total_transition_steps)
    cc_rotation_degree = -float(clockwise_rotation_degree)/total_transition_steps
    #----rotation_axis_ijk follows math's convention instead of OpenGL's. k axis points upwards----
    if rotation_face == "R":
        rotation_axis_ijk = (1, 0, 0)
    elif rotation_face == "L":
        rotation_axis_ijk = (-1, 0, 0)
    elif rotation_face == "U":
        rotation_axis_ijk = (0, 0, 1)
    elif rotation_face == "D":
        rotation_axis_ijk = (0, 0, -1)
    elif rotation_face == "F":
        rotation_axis_ijk = (0, -1, 0)
    elif rotation_face == "B":
        rotation_axis_ijk = (0, 1, 0)
    ##----calculate next coordinates using quarternion----
    ##----Can be Optimized using a middle point and 8 calculations----
    for cubie in cubies_selected:
        t = g.cubies_currentstate_dict[cubie].verticies_coordinateslist_list
        for i in range(len(t)): #e.g. [-1.5, -1.5, -1.5]=t[i]
            p_new = quarternion.qtcal(cc_rotation_degree, rotation_axis_ijk[0], rotation_axis_ijk[1], rotation_axis_ijk[2], t[i][0], t[i][1], t[i][2]) #e.g. p_new=[1,0,1]
            g.cubies_currentstate_dict[cubie].verticies_coordinateslist_list[i]=p_new
    return
#----py_game&OpenGL_init----
def init_gl_stuff(display):
    glEnable(GL_DEPTH_TEST)        #use pygame zbuffer

    aspect_ratio=display[0]/display[1]
    field_of_view_Angle=60
    zNear=0.1
    zFar=100
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(field_of_view_Angle, aspect_ratio,zNear,zFar)

#----main----
def main():
    transitioning = False
    total_transition_steps = 4 
    #--------------------------
    pygame.init()
    display = (1080,720)
    displayCenter = [display[0]/2, display[1]/2]
    isfullscreen = False
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    init_gl_stuff(display)
    #------init&configure camera, tweak the camera location using mouse later.---- 
    #------Use the OpenGL xyz axises here.----------------------
    #------Wanted to use gluLookAt to implement 3rd person perspective but it seems buggy, i.e. idk how to adjust the camera inside the while loop down below. But it is more of a library thing, so I decided to use glRotatef for now(in the mouse section).
    camera_x, camera_y, camera_z = 0, -4, 2
    gluLookAt(camera_x, camera_y, camera_z, 0,0,0, 0,0,1)
    glRotatef(-15, 0, 0, 1)
    while True:
        if transitioning:
            if rotation_remain > 0:
                rotate(rotation_face, clockwise_rotation_degree, total_transition_steps)
                rotation_remain -= 1
            else:
                print("Rotated ", rotation_face, clockwise_rotation_degree, "degree clockwise." )
                new_dict_partial = g.generate_new_cyclic_permutation_mapping_dict_partial(rotation_face, clockwise_rotation_degree, g.current_location_permutation_mapping_dict)
                transitioning = False
                g.current_location_permutation_mapping_dict.update(new_dict_partial)

        #clear screen and move camera
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_cubies(g.cubies_currentstate_dict)
        mouseMove = pygame.mouse.get_rel()

        if not transitioning:
            rotation_remain = total_transition_steps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                ##----mouse_click->view adjustion----
                elif pygame.mouse.get_pressed()[0]:
                    #mousePos = pygame.mouse.get_pos()
                    #delta = [mousePos[0]-displayCenter[0], mousePos[1]-displayCenter[1]]
                    mouseMove = pygame.mouse.get_rel()
                    glRotatef(mouseMove[0]*0.1, 0,0,1)
                    glRotatef(mouseMove[1]*0.1, 1,0,0)
                ##-----------------------------------    
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_0:
                        if isfullscreen == False:
                            print("Changing to FULLSCREEN")
                            pygame.display.set_mode(display, OPENGL | DOUBLEBUF | FULLSCREEN)
                            displayCenter = [display[0]/2, display[1]/2]
                            isfullscreen = True
                        else:
                            print("Changing to windowed mode")
                            pygame.display.set_mode(display, OPENGL | DOUBLEBUF)
                            displayCenter = [display[0]/2, display[1]/2]
                            isfullscreen = False
                        init_gl_stuff(display)
                    ##----press shift+r for R', r for R----
                    if event.key == pygame.K_r:
                        rotation_face = "R"
                        if event.mod & pygame.KMOD_SHIFT:
                            clockwise_rotation_degree = -90
                            transitioning = True
                        else:
                            clockwise_rotation_degree = 90
                            transitioning = True
                    elif event.key == pygame.K_l:
                        rotation_face = "L"
                        if event.mod & pygame.KMOD_SHIFT:
                            clockwise_rotation_degree = -90
                            transitioning = True
                        else:
                            clockwise_rotation_degree = 90
                            transitioning = True
                    elif event.key == pygame.K_u:
                        rotation_face = "U"
                        if event.mod & pygame.KMOD_SHIFT:
                            clockwise_rotation_degree = -90
                            transitioning = True
                        else:
                            clockwise_rotation_degree = 90
                            transitioning = True
                    elif event.key == pygame.K_d:
                        rotation_face = "D"
                        if event.mod & pygame.KMOD_SHIFT:
                            clockwise_rotation_degree = -90
                            transitioning = True
                        else:
                            clockwise_rotation_degree = 90
                            transitioning = True
                    elif event.key == pygame.K_f:
                        rotation_face = "F"
                        if event.mod & pygame.KMOD_SHIFT:
                            clockwise_rotation_degree = -90
                            transitioning = True
                        else:
                            clockwise_rotation_degree = 90
                            transitioning = True
                    elif event.key == pygame.K_b:
                        rotation_face = "B"
                        if event.mod & pygame.KMOD_SHIFT:
                            clockwise_rotation_degree = -90
                            transitioning = True
                        else:
                            clockwise_rotation_degree = 90
                            transitioning = True
        #------
        pygame.display.flip()
        pygame.time.wait(10)
main()
