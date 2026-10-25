#!/bin/sh
set -eu
CONTENTS=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DATA_DIR="$HOME/Library/Application Support/Zelda ALttP"
mkdir -p "$DATA_DIR"
cd "$DATA_DIR"
if [ ! -s zelda3_assets.dat ]; then
  echo 'Missing game assets. Follow the package README.md to extract your ROM.' >&2
  exit 1
fi
if [ ! -f zelda3.ini ]; then cp "$CONTENTS/Resources/zelda3.ini" zelda3.ini; fi
exec "$CONTENTS/MacOS/zelda3" --config "$DATA_DIR/zelda3.ini"
