from __future__ import annotations

from internal.models.jobOffer import JobOffer

from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import ListItem, Static


class JobListItem(ListItem):
    """Item d'offre d'emploi pour un ListView pycv."""

    DEFAULT_CSS = """
    JobListItem {
        height: 5;
        layout: grid;
        grid-size: 3 2;
        grid-columns: 4 1fr 18;
        grid-rows: 1 1 1;
        padding: 0 1 1 1;
    }

    #icon {
        content-align: left bottom;
    }

    #title {
        column-span: 2;
        text-style: bold;
        content-align: left middle;
    }

    #meta {
        column-span: 4;
        color: $text-muted;
        content-align: left middle;
    }

    #badges {
        row-span: 2;
        dock: bottom;
        content-align: center bottom;
    }

    JobListItem.-done    #icon { color: $success; }
    JobListItem.-partial #icon { color: $warning; }
    JobListItem.-pending #icon { color: $text-disabled; }
    JobListItem.-drift   #icon { color: $error; }
    """

    ICONS = {
        "done": "✓",
        "partial": "◐",
        "pending": "○",
        "drift": "⚠",
    }

    offer: reactive[JobOffer | None] = reactive(None, layout=True)

    def __init__(self, offer: JobOffer, **kwargs) -> None:
        super().__init__(**kwargs)
        self.offer = offer

    def compose(self) -> ComposeResult:
        yield Static(id="icon")
        yield Static(id="title")
        yield Static(id="meta")
        yield Static(id="badges")

    def on_mount(self) -> None:
        self.refresh_content()

    def watch_offer(self) -> None:
        if self.is_mounted:
            self.refresh_content()

    def refresh_content(self) -> None:
        offer = self.offer
        if offer is None:
            return

        state = "drift" if offer.drift_flag else offer.status
        self.set_class(state == "done", "-done")
        self.set_class(state == "partial", "-partial")
        self.set_class(state == "pending", "-pending")
        self.set_class(state == "drift", "-drift")

        self.query_one("#icon", Static).update(self.ICONS[state])
        self.query_one("#title", Static).update(offer.title)
        self.query_one("#meta", Static).update(self._subtitle(offer))
        self.query_one("#badges", Static).update(self._badges(offer))

        self.tooltip = str(offer.source)

    def _subtitle(self, offer: JobOffer) -> Text:
        parts: list[str] = []
        if offer.company:
            parts.append(offer.company)
        parts.append(offer.source.name)
        if offer.generated_at:
            parts.append(offer.generated_at.strftime("%d/%m %H:%M"))
        if offer.tokens:
            parts.append(f"{offer.tokens:,} tok".replace(",", " "))
        return Text(" · ".join(parts), overflow="ellipsis", no_wrap=True)

    def _badges(self, offer: JobOffer) -> Text:
        text = Text()
        text.append("CV ", style="dim")
        text.append(
            "✓" if offer.has_cv else "✗",
            style="green" if offer.has_cv else "red dim",
        )
        text.append("   LM ", style="dim")
        text.append(
            "✓" if offer.has_letter else "✗",
            style="green" if offer.has_letter else "red dim",
        )
        if offer.tags:
            text.append("  " + " ".join(f"#{t}" for t in offer.tags), style="cyan dim")
        return text
