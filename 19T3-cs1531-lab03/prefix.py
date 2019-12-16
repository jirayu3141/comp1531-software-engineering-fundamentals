def prefix_search(dictionary, key_prefix):
    '''
    Given a dictionary (with strings for keys) and a string, returns a new dictionary containing only the keys (and their corresponding values) for which the string is a prefix. If the string is not a prefix for any key, a KeyError is raised.

    For example,
    >>> prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a")
    {'ac': 1, 'ab': 3}
    '''

    #loop through the list, if the key has a key_prefix, add that element to
    #answer dictionary
    answer = {}
    for x in dictionary:
        if key_prefix == x[0:(len(key_prefix))]:
            answer.update({x : dictionary[x]})
    return answer

# if __name__ == '__main__':
#     print(prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a"))
#     print(prefix_search({"category": "math", "cat": "animal"}, "cat"))
