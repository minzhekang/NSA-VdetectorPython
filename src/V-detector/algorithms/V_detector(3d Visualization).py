from mayavi import mlab
import numpy as np
import random
import math

r = 0.02
Nself =500
self_radius = [r for i in range(Nself)]
xx = []
yy = []
zz = []
for i in range(Nself):
    x=1/3+random.random()/3
    y=1/3+random.random()/3
    z=1/3+random.random()/3
    xx.append(x)
    yy.append(y)
    zz.append(z)

teller = 0
N=5
x_detect = []
y_detect = []
z_detect = []
radius_detect = []
while teller<N:
    u1=random.random()
    u2=random.random()
    u3=random.random()
    ss=[x for x in range(Nself)]
    for j in range(Nself):
        ss[j]=(math.sqrt(math.pow(xx[j]-u1,2)+math.pow(yy[j]-u2,2)+math.pow(zz[j]-u3,2)))
    dmin=np.min(ss)
    if dmin>(r):
        x_detect.append(u1)
        y_detect.append(u2)
        z_detect.append(u3)
        radius_detect.append(dmin-r)
        teller += 1
        mlab.points3d(u1, u2, u3, dmin-r ,  color = (0.7,0,0), scale_factor = 1)

mlab.points3d(xx, yy, zz,self_radius,  color = (0.2,1,0), scale_factor = 1)

mlab.show()