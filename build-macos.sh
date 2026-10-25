#!/bin/sh
# Projeto macOS: Hiran Tiago Lins Borba — Toronto, ON, CA
# https://github.com/htiagolborba | Copyright (c) 2026
# Créditos e componentes de terceiros: CREDITS.md
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ -x "$PROJECT_DIR/.tools/sdl2/bin/sdl2-config" ]; then
  PATH="$PROJECT_DIR/.tools/sdl2/bin:$PATH"
  export PATH
fi
cd "$PROJECT_DIR/zelda3"
if ! xcode-select -p >/dev/null 2>&1; then
  echo 'Instale as Command Line Tools: xcode-select --install' >&2
  exit 1
fi
if ! command -v sdl2-config >/dev/null 2>&1; then
  echo 'Instale SDL2 e inclua seu bin no PATH: brew install sdl2' >&2
  exit 1
fi
if [ ! -s zelda3_assets.dat ]; then
  echo 'Pacote zelda3_assets.dat ausente; refaça a extração conforme README-macOS.md.' >&2
  exit 1
fi
make -j4 CC=clang SDLFLAGS="$(sdl2-config --static-libs) -lm"
