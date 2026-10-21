"""Check every record in the vault against schema/record-types.yaml.

Errors (exit code 1) block a merge; warnings are printed but allowed.
Run locally before pushing:  python tools/validate.py
"""

import os
import re
import sys
from collections import Counter

from archive import LEVELS, SCHEMA, Resolver, links_in, load_notes, other_files

GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"
NO_ID_IN_FILENAME = {"project", "person", "index"}


def report(kind, rel, msg):
    if GITHUB:
        print(f"::{kind} file=vault/{rel}::{msg}")
    else:
        print(f"{kind.upper():7} {rel}: {msg}")


def main():
    notes = load_notes()
    files = other_files()
    resolve = Resolver(notes, files)
    by_path = {n.path: n for n in notes}
    errors = warnings = 0

    def err(note, msg):
        nonlocal errors
        errors += 1
        report("error", note.rel, msg)

    def warn(note, msg):
        nonlocal warnings
        warnings += 1
        report("warning", note.rel, msg)

    id_counts = Counter(n.meta.get("id") for n in notes if n.meta.get("id"))

    for note in notes:
        for e in note.errors:
            err(note, e)
        meta, rtype = note.meta, note.meta.get("type")
        spec = SCHEMA["types"].get(rtype)
        if spec is None:
            err(note, f"unknown record type '{rtype}' (see schema/record-types.yaml)")
            continue

        required = SCHEMA["common_required"] + spec.get("required", [])
        method = meta.get("method")
        if rtype == "measurement" and method:
            if method not in spec["method_required"]:
                err(note, f"unknown measurement method '{method}'")
            required += spec["method_required"].get(method, [])
        for key in required:
            if meta.get(key) in (None, "", []):
                err(note, f"missing required field '{key}'")

        rid = str(meta.get("id", ""))
        if rid and not re.match(spec["id_pattern"], rid):
            err(note, f"id '{rid}' does not match {spec['id_pattern']}")
        if id_counts.get(rid, 0) > 1:
            err(note, f"id '{rid}' is used by more than one note")
        if rid and rtype not in NO_ID_IN_FILENAME and not note.path.stem.startswith(rid):
            err(note, f"note filename should start with its id '{rid}'")
        if note.access not in LEVELS:
            err(note, f"access must be one of {LEVELS}, got '{note.access}'")

        raw = meta.get("raw_data")
        if rtype == "measurement" and raw not in (None, "none"):
            if not isinstance(raw, dict) or not raw.get("location") or not raw.get("sha256"):
                err(note, "raw_data needs 'location' and 'sha256' (or the value 'none')")

        if rtype == "dataset" and note.access == "public":
            if "placeholder" in str(meta.get("doi", "")).lower():
                warn(note, "public dataset still has a placeholder DOI — mint one on Zenodo before release")

        restricted = {}
        for m in links_in([meta, note.body]):
            target = resolve(m.group(2))
            if target is None:
                err(note, f"broken link [[{m.group(2)}]]")
                continue
            linked = by_path.get(target)
            if linked and linked.level < note.level:
                restricted[linked.meta.get("id", target.stem)] = linked.access
        if restricted:
            listed = ", ".join(f"{rid} ({acc})" for rid, acc in restricted.items())
            warn(note, f"links to more restricted notes, shown as 🔒 on the {note.access} site: {listed}")

    # Every attachment must carry the ID of the record that owns its folder.
    pattern = SCHEMA["file_name_pattern"]
    for f in files:
        owners = [n for n in notes if n.path.parent == f.parent and n.meta.get("id")]
        if f.suffix == ".base" or not owners:
            continue
        rid = owners[0].meta["id"]
        if not re.match(pattern.format(id=re.escape(rid)), f.name):
            err(owners[0], f"attachment '{f.name}' must be named '{rid}_<descriptor>.<ext>' "
                           "(no spaces, lowercase extension)")

    print(f"\n{len(notes)} notes, {len(files)} attachments checked: "
          f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
