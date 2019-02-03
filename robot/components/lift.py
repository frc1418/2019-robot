import wpilib
from magicbot import will_reset_to
from magicbot import tunable

from ctre.wpi_talonsrx import WPI_TalonSRX


class Lift:
    """
    Operate robot object-lifting mechanism.
    """
    lift_motors: wpilib.SpeedControllerGroup

    lift_speed = will_reset_to(0)
    motion_constant = tunable(0.6)

    def move(self, speed: float):
        """
        Set the motor speed of the lift.
        :param speed: The requested speed, between -1 and 1.
        """
        self.lift_speed = speed

    def up(self):
        """
        Move lift upward.
        Used when controlling arm through buttons.
        """
        self.lift_speed = 1 * self.motion_constant

    def down(self):
        """
        Move lift downward.
        Used when controlling arm through buttons.
        """
        self.lift_speed = -1 * self.motion_constant

    def execute(self):
        """
        Run elevator motors.
        """
        self.lift_motors.set(-self.lift_speed)
