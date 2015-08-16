# -*- coding: utf-8 -*-
# License: CC0 1.0 Universal

from locale import setlocale, LC_NUMERIC
from anki.utils import isWin
from anki import sound, hooks
import mpv

# we need to have global state due to how sound.play() and
# sound.clearAudioQueue() are used in other modules

setlocale(LC_NUMERIC, "C")

m = None


def mpv_init():
    global m
    if m is not None:
        return

    m = mpv.Context()
    m.initialize()


def mpv_add_to_queue(path):
    if not isWin:
        path = path.encode("utf-8")

    mpv_init()
    m.command("loadfile", path, "append-play")


def mpv_clear_queue():
    if m is None:
        return

    m.command("stop")


def mpv_kill(*args):
    if m is None:
        return

    m.command("quit")

hooks.remHook("unloadProfile", sound.stopMplayer)
hooks.addHook("unloadProfile", mpv_kill)

sound._player = mpv_add_to_queue
sound._queueEraser = mpv_clear_queue
