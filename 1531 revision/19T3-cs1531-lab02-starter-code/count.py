
def count_char(input):
    '''
    Counts the number of occurrences of each character in a string. The result should be a dictionary where the key is the character and the dictionary is its count.

    For example,
    >>> count_char("HelloOo!")
    {'H': 1, 'e': 1, 'l': 2, 'o': 2, 'O': 1, '!': 1}
    '''
    
    result = {}
    # if not already in the dict, make each element into dictionary
    # for letters in input:
    #     if letters not in result.keys():
    #         result[letters] = 1
    #     else:
    #         result[letters] += 1
    
    for n in input:
        result[n] = result.get(n,0) + 1
    
    return result

if __name__ == "__main__":
    print(count_char("HelloOo!"))