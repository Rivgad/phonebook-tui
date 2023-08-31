from contact import Contact

from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.validation import Length
from textual.widgets import Footer, Input, Pretty


class EditScreen(ModalScreen[Contact | None]):
    """Screen with a dialog to quit."""

    contact: Contact
    _validation_errors: dict[str, list[str]] = {}

    BINDINGS = [("ctrl+q, escape", "back", "Back"), ("ctrl+s", "save", "Save")]

    def __init__(
        self,
        contact: Contact,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        self.contact = contact
        super().__init__(name, id, classes)

    def compose(self) -> ComposeResult:
        with Grid(id="edit_screen_grid"):
            yield Input(
                self.contact.first_name,
                placeholder="Имя",
                id="first_name",
                validators=Length(
                    minimum=1, failure_description="Имя не может быть пустым"
                ),
            )
            yield Input(
                self.contact.last_name,
                placeholder="Фамилия",
                id="last_name",
                validators=Length(
                    minimum=1, failure_description="Фамилия не может быть пустой"
                ),
            )
            yield Input(
                self.contact.patronymic,
                placeholder="Отчество",
                id="patronymic",
            )
            yield Input(
                self.contact.organization,
                placeholder="Организация",
                id="organization",
            )
            yield Input(
                self.contact.work_phone,
                placeholder="Рабочий телефон",
                id="work_phone",
            )
            yield Input(
                self.contact.personal_phone,
                placeholder="Телефон (личный)",
                id="personal_phone",
            )
        yield Pretty([])
        yield Footer()

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id is None:
            return

        setattr(self.contact, event.input.id, event.value)
        self.validate()

    @on(Input.Submitted)
    def on_input_submitted(self, _: Input.Submitted) -> None:
        self.focus_next()

    def validate(self) -> bool:
        validation_result: bool = True

        for input in self.query(Input):
            if input.id is None:
                continue

            result = input.validate(input.value)
            if result is None:
                continue
            if not result.is_valid:
                self._validation_errors[input.id] = [
                    x.description for x in result.failures if x.description is not None
                ]
                validation_result = False
            else:
                if input.id in self._validation_errors.keys():
                    self._validation_errors.pop(input.id)

        self.query_one(Pretty).update(
            [value for _, errors in self._validation_errors.items() for value in errors]
        )

        return validation_result

    def action_save(self) -> None:
        if self.validate():
            self.dismiss(self.contact)
        else:
            pass
