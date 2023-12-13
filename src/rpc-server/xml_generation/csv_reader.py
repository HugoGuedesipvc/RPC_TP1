from csv import DictReader
import csv


class CSVReader:
    def __init__(self, path):
        self.path = path

    def read_entities(self, builder, unique_ids=None, composite_key=None, counter=None):
        with open(self.path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            entities = {}
            for row in reader:
                if composite_key:
                    key = composite_key(row)
                else:
                    key = None

                if key is not None and key in entities:
                    # If the key already exists, skip this row
                    continue

                # Add the counter argument to the builder function
                entity = builder(row, counter=counter)
                entities[key] = entity

                if unique_ids is not None and key is not None:
                    unique_ids[key] = entity

            return entities
