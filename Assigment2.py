import numpy as np	
import pdb

a = np.array([[3, 4, 3],
		  [1, 5, -1],
		  [6, 3, 7]], dtype='float32')

b = np.array([10, 7, 15], dtype='float32')



def NaiveGauss(aMatrix, bMatrix):
	size = len(bMatrix)
	xValues = np.zeros(size)
	# forward elimination
	for k in range(0, size-1):
		for i in range(k+1, size):
			xMult = aMatrix[i, k] / aMatrix[k, k]
			aMatrix[i, k] = xMult
			for j in range(k+1, size):
				aMatrix[i, j] -= (xMult * aMatrix[k, j])
			bMatrix[i] -= (xMult * bMatrix[k])
	# back substitution
	xValues[size-1] = bMatrix[size-1] / aMatrix[size-1, size-1]
	for i in range(size-2, -1, -1):
		_sum = bMatrix[i]
		for j in range(i+1, size):
			 _sum -= (aMatrix[i, j] * xValues[j])
		xValues[i] = _sum / aMatrix[i, i]
	# code to format the output, float32 produces weird results like -0.0
	for x in range(len(xValues)):
		if xValues[x] == -0.0:
			xValues[x] = 0.0
	return xValues
#end NaiveGauss

indexArray = np.zeros((len(a),), dtype=int)
scaleArray = np.zeros(len(a))

#computes the scale array, index array and zeroes out entries in matrix
def Gauss(size, aMatrix, indexArray, scaleArray):
	#initialize index array
	for i in range(0, size):
		indexArray[i] = i
		smax = 0.0
		for j in range(0, size):
			smax = max(smax, aMatrix[i, j])
		#initialize scale array
		scaleArray[i] = smax
	#initiate outer loop
	for k in range(0, size-1):
		rmax = 0
		#calculate the greatest ratio, ie rmax
		for i in range(k, size):
			r = abs(aMatrix[indexArray[i], k] / scaleArray[indexArray[i]])
			if (r > rmax):	
				rmax = r
				#calculate index of greatest ratio
				j = i
		#swap 
		temp = indexArray[j]
		indexArray[j] = indexArray[k]
		indexArray[k] = temp
		#compute and store multiplier
		for i in range(k+1, size):
			xMult = (aMatrix[indexArray[i], k] / aMatrix[indexArray[k], k])
			aMatrix[indexArray[i], k] = xMult
			#modify a matrix via forward elimination
			for j in range(k+1, size):
				aMatrix[indexArray[i], j] -= (xMult*aMatrix[indexArray[k], j])
#end Gauss


#modify b vector and calculate x values
def Solve(size, aMatrix, indexArray, bMatrix):
	xValues = np.zeros(size)
	for k in range(0, size-1):
		#modify b matrix via forward elimination using multipliers stored in a matrix from Gauss method
		for i in range(k+1, size):
			bMatrix[indexArray[i]] -= (aMatrix[indexArray[i], k] * bMatrix[indexArray[k]])
	#back-substitution		
	xValues[size-1] = (bMatrix[indexArray[size-1]] / aMatrix[indexArray[size-1], size-1])
	for i in range(size-2, -1, -1):
		_sum = bMatrix[indexArray[i]]
		for j in range(i+1, size):
			_sum -= (aMatrix[indexArray[i], j] * xValues[j]) 	
		xValues[i] = _sum / aMatrix[indexArray[i], i] 
	return xValues
	#need print statements
#end Solve	



print("Calling Gauss w/SPP method: ")
Gauss(len(b),a, indexArray, scaleArray)
print("Calling Solve w/SPP method: ")
print(Solve(len(a),a,indexArray, b))