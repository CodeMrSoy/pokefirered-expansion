"""Compatibility entry point for the restored regular TM Case regression."""
import pathlib
p=pathlib.Path(__file__).with_name('pokeglass_tm_case_emulator.py')
exec(compile(p.read_text(encoding='utf-8'),str(p),'exec'))
