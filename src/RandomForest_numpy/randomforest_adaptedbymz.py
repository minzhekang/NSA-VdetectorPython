'''
Adapted from Jason Brownlee
Re-created with numpy by Min Zhe
'''
import numpy as np
import random
import pandas as pd

def feature_type(data):
	threshold = 10
	listdata = []
	datatype = []
	for i in range(len(data[0]) -1):
		row = list(data[:,i])
		number_of_diff_data = len(set(row))
		listdata.append(number_of_diff_data)
	
	for i in listdata:
		if i >= threshold:
			datatype.append( "continuous")
		else:
			datatype.append( "categorical")

	return(datatype)


def train_test_split(df, test_size, seed = random.randint(0,9999)):
	indices = df.index.tolist()
	random.seed = seed
	if isinstance(test_size, float):
		test_size = round(test_size * len(df))
	test_indices = random.sample(population=indices, k= test_size)
	test_df = df.loc[test_indices]
	train_df = df.drop(test_indices)
	return train_df, test_df

def splitting(data, column, value):
	column_values = data[:, column]
	left = data[column_values < value] # you can adjust this for more optimal values
	right = data[column_values >= value]

	return left,right

def gini_index(groups, setclass):
	n_instances = np.sum([len(group) for group in groups])
	gini = 0.0

	for group in groups:
		size = len(group)

		if size == 0:
			continue
		score = 0
		for i in setclass:
			p = (np.sum(group[:, -1] == i)) / size
			score += p*p
		gini += (1 - score)*(size/n_instances)
	return gini

def get_split(data):
	setclass = np.unique(data[:,-1])
	b_column, b_value, b_score,b_groups = 999,999,999,None
	n_rows, n_columns = data[:,:-1].shape
	for column in range(n_columns):
		for row in range(n_rows):
			groups = splitting(data, column, data[row,column])
			gini = gini_index(groups, setclass)

			if gini < b_score:
				b_column, b_value, b_score, b_groups = column, data[row,column], gini, groups
				
	return {'column': b_column, 'value':b_value, 'groups': b_groups}

def to_terminal(group):
	outcomes, counts = np.unique(group[:,-1], return_counts= True)
	index = np.argmax(counts)
	return outcomes[index]

def split(node, max_depth, min_size, depth):
	left , right = node['groups']
	del(node['groups'])
	# check for a no split
	if left.size == 0 or right.size == 0:
		node['left'] = node['right'] = to_terminal(np.concatenate((left, right), axis= 0))
		return
	# check for max depth
	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)
		return
	# process left child
	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left)
		split(node['left'], max_depth, min_size, depth+1)
	# process right child
	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], max_depth, min_size, depth+1)
	
def build_tree(train, max_depth, min_size):
	root = get_split(train)
	split(root, max_depth, min_size, 1) # where recursion occurs
	return root

def print_tree(node, depth=0):
	if isinstance(node, dict):
		print('%s[Column %d < %.3f]' % ((depth*' ', (node['column']+1), node['value'])))
		print_tree(node['left'], depth+1)
		print_tree(node['right'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))

def predict(node, row):
	if row[node['column']] < node['value']: # if predicted is less than the tree value
		if isinstance(node['left'], dict):
			return predict(node['left'], row) # recursion if left contains a dict
		else:
			return node['left'] # belongs to which class
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']

def decision_tree(train, test, max_depth, min_size):
	tree = build_tree(train, max_depth, min_size)
	predictions = list()
	for row in test:
		prediction = predict(tree, row) # it predicts based on the generated tree
		predictions.append(prediction)

	return(predictions)

def bootstrapping(train):
	n_size = int(train.shape[0]*0.8)
	bootstrap_indices = np.random.randint(low = 0, high=train.shape[0], size = n_size)
	train = train[np.unique(bootstrap_indices)]
	return train

def random_forest(train, test, max_depth, min_size, n_size=3):
	forest = list()
	train = bootstrapping(train)

	for i in range(n_size):
		y_pred = (decision_tree(train, test, max_depth, min_size))
		forest.append(y_pred)

	totallist = (list(zip(*forest))) # unpacks the values
	forest_final = list()
	for i in totallist:
		forest_final.append((max(set(i), key = i.count)))

	return forest_final

if __name__ == "__main__":
	df= pd.read_csv("iris.csv")
	df = df.drop("Id" , axis = 1)

	max_depth = 5 # maximum number of splits
	min_size = 10 # min-size of each group

	train, test = train_test_split(df, 0.2)
	train = train.values
	test = test.values


	y_pred = (decision_tree(train, test, max_depth, min_size))
	correct = [i for i,j in zip(y_pred, test[:,-1]) if i==j]
	print(len(correct))
	print("Accuracy for decision tree is %s%%" % round((len(correct)/len(test[:,-1]) * 100),2) )

	y_pred2 = (random_forest(train,test,max_depth,min_size, 6))
	correct2 = [i for i,j in zip(y_pred2, test[:,-1]) if i==j]
	print(len(correct2))
	print("Accuracy for random forest is %s%%" % round((len(correct2)/len(test[:,-1]) * 100),2) )

	