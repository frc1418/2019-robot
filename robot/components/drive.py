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

    y_multiplier = tunable(1.0)
    x_multiplier = tunable(1.0)
    rot_multiplier = tunable(0.5)

    strafe_y_multiplier = tunable(0.5)
    strafe_x_multiplier = tunable(0.5)

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

    def strafe(self, left: bool, right: bool, forward: bool, backward: bool):
        """
        Override move to move finely, i.e. when aligning to a target.
        :param left: Move left?
        :param right: Move right?
        :param forward: Move forward?
        :param backward: Move backward?
        """
        if left or right or forward or backward:
            if left:
                self.x -= 1
            if right:
                self.x += 1
            if forward:
                self.y += 1
            if backward:
                self.y -= 1

            self.y *= self.strafe_y_multiplier
            self.x *= self.strafe_x_multiplier
            self.rot = 0

    def execute(self):
        """
        Handle driving.
        """
        self.train.driveCartesian(
            self.y_multiplier * self.y,
            self.x_multiplier * self.x,
            self.rot_multiplier * self.rot
        )
