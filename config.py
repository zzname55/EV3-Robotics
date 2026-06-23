# config.py enthält alle wichtigen Einstellwerte.


# Roboter-Maße
WHEEL_DIAMETER = 52
AXLE_TRACK = 116


# Normale Geschwindigkeit
DRIVE_SPEED = 180
DRIVE_ACCELERATION = 200

TURN_RATE = 90
TURN_ACCELERATION = 120


# Hinderniserkennung
# 200 mm = 20 cm
OBSTACLE_DISTANCE = 200

# Wenn ein Hindernis erkannt wird, stoppt der Roboter 2 Sekunden.
OBSTACLE_STOP_TIME = 2000


# Rot-Erkennung
# Wenn Rot erkannt wird, stoppt der Roboter 10 Sekunden.
RED_STOP_TIME = 10000

# Danach wird Rot 2 Sekunden nicht mehr geprüft.
# Der Roboter fährt in dieser Zeit normal weiter.
RED_IGNORE_TIME = 2000


# Rückfahrstrecke im Inside Mode
BACKUP_DISTANCE = 120


# Schwarz-Erkennung
BLACK_REFLECTION_LIMIT = 30


# Inside Mode
AVOID_TURN_ANGLE = 90


# Modi
MODE_LINE = 0
MODE_INSIDE = 1


# Line Mode
LINE_DRIVE_SPEED = 90

LINE_TARGET_REFLECTION = 35

LINE_KP = 1.5

LINE_MAX_TURN_RATE = 70


# Wartezeiten
SHORT_WAIT = 300
SENSOR_WAIT = 10