import magicbot
import wpilib
import wpilib.drive

from wpilib.buttons import JoystickButton
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive
from automations import seek_target
from magicbot import tunable

import navx
from ctre.wpi_talonsrx import WPI_TalonSRX


class Robot(magicbot.MagicRobot):
    # Components
    drive = drive.Drive

    # Automations
    seek_target = seek_target.SeekTarget

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.joystick_alt = wpilib.Joystick(2)

        # Button
        self.button_strafe_left = JoystickButton(self.joystick_left, 4)
        self.button_strafe_right = JoystickButton(self.joystick_left, 5)
        self.button_strafe_forward = JoystickButton(self.joystick_left, 3)
        self.button_strafe_backward = JoystickButton(self.joystick_left, 2)

        self.button_target = ButtonDebouncer(self.joystick_right, 3)

        # Drive motor controllers
        # ID SCHEME:
        #   10^1: 1 = left, 2 = right
        #   10^0: 0 = front, 5 = rear
        self.lf_motor = WPI_TalonSRX(10)
        self.lr_motor = WPI_TalonSRX(15)
        self.rf_motor = WPI_TalonSRX(20)
        self.rr_motor = WPI_TalonSRX(25)

        # Drivetrain
        self.train = wpilib.drive.MecanumDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()
        self.navx.reset()

        # Utility
        self.ds = wpilib.DriverStation.getInstance()
        self.timer = wpilib.Timer()
        self.pdp = wpilib.PowerDistributionPanel(0)
        self.compressor = wpilib.Compressor()

        # Camera server
        wpilib.CameraServer.launch('camera/camera.py:main')

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        self.time = int(self.timer.getMatchTime())
        self.voltage = self.pdp.getVoltage()
        self.rotation = self.navx.getAngle() % 360

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """

        # Call autonomous
        super().autonomous()

    def disabledInit(self):
        """
        Executed once right away when robot is disabled.
        """
        # Reset Gyro to 0
        self.navx.reset()

    def disabledPeriodic(self):
        """
        Executed periodically while robot is disabled.
        Useful for testing.
        """
        pass

    def teleopInit(self):
        """
        Executed when teleoperated mode begins.
        """
        self.compressor.start()

    def teleopPeriodic(self):
        """
        Executed periodically while robot is in teleoperated mode.
        """
        # Read from joysticks and move drivetrain accordingly
        self.drive.move(x=-self.joystick_left.getY(),
                        y=self.joystick_left.getX(),
                        rot=self.joystick_right.getX(),
                        real=True)

        self.drive.strafe(self.button_strafe_left.get(),
                          self.button_strafe_right.get(),
                          self.button_strafe_forward.get(),
                          self.button_strafe_backward.get())

        if self.button_target.get():
            self.seek_target.start()


if __name__ == '__main__':
    wpilib.run(Robot)
