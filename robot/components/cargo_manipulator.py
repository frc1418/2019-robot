import wpilib
from magicbot import will_reset_to
from magicbot import tunable
from ctre.wpi_talonsrx import WPI_TalonSRX


class CargoManipulator:
    """
    Operate cargo manipulation system.
    """
    # cargo_intake_motors: wpilib.SpeedControllerGroup
    left_cargo_intake_motor: WPI_TalonSRX

    pull_speed = (0.5)
    light_pull_speed = (0.2)
    push_speed = (1.0)
    intake_speed = will_reset_to(0)

    def pull(self):
        """
        """
        self.intake_speed = -self.pull_speed

    def pull_lightly(self):
        """
        Pull at a lower speed, to hold in ball.
        """
        self.intake_speed = -self.light_pull_speed

    def push(self):
        """
        Move lift downward.
        Used when controlling arm through buttons.
        """
        self.intake_speed = self.push_speed

    def execute(self):
        """
        Run elevator motors.
        """
        # self.cargo_intake_motors.set(-self.intake_speed)
        self.left_cargo_intake_motor.set(self.intake_speed)
