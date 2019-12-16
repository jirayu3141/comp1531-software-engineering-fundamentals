class Tourist:
    def __init__(self):
        pass

class Tour:
    def __init__(self):
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)

class City:
    def __init__(self):
        pass

class Hotel:
    def __init__(self):
        self.rooms = []

class Room:
    def __init__(self, number, grade):
        self.bookings = []
        self.grade = grade

    def add_booking(self, tourist, arrival, departure):
        self.bookings.append(Booking(tourist, self, arrival, departure))

class Booking:
    def __init__(self, tourist, room, arrival, departure):
        self.room = room
        self.tourist = tourist
        self.arrival = arrival
        self.departure = departure

class Grade:
    pass