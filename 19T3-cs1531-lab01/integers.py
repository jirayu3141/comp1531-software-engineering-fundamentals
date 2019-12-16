'''
TODO Complete this file by following the instructions in the lab exercise.
'''

integers = [1, 2, 3, 4, 5]
integers.append(6)
total = 0
for x in range(0, len(integers)):
	total += integers[x]
print (total) 	
print(sum(integers))
