# Living Quantum World playtest

Use Windows 10 or 11, x64, and extract the whole ZIP to a writable folder. No emulator install, model download or connection is needed.

1. Double-click **Play Pallet Demo.cmd**, press Enter at the title screen, then choose **Continue** with **Z**. The separate demo save starts in Pallet Town with the Pokédex, PokéGlass, Pikachu and Squirtle.
2. Walk a few steps so Pikachu is visible. Find the man near the pond in southern Pallet Town who talks about PC storage. Face him and press **Z**. The resident reacts to Pikachu and Squirtle using different topics. If a reply is still being prepared, the window title says **NPC is thinking**.
3. Open PokéGlass with **Enter**, switch Squirtle into the first party slot, exit the menu, and walk a few steps. Talk to the same resident again to see how the dialogue changes. The demo save is separate from the normal adventure launched by **Play.cmd**.

| Game input | Keyboard |
| --- | --- |
| Direction pad | Arrow keys |
| A / B | Z / X |
| Start / Select | Enter / Backspace |
| L / R | A / S |

The demo prepares both replies in the background as it opens. Ready replies are reused during that session. A first encounter can still wait if it reaches the resident before generation finishes. The original PC-storage tip appears if inference times out, isolation cannot start, or the dialogue fails validation. The app writes battery saves, previous-save backups and an inference log under `%LOCALAPPDATA%\LivingQuantumWorld`. Inspect `dialogue.jsonl` for the observed Pokémon, generated text, validator result, elapsed time or worker error.

## Windows isolation check

Open Command Prompt in the extracted folder and run `Play.cmd --sandbox-test`. It launches a probe through the same AppContainer and attempts to read and write a temporary file outside its allowed folder, to start a child command, and to open an internet connection. All four values in the printed denial report should be 1. Then run `Play.cmd --model-test` to check that the restricted worker can load the bundled model and return a valid Pikachu reply. The playable build is a Windows test package. Its AppContainer and probe require a native Windows run to confirm the denials.

## Included software

The test uses a statically linked CPU-only [llama.cpp b6500](https://github.com/ggml-org/llama.cpp/tree/b6500) worker with the official [Qwen2.5-0.5B-Instruct Q4_0 weights](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/tree/9217f5d), [mGBA libretro at 7a12d6d](https://github.com/mgba-emu/mgba/tree/7a12d6d4b9acb14c0ae62c9166b6a2f3d08007f6), [SDL2 2.32.10](https://github.com/libsdl-org/SDL/releases/tag/release-2.32.10) and [Python 3.12.10](https://www.python.org/downloads/release/python-31210/). Licenses are included in the archive.
