# sensor.py erstellt alle Sensoren.

from pybricks.ev3devices import UltrasonicSensor, ColorSensor
from pybricks.parameters import Port


# Ultraschallsensor vorne
ultra = UltrasonicSensor(Port.S4)


# Farbsensor nach unten auf den Boden
farbe = ColorSensor(Port.S3)