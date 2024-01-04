import xml.etree.ElementTree as ET




class CreditCard:
    counter = 0

    def __init__(self, card_type):
        CreditCard.counter += 1
        self._id = CreditCard.counter
        self._card_type = card_type

    def to_xml(self):
        el = ET.Element("CreditCard")
        el.set("id", str(self._id))
        el.set("card_type", self._card_type)
        return el

    def get_id(self):
        return self._id
    
    def set_id(self, new_id):
        self._id = new_id

    def __str__(self):
        return f"CreditCard ID: {self._id}, card_type: {self._card_type}"


CreditCard.counter = 0
