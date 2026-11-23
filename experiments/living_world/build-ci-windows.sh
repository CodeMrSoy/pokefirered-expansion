#!/usr/bin/env bash
# Build a candidate on Linux, then test the unchanged ZIP on a Windows runner.
set -euo pipefail
root=$(pwd)
app="$root/experiments/living_world"
output=$(realpath -m "$1")
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
inputs="$work/inputs"
mkdir -p "$inputs/licenses"

fetch() {
    echo "Fetching ${2##*/}"
    curl -fLsS --retry 3 --output "$2" "$1"
}

fetch https://raw.githubusercontent.com/libsdl-org/SDL/release-2.32.10/LICENSE.txt "$inputs/licenses/SDL-LICENSE.txt"
fetch https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip "$inputs/python-win.zip"
fetch https://libsdl.org/release/SDL2-2.32.10-win32-x64.zip "$inputs/sdl-win.zip"
weights=https://huggingface.co/unsloth/Qwen3-0.6B-GGUF
model=626eb58354de1127ccd7a9dc213485a3b716534c
fetch "$weights/resolve/$model/Qwen3-0.6B-Q4_K_M.gguf" "$inputs/model-q4.gguf"
fetch https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/LICENSE "$inputs/licenses/Qwen-LICENSE.txt"

mingw=llvm-mingw-20251007-ucrt-ubuntu-22.04-x86_64
fetch "https://github.com/mstorsjo/llvm-mingw/releases/download/20251007/$mingw.tar.xz" "$work/mingw.tar.xz"
echo "ee1c1f3e4a584f231b1d664eb1f4b9d9f7cae133b64b55dae749f50969cef958  $work/mingw.tar.xz" | sha256sum -c
tar -xJf "$work/mingw.tar.xz" -C "$work"
target="$work/$mingw/bin/x86_64-w64-mingw32"
win_cmake=(-DCMAKE_SYSTEM_NAME=Windows "-DCMAKE_C_COMPILER=$target-clang" "-DCMAKE_CXX_COMPILER=$target-clang++"
           "-DCMAKE_RC_COMPILER=$target-windres" -DCMAKE_BUILD_TYPE=Release)

mgba=7a12d6d4b9acb14c0ae62c9166b6a2f3d08007f6
llama=a7a98e0fffed794396b3fbad4dcdbbc184963645
git init -q "$work/mgba"
git -C "$work/mgba" fetch -q --depth=1 https://github.com/mgba-emu/mgba.git "$mgba"
git -C "$work/mgba" checkout -q FETCH_HEAD
git init -q "$work/llama"
git -C "$work/llama" fetch -q --depth=1 https://github.com/ggml-org/llama.cpp.git "$llama"
git -C "$work/llama" checkout -q FETCH_HEAD

mgba_options=(-DSKIP_LIBRARY=ON -DBUILD_LIBRETRO=ON -DDISABLE_DEPS=ON -DBUILD_SDL=OFF -DBUILD_QT=OFF -DBUILD_GL=OFF -DBUILD_GLES2=OFF
              -DBUILD_GLES3=OFF -DBUILD_LTO=OFF -DUSE_PNG=OFF -DUSE_ZLIB=OFF -DUSE_LIBZIP=OFF
              -DUSE_MINIZIP=OFF -DUSE_FFMPEG=OFF -DUSE_LUA=OFF -DUSE_SQLITE3=OFF -DUSE_ELF=OFF)
cmake -S "$work/mgba" -B "$work/mgba-win" "${win_cmake[@]}" "${mgba_options[@]}"
cmake --build "$work/mgba-win" --target mgba_libretro --parallel 4
cp "$work/mgba-win/mgba_libretro.dll" "$inputs/mgba_libretro.dll"
cmake -S "$work/mgba" -B "$work/mgba-linux" -DCMAKE_BUILD_TYPE=Release "${mgba_options[@]}"
cmake --build "$work/mgba-linux" --target mgba_libretro --parallel 4

cmake -S "$work/llama" -B "$work/llama-win" "${win_cmake[@]}" -DBUILD_SHARED_LIBS=OFF \
    -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_TOOLS=OFF \
    -DLLAMA_BUILD_SERVER=OFF -DGGML_OPENMP=OFF -DGGML_NATIVE=OFF -DGGML_AVX=OFF -DGGML_AVX2=OFF \
    -DGGML_BMI2=OFF -DGGML_FMA=OFF -DGGML_F16C=OFF -DGGML_LLAMAFILE=OFF
cmake --build "$work/llama-win" --target llama --parallel 4
"$target-clang++" -std=c++17 -O2 -static -municode -I"$work/llama/include" -I"$work/llama/ggml/include" \
    "$app/offline-worker.cpp" "$work/llama-win/src/libllama.a" "$work/llama-win/ggml/src/ggml.a" \
    "$work/llama-win/ggml/src/ggml-cpu.a" "$work/llama-win/ggml/src/ggml-base.a" -o "$inputs/offline-worker.exe"
"$target-clang" -std=c11 -O2 -municode "$app/sandbox-win.c" -luserenv -ladvapi32 -o "$inputs/sandbox.exe"
"$target-clang" -std=c11 -O2 -municode "$app/security_probe.c" -lws2_32 -o "$inputs/sandbox-probe.exe"
cp "$work/llama/LICENSE" "$inputs/licenses/llama.cpp-LICENSE.txt"
cp "$work/mgba/LICENSE" "$inputs/licenses/mGBA-LICENSE.txt"


make -j4 > "$root/rom-build.log" 2>&1 || { tail -80 "$root/rom-build.log"; exit 1; }
export MGBA_CORE="$work/mgba-linux/mgba_libretro.so" ADVENTURE_TEST_MODE=1
export ARM_NM=arm-none-eabi-nm
export WORLD_CATALOG="$root/phase17-catalog.json"
python -B "$app/build-world-catalog.py" "$root/pokefirered.gba" "$root/pokefirered.elf" "$WORLD_CATALOG"
for mode in 0 1; do
    ADVENTURE_TEST_MODE=$mode QUANTUM_QA_OUTPUT="$work/native-world-$mode" \
        WORLD_EXAMPLE="$root/phase17-initial-world-example.json" python -B tests/living_world_native_manifest.py
done
WORLD_TEST_NO_RANDOMIZER=1 ADVENTURE_TEST_MODE=0 QUANTUM_QA_OUTPUT="$work/native-world-authored" \
    python -B tests/living_world_native_manifest.py
WORLD_TEST_PROTECT=1 ADVENTURE_TEST_MODE=1 QUANTUM_QA_OUTPUT="$work/native-world-protected" \
    python -B tests/living_world_native_manifest.py
export QUANTUM_QA_OUTPUT="$work/fixture-logs"
LIVING_WORLD_TEST_SAVE="$inputs/PalletTest.sav" python -B tests/living_world_bridge_emulator.py
LIVING_WORLD_TEST_SAVE="$inputs/PalletSocialTest.sav" LIVING_WORLD_SOCIAL_FIXTURE=1 python -B tests/living_world_bridge_emulator.py
LIVING_WORLD_PEWTER_FIXTURE=1 python -B tests/living_world_brock_emulator.py
cp "$QUANTUM_QA_OUTPUT"/Pewter{,Society}Test.sav "$QUANTUM_QA_OUTPUT"/Phase13Pewter.sav "$inputs/"
cmake -S "$work/llama" -B "$work/llama-linux" -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF \
    -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF -DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_TOOLS=OFF \
    -DLLAMA_BUILD_SERVER=OFF -DGGML_OPENMP=OFF -DGGML_NATIVE=OFF -DGGML_LLAMAFILE=OFF
cmake --build "$work/llama-linux" --target llama --parallel 4
export LIVING_WORLD_AGENCY_RUNTIME="$work/agency-runtime"
mkdir "$LIVING_WORLD_AGENCY_RUNTIME"
ln -s "$inputs/model-q4.gguf" "$LIVING_WORLD_AGENCY_RUNTIME/model.gguf"
gcc -O2 -c "$app/sandbox-linux.c" -o "$work/sandbox.o"
g++ -std=c++17 -O2 -I"$work/llama/include" -I"$work/llama/ggml/include" "$app/offline-worker.cpp" \
    "$work/sandbox.o" -Wl,--start-group "$work/llama-linux/src/libllama.a" \
    "$work/llama-linux/ggml/src/"libggml*.a -Wl,--end-group -ldl -lpthread -lm -o "$LIVING_WORLD_AGENCY_RUNTIME/offline-worker"
for mode in 0 1; do
    ADVENTURE_TEST_MODE=$mode QUANTUM_QA_OUTPUT="$work/kanto-$mode" python -B tests/living_world_kanto_emulator.py
    ADVENTURE_TEST_MODE=$mode QUANTUM_QA_OUTPUT="$work/autonomy-$mode" python -B tests/living_world_autonomy_emulator.py
    ADVENTURE_TEST_MODE=$mode QUANTUM_QA_OUTPUT="$work/evolution-$mode" python -B tests/living_world_rules_emulator.py
done
python -B "$app/package-windows.py" "$inputs" "$output" --built-mgba
sha256sum "$output" > "$output.sha256"
