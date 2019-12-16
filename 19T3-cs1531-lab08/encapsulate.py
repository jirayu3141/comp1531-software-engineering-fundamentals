import datetime

# 1. made name and birth-year private
# 2. create functions for getName to ensure that name doesn't get changed accidentally
# 3. create functions to get user's info 

class Student:
    def __init__(self, firstName, lastName, birth_year):
        self.__name = firstName + " " + lastName
        self.__birth_year = birth_year

    def age(self):
        return datetime.date.today().year - self.__birth_year

    def getName(self):
        return self.__name


if __name__ == '__main__':
    s = Student("Rob", "Everest", 1961)
    print(f"{s.getName()} is {s.age()} old")
