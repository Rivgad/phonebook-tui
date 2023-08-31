from typing import Callable
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input
from textual.reactive import reactive

from contacts_repository import ContactsRepository
from contact import Contact
from edit_screen import EditScreen
from filter import Filter
from contacts_table import ContactsTable

FILE_NAME = "phonebook.csv"


class PhonebookApp(App):
    filter_predicate = reactive[Callable[[Contact], bool]](
        lambda: lambda _: True, always_update=True
    )

    CSS_PATH = "main.tcss"

    BINDINGS = [
        ("q, ctrl+q, escape", "quit", "Quit"),
        ("f, F, а, А", "focus_on_filter", "Filter"),
    ]

    def __init__(self, file_name: str, **kwargs):
        self.repository = ContactsRepository(file_name)

        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        self.title = "Телефонный справочник"

        yield Header()
        yield Filter(classes="hide")
        yield ContactsTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.get_table()
        table.contacts = self.repository.all()
        table.focus()

    def get_table(self) -> ContactsTable:
        return self.query_one(ContactsTable)

    def refresh_contacts(self) -> None:
        self.get_table().contacts = list(self.repository.query(self.filter_predicate))

    def watch_filter_predicate(self, _) -> None:
        self.refresh_contacts()

    @on(ContactsTable.EditRequested)
    def on_edit_requested(self, event: ContactsTable.EditRequested) -> None:
        def get_result(contact: Contact | None) -> None:
            if contact is None:
                return
            self.repository.update(contact.id, contact.to_dict())
            self.refresh_contacts()

        self.push_screen(EditScreen(event.contact, id="edit_screen"), get_result)

    @on(ContactsTable.InsertRequested)
    def on_insert_requested(self, _: ContactsTable.InsertRequested):
        def get_result(contact: Contact | None) -> None:
            if contact is None:
                return
            self.repository.insert(contact)
            self.refresh_contacts()

        self.push_screen(EditScreen(Contact(0, "", ""), id="edit_screen"), get_result)

    @on(ContactsTable.DeleteRequested)
    def on_delete_requested(self, event: ContactsTable.DeleteRequested):
        self.repository.delete(event.contact_id)
        self.refresh_contacts()

    def action_focus_on_filter(self):
        filter = self.query_one(Filter)
        self.set_focus(filter.query(Input)[0])

    @on(Filter.Changed)
    def on_filter_changed(self, event: Filter.Changed):
        self.filter_predicate = event.predicate

    @on(Filter.RequestBack)
    def on_filter_request_back(self, _: Filter.RequestBack):
        self.get_table().focus()


app = PhonebookApp(FILE_NAME)
if __name__ == "__main__":
    app.run()
