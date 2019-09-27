import re
import numpy as np

helloFile = open('test.lin')
helloContent = helloFile.read()
p = re.compile('\n')
n = len(p.findall(helloContent)) - 1
p = re.compile('-?[0-9]+.[0-9]+')
string_array = p.findall(helloContent)
a_array = np.zeros(shape=(n,n))
b_array = np.zeros(n)
# max_a_count = len(string_array) - n 
count = 0

for x in range(n):
	for y in range(n):
		a_array[x, y] = float(string_array[count])
		# print (a_array[x, y])
		# print (a_count)
		count += 1
print(a_array)

for z in range(n):
	b_array[z] = float(string_array[count])
	count += 1

print(b_array)