#create function to get input from the user
#make amount of input variable
# use python build-in min
# create muliplyList function to replace literal lines of code
from string import ascii_lowercase

def getInput(num):
    my_input = []
    for i, letter in enumerate(ascii_lowercase):
        x = input(f"Enter {letter}: ")
        my_input.append(int(x))
        #break out of loop
        if i >= num-1:
            break
    return my_input

def multiplyList(myList, start, end):
    result = 1
    for x in range(start ,end): 
        result = result * myList[x]
        print(x)
    return result 

if __name__ == '__main__':
    my_list = getInput(num=5)
    my_min =  min(my_list)
    print("Minimum: " + str(my_min))
    print(f"Product of first 4 numbers: {multiplyList(my_list, start=0, end=4)}")
    print(f"Product of last 4 numbers: {multiplyList(my_list, end=len(my_list), start=len(my_list)-4)}")