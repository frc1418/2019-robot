import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class Climber:
    """
    Piston set for pushing robot into the air.
    """
    front_climb_piston: wpilib.DoubleSolenoid
    back_climb_piston: wpilib.DoubleSolenoid

    front_extended = will_reset_to(False)
    back_extended = will_reset_to(False)

    def extend_front(self):
        """
        Extend front piston.
        """
        self.front_extended = True

    def retract_front(self):
        """
        Retract front piston.
        """
        self.front_extended = False

    def extend_back(self):
        """
        Extend back piston.
        """
        self.back_extended = True

    def retract_back(self):
        """
        Retract back piston.
        """
        self.extended = False

    def execute(self):
        """
        Run component.
        """
        if self.front_extended:
            self.front_climb_piston.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.front_climb_piston.set(wpilib.DoubleSolenoid.Value.kReverse)
        if self.back_extended:
            self.back_climb_piston.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.back_climb_piston.set(wpilib.DoubleSolenoid.Value.kReverse)
