#!/usr/bin/env bash
# macOS/Windows adaptation: Hiran Tiago Lins Borba, Toronto, ON, CA.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CC="${WINDOWS_CC:-x86_64-w64-mingw32-gcc}"
WINDRES="${WINDOWS_WINDRES:-x86_64-w64-mingw32-windres}"
: "${SDL2_WINDOWS_PREFIX:?Set SDL2_WINDOWS_PREFIX to the Windows x86_64 SDL2 development prefix}"
mkdir -p "$ROOT/build/windows"
cd "$ROOT/zelda3"
"$WINDRES" "$ROOT/packaging/windows.rc" -O coff -o "$ROOT/build/windows/zelda3.res"
"$CC" -O2 -Werror -DSYSTEM_VOLUME_MIXER_AVAILABLE=0 -DSDL_MAIN_HANDLED \
  -I . -I "$SDL2_WINDOWS_PREFIX/include/SDL2" \
  src/*.c snes/*.c third_party/gl_core/gl_core_3_1.c \
  third_party/opus-1.3.1-stripped/opus_decoder_amalgam.c \
  "$ROOT/build/windows/zelda3.res" -L "$SDL2_WINDOWS_PREFIX/lib" \
  -lSDL2 -lm -o "$ROOT/build/windows/zelda3.exe"
cp "$SDL2_WINDOWS_PREFIX/bin/SDL2.dll" "$ROOT/build/windows/SDL2.dll"
echo "Windows x86_64 build: $ROOT/build/windows/zelda3.exe"
