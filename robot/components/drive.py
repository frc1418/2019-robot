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
        Configure drivetrain at start.
        """
        pass

    def move(self, y: float, x: float, rot: float, real: bool = False):
        """
        Move robot.
        :param y: Speed of motion in the y direction. [-1..1]
        :param x: Speed of motion in the x direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        :param real: Is a real driver at the controls? Hence, should drive constants be accounted for?
        """
        if real:
            y *= self.y_multiplier
            x *= self.x_multiplier
            rot *= self.rot_multiplier
        self.y = y
        self.x = x
        self.rot = rot

    def strafe(self, left: bool, right: bool, forward: bool, backward: bool):
        """
        Move finely, i.e. when aligning to a target.
        :param left: Move left?
        :param right: Move right?
        :param forward: Move forward?
        :param backward: Move backward?
        """
        if left or right or forward or backward:
            self.x = 0
            self.y = 0

            if left:
                self.y -= 1
            if right:
                self.y += 1
            if forward:
                self.x += 1
            if backward:
                self.x -= 1

            self.y *= self.strafe_y_multiplier
            self.x *= self.strafe_x_multiplier
            self.rot = 0

    def execute(self):
        """
        Handle driving.
        """
        self.train.driveCartesian(self.y, self.x, self.rot)
