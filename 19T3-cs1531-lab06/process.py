from unpickle import unpickle
from json import dumps
import pickle

content = dumps({
    'mostCommon' : unpickle(),
    'rawData' : pickle.load(open("shapecolour.p", "rb"))
    }, sort_keys=True, indent=4)

with open('processed.json', 'w') as file:
    file.write(content)