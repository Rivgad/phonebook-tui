from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Contact:
    surname: str
    name: str
    patronymic: Optional[str] = field(default=None)
    organization: Optional[str] = field(default=None)
    work_phone: Optional[str] = field(default=None)
    personal_phone: Optional[str] = field(default=None)
