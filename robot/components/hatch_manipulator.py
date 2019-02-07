import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class HatchManipulator:
    """
    Operate robot object-lifting mechanism.
    """
    hatch_solenoid: wpilib.DoubleSolenoid

    position = will_reset_to(wpilib.DoubleSolenoid.Value.kReverse)

    @property
    def is_extended(self):
        """
        Get whether robot hatch pistons are extended.
        """
        return self.hatch_solenoid.get() == wpilib.DoubleSolenoid.Value.kForward

    @property
    def is_retracted(self):
        """
        Get whether robot hatch pistons are retracted.
        """
        return self.hatch_solenoid.get() == wpilib.DoubleSolenoid.Value.kReverse

    def extend(self):
        """
        Extend hatch pistons.
        """
        self.position = wpilib.DoubleSolenoid.Value.kForward

    def retract(self):
        """
        Retract hatch pistons.
        """
        self.position = wpilib.DoubleSolenoid.Value.kReverse

    def actuate(self):
        """
        Extend or retract hatch pistons based on current position.
        """
        if self.is_extended:
            self.retract()
        else:
            self.extend()

    def execute(self):
        """
        Run component.
        """
        self.hatch_solenoid.set(self.position)
