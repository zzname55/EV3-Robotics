
# config.py enthält alle wichtigen Einstellwerte.


# Roboter-Maße
WHEEL_DIAMETER = 52
AXLE_TRACK = 116


# Geschwindigkeitseinstellungen
DRIVE_SPEED = 220
DRIVE_ACCELERATION = 200

TURN_RATE = 90
TURN_ACCELERATION = 120


# Hinderniserkennung
# 200 mm = 20 cm
OBSTACLE_DISTANCE = 200


# Rückfahrstrecke
BACKUP_DISTANCE = 120


# Schwarz-Erkennung
# Falls Schwarz nicht gut erkannt wird: 20 oder 25 testen.
BLACK_REFLECTION_LIMIT = 15


# Drehwinkel beim Ausweichen
AVOID_TURN_ANGLE = 90


# Modi
MODE_INSIDE = 0
MODE_LINE = 1


# Rot-Moduswechsel
MODE_SWITCH_WAIT = 1000
RED_FORWARD_DISTANCE = 80


# Linienfolge-Modus
LINE_DRIVE_SPEED = 120
LINE_TURN_RATE = 45


# Gelb-Spezial-Aktion
# Gelb dauert jetzt nur noch ca. 3 Sekunden.
YELLOW_ACTION_TIME = 3000

# Drehgeschwindigkeit während der Gelb-Aktion.
# 120 Grad/s * 3 s = ungefähr 360 Grad.
# Wenn er sich stärker drehen soll, erhöhe den Wert.
YELLOW_TURN_RATE = 120

# Nach Gelb kurz weiterfahren
YELLOW_FORWARD_DISTANCE = 100


# Wartezeiten
SHORT_WAIT = 300
SENSOR_WAIT = 10