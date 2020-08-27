from quaternion import quaternion
import array
def rotate(px,py,pz,ccAngleinDegree,axis_i,axis_j,axis_k):
    q=quaternion(ccAngleinDegree,axis_i,axis_j,axis_k)
    q.lsq()
    q_revert=quaternion(-ccAngleinDegree,axis_i,axis_j,axis_k)
    p=array.array('d',[px,py,pz])
    print("p=",p)
    pq=q*p
    print("pxq= ", pq)
    q_revert.lsq()
    p_new=pq*q_revert
    print("p_new=: ", p_new)
    return p_new
