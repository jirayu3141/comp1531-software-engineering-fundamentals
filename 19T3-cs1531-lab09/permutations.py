import itertools
def lols(string):
    if len(string) == 0:
        return ['']
    prevList = permutations(string[1:len(string)])
    nextList = []
    for i in range(0,len(prevList)):
        for j in range(0,len(string)):
            newString = prevList[i][0:j]+string[0]+prevList[i][j:len(string)-1]
            if newString not in nextList:
                nextList.append(newString)
    return nextList

def permutations(string):
    '''
    For the given string, yield all permutations of the characters of that string in any order. For example:
    >>> sorted(list(permutations('ABC')))
    ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']

    If a character occurs more than once in the input string, each occurrence is still considered distinct. For example:
    >>> sorted(list(permutations('ABB')))
    ['ABB', 'ABB', 'BAB', 'BAB', 'BBA', 'BBA']
    '''
    yield True



