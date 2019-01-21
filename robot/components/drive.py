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

    fine_movement = will_reset_to(False)
    fine_speed_multiplier = tunable(0.5)
    fine_rotation_multiplier = tunable(0.5)

    def __init__(self):
        self.enabled = False

    def setup(self):
        """
        Set input threshold.
        """
        self.train.setDeadband(0.1)

    def move(self, y: float, x: float, rot: float, fine_movement: bool = False, unidirectional: bool = False):
        """
        Move robot.
        :param y: Speed of motion in the y direction. [-1..1]
        :param x: Speed of motion in the x direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        :param fine_movement: Decrease speeds for precise motion.
        :param unidirectional: Move only in x or y plane, zeroing other axis for straight motion
        """
        if unidirectional:
            if abs(y) >= abs(x):
                x = 0
            else:
                y = 0
        self.y = y
        self.x = x
        self.rot = rot
        self.fine_movement = fine_movement

    def execute(self):
        """
        Handle driving.
        """
        self.train.driveCartesian(
            self.speed_constant * self.y * (self.fine_speed_multiplier if self.fine_movement else 1),
            self.speed_constant * self.x * (self.fine_speed_multiplier if self.fine_movement else 1),
            self.rotational_constant * self.rot * (self.fine_rotation_multiplier if self.fine_movement else 1)
        )
