from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


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
