from datetime import date


class Vehicle:
    def __init__(self, vehicle_type):
        self._id = None
        self._is_auction = None
        self._model = None
        self._make = None
        self._model = None
        self._price = None
        self._image_url = None
        self._link = None
        self._year = None
        self._mileage = None
        self._fuel = None
        self._transmission = None
        self._bodytype = None
        self._drive = None
        self._type = vehicle_type
        self._date_today = date.today().strftime('%d-%m-%Y')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def is_auction(self):
        return self._is_auction

    @is_auction.setter
    def is_auction(self, value):
        self._is_auction = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def make(self):
        return self._make

    @make.setter
    def make(self, value):
        self._make = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, value):
        self._image_url = value

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, value):
        self._link = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        self._mileage = value

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        self._fuel = value

    @property
    def transmission(self):
        return self._transmission

    @transmission.setter
    def transmission(self, value):
        self._transmission = value

    @property
    def bodytype(self):
        return self._bodytype

    @bodytype.setter
    def bodytype(self, value):
        self._bodytype = value

    @property
    def drive(self):
        return self._drive

    @drive.setter
    def drive(self, value):
        self._drive = value

    def to_dict_with_price(self):
        vehicle_dict = self.to_dict()
        vehicle_dict[f"Price {self._date_today}"] = self.price
        return vehicle_dict

    def to_dict(self) -> dict:
        return {
            "Type": self.type,
            "ID": self.id,
            "Is Auction": self.is_auction,
            "Make": self.make,
            "Model": self.model,
            "Link": self.link,
            "Year": self.year,
            "Mileage": self.mileage,
            "Fuel": self.fuel,
            "Transmission": self.transmission,
            "Body type": self.bodytype,
            "Drive": self.drive
        }

    def __repr__(self):
        return (f"{self._type}("
                f"id={self._id}, "
                f"is_auction={self._is_auction}, "
                f"make='{self._make}', "
                f"model={self._model}, "
                f"price={self._price}"
                f")")
