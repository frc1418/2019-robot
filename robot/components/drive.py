import wpilib
import wpilib.drive
from magicbot import will_reset_to
from magicbot import tunable


class Drive:
    """
    Handle robot drivetrain.
    All drive interaction must go through this class.
    """

    train: wpilib.drive.MecanumDrive

    y = will_reset_to(0)
    x = will_reset_to(0)
    rot = will_reset_to(0)

    speed_constant = tunable(1.05)
    rotational_constant = tunable(0.5)

    strafe_multiplier = tunable(0.5)
    strafe_rotation_multiplier = tunable(0.5)

    def __init__(self):
        self.enabled = False

    def setup(self):
        """
        Set input threshold.
        """
        pass

    def move(self, y: float, x: float, rot: float):
        """
        Move robot.
        :param y: Speed of motion in the y direction. [-1..1]
        :param x: Speed of motion in the x direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        """
        self.y = y
        self.x = x
        self.rot = rot

    def execute(self):
        """
        Handle driving.
        """
        self.train.driveCartesian(
            self.speed_constant * self.y,
            self.speed_constant * self.x,
            self.rotational_constant * self.rot
        )
