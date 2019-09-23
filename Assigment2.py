import numpy as np	
import pdb

a = np.array([[3, 4, 3],
		  [1, 5, -1],
		  [6, 3, 7]], dtype='float32')

b = np.array([10, 7, 15], dtype='float32')

def NaiveGauss(aMatrix, bMatrix):
	size = len(bMatrix)
	subMatrix = np.zeros(size)
	for k in range(0, size-1):
		for i in range(k+1, size):
			xMult = aMatrix[i, k] / aMatrix[k, k]
			aMatrix[i, k] = xMult
			for j in range(k+1, size):
				aMatrix[i, j] = aMatrix[i, j] - (xMult * aMatrix[k, j])
			bMatrix[i] = bMatrix[i] - (xMult * bMatrix[k])
	subMatrix[size-1] = bMatrix[size-1] / aMatrix[size-1, size-1]
	for i in range(size-2, -1, -1):
		_sum = bMatrix[i]
		for j in range(i+1, size):
			_sum = _sum - (aMatrix[i, j] * subMatrix[j])
		subMatrix[i] = _sum / aMatrix[i, i]
	#code to format the output, float32 produces weird results like -0.0
	for x in range(len(subMatrix)):
		if subMatrix[x] == -0.0:
			subMatrix[x] = 0.0
	return subMatrix

print(NaiveGauss(a,b))
