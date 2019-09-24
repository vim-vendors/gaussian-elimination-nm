import numpy as np	
import pdb

a = np.array([[3, 4, 3],
		  [1, 5, -1],
		  [6, 3, 7]], dtype='float32')

b = np.array([10, 7, 15], dtype='float32')

def NaiveGauss(aMatrix, bMatrix):
	size = len(bMatrix)
	subVector = np.zeros(size)
	# forward elimination
	for k in range(0, size-1):
		for i in range(k+1, size):
			xMult = aMatrix[i, k] / aMatrix[k, k]
			aMatrix[i, k] = xMult
			for j in range(k+1, size):
				aMatrix[i, j] -= (xMult * aMatrix[k, j])
			bMatrix[i] -= (xMult * bMatrix[k])
	# back substitution
	subVector[size-1] = bMatrix[size-1] / aMatrix[size-1, size-1]
	for i in range(size-2, -1, -1):
		_sum = bMatrix[i]
		for j in range(i+1, size):
			 _sum -= (aMatrix[i, j] * subVector[j])
		subVector[i] = _sum / aMatrix[i, i]
	# code to format the output, float32 produces weird results like -0.0
	for x in range(len(subVector)):
		if subVector[x] == -0.0:
			subVector[x] = 0.0
	return subVector
#end NaiveGauss

def Gauss(size, aMatrix):
	print("Pre - aMatrix: ")
	print(aMatrix)
	indexArray = np.zeros((size,), dtype=int)
	ratioArray = np.zeros(size)
	for i in range(0, size):
		indexArray[i] = i
		smax = 0.0
		for j in range(0, size):
			smax = max(smax, aMatrix[i, j])
		ratioArray[i] = smax
	for k in range(0, size-1):
		rmax = 0
		for i in range(k, size):
			#pdb.set_trace()
			r = abs(aMatrix[indexArray[i], k] / ratioArray[indexArray[i]])
			if (r > rmax):	
				rmax = r
				j = i
		temp = indexArray[j]
		indexArray[j] = indexArray[k]
		indexArray[k] = temp
		for i in range(k+1, size):
			xMult = (aMatrix[indexArray[i], k] / aMatrix[indexArray[k], k])
			aMatrix[indexArray[i], k] = xMult
			for j in range(k+1, size):
				aMatrix[indexArray[i], j] -= (xMult*aMatrix[indexArray[k], j])
#need to return something?
	print("Post - aMatrix: ")
	print(aMatrix)
	print("ratioArray:")
	print(ratioArray)
	print("indexArray: ")
	print(indexArray)
#end Gauss

print("Calling Gauss w/SPP method: ")
Gauss(len(b),a)

def Solve(size, aMatrix, indexArray, bMatrix, subVector):
	for k in range(0, size-1):
		for i in range(k+1, n):
			bMatrix[indexArray[i]] -= (aMatrix[indexArray[i], k] * bMatrix[indexArray[k]])
	subVector[size-1] = (bMatrix[indexArray[size-1]] / aMatrix[indexArray[size-1], size-1])
	for i in range(size-2, -1, -1):
		_sum = bMatrix[indexArray[i]]
		for j in range(i+1, n):
			_sum -= (aMatrix[indexArray[i], j] * subVector[j]) 	
		subVector[i] = _sum / aMatrix[indexArray[i], i] 
#need to return something?
#need print statements
#end Solve	
