def inverse(d):
    '''
    Given a dictionary d, invert its structure such that values in d map to lists of keys in d. For example:
    >>> inverse({1: 'A', 2: 'B', 3: 'A'})
    {'A': [1, 3], 'B': [2]}
    '''
    dict = {}
    for x in d.items():
        if x[1] not in dict:
            dict.update({x[1]: [x[0]]})
        else:
            dict[x[1]].append(x[0])
    return dict



if __name__ == "__main__":
    print(inverse({1: 'A', 2: 'B', 3: 'A'}))
