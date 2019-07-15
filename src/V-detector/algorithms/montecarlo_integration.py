import numpy as np
import matplotlib.pyplot as plt

def montecarlo(N, r):
	x = np.random.uniform(low = -r, high =r, size=[N, 1])
	y = np.random.uniform(low = -r, high =r, size=[N, 1])
	euclidean_dist = x**2 + y**2 < r**2 # This gives boolean values
	x_inside = x[euclidean_dist]
	y_inside = y[euclidean_dist]

	approximated_area = (np.sum(euclidean_dist)/N)*(r*2)*(r*2) # 2*2 is the area of the square

	fig = plt.figure(figsize = [4,4])
	plt.scatter(x,y, color = 'g')
	plt.scatter(x_inside,y_inside, color = 'b')
	plt.title("The approximated area of circle is {}".format(approximated_area))
	plt.show()

montecarlo(1000, 1)