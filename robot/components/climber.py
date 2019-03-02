import wpilib


class Climber:
    """
    Piston set for pushing robot into the air.
    """
    front_climb_piston: wpilib.DoubleSolenoid
    back_climb_piston: wpilib.DoubleSolenoid

    # TODO: on_enable, get() the actual position.
    front_position = wpilib.DoubleSolenoid.Value.kForward
    requested_front_position = wpilib.DoubleSolenoid.Value.kReverse
    back_position = wpilib.DoubleSolenoid.Value.kForward
    requested_back_position = wpilib.DoubleSolenoid.Value.kReverse

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
