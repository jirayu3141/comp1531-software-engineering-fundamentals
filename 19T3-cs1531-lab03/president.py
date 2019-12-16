president = {
    'name' : 'Ian Jacobs',
    'age' : 54,
    'staff' : [ 'Sally', 'Bob', 'Rob', 'Hayden' ]
}

## TODO: Write code below this line
#remove Hayden
del president['staff'][3]

#sort staff
president['staff'] = sorted(president['staff'])

#add mark
president['mark'] = ['19T1: 77','19T2: 88', '19T3: 99']

print(president)

## TODO: Write code above this line