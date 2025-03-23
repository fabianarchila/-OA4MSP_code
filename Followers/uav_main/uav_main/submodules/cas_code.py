import numpy as np


def inside_cone(pe,ps,pb):

    c_se=np.cross(ps,pe)
    c_sb=np.cross(ps,pb)
    c_be=np.cross(pb,pe)
    c_eb=np.cross(pe,pb)
    c_bs=np.cross(pb,ps)
   
    inside=False
    if c_se>=0:
        if c_sb>=0 and c_be>=0:
            
            ide=True
    else:
        if (c_eb>=0 and c_bs>=0):
            inside=True
    return inside

def rotate(angle):
    matrix=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    return matrix

def forces_zonas(current_pos,goal, obstacle,zonas):
    Ft=np.zeros([1,2])
    k_eta1=1
    k_eta2=2
    k_eta3=2
    r=4
    r2=8
    

    alpha=np.arctan2((goal[1]-obstacle[1]),(goal[0]-obstacle[0]))
    
    point_t1=np.dot(rotate(alpha),np.array([r,0]))+obstacle
    x_p=point_t1[0]
    y_p=point_t1[1]
    
    p1=np.dot([x_p-obstacle[0],y_p-obstacle[1]],rotate(np.pi/2))+obstacle
    p2=np.dot([x_p-obstacle[0],y_p-obstacle[1]],rotate(-np.pi/2))+obstacle


    r3=6
    p3=(p1-obstacle)*r3+obstacle

    r4=6
    p4=(p2-obstacle)*r4+obstacle
    #print(p4)
    if zonas==1:
        Ft=k_eta2*(p3-current_pos)
    elif zonas==2:
        Ft=k_eta2*(p4-current_pos)
    elif zonas==3:
        Ft=-k_eta3*(obstacle-current_pos)
        # dist=np.sqrt((obstacle[0]-current_pos[0])**2+(obstacle[1]-current_pos[1])**2)
        # ro=0.8
        # Ft=6*k_eta3*( (1/dist)-1/ro )*(1/dist**2)*(obstacle-current_pos)
        # print(Ft)
    elif zonas==0:
        Ft=k_eta1*(goal-current_pos)

    return Ft



def zonas(current_pos,goal, obstacle):
    zona=0

    r=4
    r2=8
    d=np.sqrt((goal[0]-obstacle[0])**2+(goal[1]-obstacle[1])**2)
    
    
    alpha=np.arctan2((goal[1]-obstacle[1]),(goal[0]-obstacle[0]))
    angle=np.arccos(r/d)

    delta=0.05

    point_t1=np.dot(rotate(alpha),np.array([r,0]))+obstacle
    x_p=point_t1[0]
    y_p=point_t1[1]
    
    p1=np.dot([x_p-obstacle[0],y_p-obstacle[1]],rotate(np.pi/2))+obstacle
    p2=np.dot([x_p-obstacle[0],y_p-obstacle[1]],rotate(-np.pi/2))+obstacle

    p_circle1=np.dot(np.array([r*np.cos(angle),r*np.sin(angle)]),rotate(-alpha))+obstacle
    p_circle2=np.dot(np.array([r*np.cos(angle),-r*np.sin(angle)]),rotate(-alpha))+obstacle

    r3=3
    p3=(p1-obstacle)*r3+obstacle

    r4=3
    p4=(p2-obstacle)*r4+obstacle


    if inside_cone(p_circle1-goal,obstacle-goal,np.array([current_pos[0],current_pos[1]])-goal) and np.sqrt((current_pos[0]-obstacle[0])**2+(current_pos[1]-obstacle[1])**2  )<r2 and np.sqrt((current_pos[0]-obstacle[0])**2+(current_pos[1]-obstacle[1])**2  )>r and inside_cone(p2-obstacle,np.dot(goal-obstacle,rotate(np.pi)),np.array([current_pos[0],current_pos[1]])-obstacle):
        zona=2
        
    elif inside_cone(obstacle-goal,p_circle2-goal,np.array([current_pos[0],current_pos[1]])-goal) and np.sqrt((current_pos[0]-obstacle[0])**2+(current_pos[1]-obstacle[1])**2  )<r2 and np.sqrt((current_pos[0]-obstacle[0])**2+(current_pos[1]-obstacle[1])**2  )>r and inside_cone(np.dot(goal-obstacle,rotate(np.pi)),p1-obstacle,np.array([current_pos[0],current_pos[1]])-obstacle):
        zona=1

    elif np.sqrt((current_pos[0]-obstacle[0])**2+(current_pos[1]-obstacle[1])**2  )<=r:
        zona=3

    else:
        zona=0
    return zona