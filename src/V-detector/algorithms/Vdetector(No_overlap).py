from pylab import *
from scipy.spatial import distance
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random
import time
from tqdm import tqdm

fig, ax =plt.subplots()
Nself = 500
s= [x for x in range(Nself)]
r = 0.02
for i in range(Nself):
	x = 1/3 + random()/3
	y = 1/3 + random()/3
	s[i] = [x,y]

def generateGreyCircles():
	for i in range(Nself):
		circle = Circle((s[i][0],s[i][1]), radius = r, edgecolor = "black", facecolor = "grey")
		ax.add_patch(circle)

patches = []
NumberofDetectors = 60
Detectorlist = []
def generateGreenCircles():
	teller = len(patches)
	pbar = tqdm(total=NumberofDetectors, initial = 0)

	while len(patches) < NumberofDetectors:
		x1 = random()
		y1 = random()
		ss = [x for x in range(Nself)]
		shouldprint = True
		for i in range(Nself):
			ss[i]=(sqrt(math.pow(s[i][0]-x1,2)+math.pow(s[i][1]-y1,2)))
		dmin = np.min(ss)
		newradius = dmin-r
		
		for j in Detectorlist:
			if incircle(x1,y1,newradius , j[0],j[1],j[2]):
				shouldprint = False
			
		if shouldprint and (dmin>r):
			Detectorlist.append([x1,y1,dmin-r])
			circle = Circle((x1,y1), radius = newradius , edgecolor='black', facecolor='lightgreen')
			patches.append(ax.add_patch(circle))
			pbar.update(1)

	pbar.close()
			
def incircle(x1,y1,r1,x2,y2,r2):
	dist = math.sqrt( ((x2-x1)**2) + ((y2-y1)**2) )
	return dist <= (r2+r1)

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
generateGreyCircles()
generateGreenCircles()



FP=0
TN=0
TP=0
FN=0
M=1000 #number of random points drawn for the evaluation
for t in range(M):
    p1 = random()
    p2 = random()
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
        ss = [x for x in range(NumberofDetectors)]
        for j in range(NumberofDetectors):
            ss[j] = (sqrt(math.pow(Detectorlist[j][0] - p1, 2) + math.pow(Detectorlist[j][1] - p2, 2)))-Detectorlist[j][2]
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



plt.show()

