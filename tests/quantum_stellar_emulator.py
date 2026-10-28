#!/usr/bin/env python3
"""Compatibility entry point for the current Safari-ticket/Koga story checks.

Giovanni's old ticket-drop quest was retired; its assertions are superseded by
real Safari gift, full-bag recovery, ticketed ferry and normal Giovanni checks.
"""
import pathlib
import runpy

runpy.run_path(str(pathlib.Path(__file__).with_name('havora_koga_emulator.py')), run_name='__main__')
