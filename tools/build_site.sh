#!/usr/bin/env bash
# Build one website per audience into _site/:
#   _site/            public
#   _site/collab/     collaboration   (production: behind the login gate, not here)
#   _site/internal/   group-internal  (production: behind the login gate, not here)
#
#   tools/build_site.sh                      # all three tiers
#   TIERS=public tools/build_site.sh         # just one
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
QUARTZ_VERSION=v4.5.2
QUARTZ=${QUARTZ_DIR:-$ROOT/.quartz}
SITE_ROOT=${SITE_ROOT:-https://msekatchev.github.io/group-archive-demo}
TIERS=${TIERS:-"public collaboration internal"}

if [ ! -d "$QUARTZ" ]; then
  git clone --quiet --depth 1 --branch "$QUARTZ_VERSION" https://github.com/jackyzha0/quartz.git "$QUARTZ"
  (cd "$QUARTZ" && npm ci --silent)
fi
cp "$ROOT/site/quartz.config.ts" "$ROOT/site/quartz.layout.ts" "$QUARTZ/"

cd "$ROOT"
python3 tools/validate.py
rm -rf build _site

# Public goes first: Quartz empties its output folder, which would wipe the sub-sites.
for tier in $TIERS; do
  case $tier in
    public) sub="" ;;
    collaboration) sub="collab" ;;
    internal) sub="internal" ;;
  esac
  python3 tools/build_tier.py --tier "$tier" --out "build/$tier" --site-root "$SITE_ROOT"
  (cd "$QUARTZ" && ARCHIVE_TIER=$tier ARCHIVE_BASE_URL="${SITE_ROOT#*://}${sub:+/$sub}" \
    npx quartz build -d "$ROOT/build/$tier" -o "$ROOT/_site/$sub" >/dev/null)
  echo "  built _site/$sub"
done
