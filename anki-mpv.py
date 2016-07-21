# -*- coding: utf-8 -*-
# See the LICENSE file for license details.

from locale import setlocale, LC_NUMERIC
from anki import sound, hooks
import mpv

# we need to have global state due to how sound.play() and
# sound.clearAudioQueue() are used in other modules


m = None


def mpv_init():
    global m

    setlocale(LC_NUMERIC, "C")

    m = mpv.Context()
    m.initialize()


def mpv_add_to_queue(path):
    if m is None:
        mpv_init()

    m.command("loadfile", path, "append-play")


def mpv_clear_queue():
    if m is None:
        return

    m.command("stop")


def mpv_kill(*args):
    global m

    if m is None:
        return

    m.command("quit")
    m = None

hooks.remHook("unloadProfile", sound.stopMplayer)
hooks.addHook("unloadProfile", mpv_kill)

sound._player = mpv_add_to_queue
sound._queueEraser = mpv_clear_queue
