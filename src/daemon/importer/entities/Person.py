import xml.etree.ElementTree as ET


class Person:
    counter = 0

    def __init__(self, first_name, last_name):
        Person.counter += 1
        self._id = Person.counter
        self._first_name = first_name
        self._last_name = last_name

    def to_xml(self):
        el = ET.Element("Person")
        el.set("id", str(self._id))
        el.set("first_name", self._first_name)
        el.set("last_name", self._last_name)
        return el

    def get_id(self):
        return self._id
    
    def set_id(self, new_id):
        self._id = new_id  # Assuming _id is directly modifiable

    def __str__(self):
        return f"Person ID: {self._id}, first_name: {self._first_name}, last_name: {self._last_name}"


Person.counter = 0
