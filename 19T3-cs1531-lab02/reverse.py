def reverse_words(string_list):
    '''
   Given a list of strings, return a new list where the order of the words is reversed.
 
   For example,
   >>> reverse_words(["Hello World", "I am here"])
   ['World Hello', 'here am I']
   '''
    output = []
 
 
    for x in string_list:
        s = ''
        newList = x.split(' ')
        newList.reverse()
        s += ' '.join(newList)
        output.append(s)
           
    if output == []:
        return None
 
    return output
 
def test_reverse():
    assert reverse_words(["Hello World", "I am here"]) == ['World Hello', 'here am I']
    assert reverse_words(["Hello Hello", "Azuza", "Good bye"]) == ["Hello Hello", "Azuza", "bye Good"]
    assert reverse_words([]) == None
    assert reverse_words(["! & ^", "!&^"]) == ["^ & !", "!&^"]
    assert reverse_words(["  ", " a b", "b  a", "   a  b c"]) == ["  ", "b a ", "a  b", "c b  a   "]