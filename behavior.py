# behavior.py enthält das Verhalten des Roboters.
#
# Modi:
#
# MODE_INSIDE:
#   Roboter bleibt im schwarzen Viereck.
#
# MODE_LINE:
#   Roboter folgt der schwarzen Linie.
#
# Rot:
#   Wechselt zwischen MODE_INSIDE und MODE_LINE.
#
# Gelb:
#   Roboter dreht sich ca. 3 Sekunden lang.
#   Währenddessen spielt er eine kurze Melodie.
#
# Hindernisse:
#   Werden in beiden Modi erkannt.

from pybricks.parameters import Color
from pybricks.tools import wait

from config import (
    DRIVE_SPEED,
    DRIVE_ACCELERATION,
    TURN_RATE,
    TURN_ACCELERATION,
    OBSTACLE_DISTANCE,
    BLACK_REFLECTION_LIMIT,
    SHORT_WAIT,
    SENSOR_WAIT,
    MODE_INSIDE,
    MODE_LINE,
    MODE_SWITCH_WAIT,
    RED_FORWARD_DISTANCE,
    LINE_DRIVE_SPEED,
    LINE_TURN_RATE,
    YELLOW_ACTION_TIME,
    YELLOW_TURN_RATE,
    YELLOW_FORWARD_DISTANCE,
)

from movement import (
    drive_forward,
    drive_back,
    turn_away,
    stop_robot,
)


def black_detected(color_sensor):
    """
    Prüft, ob Schwarz erkannt wurde.
    """

    return color_sensor.reflection() <= BLACK_REFLECTION_LIMIT


def red_detected(color_sensor):
    """
    Prüft, ob Rot erkannt wurde.
    Rot wechselt den Modus.
    """

    return color_sensor.color() == Color.RED


def yellow_detected(color_sensor):
    """
    Prüft, ob Gelb erkannt wurde.
    Gelb startet die Spezial-Aktion.
    """

    return color_sensor.color() == Color.YELLOW


def obstacle_detected(ultrasonic_sensor):
    """
    Prüft, ob ein Hindernis vorne erkannt wurde.
    """

    return ultrasonic_sensor.distance() <= OBSTACLE_DISTANCE


def handle_obstacle(robot, ev3):
    """
    Verhalten bei Hindernis:
    stoppen, piepen, zurückfahren, wegdrehen.
    """

    stop_robot(robot)
    ev3.speaker.beep()
    wait(SHORT_WAIT)

    drive_back(robot)
    wait(SHORT_WAIT)

    turn_away(robot)
    wait(SHORT_WAIT)


def handle_yellow_marker(robot, ev3):
    """
    Spezial-Aktion bei Gelb.

    Ablauf:
    1. Stoppen
    2. Ca. 3 Sekunden drehen
    3. Währenddessen kurze Melodie spielen
    4. Danach kurz weiterfahren
    """

    stop_robot(robot)
    wait(100)

    # Drehung starten.
    # 0 = nicht vorwärts fahren.
    # -YELLOW_TURN_RATE = auf der Stelle drehen.
    robot.drive(0, -YELLOW_TURN_RATE)

    # Kurze eigene Melodie, ca. 3 Sekunden.
    melody = [
        (1000, 200),
        (1200, 200),
        (1400, 200),
        (1600, 300),
        (1400, 200),
        (1200, 200),
        (1000, 300),
        (1300, 200),
        (1600, 400),
    ]

    time_played = 0

    for frequency, duration in melody:
        ev3.speaker.beep(frequency, duration)
        wait(40)

        time_played = time_played + duration + 40

        if time_played >= YELLOW_ACTION_TIME:
            break

    # Falls noch etwas Zeit übrig ist, weiter drehen und kurze Töne spielen.
    while time_played < YELLOW_ACTION_TIME:
        ev3.speaker.beep(1200, 150)
        wait(100)

        time_played = time_played + 250

    # Drehung stoppen.
    stop_robot(robot)
    wait(SHORT_WAIT)

    # Kurz weiterfahren, damit Gelb verlassen wird.
    robot.straight(YELLOW_FORWARD_DISTANCE)
    wait(SHORT_WAIT)


def stay_inside_square_step(robot, color_sensor, ev3):
    """
    Verhalten im Viereck-Modus.

    Wenn Schwarz erkannt wird:
    Der Roboter ist am Rand.
    Er fährt zurück und dreht weg.

    Wenn kein Schwarz erkannt wird:
    Der Roboter fährt geradeaus.
    """

    if black_detected(color_sensor):
        stop_robot(robot)
        ev3.speaker.beep()
        wait(SHORT_WAIT)

        drive_back(robot)
        wait(SHORT_WAIT)

        turn_away(robot)
        wait(SHORT_WAIT)

    else:
        drive_forward(robot)


def follow_black_line_step(robot, color_sensor):
    """
    Einfacher Linienfolge-Modus.

    Wenn Schwarz erkannt wird:
    geradeaus fahren.

    Wenn kein Schwarz erkannt wird:
    langsam drehen, um Schwarz wiederzufinden.
    """

    if black_detected(color_sensor):
        robot.drive(LINE_DRIVE_SPEED, 0)
    else:
        robot.drive(60, -LINE_TURN_RATE)


def switch_mode(current_mode, ev3):
    """
    Wechselt zwischen den Modi.

    MODE_INSIDE -> MODE_LINE
    MODE_LINE   -> MODE_INSIDE
    """

    ev3.speaker.beep()

    if current_mode == MODE_INSIDE:
        return MODE_LINE

    return MODE_INSIDE


def run_mode_switch_robot(robot, ultrasonic_sensor, color_sensor, ev3):
    """
    Hauptprogramm.

    Reihenfolge:
    1. Gelb prüfen
    2. Rot prüfen
    3. Hindernis prüfen
    4. Aktuellen Modus ausführen
    """

    # Geschwindigkeit einstellen
    robot.settings(
        DRIVE_SPEED,
        DRIVE_ACCELERATION,
        TURN_RATE,
        TURN_ACCELERATION
    )

    # Startmodus
    mode = MODE_INSIDE

    # Rot-Sperre:
    # Verhindert, dass Rot auf derselben Fläche mehrfach schaltet.
    red_locked = False

    while True:

        # Farben lesen
        yellow_now = yellow_detected(color_sensor)
        red_now = red_detected(color_sensor)

        # Rot wieder freigeben, wenn der Roboter nicht mehr auf Rot ist.
        if not red_now:
            red_locked = False

        # Gelb hat höchste Priorität.
        if yellow_now:
            handle_yellow_marker(robot, ev3)

        # Rot wechselt den Modus.
        elif red_now and not red_locked:
            stop_robot(robot)

            mode = switch_mode(mode, ev3)

            red_locked = True

            wait(MODE_SWITCH_WAIT)

            # Kurz weiterfahren, damit die rote Fläche verlassen wird.
            robot.straight(RED_FORWARD_DISTANCE)
            wait(SHORT_WAIT)

        # Hindernis erkannt.
        elif obstacle_detected(ultrasonic_sensor):
            handle_obstacle(robot, ev3)

        # Modus 1:
        # Im schwarzen Viereck bleiben.
        elif mode == MODE_INSIDE:
            stay_inside_square_step(robot, color_sensor, ev3)

        # Modus 2:
        # Schwarzer Linie folgen.
        elif mode == MODE_LINE:
            follow_black_line_step(robot, color_sensor)

        wait(SENSOR_WAIT)