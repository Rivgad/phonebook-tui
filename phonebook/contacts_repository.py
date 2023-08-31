from typing import Any, Callable, Iterator

from errors import ItemNotFoundError, KeyFoundError
from contact import Contact
from csv_writer import CsvWriter


class ContactsRepository(CsvWriter):
    def all(self) -> list[Contact]:
        return [x for x in self.read_items()]

    def read_items(self) -> Iterator[Contact]:
        for data in self.read_file():
            try:
                yield Contact.from_dict(data)
            except ValueError:
                raise

    def insert(self, contact: Contact, auto_incr_id=True):
        items = self.all()
        if auto_incr_id:
            max_id = max([item.id for item in items], default=0)
            contact.id = max_id + 1
        else:
            if contact.id in [col_item.id for col_item in items]:
                raise KeyFoundError(f"Item {contact.id} already in the collection.")

        self.append_file(contact)

        return contact

    def update(self, id: int, values: dict) -> Contact:
        items = self.all()

        item = next(((i, x) for i, x in enumerate(items) if x.id == id), None)

        if item is None:
            raise ItemNotFoundError(f"Contact with id = {id} not found")

        idx, contact = item

        for key, val in values.items():
            if key != "id":
                setattr(contact, key, val)

        items[idx] = contact

        self.write_file(items)

        return contact

    def delete(self, id: int) -> Contact:
        items = self.all()

        item = next(((i, x) for i, x in enumerate(items) if x.id == id), None)

        if item is None:
            raise ItemNotFoundError(f"Contact with id = {id} not found")

        idx, contact = item

        del items[idx]

        self.write_file(items)

        return contact

    def get_by_id(self, id: int) -> Contact:
        item = next(self.query(lambda x: x.id == id), None)

        if item is None:
            raise ItemNotFoundError(f"Contact with id = {id} not found")

        return item

    def query(self, predicate: Callable[[Contact], Any]) -> Iterator[Contact]:
        return filter(predicate, self.all())
