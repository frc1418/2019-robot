# 2019 Robot Code
**Robot Code** | [Dashboard](https://github.com/frc1418/2019-dashboard) | [Vision](https://github.com/frc1418/2019-vision)

[![Build Status](https://travis-ci.com/frc1418/2019-robot.svg?token=VDF6qgkKLeZhHqMRYJnC&branch=master)](https://travis-ci.com/frc1418/2019-robot)

> Code for Team 1418's 2019 competition robot, which is so far unnamed.

## Deploying onto the robot
Before deploying, you must [install robotpy](http://robotpy.readthedocs.io/en/stable/install/robot.html#install-robotpy) on your robot.

You may then deploy code at any time:

	python3 robot.py deploy

During development of last year's robot code, we created a Bash script `deploy.sh` to automate some tasks related to code deploy. You can find that tool, `dep`, [here](https://github.com/frc1418/dep). We recommend that you make use of it to simplify your deploy process and remove pesky steps like manually changing your WiFi network.

## Testing/Simulation
You may run the `pyfrc` simulator to test this code thus:

    python3 robot.py sim

## Controls
We use three total joysticks to control the robot:

* 2 x **Logitech Attack 3** (`joystick_left` and `joystick_right`)
* 1 x **Logitech Extreme 3D Pro** (`joystick_alt`)

<img src="res/ATK3.png" height="600"><img src="res/X3D.png" height="600">

## Setting up `git` hooks:

`git` hooks change the process of committing by adding processes before or after the process of committing. After cloning, you should run

	./setup.sh

This will set up hooks to run tests before committing to help avoid easy-to-fix errors in the code.

## File Structure

    robot/
    	The robot code lives here.
        automations/
            Automatic scripts for performing common functions.
        autonomous/
            Autonomous modes.
        common/
            New robotpy components.
        components/
            Abstractions for major robot systems.
        controllers/
            Software implementations not corresponding to physical robot components.
	tests/
		py.test-based unit tests that test the code and can be run via pyfrc.

## Authors
* [Erik Boesen](https://github.com/ErikBoesen), Programming Captain
* [Andrew Lester](https://github.com/AndrewLester)
* [Joe Carpenter](https://github.com/JosephCarpenter)
* [Bobby Miller](https://github.com/BobbyMi11er)

Special thanks goes to [Tim Winters](https://github.com/Twinters007), former 1418 Programming Captain, who tirelessly worked as a mentor to help us reach new heights with this year's robot code.

## Licensing
In-season, use of this software is restricted by the FRC rules. After the season ends, the [MIT License](LICENSE) applies instead.
