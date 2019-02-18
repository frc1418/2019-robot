import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class CargoManipulator:
    """
    Operate cargo manipulation system.
    """
    cargo_intake_motors: wpilib.SpeedControllerGroup

    pull_speed = tunable(0.6)
    push_speed = tunable(0.6)
    intake_speed = will_reset_to(0)

    def pull(self):
        """
        """
        self.intake_speed = -self.pull_speed

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
        self.cargo_intake_motors.set(-self.intake_speed)
