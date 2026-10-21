"""Assemble the content one audience is allowed to see, ready for Quartz to render.

    python tools/build_tier.py --tier public        --out build/public
    python tools/build_tier.py --tier collaboration --out build/collaboration
    python tools/build_tier.py --tier internal      --out build/internal

A note is included when its `access` is at least as open as the tier being built.
Attachments inherit the access of the record note in their folder. Links to
anything outside the tier are replaced by a lock and the record ID, so a public
page never reveals the title or content of an internal one.
"""

import argparse
import re
import shutil
from pathlib import Path

import yaml

from archive import LEVELS, SCHEMA, VAULT, WIKILINK, Resolver, load_notes, other_files

TIER_LABEL = {"internal": "Group-internal", "collaboration": "Collaboration", "public": "Public"}
TIER_PATH = {"public": "", "collaboration": "collab/", "internal": "internal/"}
HIDDEN_FIELDS = {"title", "tags", "aliases", "cssclasses"}
UNNUMBERED = {"index", "person", "project"}  # page titles that don't get the record ID prefixed


def fmt(value):
    if isinstance(value, list):
        return ", ".join(fmt(v) for v in value)
    if isinstance(value, dict):
        return "; ".join(f"{k}: {fmt(v)}" for k, v in value.items())
    return str(value)


def cell(value):
    return re.sub(r"(?<!\\)\|", r"\\|", fmt(value)).replace("\n", " ")


# --- Obsidian Bases -> static tables -----------------------------------------
def base_matches(expr, note):
    if isinstance(expr, dict):
        (op, items), = expr.items()
        results = [base_matches(e, note) for e in items]
        return {"and": all, "or": any}.get(op, lambda r: not any(r))(results)
    expr = expr.strip()
    if m := re.fullmatch(r'(?:note\.)?([\w.]+)\s*(==|!=)\s*"([^"]*)"', expr):
        equal = fmt(note.meta.get(m.group(1), "")) == m.group(3)
        return equal if m.group(2) == "==" else not equal
    if m := re.fullmatch(r'file\.inFolder\("([^"]*)"\)', expr):
        return note.rel.startswith(m.group(1).rstrip("/") + "/")
    if m := re.fullmatch(r'file\.hasTag\("([^"]*)"\)', expr):
        return m.group(1) in (note.meta.get("tags") or [])
    raise ValueError(f"unsupported Bases filter for the static site: {expr}")


def render_base(path, view_name, notes):
    spec = yaml.safe_load(path.read_text()) or {}
    views = spec.get("views", [{}])
    view = next((v for v in views if v.get("name") == view_name), views[0])
    filters = [f for f in (spec.get("filters"), view.get("filters")) if f]
    rows = [n for n in notes if all(base_matches(f, n) for f in filters)]
    for s in reversed(view.get("sort", [])):
        prop = s["property"].removeprefix("note.")
        rows.sort(key=lambda n: fmt(n.meta.get(prop, "")), reverse=s.get("direction") == "DESC")
    cols = view.get("order", ["file.name"])
    props = spec.get("properties", {})

    def header(c):
        return props.get(c, {}).get("displayName") or {"file.name": "Record"}.get(c, c.removeprefix("note."))

    def value(n, c):
        return f"[[{n.path.stem}]]" if c == "file.name" else n.meta.get(c.removeprefix("note."), "")

    lines = ["| " + " | ".join(header(c) for c in cols) + " |", "|" + " --- |" * len(cols)]
    lines += ["| " + " | ".join(cell(value(n, c)) for c in cols) + " |" for n in rows[: view.get("limit")]]
    if not rows:
        lines.append("| *(no records visible at this access level)* |" + " |" * (len(cols) - 1))
    return "\n".join(lines)


# --- per-note rewriting -------------------------------------------------------
def build(tier, out, site_root):
    floor = LEVELS.index(tier)
    notes = load_notes()
    files = other_files()
    resolve = Resolver(notes, files)
    by_path = {n.path: n for n in notes}
    visible = [n for n in notes if n.level >= floor]
    visible_paths = {n.path for n in visible}

    def file_visible(f):
        owners = [n for n in notes if n.path.parent == f.parent]
        return any(o.path in visible_paths for o in owners) if owners else True

    def rewrite_link(m):
        embed, target, anchor, alias = m.groups()
        path = resolve(target)
        if path is None:
            return m.group(0)
        if path.suffix == ".base":
            return render_base(path, anchor.lstrip("#"), visible) if embed else f"*{path.stem} catalogue*"
        if path in by_path and path not in visible_paths:
            rid = by_path[path].meta.get("id", "record")
            return f"🔒 `{rid}` *(restricted)*"
        if path not in by_path and not file_visible(path):
            return "🔒 *restricted file*"
        return m.group(0)

    strip = set(SCHEMA["private_fields"]) if tier != "internal" else set()
    switcher = " · ".join(f"[{TIER_LABEL[t]}]({site_root.rstrip('/')}/{TIER_PATH[t]})"
                          for t in ("public", "collaboration", "internal")) if site_root else ""

    shutil.rmtree(out, ignore_errors=True)
    for note in visible:
        meta = {k: v for k, v in note.meta.items() if k not in strip}
        rows = [(k, v) for k, v in meta.items() if k not in HIDDEN_FIELDS and k != "synthetic"]
        banner = [f"> [!info] Viewing as **{TIER_LABEL[tier]}** · demo archive, all data synthetic"]
        if switcher:
            banner.append(f"> Switch audience: {switcher}")
        table = ["> [!abstract]- Record metadata", "> | Field | Value |", "> | --- | --- |"]
        table += [f"> | `{k}` | {cell(v)} |" for k, v in rows]
        rtype = note.meta.get("type")
        body = "\n".join(banner) + "\n\n"
        if rtype not in ("index", None):
            body += "\n".join(table) + "\n\n"
        body += re.sub(r"\A\s*# .*\n", "", note.body)  # Quartz renders the title itself
        body = WIKILINK.sub(rewrite_link, body)

        front = {k: meta[k] for k in ("title", "tags", "aliases", "created") if k in meta}
        if rtype not in UNNUMBERED and "id" in meta:
            front["title"] = f"{meta['id']} · {meta.get('title', note.path.stem)}"
        dest = out / note.rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("---\n" + yaml.safe_dump(front, sort_keys=False, allow_unicode=True) + "---\n" + body,
                        encoding="utf-8")

    copied = 0
    for f in files:
        if f.suffix != ".base" and file_visible(f):
            dest = out / f.relative_to(VAULT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dest)
            copied += 1
    print(f"{TIER_LABEL[tier]} tier: {len(visible)}/{len(notes)} notes, {copied} attachments -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tier", choices=LEVELS, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--site-root", default="", help="base URL, used for the audience switcher links")
    args = ap.parse_args()
    build(args.tier, args.out, args.site_root)
