
def reverse_words(string_list):
    '''
    Given a list of strings, return a new list where the order of the words is reversed.

    For example,
    >>> reverse_words(["Hello World", "I am here"])
    ['World Hello', 'here am I']
    '''
    result = []
    for word in string_list:
        word = word.split(' ')
        word.reverse()
        result.append(" ".join(word))
        
    return result



if __name__ == "__main__":
    print(reverse_words(["Hello World", "I am here"]))
