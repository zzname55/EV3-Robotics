# hardware.py erstellt EV3, Motoren und DriveBase.

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

from config import WHEEL_DIAMETER, AXLE_TRACK


# EV3-Stein
ev3 = EV3Brick()


# Motoren
# Linker Motor an Port C
# Rechter Motor an Port B
motor_links = Motor(Port.C)
motor_rechts = Motor(Port.B)


# Fahrbasis
killer = DriveBase(
    motor_links,
    motor_rechts,
    WHEEL_DIAMETER,
    AXLE_TRACK
)