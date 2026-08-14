from __future__ import annotations

from datetime import datetime

from internal.models.jobOffer import JobOffer

from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import ListItem, Static


def _age(when: datetime) -> str:
    seconds = max(0.0, (datetime.now() - when).total_seconds())
    if seconds < 3600:
        return f"{int(seconds // 60)}min"
    if seconds < 86400:
        return f"{int(seconds // 3600)}h"
    return f"{int(seconds // 86400)}j"


class JobListItem(ListItem):
    DEFAULT_CSS = """
    JobListItem {
        height: 4;
        layout: grid;
        grid-size: 2 3;
        grid-columns: 4 1fr;
        grid-rows: 1 1 1;
        padding: 0 1 1 0;
    }

    #icon {
        row-span: 3;
        content-align: center top;
    }

    #title {
        text-style: bold;
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }

    #meta, #badges {
        text-wrap: nowrap;
        text-overflow: ellipsis;
    }

    #meta {
        color: $text-muted;
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
        # le chemin complet reste dans le tooltip : ici on garde ce qui
        # distingue l'offre, pas ce qui remplit la ligne
        parts: list[str] = [offer.company or offer.source.name]
        if offer.generated_at:
            parts.append(_age(offer.generated_at))
        if offer.tokens:
            parts.append(f"{offer.tokens:,} tok".replace(",", " "))
        return Text(" · ".join(parts), overflow="ellipsis", no_wrap=True)

    def _badges(self, offer: JobOffer) -> Text:
        text = Text(overflow="ellipsis", no_wrap=True)
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
