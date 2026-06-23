# movement.py enthält Bewegungsfunktionen.

from config import (
    DRIVE_SPEED,
    BACKUP_DISTANCE,
    AVOID_TURN_ANGLE,
)


def drive_forward(robot):
    """
    Roboter fährt geradeaus.
    """

    robot.drive(DRIVE_SPEED, 0)


def drive_back(robot):
    """
    Roboter fährt ein Stück rückwärts.
    """

    robot.straight(-BACKUP_DISTANCE)


def turn_away(robot):
    """
    Roboter dreht sich vom Rand weg.
    """

    robot.turn(-AVOID_TURN_ANGLE)


def stop_robot(robot):
    """
    Roboter stoppt.
    """

    robot.stop()