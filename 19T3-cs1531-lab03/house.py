class House:

    def __init__(self, name, adderss, bedrooms):
        self.name = name
        self.address = adderss
        self.bedrooms = bedrooms
        self.lastSoldPrice = None
        self.forSale = None
    
    def advertise(self):
        self.forSale = True

    def sell(self, name, price):
        if self.forSale is True:
            self.lastSoldPrice = price
            self.name = name
        else:
            raise Exception


# Rob built a mansion with 6 bedrooms
mansion = House("Rob", "123 Fake St, Kensington", 6)


# Viv built a 3 bedroom bungalow
bungalow = House("Viv", "42 Wallaby Way, Sydney", 3)

# The bungalow is advertised for sale
bungalow.advertise()

# Hayden tries to buy the mansion but can't
try:
    mansion.sell("Hayden", 3000000)
except Exception:
    print("Hayden is sad")

# He settles for buying the Bungalow instead
bungalow.sell("Hayden", 1000000)