import xml.etree.ElementTree as ET


class Car:
    counter = 0

    def __init__(self, brand, model, color, year_of_manufacture):
        Car.counter += 1
        self._id = Car.counter
        self._brand = brand
        self._model = model
        self._color = color
        self._year_of_manufacture = year_of_manufacture

    def to_xml(self):
        el = ET.Element("Car")
        el.set("id", str(self._id))
        el.set("brand", self._brand)
        el.set("model", self._model)
        el.set("color", self._color)
        el.set("year_of_manufacture", str(self._year_of_manufacture))
        return el

    def get_id(self):
        return self._id
    
    def set_id(self, new_id):
        self._id = new_id

    def __str__(self):
        return f"Car ID: {self._id}, brand: {self._brand}, model: {self._model}, color: {self._color}, year_of_manufacture: {self._year_of_manufacture}"


Car.counter = 0
