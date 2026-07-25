import tomllib
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "prompts.toml"

def load_config(path: Path = CONFIG_PATH) -> dict:
    try:
        with path.open("rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        raise SystemExit(f"Configuration introuvable : {path}")
    except tomllib.TOMLDecodeError as exc:
        raise SystemExit(f"Configuration invalide : {exc}")

    for kind in ("cv", "letter"):
        section = config[kind]
        section["system"] = section["system"].strip()
        section["user"] = section["user"].strip()
        for placeholder in ("{cv}", "{job}"):
            if placeholder not in section["user"]:
                raise SystemExit(f"[{kind}] user doit contenir {placeholder}")
    return config
