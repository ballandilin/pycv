from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path
from internal.tui.jobList import JobOffer


BASE = Path("~/dev/pycv/offres").expanduser()


def _dt(days: float = 0, hours: float = 0) -> datetime:
    return datetime(2026, 8, 10, 15, 23) - timedelta(days=days, hours=hours)


MOCK_OFFERS: list[JobOffer] = [
    # ── done : CV + lettre générés, Ok──────────────────────────
    JobOffer(
        title="Développeur Python Backend",
        company="Doctolib",
        source=BASE / "doctolib_python_backend.txt",
        cv_path=BASE / "doctolib_python_backend" / "cv_adapte.md",
        letter_path=BASE / "doctolib_python_backend" / "lettre.md",
        generated_at=_dt(hours=2),
        tokens=4820,
        tags=["remote", "senior"],
    ),
    JobOffer(
        title="Ingénieur Plateforme Data",
        company="Back Market",
        source=BASE / "backmarket_data_platform.md",
        cv_path=BASE / "backmarket_data_platform" / "cv_adapte.md",
        letter_path=BASE / "backmarket_data_platform" / "lettre.md",
        generated_at=_dt(days=1, hours=4),
        tokens=5310,
        tags=["hybride", "cdi"],
    ),
    JobOffer(
        title="Site Reliability Engineer",
        company="OVHcloud",
        source=BASE / "ovh_sre.txt",
        cv_path=BASE / "ovh_sre" / "cv_adapte.md",
        letter_path=BASE / "ovh_sre" / "lettre.md",
        generated_at=_dt(days=6),
        tokens=3990,
        tags=["lille"],
    ),
    # ── drift : la lettre a hérité/amplifié une dérive du CV ──────────────
    JobOffer(
        title="Lead Developer Full-Stack",
        company="Qonto",
        source=BASE / "qonto_lead_fullstack.txt",
        cv_path=BASE / "qonto_lead_fullstack" / "cv_adapte.md",
        letter_path=BASE / "qonto_lead_fullstack" / "lettre.md",
        generated_at=_dt(hours=6),
        tokens=6140,
        drift_flag=True,
        tags=["remote", "à-vérifier"],
    ),
    JobOffer(
        title="Architecte Cloud AWS",
        company="Theodo",
        source=BASE / "theodo_archi_cloud.md",
        cv_path=BASE / "theodo_archi_cloud" / "cv_adapte.md",
        letter_path=BASE / "theodo_archi_cloud" / "lettre.md",
        generated_at=_dt(days=2, hours=1),
        tokens=7025,
        drift_flag=True,
        tags=["certif-inventée"],
    ),
    # ── partial : CV seul (lettre pas encore lancée / échec) ──────────────
    JobOffer(
        title="Développeur Python / Django",
        company="Ubisoft",
        source=BASE / "ubisoft_django.txt",
        cv_path=BASE / "ubisoft_django" / "cv_adapte.md",
        letter_path=None,
        generated_at=_dt(minutes := 0, hours=0.5),
        tokens=2450,
        tags=["montpellier"],
    ),
    JobOffer(
        title="Data Engineer Spark",
        company="Carrefour",
        source=BASE / "carrefour_data_engineer.txt",
        cv_path=BASE / "carrefour_data_engineer" / "cv_adapte.md",
        letter_path=None,
        generated_at=_dt(days=3),
        tokens=2880,
        tags=[],
    ),
    # ── partial inverse : lettre sans CV (cas dégradé à détecter) ─────────
    JobOffer(
        title="Consultant DevOps",
        company="Sopra Steria",
        source=BASE / "sopra_devops.md",
        cv_path=None,
        letter_path=BASE / "sopra_devops" / "lettre.md",
        generated_at=_dt(days=4, hours=3),
        tokens=1620,
        tags=["esn"],
    ),
    # ── pending : rien de généré ──────────────────────────────────────────
    JobOffer(
        title="Développeur Rust Systèmes Embarqués",
        company="Ledger",
        source=BASE / "ledger_rust_embedded.txt",
    ),
    JobOffer(
        title="Machine Learning Engineer",
        company="Mistral AI",
        source=BASE / "mistral_mle.md",
        tags=["paris", "concurrentiel"],
    ),
    JobOffer(
        title="Tech Lead Node.js",
        company=None,  # entreprise non renseignée dans la description
        source=BASE / "offre_anonyme_techlead.txt",
    ),
    # ── cas limites d'affichage ───────────────────────────────────────────
    JobOffer(
        title="Ingénieur Développement Logiciel Senior — Plateforme "
        "Distribuée Temps Réel (H/F/NB)",
        company="Amadeus IT Group SAS France Sophia Antipolis",
        source=BASE / "amadeus_ingenieur_developpement_logiciel_senior_"
        "plateforme_distribuee_temps_reel.txt",
        cv_path=BASE / "amadeus" / "cv_adapte.md",
        letter_path=BASE / "amadeus" / "lettre.md",
        generated_at=_dt(days=9, hours=7),
        tokens=12480,
        tags=["nice", "anglais", "on-site", "grand-groupe", "process-long"],
    ),
    JobOffer(
        title="Dev",
        company="X",
        source=BASE / "dev.txt",
        cv_path=BASE / "dev" / "cv_adapte.md",
        letter_path=BASE / "dev" / "lettre.md",
        generated_at=_dt(days=0.02),
        tokens=890,
    ),
    JobOffer(
        title="Développeur Fullstack — Réf. #A/B[42]",  # test markup=False
        company="Société Générale",
        source=BASE / "socgen_fullstack.txt",
        tags=["markup-test"],
    ),
]
