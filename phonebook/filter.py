import re
from contact import Contact


from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widgets import Input, Static


from typing import Callable


class Filter(Static):
    BINDINGS = [
        ("ctrl+q, escape", "back", "Back"),
    ]

    class Changed(Message):
        def __init__(
            self, input_name: str, value: str, predicate: Callable[[Contact], bool]
        ) -> None:
            self.input_name = input_name
            self.value = value
            self.predicate = predicate
            super().__init__()

    class RequestBack(Message):
        pass

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input(
                placeholder="Имя",
                id="first_name",
            ),
            Input(
                placeholder="Фамилия",
                id="last_name",
            ),
            Input(
                placeholder="Отчество",
                id="patronymic",
            ),
            Input(
                placeholder="Организация",
                id="organization",
            ),
            Input(
                placeholder="Рабочий телефон",
                id="work_phone",
            ),
            Input(placeholder="Телефон (личный)", id="personal_phone"),
            id="filter_grid",
        )

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed):
        if event.input.id is None:
            return

        self.post_message(
            self.Changed(event.input.id, event.input.value, self.get_predicate())
        )

    def action_back(self) -> None:
        self.post_message(self.RequestBack())

    def get_predicate(self) -> Callable[[Contact], bool]:
        predicates: list[Callable[[Contact], bool]] = []

        for field in self.query(Input):
            if field.id is None or len(field.value) == 0:
                continue

            predicates.append(self._build_predicate(field.id, field.value))

        def disjoined(x):
            return all(fn(x) for fn in predicates)

        return disjoined

    def _build_predicate(self, field_name: str, value: str):
        return lambda contact: self._clear_str(value) in self._clear_str(
            contact[field_name]
        )

    @classmethod
    def _clear_str(cls, string: str) -> str:
        return re.sub(r"\W+", "", string).lower()
