# EV3 Robotics

EV3 Robotics is a LEGO Mindstorms EV3 project that uses MicroPython to control motors, sensors, obstacle detection, and color-based behavior modes. The robot can stay inside a marked area, follow a black line, react to colored markers, avoid obstacles autonomously, and can be extended with more features in the future.

## Features

* Autonomous driving using the EV3 DriveBase
* Obstacle detection with an ultrasonic sensor
* Color detection with an EV3 color sensor
* Black border detection to stay inside a marked area
* Black line following mode
* Red marker detection to switch between behavior modes
* Yellow marker detection for a short special action
* Clean project structure with separated configuration, hardware, sensor, movement, and behavior logic

## Project Structure

```text
ev3_robotics/
├── main.py
├── config.py
├── hardware.py
├── sensor.py
├── movement.py
└── behavior.py
```

## File Overview

### `main.py`

The main entry point of the project. It imports the robot hardware, sensors, and behavior logic, then starts the main robot program.

### `config.py`

Contains the main settings for the robot, such as wheel size, axle track, speed values, obstacle distance, color detection values, and mode settings.

### `hardware.py`

Creates the EV3 brick, the motors, and the DriveBase.

Current motor setup:

```text
Left motor:  Port C
Right motor: Port B
```

### `sensor.py`

Creates the sensors used by the robot.

Current sensor setup:

```text
Ultrasonic sensor: Port S4
Color sensor:      Port S3
```

### `movement.py`

Contains reusable movement functions, such as driving forward, driving backward, turning away from borders or obstacles, and stopping the robot.

### `behavior.py`

Contains the main behavior logic of the robot, including obstacle avoidance, color reactions, and mode switching.

## Behavior Modes

### Inside Mode

In this mode, the robot tries to stay inside a black-bordered area. When the color sensor detects the black border, the robot drives backward, turns away, and continues driving.

### Line Mode

In this mode, the robot follows a black line. When the robot loses the line, it turns slowly to search for it again.

## Color Behavior

### Black

Black is used for both the border of the driving area and the line-following mode. The robot detects black using the reflection value of the color sensor.

### Red

Red is used to switch between the two behavior modes:

```text
Inside Mode → Line Mode
Line Mode   → Inside Mode
```

A lock system prevents the robot from switching multiple times while standing on the same red marker.

### Yellow

Yellow starts a short special action. When yellow is detected, the robot stops, plays a short melody, turns for a short time, and then continues its normal task.

## Requirements

* LEGO Mindstorms EV3 Brick
* LEGO EV3 motors
* LEGO EV3 ultrasonic sensor
* LEGO EV3 color sensor
* EV3 MicroPython / Pybricks
* Visual Studio Code with the EV3 MicroPython extension

## How to Run

1. Open the project folder in Visual Studio Code.
2. Make sure all project files are in the same folder.
3. Connect the EV3 brick.
4. Upload the project to the EV3.
5. Run `main.py`.

## Calibration

The robot may need calibration depending on the surface, lighting, and build quality.

Important values in `config.py`:

```python
WHEEL_DIAMETER = 52
AXLE_TRACK = 116
BLACK_REFLECTION_LIMIT = 15
DRIVE_SPEED = 220
```

### If the robot does not detect black correctly

Try increasing the black reflection limit:

```python
BLACK_REFLECTION_LIMIT = 20
```

or:

```python
BLACK_REFLECTION_LIMIT = 25
```

### If the robot drives too fast

Lower the drive speed:

```python
DRIVE_SPEED = 150
```

### If the robot turns too much or too little

Adjust the axle track or turn angle:

```python
AXLE_TRACK = 116
AVOID_TURN_ANGLE = 90
```

## Current Behavior Flow

```text
Start
↓
Check yellow marker
↓
Check red marker
↓
Check obstacle
↓
Run current mode
↓
Repeat
```

## Future Improvements

Possible future improvements include:

* Better line following with a PID controller
* More accurate color calibration using RGB values
* Gyro-based turning for cleaner rotations
* Additional color actions
* Sound effects or speech output
* Improved obstacle avoidance behavior
* A display menu on the EV3 brick
