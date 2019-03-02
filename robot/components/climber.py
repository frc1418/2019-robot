import wpilib


class Climber:
    """
    Piston set for pushing robot into the air.
    """
    front_climb_piston: wpilib.DoubleSolenoid
    back_climb_piston: wpilib.DoubleSolenoid

    def on_enable(self):
        """
        Called when robot is enabled.
        """
        self.front_position = self.front_climb_piston.get()
        self.retract_front()
        self.back_position = self.back_climb_piston.get()
        self.retract_back()

    def extend_front(self):
        """
        Extend front piston.
        """
        self.requested_front_position = wpilib.DoubleSolenoid.Value.kForward

    def retract_front(self):
        """
        Retract front piston.
        """
        self.requested_front_position = wpilib.DoubleSolenoid.Value.kReverse

    def extend_back(self):
        """
        Extend back piston.
        """
        self.requested_back_position = wpilib.DoubleSolenoid.Value.kForward

    def retract_back(self):
        """
        Retract back piston.
        """
        self.requested_back_position = wpilib.DoubleSolenoid.Value.kReverse

    def execute(self):
        """
        Run component.
        """
        if self.requested_front_position != self.front_position:
            self.front_position = self.requested_front_position
            self.front_climb_piston.set(self.front_position)
        if self.requested_back_position != self.back_position:
            self.back_position = self.requested_back_position
            self.back_climb_piston.set(self.back_position)
