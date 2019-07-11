import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from numba import jit

file = ""
data = pd.read_csv(file)
NormAttList = data["Normal/Attack"]
data = data.drop(["Normal/Attack"], axis= 1) #only the numerical variables
Nself = len(data.values) # gives you the total number of data
radius_self = 0.02 # conservative is not 0

def euc_distance(array1, array2): # euclidean function
	return np.power(np.sum((array1 - array2)**2, axis = 1) , 0.5)

@jit
def randomvalues(N):
	list1 = []
	for i in range(N):
		list1.append(random.random())
	return(list1)

# Calculation of self-volume

num_hits = 0
N = 10000
#pbar = tqdm(total=N, initial = 0, desc= "Generating detectors!") # progress-bar

biglist = []

for i in range(N):
	coordinates = biglist.append(randomvalues(data.shape[1]))

distance = np.array([np.min(euc_distance(val, data.values)) for val in biglist])
inside = distance <= radius_self
num_hits = np.sum(inside)

print(inside)
print(N)
print(num_hits)

#[False False False ... False False False]
#10000
#100
#[Finished in 1780.1s]