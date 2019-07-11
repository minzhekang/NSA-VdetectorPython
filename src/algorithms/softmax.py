def softmax(x):
 	return np.exp(x) / np.sum(np.exp(x), axis=0)

 