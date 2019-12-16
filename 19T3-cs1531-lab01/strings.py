'''
TODO Complete this file by following the instructions in the lab exercise.
'''

strings = ['This', 'list', 'is', 'now', 'all', 'together']

for word in strings[:-1]:
    print(word, end= ' ')
print(strings[len(strings)-1])

print(' '.join(strings))