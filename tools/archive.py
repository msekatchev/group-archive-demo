"""Shared helpers for reading the Obsidian vault: notes, front matter and wikilinks."""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
SCHEMA = yaml.safe_load((ROOT / "schema/record-types.yaml").read_text())
LEVELS = SCHEMA["access_levels"]  # index 0 = most restricted
SKIP_DIRS = {".obsidian", ".trash", "Templates"}

WIKILINK = re.compile(r"(!?)\[\[([^\[\]|#^]+)((?:[#^][^\[\]|]*)?)((?:\\?\|[^\[\]]*)?)\]\]")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


@dataclass
class Note:
    path: Path
    meta: dict
    body: str
    errors: list = field(default_factory=list)

    @property
    def rel(self):
        return self.path.relative_to(VAULT).as_posix()

    @property
    def access(self):
        return self.meta.get("access", SCHEMA["default_access"])

    @property
    def level(self):
        return LEVELS.index(self.access) if self.access in LEVELS else 0


def skipped(path):
    return any(part in SKIP_DIRS for part in path.relative_to(VAULT).parts)


def load_notes():
    notes = []
    for path in sorted(VAULT.rglob("*.md")):
        if skipped(path):
            continue
        text = path.read_text(encoding="utf-8")
        m = FRONTMATTER.match(text)
        note = Note(path, {}, text[m.end():] if m else text)
        if not m:
            note.errors.append("missing front matter")
        else:
            try:
                note.meta = yaml.safe_load(m.group(1)) or {}
            except yaml.YAMLError as exc:
                note.errors.append(f"front matter is not valid YAML: {exc}")
        notes.append(note)
    return notes


def other_files():
    return sorted(p for p in VAULT.rglob("*")
                  if p.is_file() and p.suffix != ".md" and not skipped(p) and p.name != ".DS_Store")


class Resolver:
    """Resolve wikilink targets the way Obsidian does ('shortest path when possible')."""

    def __init__(self, notes, files):
        self.by_name = {}
        for n in notes:
            self.by_name.setdefault(n.path.stem.lower(), []).append(n.path)
            self.by_name.setdefault(n.path.name.lower(), []).append(n.path)
        for f in files:
            self.by_name.setdefault(f.name.lower(), []).append(f)

    def __call__(self, target):
        target = target.strip()
        key = target.split("/")[-1].lower()
        hits = self.by_name.get(key, [])
        if len(hits) > 1:
            hits = [h for h in hits if h.as_posix().lower().endswith(target.lower())] or hits
        return hits[0] if hits else None


def links_in(value):
    """Yield every wikilink match in a string, or in strings nested in lists/dicts."""
    if isinstance(value, str):
        yield from WIKILINK.finditer(value)
    elif isinstance(value, list):
        for v in value:
            yield from links_in(v)
    elif isinstance(value, dict):
        for v in value.values():
            yield from links_in(v)
