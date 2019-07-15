import matplotlib.animation as animation
from scipy.integrate import odeint
from numpy import arange
from pylab import *
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Ellipse

fig, ax = plt.subplots()
#fig = figure()
xlabel('x')
ylabel('y')
z=8
#circ = Ellipse((0.5, 0.5),width=0.75/z, height=1/z,edgecolor='black',facecolor='white')
Nself=500
s=[x for x in range(Nself)]
#print(s)
r=0.02
for i in range(Nself):
    x=1/3+random.random()/3
    y=1/3+random.random()/3
    s[i]=[x,y]
    circ = Circle((x,y),radius=r,edgecolor='black',facecolor='grey')
    ax.add_patch(circ)
N=100 #the number of constructed detectors
teller=0
D=[x for x in range(N)]
while teller < N:
    u1=random.random()
    u2=random.random()
    ss=[x for x in range(Nself)]
    #ss[k]=[u1,u2]
    for j in range(Nself):
        ss[j]=(sqrt(math.pow(s[j][0]-u1,2)+math.pow(s[j][1]-u2,2)))
    dmin=np.min(ss)
    #print("Min = ",dmin)
    if (dmin > r):
        circ = Circle((u1, u2), radius=dmin-r, edgecolor='black', facecolor='lightgreen')
        ax.add_patch(circ)
        D[teller]=[u1,u2,dmin-r]
        teller=teller+1

ax.xaxis.label.set_size(20)
ax.yaxis.label.set_size(20)

ax.set_xticks([])
ax.set_yticks([])
#ax.axes.get_xaxis().set_visible(False)
#ax.axis('off')
ax.tick_params(labelbottom='off')
ax.tick_params(right='off')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

FP=0
TN=0
TP=0
FN=0
M=1000 #number of random points drawn for the evaluation
for t in range(M):
    p1 = random.random()
    p2 = random.random()
    circ = Circle((p1, p2), radius=0.005, edgecolor='black', facecolor='red')
    ax.add_patch(circ)
    if (p1>1/3) and (p1<2/3) and (p2>1/3) and (p2<2/3):
        ss = [x for x in range(Nself)]
        for j in range(Nself):
            ss[j] = (sqrt(math.pow(s[j][0] - p1, 2) + math.pow(s[j][1] - p2, 2)))
        dmin = np.min(ss)
        if dmin > r:
            FP=FP+1
            #print("False Positive")
        else:
            TN=TN+1
            #print("True Negative")
    else:
        ss = [x for x in range(N)]
        for j in range(N):
            ss[j] = (sqrt(math.pow(D[j][0] - p1, 2) + math.pow(D[j][1] - p2, 2)))-D[j][2]
        dmin = np.min(ss)
        if dmin > 0:
            FN = FN + 1
            #print("False Negative")
        else:
            TP = TP + 1
            #print("True Positive")
plt.ylim(0,1)
plt.xlim(0,1)
plt.gca().set_aspect('equal', adjustable='box')
print("Detection Rate = ",TP/(TP+FN))
print("False Alarm Rate = ",FP/(FP+TN))
print("Check:", FN+TN+FP+TP)
print("TP = ",TP)
print("FN = ",FN)
print("FP = ",FP)
print("TN = ",TN)
print("Approximation DR =", 1-3*r/2-9*math.pi/8*r*r)
show()