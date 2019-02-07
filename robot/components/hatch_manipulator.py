import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class HatchManipulator:
    """
    Operate robot object-lifting mechanism.
    """
    hatch_solenoid: wpilib.DoubleSolenoid

    extended = will_reset_to(False)

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
        Extend hatch piston.
        """
        self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    def retract(self):
        """
        Retract hatch_solenoid.
        """
        self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

    def actuate(self):
        """
        Extend or retract hatch_solenoid based on current position.
        """
        if self.is_extended:
            self.retract()
        else:
            self.extend()

    def execute(self):
        """
        Run component.
        """
        if self.extended:
            self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
