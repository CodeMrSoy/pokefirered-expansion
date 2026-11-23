# Pokémon Quantum

A Pokémon FireRed expansion featuring Classic Kanto, the Quantum adventure in
Vidra, PokéGlass, and reusable field tools.

| Branch | Purpose |
| --- | --- |
| [`Pokemon-Quantum-V3`](https://github.com/CodeMrSoy/pokefirered-expansion/tree/Pokemon-Quantum-V3) | Integrates playable game changes |
| [`Living-World`](https://github.com/CodeMrSoy/pokefirered-expansion/tree/Living-World) | Develops the native bridge, simulation, and Windows companion |
| [`Pokemon-Quantum-V2`](https://github.com/CodeMrSoy/pokefirered-expansion/tree/Pokemon-Quantum-V2) | Stable V2 release and save-migration baseline |

Build with `make -j4` after installing the ARM GNU toolchain and host build
dependencies. See [INSTALL.md](INSTALL.md#pokémon-quantum-quick-start) for the
Quantum build and [the branch guide](docs/branches/README.md) for development,
tests, and milestones.

## Source layout

| Path | Contents |
| --- | --- |
| `src/`, `include/`, `asm/` | Native GBA source, headers and assembly |
| `data/`, `graphics/`, `sound/` | Maps, scripts, layouts, sprites, palettes and audio inputs |
| `tools/` | Host tools and generators used by the FireRed build |
| `test/`, `tests/` | Native tests and Python/emulator regression drivers |
| `docs/` | Build, mechanics, maps and verification notes |
| `experiments/living_world/` on Living-World | Simulation, native world catalog, launchers and package tooling |

## Credits

Pokémon Quantum builds on [cawtds/pokefirered-expansion](https://github.com/cawtds/pokefirered-expansion)
and [pret/pokefirered](https://github.com/pret/pokefirered). The FireRed expansion
inherits contributions from [rh-hideout/pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion/wiki/Credits)
and [Sotomura/pokefirered-rtc](https://github.com/Sotomura/pokefirered/tree/pokefirered-rtc).
See the individual notices under `tools/` for bundled tool licenses.
