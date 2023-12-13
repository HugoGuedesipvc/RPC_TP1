import xml.dom.minidom as md
import xml.etree.ElementTree as ET
import requests

from xml_generation.csv_reader import CSVReader
from xml_generation.entities.Person import Person
from xml_generation.entities.Car import Car
from xml_generation.entities.CreditCard import CreditCard
from xml_generation.entities.Sales import Sales


class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = CSVReader(path)
        self.person_counter = 0
        self.car_counter = 0
        self.credit_card_counter = 0
        self.sale_counter = 0
        self.gps_cache = {}

    def get_or_generate_id(self, unique_ids, key, counter):
        if key not in unique_ids:
            counter += 1
            unique_ids[key] = counter
        return unique_ids[key]

    def get_gps_coordinates(self, sale):
        try:
            location = sale.get_country()

            # Verificar se as coordenadas estão em cache
            if location in self.gps_cache:
                return self.gps_cache[location]

            nominatim_url = "https://nominatim.openstreetmap.org/search"
            params = {
                'format': 'json',
                'limit': 1,
                'q': location,
            }
            response = requests.get(nominatim_url, params=params)
            data = response.json()

            if data and data[0].get('lat') and data[0].get('lon'):
                lat = data[0]['lat']
                lon = data[0]['lon']

                # Armazenar as coordenadas na cache
                self.gps_cache[location] = f"{lat}, {lon}"

                return f"{lat}, {lon}"

            return None

        except Exception as e:
            print(f"Erro na função gps: {e}")
            print(f"Location: {sale.get_country()}")
            raise  # Levanta a exceção para indicar o erro

    def to_xml(self):
        # Separate dictionaries for each entity type
        person_ids = {}
        car_ids = {}
        credit_card_ids = {}
        sale_ids = {}

        try:
            import xml.etree.ElementTree as ET
        except Exception as e:
            print(f"Erro ao importar xml.etree.ElementTree: {e}")

        # read persons
        persons = self._reader.read_entities(
            builder=lambda row, counter=self.person_counter: Person(
                first_name=row["First Name"],
                last_name=row["Last Name"]
            ),
            unique_ids=person_ids,
            composite_key=lambda row: f"person_{row['First Name']}_{row['Last Name']}",
            counter=self.person_counter
        )

        # read cars
        cars = self._reader.read_entities(
            builder=lambda row, counter=self.car_counter: Car(
                brand=row["Car Brand"],
                model=row["Car Model"],
                color=row["Car Color"],
                year_of_manufacture=row["Year of Manufacture"]
            ),
            unique_ids=car_ids,
            composite_key=lambda row: f"car_{row['Car Brand']}_{row['Car Model']}_{row['Car Color']}_{row['Year of Manufacture']}",
            counter=self.car_counter
        )

        # read credit cards
        credit_cards = self._reader.read_entities(
            builder=lambda row, counter=self.credit_card_counter: CreditCard(
                card_type=row["Credit Card Type"]
            ),
            unique_ids=credit_card_ids,
            composite_key=lambda row: f"credit_card_{row['Credit Card Type']}",
            counter=self.credit_card_counter
        )

        # read sales
        sales = self._reader.read_entities(
            builder=lambda row, counter=self.sale_counter: Sales(
                country=row["Country"],
                person_id=self.get_or_generate_id(person_ids, f"person_{row['First Name']}_{row['Last Name']}",
                                                  counter),
                car_id=self.get_or_generate_id(car_ids,
                                               f"car_{row['Car Brand']}_{row['Car Model']}_{row['Car Color']}_{row['Year of Manufacture']}",
                                               counter),
                credit_card_id=self.get_or_generate_id(credit_card_ids, f"credit_card_{row['Credit Card Type']}",
                                                       counter),
            ),
            unique_ids=sale_ids,
            composite_key=lambda
                row: f"sale_{row['Country']}_{row['First Name']}_{row['Last Name']}_{row['Car Brand']}_{row['Car Model']}_{row['Car Color']}_{row['Year of Manufacture']}_{row['Credit Card Type']}",
            counter=self.sale_counter
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
            coordinates = self.get_gps_coordinates(sale)
            if coordinates:
                sale_elem = sale.to_xml()
                sale_elem.set('latitude', coordinates.split(', ')[0])
                sale_elem.set('longitude', coordinates.split(', ')[1])
                sales_el.append(sale_elem)

        root_el.append(persons_el)
        root_el.append(cars_el)
        root_el.append(credit_cards_el)
        if len(sales_el) > 0:  # Verificar se há vendas antes de adicioná-las ao elemento raiz
            root_el.append(sales_el)

        return root_el

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()
