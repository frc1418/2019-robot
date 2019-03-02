import wpilib


class Climber:
    """
    Piston set for pushing robot into the air.
    """
    front_climb_piston: wpilib.DoubleSolenoid
    back_climb_piston: wpilib.DoubleSolenoid

    front_extended = False
    back_extended = False

    def extend_front(self):
        """
        Extend front piston.
        """
        if not self.front_extended:
            self.front_climb_piston.set(wpilib.DoubleSolenoid.Value.kForward)
            self.front_extended = True

    def retract_front(self):
        """
        Retract front piston.
        """
        if self.front_extended:
            self.front_climb_piston.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.front_extended = False

    def extend_back(self):
        """
        Extend back piston.
        """
        if not self.back_extended:
            self.back_climb_piston.set(wpilib.DoubleSolenoid.Value.kForward)
            self.back_extended = True

    def retract_back(self):
        """
        Retract back piston.
        """
        if self.back_extended:
            self.back_climb_piston.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.back_extended = False

    def execute(self):
        """
        Run component.
        """
        pass
