#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from ctre.wpi_talonsrx import WPI_TalonSRX


class TestRobot(magicbot.MagicRobot):
    def createObjects(self):
        """
        Initialize testbench components.
        """
        self.joystick = wpilib.Joystick(0)
        self.lift_talon = WPI_TalonSRX(40)

    def teleopPeriodic(self):
        """
        Spin all motors at full speed.
        """
        self.lift_talon.set(0.3)
        print(self.lift_talon.getSelectedSensorPosition())


if __name__ == '__main__':
    wpilib.run(TestRobot)
