from contact import Contact

from textual import on
from textual.app import ComposeResult
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable
from textual.widgets.data_table import RowDoesNotExist


FIELD_LABEL_BINDINGS = {
    "id": "Id",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "patronymic": "Отчество",
    "organization": "Организация",
    "work_phone": "Рабочий телефон",
    "personal_phone": "Телефон (личный)",
}


class ContactsTable(Widget):
    _data_table: DataTable[str]
    contacts = reactive[list[Contact]]([], layout=True)

    BINDINGS = [
        ("ENTER", "action_edit", "Edit"),
        ("i, I, ш, Ш", "insert", "Insert"),
        ("d, D, в, В, del", "delete", "Delete"),
    ]

    class EditRequested(Message):
        def __init__(self, contact: Contact):
            self.contact = contact
            super().__init__()

    class InsertRequested(Message):
        pass

    class DeleteRequested(Message):
        def __init__(self, contact_id: int):
            self.contact_id = contact_id
            super().__init__()

    @property
    def data_table(self) -> DataTable[str]:
        return self._data_table

    def compose(self) -> ComposeResult:
        self._data_table = DataTable[str]()
        self.data_table.cursor_type = "row"
        yield self.data_table

    def on_mount(self) -> None:
        for field_name, label in FIELD_LABEL_BINDINGS.items():
            self.data_table.add_column(label, key=field_name)

    def focus(self, scroll_visible: bool = True):
        self.screen.set_focus(self.data_table, scroll_visible)
        return self

    def watch_contacts(self, contacts: list[Contact]) -> None:
        self.data_table.clear()
        for contact in contacts:
            self.data_table.add_row(
                *[str(value) for _, value in contact.to_dict().items()],
                key=str(contact.id)
            )

    def action_insert(self):
        self.post_message(self.InsertRequested())

    @on(DataTable.RowSelected)
    def action_edit(self, event: DataTable.RowSelected) -> None:
        if event.row_key.value is None:
            return

        id = int(event.row_key.value)
        contact = next(filter(lambda contact: contact.id == id, self.contacts), None)
        if contact is None:
            return

        self.post_message(self.EditRequested(contact))

    def action_delete(self):
        try:
            id = int(self.data_table.get_row_at(self.data_table.cursor_row)[0])
            self.post_message(self.DeleteRequested(id))
        except RowDoesNotExist:
            pass
