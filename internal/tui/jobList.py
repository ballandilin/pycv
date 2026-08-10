from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import ListItem, Static


@dataclass
class JobOffer:
    """Modèle de données d'une offre traitée par pycv."""

    title: str
    source: Path
    cv_path: Path | None = None
    letter_path: Path | None = None
    company: str | None = None
    generated_at: datetime | None = None
    tokens: int | None = None
    drift_flag: bool = False
    tags: list[str] = field(default_factory=list)

    @property
    def has_cv(self) -> bool:
        return self.cv_path is not None and self.cv_path.exists()

    @property
    def has_letter(self) -> bool:
        return self.letter_path is not None and self.letter_path.exists()

    @property
    def status(self) -> str:
        """pending | partial | done"""
        if self.has_cv and self.has_letter:
            return "done"
        if self.has_cv or self.has_letter:
            return "partial"
        return "pending"


class JobListItem(ListItem):
    """Item d'offre d'emploi pour un ListView pycv."""

    DEFAULT_CSS = """
    JobListItem {
        height: 4;
    }
    JobListItem > Horizontal {
        height: 100%;
    }
    JobListItem .status-icon {
        width: 4;
        content-align: center middle;
    }
    JobListItem .body {
        width: 1fr;
        height: 100%;
    }
    JobListItem .title {
        text-style: bold;
    }
    JobListItem .subtitle {
        color: $text-muted;
    }
    JobListItem .badges {
        width: auto;
        content-align: right middle;
        padding-right: 1;
    }

    JobListItem.-done   .status-icon { color: $success; }
    JobListItem.-partial .status-icon { color: $warning; }
    JobListItem.-pending .status-icon { color: $text-disabled; }
    JobListItem.-drift   .status-icon { color: $error; }
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
        with Horizontal():
            yield Static(id="icon", classes="status-icon")
            with Vertical(classes="body"):
                yield Static(id="title", classes="title")
                yield Static(id="subtitle", classes="subtitle")
            yield Static(id="badges", classes="badges")

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
        self.query_one("#subtitle", Static).update(self._subtitle(offer))
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

