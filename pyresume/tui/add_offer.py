from pathlib import Path

from pyresume.models import JobOffer
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class AddOfferScreen(ModalScreen[JobOffer | None]):
    CSS_PATH = "../../style/add_offer_modal.tcss"

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Add a new job offer", id="question"),
            Input(placeholder="Title *", id="title"),
            Input(placeholder="Company", id="company"),
            Input(placeholder="Offer file path *", id="source"),
            Input(placeholder="Tags (comma separated)", id="tags"),
            Button("Add", variant="primary", id="add"),
            Button("Cancel", variant="default", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        else:
            self._submit()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._submit()

    def _submit(self) -> None:
        title = self.query_one("#title", Input).value.strip()
        source = self.query_one("#source", Input).value.strip()
        if not title:
            self.notify("Title is required", severity="error")
            return
        path = Path(source).expanduser()
        if not source or not path.is_file():
            self.notify(f"Offer file not found: {source}", severity="error")
            return

        self.dismiss(
            JobOffer(
                title=title,
                source=path,
                company=self.query_one("#company", Input).value.strip() or None,
                tags=[
                    t.strip()
                    for t in self.query_one("#tags", Input).value.split(",")
                    if t.strip()
                ],
            )
        )
