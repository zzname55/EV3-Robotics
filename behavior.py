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
#   Roboter dreht sich ca. 15 Sekunden lang.
#   Dabei macht er ungefähr 900 Grad:
#   360 + 360 + 180.
#   Währenddessen spielt er eine eigene Pop-Melodie.
#
# Blau:
#   Roboter sagt einen Satz und macht danach im aktuellen Modus weiter.
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


def blue_detected(color_sensor):
    """
    Prüft, ob Blau erkannt wurde.

    Manche dunklen Blautöne werden vom EV3-Farbsensor
    nicht sauber als Color.BLUE erkannt.
    Deshalb prüfen wir zusätzlich rgb().
    """

    color = color_sensor.color()

    # Normale Farberkennung
    if color == Color.BLUE:
        return True

    # Zusätzliche Prüfung für dunkles Royal Blue
    r, g, b = color_sensor.rgb()

    # Blau bedeutet meistens:
    # Blau-Wert ist deutlich höher als Rot und Grün.
    if b > r + 5 and b > g + 5:
        return True

    return False


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


def handle_blue_marker(robot, ev3):
    """
    Spezial-Aktion bei Blau.

    Der Roboter:
    1. stoppt sofort
    2. sagt den Satz
    3. wartet kurz
    4. macht danach normal weiter
    """

    stop_robot(robot)
    wait(200)

    ev3.speaker.say(
        "Hello master. I will continue my work. Juan is a good master."
    )

    wait(300)


def handle_yellow_marker(robot, ev3):
    """
    Spezial-Aktion bei Gelb.

    Ablauf:
    1. Stoppen
    2. 15 Sekunden drehen
    3. Währenddessen Melodie spielen
    4. Danach kurz weiterfahren
    """

    stop_robot(robot)
    wait(100)

    # Drehung starten.
    # 0 = nicht vorwärts fahren.
    # -YELLOW_TURN_RATE = auf der Stelle drehen.
    robot.drive(0, -YELLOW_TURN_RATE)

    # Eigene kurze Pop-Melodie.
    # Das ist nicht die exakte Wonderwall-Melodie,
    # sondern eine eigene Melodie mit ähnlichem Gefühl.
    melody = [
        (659, 300), (784, 300), (880, 500), (784, 300),
        (659, 300), (587, 500), (659, 300), (784, 300),

        (880, 500), (988, 300), (880, 300), (784, 500),
        (659, 300), (587, 300), (659, 500), (784, 300),

        (880, 300), (784, 300), (659, 500), (587, 300),
        (659, 300), (784, 500), (880, 300), (988, 300),

        (880, 500), (784, 300), (659, 300), (587, 500),
        (659, 300), (784, 300), (659, 700),
    ]

    time_played = 0

    # Melodie abspielen.
    # Der Roboter dreht weiter, weil robot.drive() vorher gestartet wurde.
    for frequency, duration in melody:
        ev3.speaker.beep(frequency, duration)
        wait(40)

        time_played = time_played + duration + 40

        if time_played >= YELLOW_ACTION_TIME:
            break

    # Falls die Melodie kürzer als 15 Sekunden ist,
    # spielt er kurze Töne weiter.
    while time_played < YELLOW_ACTION_TIME:
        ev3.speaker.beep(784, 150)
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
    2. Blau prüfen
    3. Rot prüfen
    4. Hindernis prüfen
    5. Aktuellen Modus ausführen
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

    # Blau-Sperre:
    # Verhindert, dass der Satz auf derselben blauen Fläche dauernd wiederholt wird.
    blue_locked = False

    while True:

        # Farben lesen
        yellow_now = yellow_detected(color_sensor)
        blue_now = blue_detected(color_sensor)
        red_now = red_detected(color_sensor)

        # Rot wieder freigeben, wenn der Roboter nicht mehr auf Rot ist.
        if not red_now:
            red_locked = False

        # Blau wieder freigeben, wenn der Roboter nicht mehr auf Blau ist.
        if not blue_now:
            blue_locked = False

        # Gelb hat höchste Priorität.
        if yellow_now:
            handle_yellow_marker(robot, ev3)

        # Blau spricht nur einmal pro blauer Fläche.
        elif blue_now and not blue_locked:
            handle_blue_marker(robot, ev3)
            blue_locked = True
            
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