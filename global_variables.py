from cubies import *
import math
#----plus or minus----
sign = lambda x: math.copysign(1, x)
#----it will be used in permutation, so the order matters----
all_cubies=(
    "FLU", "FU", "FUR",
    "FL", "F", "FR",
    "FLD", "FD", "FRD",
    "RU", "RUB", "R",
    "RB", "RD", "RBD",
    "UB", "UBL", "B",
    "BL", "BD", "BLD",
    "LU", "L", "LD",
    "U", "D"
    )
#-------------------------
##generate_cubies(to draw)_dict
def cubies_dict_generate(cubies=all_cubies):
    l=cubies
    if len(cubies)==0:
        cubies_dict={}
        return cubies_dict
    cubies_dict={}
    for i in range(len(l)):
        cubie_key=str(l[i])
        cubie_attr_value=cubie(cubie_key) #an obj in the cubie class
        cubies_dict.update({cubie_key:cubie_attr_value})
    return cubies_dict
cubies_currentstate_dict=cubies_dict_generate(all_cubies)
state_dict_stack=[]
total_transition_steps=int(0)

#--------the original mapping--------
#(F)ront_face:   
#    [0:FLU, 1:FU, 2:FUR]
#    [3:FL, 4:F, 5:FR]
#    [6:FLD, 7:FD, 8:FRD]
#(R)ight_face:
#    [2, 9:RU, 10:RUB]
#    [5, 11:R, 12:RB]
#    [8, 13:RD, 14:RBD]
#(B)ack_face:
#    [10, 15:UB, 16:UBL]
#    [12, 17:B, 18:BL]
#    [14, 19:BD, 20:BLD]
#(L)eft_face:
#    [16, 21:LU, 0]
#    [18, 22:L, 3]
#    [20, 23:LD, 6]
#(U)pper_face:
#    [16, 15, 10]
#    [21, 24:U, 9]
#    [0, 1, 2]
#(D)own_face:
#    [6, 7, 8]
#    [23, 25:D, 13]
#    [20, 19, 14]
#--------------------------------
#the initial mapping_dict={0:FUL, 1:FU, 2:FUR, 3:..., 25:D}, where {position_ID:cubie_ID}
current_location_permutation_mapping_dict=dict(zip(list(range(26)),all_cubies))

##generate the new partial dict for updating
##the result shall be part of the permutation_mapping_dict. {position_ID:cubie_ID,...}, e.g. {0:"UFR"}
def generate_new_cyclic_permutation_mapping_dict_partial(rotation_face, clockwise_rotation_degree, mapping_dict):
    #----6x2 permutation tuple dict----
    permutation_dict={
        'F':((0, 2, 8, 6), (1, 5, 7, 3)),
        'R':((2, 10, 14, 8), (9, 12, 13, 5)),
        'B':((10, 16, 20, 14), (15, 18, 19, 12)),
        'L':((16, 0, 6, 20), (21, 3, 23, 18)),
        'U':((16, 10, 2, 0), (15, 9, 1, 21)),
        'D':((6, 8, 14, 20), (7, 13, 19, 23))
    }
    #-----------------------------
    total_permutation_needed=int(round(clockwise_rotation_degree/90))
    new_dict_partial={}
    t=permutation_dict[rotation_face]
    for l in t: #e.g. l=(0, 2, 8, 6) then (1, 5, 7, 3) 
        for i in range(len(l)):
            #----j is the range(3) in l----
            j=i-total_permutation_needed
            while j > 3:
                j=j-4
            while j < 0:
                j=j+4
            #-----------------------------
            the_slot=l[i]
            new_cubiesID_in_the_slot_key=l[j]
            new_dict_partial.update({the_slot:mapping_dict[new_cubiesID_in_the_slot_key]})
#    global current_location_permutation_mapping_dict
#    print("parts before rotation:", current_location_permutation_mapping_dict.items(), "\n parts to be updated:", new_dict_partial.items())
    return new_dict_partial














