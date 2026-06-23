#!/usr/bin/env pybricks-micropython

# main.py ist der Startpunkt des Programms.

from hardware import ev3, killer
from sensor import ultra, farbe
from behavior import run_mode_switch_robot


# Startsignal
ev3.speaker.beep()

# Hauptprogramm starten
run_mode_switch_robot(killer, ultra, farbe, ev3)