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
        self.lift_motors = [wpilib.Victor(i) for i in range(4, 8)]
        for motor in self.lift_motors:
            motor.setDeadband(0.2)

    def teleopPeriodic(self):
        """
        Spin all motors at full speed.
        """
        for motor in self.lift_motors:
            # Correcting for odd joystick
            motor.set(-self.joystick.getY() * 2 - 1)


if __name__ == '__main__':
    wpilib.run(TestRobot)
