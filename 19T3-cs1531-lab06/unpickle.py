import pickle
import collections

def unpickle():
    #unpickle shapecolor.p
    DATA = pickle.load(open("shapecolour.p", "rb"))

    #convert dictionaries into tuple 
    item_set = list()
    for item in DATA:
        added_item = item['shape'], item['colour']
        item_set.append(added_item)

    #extract most common element
    most_common_item = collections.Counter(item_set).most_common(1)
    shape, colour = most_common_item[0][0]

    return {'shape' : shape, 'colour': colour}

def main():
    print(unpickle())    

if __name__ == "__main__":
    main() 