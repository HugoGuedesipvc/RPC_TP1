import xml.etree.ElementTree as ET
class Sales:
    counter = 0

    def __init__(self, country, person_id, car_id, credit_card_id):
        Sales.counter += 1
        self._id = Sales.counter
        self._country = country
        self._person_id = person_id
        self._car_id = car_id
        self._credit_card_id = credit_card_id

    def to_xml(self, coordinates=None):
        el = ET.Element("Sales")
        el.set("id", str(self._id))
        el.set("country", self._country)
        el.set("person_id", str(self._person_id))
        el.set("car_id", str(self._car_id))
        el.set("credit_card_id", str(self._credit_card_id))

        # Adiciona coordenadas GPS ao XML se fornecidas
        if coordinates:
            gps_el = ET.SubElement(el, 'GPS')
            gps_el.set('latitude', coordinates.split(', ')[0])
            gps_el.set('longitude', coordinates.split(', ')[1])

        return el

    def get_id(self):
        return self._id

    def set_id(self, new_id):
        self._id = new_id

    def get_country(self):
        return self._country

    def set_country(self, new_country):
        self._country = new_country

    def __str__(self):
        return f"Sales ID: {self._id}, country: {self._country}, person_id: {self._person_id}, car_id: {self._car_id}, credit_card_id: {self._credit_card_id}"

# Reinicia o contador
Sales.counter = 0
