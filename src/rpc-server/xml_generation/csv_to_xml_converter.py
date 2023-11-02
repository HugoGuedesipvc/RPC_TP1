import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from csv_reader import CSVReader
from entities.Person import Person
from entities.Car import Car
from entities.CreditCard import CreditCard
from entities.Sales import Sales


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)

    def to_xml(self):
        # read persons
        persons = self._reader.read_entities(
            attr="First Name",
            builder=lambda row: Person(
                first_name=row["First Name"],
                last_name=row["Last Name"]
            )
        )

        # read cars
        cars = self._reader.read_entities(
            attr="Car Brand",
            builder=lambda row: Car(
                brand=row["Car Brand"],
                model=row["Car Model"],
                color=row["Car Color"],
                year_of_manufacture=row["Year of Manufacture"]
            )
        )

        # read credit cards
        credit_cards = self._reader.read_entities(
            attr="Credit Card Type",
            builder=lambda row: CreditCard(
                card_type=row["Credit Card Type"]
            )
        )

        # read sales
        sales = self._reader.read_entities(
            attr="Country",
            builder=lambda row: Sales(
                country=row["Country"],
                person_id=persons[row["First Name"]].get_id(),
                car_id=cars[row["Car Brand"]].get_id(),
                credit_card_id=credit_cards[row["Credit Card Type"]].get_id()
            )
        )

        # generate the final xml
        root_el = ET.Element("Data")

        persons_el = ET.Element("Persons")
        for person in persons.values():
            persons_el.append(person.to_xml())

        cars_el = ET.Element("Cars")
        for car in cars.values():
            cars_el.append(car.to_xml())

        credit_cards_el = ET.Element("CreditCards")
        for credit_card in credit_cards.values():
            credit_cards_el.append(credit_card.to_xml())

        sales_el = ET.Element("Sales")
        for sale in sales.values():
            sales_el.append(sale.to_xml())

        root_el.append(persons_el)
        root_el.append(cars_el)
        root_el.append(credit_cards_el)
        root_el.append(sales_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

