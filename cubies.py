#--------------------
#The cubie class. Generate (26) cubie objects for 3D Graphical rendering
#--------------------
import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

EdgeLength_of_the_cubie=0.5
l=EdgeLength_of_the_cubie/2
#define vertices from D to U, F to B, L to R
verticies_default=(
        (-l,-l,-l), (l,-l,-l),
        (l,l,-l), (-l,l,-l),
        (-l,-l,l), (l,-l,l),
        (l,l,l), (-l,l,l),
    )
faces_default_dict={
        'D':(0,1,2,3), 'U':(4,5,6,7),
        'F':(0,1,5,4), 'B':(3,2,6,7),
        'L':(0,3,7,4), 'R':(1,2,6,5)
    }
colors_dict={
        'D':(1, 1, 0.8), 'U':(0.7, 1, 0.2),
        'F':(0.2, 0.7, 0.2), 'B':(0.1, 0.3, 1),
        'L':(0.7, 0.1, 0), 'R':(0.9, 0.5, 0)
    }
edges_default=(
        (0,1), (0,3),
        (0,4), (2,1),
        (2,3), (2,6),
        (5,1), (5,4),
        (5,6), (7,3),
        (7,4), (7,6)
    )
#---------------------
#a=cubie("UFR") -> the UFR cubie object
#-----------------------
class cubie:
    def __init__(self,pos): #pos=a string, "UFR" or "F" or "DB" .etc, see wiki notation.
        pos=str(pos)
        color_of_the_faces_dict={}
        defaultColor=(0.5,0.5,0.5)   #GL RGB gray
        for face in faces_default_dict: 
            #all faces default gray
            color_of_the_faces_dict.update({face:defaultColor})
        for outsideface in pos:
            #paint cubies outside face
            color_of_the_faces_dict.update({outsideface:colors_dict[outsideface]})

        #calculate one dimentional drift of, e.g. "U" "F" "R", then sum up
        drift_cases={
                'D':(0,0,-2*l), 'U':(0,0,2*l),
                'F':(0,-2*l,0), 'B':(0,2*l,0),
                'L':(-2*l,0,0), 'R':(2*l,0,0)
                }
        coordinates_drift=(0,0,0)   #initialize
        for key in pos:
            one_dimensional_drift=drift_cases.get(key)
            coordinates_drift=list(map(sum,zip(coordinates_drift, one_dimensional_drift)))
        verticies_cubie=list(verticies_default)
        for i in range(len(verticies_cubie)):
            verticies_cubie[i]=list(map(sum,zip(verticies_cubie[i],coordinates_drift)))

        self.faces_dict=faces_default_dict
        self.faces_color_dict=color_of_the_faces_dict
        self.center_coordinates_list=coordinates_drift
        self.verticies_coordinateslist_list=list(verticies_cubie)
        self.edges_tuple=edges_default
#------------------------
#generate the cubies (now in main.py)
#------------------------
#def cubies_generate():
#    l=(
#        "DFL", "DF", "DFR",
#        "FL", "F", "FR",
#        "UFL", "UF", "UFR",
#        "DR", "R", "UR",
#        "DRB", "RB", "URB",
#        "DL", "L", "UL",
#        "DLB", "LB", "ULB",
#        "DB", "B", "UB",
#        "D", "U"
#        )
#    cubies26_dict={}
#    for i in range(len(l)):
#        cubie_key=str(l[i])
#        cubie_attr_value=cubie(cubie_key) #an obj in the cubie class
#        cubies26_dict.update({cubie_key:cubie_attr_value})
#    return cubies26_dict
#
#cubies26_dict=cubies_generate()
#
#Sample Output:
#t=cubies26_dict
#>>> t['DFL'].verticies_coordinateslist_tuple
#([-1.5, -1.5, -1.5], [-0.5, -1.5, -1.5], [-0.5, -0.5, -1.5], [-1.5, -0.5, -1.5], [-1.5, -1.5, -0.5], [-0.5, -1.5, -0.5], [-0.5, -0.5, -0.5], [-1.5, -0.5, -0.5])
#>>> t['DFL'].edges_tuple
#((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 6), (5, 1), (5, 4), (5, 6), (7, 3), (7, 4), (7, 6))
#>>> t['DFL'].faces_dict
#{'D': (0, 1, 2, 3), 'U': (4, 5, 6, 7), 'F': (0, 1, 5, 4), 'B': (3, 2, 6, 7), 'L': (0, 3, 7, 4), 'R': (1, 2, 6, 5)}
#>>> t['DFL'].faces_color_dict
#{'D': (1, 0, 0), 'U': (0.5, 0.5, 0.5), 'F': (0, 0, 1), 'B': (0.5, 0.5, 0.5), 'L': (1, 0, 1), 'R': (0.5, 0.5, 0.5)}
#>>> t['DFL'].center_coordinates_list
#[-1.0, -1.0, -1.0]
