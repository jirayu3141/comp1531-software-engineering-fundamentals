"""Question 1:  Given two Latitude/Longitude coordinates, find out what time I would arrive at my destination if I left now. Assume I travel at the local country's highway speed"""

def findEarthDistance(latLng1, latLng2):
	pass

def findHighwaySpeed(latLng):
	pass

def arrivalTime(latLng1, latLng2) # Two tuples
	distance = findEarthDistance(latLng1, latLng2)
	localHighwaySpeed = findHighwaySpeed(latLng2)
	timeTakenSeconds = distance / localHighwaySpeed
	finalTime = datetime.datetime.now().adjust(seconds=timeTakenSeconds)
	print(finalTime)

if __name__ == '__main__':
    print(arrivalTime((53,64),(14,44)))