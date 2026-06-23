# behavior.py enthält das Verhalten des Roboters.
#
# Start:
#   Roboter startet im Line Mode und folgt der schwarzen Linie.
#
# Rechte EV3-Taste:
#   Wenn die rechte Taste gedrückt wird,
#   wechselt der Roboter in den Inside Mode.
#
# Rot:
#   Wenn Rot erkannt wird:
#   - Roboter stoppt 10 Sekunden
#   - danach fährt er sofort weiter
#   - Rot wird für 2 Sekunden nicht mehr geprüft
#
# Ultraschallsensor:
#   Wenn ein Hindernis erkannt wird,
#   stoppt der Roboter 2 Sekunden
#   und fährt danach weiter.

from pybricks.parameters import Button, Color
from pybricks.tools import wait, StopWatch

from config import (
    DRIVE_SPEED,
    DRIVE_ACCELERATION,
    TURN_RATE,
    TURN_ACCELERATION,
    OBSTACLE_DISTANCE,
    OBSTACLE_STOP_TIME,
    RED_STOP_TIME,
    RED_IGNORE_TIME,
    BLACK_REFLECTION_LIMIT,
    SHORT_WAIT,
    SENSOR_WAIT,
    MODE_LINE,
    MODE_INSIDE,
    LINE_DRIVE_SPEED,
    LINE_TARGET_REFLECTION,
    LINE_KP,
    LINE_MAX_TURN_RATE,
)

from movement import (
    drive_forward,
    drive_back,
    turn_away,
    stop_robot,
)


def black_detected(color_sensor):
    """
    Prüft, ob der Sensor Schwarz oder eine dunkle Fläche erkennt.
    """

    return color_sensor.reflection() <= BLACK_REFLECTION_LIMIT


def red_detected(color_sensor):
    """
    Prüft, ob Rot erkannt wurde.

    Wichtig:
    Diese Funktion wird nur aufgerufen, wenn Rot gerade nicht ignoriert wird.
    """

    return color_sensor.color() == Color.RED


def obstacle_detected(ultrasonic_sensor):
    """
    Prüft, ob vorne ein Hindernis erkannt wurde.
    """

    return ultrasonic_sensor.distance() <= OBSTACLE_DISTANCE


def right_button_pressed(ev3):
    """
    Prüft, ob die rechte Taste am EV3 gedrückt wurde.
    """

    return Button.RIGHT in ev3.buttons.pressed()


def handle_obstacle(robot, ev3):
    """
    Verhalten bei Hindernis.

    Der Roboter stoppt 2 Sekunden und fährt danach weiter.
    """

    stop_robot(robot)
    ev3.speaker.beep()
    wait(OBSTACLE_STOP_TIME)


def handle_red_marker(robot, ev3):
    """
    Verhalten bei Rot.

    Der Roboter:
    1. stoppt
    2. piept
    3. wartet 10 Sekunden
    4. fährt danach im normalen Programm weiter
    """

    stop_robot(robot)
    ev3.speaker.beep()
    wait(RED_STOP_TIME)


def stay_inside_square_step(robot, color_sensor, ev3):
    """
    Inside Mode.

    Der Roboter fährt im hellen Innenbereich.
    Wenn er Schwarz erkennt, ist er am schwarzen Rand.
    Dann fährt er zurück und dreht weg.
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


def clamp(value, minimum, maximum):
    """
    Begrenzt einen Wert auf einen Mindest- und Maximalwert.
    """

    if value < minimum:
        return minimum

    if value > maximum:
        return maximum

    return value


def follow_black_line_step(robot, color_sensor):
    """
    Line Mode.

    Der Roboter folgt der schwarzen Linie über den Reflexionswert.
    Farben wie Gelb oder Blau werden hier nicht extra geprüft.
    """

    reflection = color_sensor.reflection()

    error = reflection - LINE_TARGET_REFLECTION

    turn_rate = error * LINE_KP

    turn_rate = clamp(
        turn_rate,
        -LINE_MAX_TURN_RATE,
        LINE_MAX_TURN_RATE
    )

    robot.drive(LINE_DRIVE_SPEED, turn_rate)


def run_robot(robot, ultrasonic_sensor, color_sensor, ev3):
    """
    Hauptprogramm.

    Startmodus:
        MODE_LINE

    Rechte Taste:
        Wechsel zu MODE_INSIDE

    Rot:
        Stoppt 10 Sekunden.
        Danach wird Rot 2 Sekunden nicht geprüft,
        aber der Roboter fährt direkt weiter.

    Ultraschall:
        Stoppt bei Hindernis für 2 Sekunden.
    """

    robot.settings(
        DRIVE_SPEED,
        DRIVE_ACCELERATION,
        TURN_RATE,
        TURN_ACCELERATION
    )

    # Start: Roboter folgt der schwarzen Linie.
    mode = MODE_LINE

    # Button-Lock:
    # Verhindert, dass ein langer Tastendruck mehrfach gezählt wird.
    right_button_locked = False

    # Timer für die Rot-Ignorierzeit.
    watch = StopWatch()

    # Bis zu dieser Zeit wird Rot nicht geprüft.
    # 0 bedeutet: Rot wird aktuell normal geprüft.
    red_ignore_until = 0

    while True:

        current_time = watch.time()

        # Prüfen, ob Rot gerade ignoriert werden soll.
        red_is_ignored = current_time < red_ignore_until

        # Rechte Taste lesen.
        right_now = right_button_pressed(ev3)

        # Rot nur scannen, wenn Rot gerade NICHT ignoriert wird.
        # Dadurch wird bei großen roten Flächen nicht direkt wieder gestoppt.
        if red_is_ignored:
            red_now = False
        else:
            red_now = red_detected(color_sensor)

        # Wenn Taste losgelassen wird, darf sie später wieder zählen.
        if not right_now:
            right_button_locked = False

        # Rechte Taste wechselt in Inside Mode.
        if right_now and not right_button_locked:
            stop_robot(robot)
            ev3.speaker.beep()
            wait(SHORT_WAIT)

            mode = MODE_INSIDE
            right_button_locked = True

        # Rot erkannt und Rot wird gerade nicht ignoriert.
        elif red_now:
            handle_red_marker(robot, ev3)

            # Nach dem 10-Sekunden-Warten:
            # Rot für 2 Sekunden nicht mehr scannen.
            # Der Roboter fährt in dieser Zeit normal weiter.
            red_ignore_until = watch.time() + RED_IGNORE_TIME

        # Ultraschall wirkt in beiden Modi.
        elif obstacle_detected(ultrasonic_sensor):
            handle_obstacle(robot, ev3)

        # Inside Mode:
        # Roboter bleibt im schwarzen Viereck.
        elif mode == MODE_INSIDE:
            stay_inside_square_step(robot, color_sensor, ev3)

        # Line Mode:
        # Roboter folgt der schwarzen Linie.
        elif mode == MODE_LINE:
            follow_black_line_step(robot, color_sensor)

        wait(SENSOR_WAIT)