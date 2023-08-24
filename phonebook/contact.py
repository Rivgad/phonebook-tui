from dataclasses import asdict, dataclass, field
from typing import Optional

from errors import DataToItemError


@dataclass
class Contact:
    id: int
    first_name: str
    last_name: str
    patronymic: Optional[str] = field(default=None)
    organization: Optional[str] = field(default=None)
    work_phone: Optional[str] = field(default=None)
    personal_phone: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict):
        try:
            data["id"] = int(data["id"])
            return Contact(**data)
        except Exception as ex:
            raise DataToItemError(f"Could not transform {data}") from ex

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        return "; ".join(
            x if x is not None else ""
            for x in [
                str(self.id),
                self.first_name,
                self.last_name,
                self.patronymic,
                self.organization,
                self.work_phone,
                self.personal_phone,
            ]
        )
