import pandas as pd
import numpy as np
import random
from tqdm import tqdm

pd.set_option('display.expand_frame_repr', False)
file = ""

data = pd.read_csv(file)
NormAttList = data["Normal/Attack"]
data = data.drop(["Normal/Attack"], axis= 1) # only the numerical variables

Nself = len(data.values) # gives you the total number of data
radius_self = 0.02 # self radius of normal data

def euc_distance(array1, array2): # euclidean function
	return np.power(np.sum((array1 - array2)**2, axis = 1) , 0.5)


def gen_detectors():
	listarray = []
	listarray.append(random.random())
	listarray.append(random.random())
	listarray.append(random.choice([0, 0.5 , 1.0]))
	listarray.append(random.choice([0, 0.5 , 1.0]))
	listarray.append(random.choice([0, 0.5 , 1.0]))
	return np.array(listarray)

N = 100 # number of detectors
counter = 0
D = [x for x in range(N)] 
Dradius = [x for x in range(N)]
pbar = tqdm(total=N, initial = 0, desc= "Generating detectors!") # progress-bar

while counter < N:
	detector = gen_detectors()
	distance_list = list(euc_distance(data, detector)) # calculates in a large array
	dmin = np.min(distance_list) # calculates the minimum distance between current detector and all the data
	detector_radius = dmin-radius_self # minus away the radius_self to ensure it doesnt overlap
	if dmin > radius_self:
		D[counter] = detector
		Dradius[counter] = detector_radius
		counter += 1
		pbar.update(1)
pbar.close()


#############################Test Phase#####################################
print("Initializing test phase...")
file2 = ""
data2 = pd.read_csv(file2)
NormAttListTest = data2["Normal/Attack"]
data2 = data2.drop(["Normal/Attack"], axis = 1) #axis = 1 refers to the row

FP=0
FN=0
TP=0
TN=0
AttListTest = np.array([val == 'Attack' for val in NormAttListTest]) # this prints boolean values for which the data is "Attack"
NormListTest = np.array([val == 'Normal' for val in NormAttListTest])

D = np.array(D)
distance_test = np.array([euc_distance(val, D) - Dradius for val in data2.values]) # distance of detector and test point minus the detector radius

#distance_test = euc_distance2(data2.values[:, None, :], D[None, :, :]) - Dradius  # broadcasting results in memory error
print("Evaluating minimum distance!")
#distance_test_min = np.array([np.min(val) for val in distance_test])
distance_test_min = np.min(distance_test, axis = 1)

print("Calculated")
TP += np.sum( (distance_test_min < 0) & AttListTest)
FN += np.sum( (distance_test_min > 0) & AttListTest)
FP += np.sum( (distance_test_min < 0) & NormListTest)
TN += np.sum( (distance_test_min > 0) & NormListTest)

print("Total number of data in test = ", len(data2.values))
print("Total number of data checked = ", FN+TN+FP+TP)
print("Number of Attacks = ",np.sum(AttListTest))
print("Number of Normal = ",np.sum(NormListTest))

print("Detection Rate = ",TP/(TP+FN))
print("False Alarm Rate = ",FP/(FP+TN))
print("TP = ",TP)
print("FN = ",FN)
print("FP = ",FP)
print("TN = ",TN)
