import re
import numpy as np	
import sys
import time
#time the script, ends when method is called and completes
start_time = time.time()

#get command line arguments
data_file = ''
scaledTrue = False

if (len(sys.argv) == 2):
	data_file = str(sys.argv[1])
elif (len(sys.argv) == 3):
	data_file = str(sys.argv[2])
	scaledTrue = True

#extract file info and parse with regex
helloFile = open(data_file)
helloContent = helloFile.read()
p = re.compile('\n')
n = len(p.findall(helloContent)) - 1
p = re.compile('-?[0-9]+.[0-9]+')
string_array = p.findall(helloContent)
a_array = np.zeros(shape=(n,n))
b_array = np.zeros(n)
count = 0

#extract and initialize A Matrix
for x in range(n):
	for y in range(n):
		a_array[x, y] = float(string_array[count])
		count += 1

#extract and initialize B Matrix
for z in range(n):
	b_array[z] = float(string_array[count])
	count += 1

indexArray = np.zeros((len(a_array),), dtype=int)
scaleArray = np.zeros(len(a_array))

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
#end Solve	

#choose method based on scaledTrue boolean value
if (scaledTrue == False):
	print("Naive Gaussian method: ")
	solution = str(NaiveGauss(a_array, b_array))
	print(solution)
	print("--- %s seconds ---" % (time.time() - start_time))
else:
	print("Gaussian Elimination w/ SPP method: ")
	Gauss(len(b_array),a_array, indexArray, scaleArray)
	solution = str(Solve(len(a_array),a_array,indexArray, b_array))
	print(solution)
	print("--- %s seconds ---" % (time.time() - start_time))

#output to file
outputSol = data_file
extract = re.search('(.+?).lin', outputSol)
if extract:
    outputSol = str(extract.group(1)) + ".sol"

outputFile = open(outputSol, 'w')
outputFile.write(solution)
outputFile.close()
helloFile .close()

