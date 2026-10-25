# Native Map and Storage apps

The six Pokeglass app icons and script IDs are unchanged. Map opens FireRed's
normal Town Map directly (not the custom atlas and not an automatic Fly picker).
The native map's island switch is disabled even when older saves retain Sevii
unlock flags. The field-tool Fly screen keeps its separate native entry point.

Storage opens the game's existing Pokemon Storage PC menu and box UI, including
Move Pokemon, Deposit, Withdraw, Move Items and the normal box options. The custom
tablet storage implementation is removed. The PC engine and Pokemon/save formats
are unchanged, and the existing stored-Pokemon/item recovery runs before entry.
Both native apps clean up the tablet window/blending, then return to the launcher
through the existing script when closed.

A development ROM compiled successfully. Native mGBA tests cover all six app
launches/returns, Kanto with both old Sevii flags set, deposit/withdraw and boxed
payload integrity, Move Items, last-party-member deposit protection and unlocked
field exit. The obsolete custom-storage UI fixtures are replaced by
`pokeglass_native_apps_emulator.py`; the app-grid and avatar map fixtures now
expect the native screens. Review images are actual ROM captures.
