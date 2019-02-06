#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive


class TestRobot(magicbot.MagicRobot):
    def createObjects(self):
        """
        Initialize testbench components.
        """
        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        """
        Spin all motors at full speed.
        """
        pass


if __name__ == '__main__':
    wpilib.run(TestRobot)
