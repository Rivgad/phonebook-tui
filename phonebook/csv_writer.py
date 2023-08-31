from contact import Contact


import csv
from pathlib import Path
from typing import Iterator, Optional, TextIO


class CsvWriter:
    _fieldnames: Optional[list[str]] = None
    _filename: Path
    kwds_csv: dict = {}

    def __init__(self, filename: Path, fieldnames: Optional[list[str]] = None):
        self._filename = filename
        self._fieldnames = fieldnames

    @property
    def filepath(self) -> Path:
        file_non_zero = self._filename.exists() and self._filename.stat().st_size > 0
        if not file_non_zero:
            self._create_file(if_exists="ignore")

        return self._filename

    def append_file(self, item: Contact):
        "Write a single item at the end of the file"
        with open(self.filepath, "a", newline="") as file:
            writer = self._get_writer(file)
            writer.writerow(item.to_dict())

    def read_file(self) -> Iterator[dict]:
        "Read repository file"
        with open(self.filepath, "r") as file:
            reader = self._get_reader(file)

            next(reader, None)

            for data in reader:
                yield data

    def write_file(self, items: list[Contact]):
        "Write the file with new content of items"
        with open(self.filepath, "w", newline="") as file:
            writer = self._get_writer(file)
            writer.writeheader()
            for item in items:
                writer.writerow(item.to_dict())

    def _create_file(self, if_exists="raise"):
        "Create the repository file"
        if if_exists == "raise" and self._filename.exists():
            raise FileExistsError(f"Repository file {self._filename} already exists.")
        with open(self._filename, "w", newline="") as file:
            writer = self._get_writer(file)
            writer.writeheader()

    def get_headers(self) -> list[str]:
        "Get headers of the CSV file"
        if self._fieldnames is not None:
            return self._fieldnames
        elif hasattr(Contact, "__annotations__"):
            return list(Contact.__annotations__.keys())
        else:
            raise TypeError("Cannot determine CSV headers")

    def _get_writer(self, buff: TextIO):
        return csv.DictWriter(buff, fieldnames=self.get_headers(), **self.kwds_csv)

    def _get_reader(self, buff: TextIO):
        return csv.DictReader(buff, fieldnames=self.get_headers(), **self.kwds_csv)
