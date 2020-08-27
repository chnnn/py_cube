#----------------
#The quaternion calculator. 
#Used in generating custom 3D animation.
#Input a 3D starting point, as well as rotation axises and rotation degree.
#Output the point's rotation result.
#The calculation follows this logic: p_new=qxpxq_revert. where q is the "rotation" represented in quaternion, and p is the point to rotate. p shall be an 1x3 array, p=array.array('d',[i,j,k])
#----------------
import math
import array
class quaternion:
    def __init__(self,CounterclockRotationAngleinDegree,axis_i,axis_j,axis_k):
        self.theta=math.radians(CounterclockRotationAngleinDegree/2)
        normalization_constant=math.sqrt(axis_i**2+axis_j**2+axis_k**2)
        self.a=float(math.cos(self.theta))
        self.b=float(math.sin(self.theta)*axis_i/normalization_constant)
        self.c=float(math.sin(self.theta)*axis_j/normalization_constant)
        self.d=float(math.sin(self.theta)*axis_k/normalization_constant)
    def lsq(self):
        print("q.{a-d}", self.a,self.b,self.c,self.d)
    def __mul__(self,other): 
        if hasattr(other, "__len__"):
            if 3==len(other):
                a1=self.a
                b1=self.b
                c1=self.c
                d1=self.d
                a2=0
                b2=other[0]
                c2=other[1]
                d2=other[2]
                H=HamiltonProduct(a1,b1,c1,d1,a2,b2,c2,d2)
                return H
            if 4==len(other):
                a1=self.a
                b1=self.b
                c1=self.c
                d1=self.d
                a2=other[0]
                b2=other[1]
                c2=other[2]
                d2=other[3]
                H=HamiltonProduct(a1,b1,c1,d1,a2,b2,c2,d2)
                return H
    def __rmul__(self,other):
        if hasattr(other, "__len__"):
            if 3==len(other):
                a2=self.a
                b2=self.b
                c2=self.c
                d2=self.d
                a1=0
                b1=other[0]
                c1=other[1]
                d1=other[2]
                H=HamiltonProduct(a1,b1,c1,d1,a2,b2,c2,d2)
                return H
            if 4==len(other):
                a2=self.a
                b2=self.b
                c2=self.c
                d2=self.d
                a1=other[0]
                b1=other[1]
                c1=other[2]
                d1=other[3]
                H=HamiltonProduct(a1,b1,c1,d1,a2,b2,c2,d2)
                return H

def HamiltonProduct(a1,b1,c1,d1,a2,b2,c2,d2):
    H=array.array('d', [a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2, a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2])
    return H
def qtcal(ccRotationinDegree, axis_i, axis_j, axis_k, p_i, p_j, p_k):
    q=quaternion(ccRotationinDegree,axis_i,axis_j,axis_k)
    q_revert=quaternion(-ccRotationinDegree,axis_i,axis_j,axis_k)
    p=array.array('d',[p_i,p_j,p_k])
    p_new=q*p*q_revert
    p_new=list(p_new)
    p_new.pop(0)
    return p_new
    
def getInputs():
    degree=float(input("Counter-Clockwise-Rotation-Angle in degree: "))
    axis_i=float(input("Rotation axis i value: "))
    axis_j=float(input("Rotation axis j value: "))
    axis_k=float(input("Rotation axis k value: "))
    p_i=float(input("Point to Rotate i value: "))
    p_j=float(input("Point to Rotate j value: "))
    p_k=float(input("Point to Rotate k value: "))
    return degree, axis_i, axis_j, axis_k, p_i, p_j, p_k
def main():
    ccRotationinDegree, axis_i, axis_j, axis_k, p_i, p_j, p_k = getInputs()
    q=quaternion(ccRotationinDegree,axis_i,axis_j,axis_k)
    q_revert=quaternion(-ccRotationinDegree,axis_i,axis_j,axis_k)
    p=array.array('d',[p_i,p_j,p_k])
    p_new=q*p*q_revert
    #print("p_new=: ", p_new[1],"i, ",p_new[2],"j, ",p_new[3],"k")
    print("p_new=: ", "{0:.2f}".format(p_new[1]), "i, ", "{0:.2f}".format(p_new[2]), "j, ", "{0:.2f}".format(p_new[2]), "k")
    return
#main()
