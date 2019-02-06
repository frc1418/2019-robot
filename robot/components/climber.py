import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class Climber:
    """
    Piston set for pushing robot into the air.
    """
    front_climb_piston: wpilib.DoubleSolenoid

    extended = will_reset_to(False)

    def extend_front(self):
        """
        Extend front piston.
        """
        self.extended = True

    def retract_front(self):
        """
        Retract front piston.
        """
        self.extended = False

    def execute(self):
        """
        Run component.
        """
        if self.extended:
            self.front_climb_piston.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.front_climb_piston.set(wpilib.DoubleSolenoid.Value.kReverse)
