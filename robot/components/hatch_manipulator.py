import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class HatchManipulator:
    """
    Operate robot object-lifting mechanism.
    """
    hatch_solenoid: wpilib.DoubleSolenoid

    extended = will_reset_to(False)

    def extend(self):
        """
        Extend hatch piston.
        """
        self.extended = True

    def retract(self):
        """
        Retract hatch_solenoid.
        """
        self.extended = False

    def actuate(self):
        """
        Extend or retract hatch_solenoid based on current position.
        """
        """
        if self.is_retracted:
            self.extend()
        else:
            self.retract()

        self.extended = self.is_extended
        """
        if self.extended:
            self.retract()
        else:
            self.extend()
        self.extended = not self.extended

    def execute(self):
        """
        Run component.
        """
        if self.extended:
            self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.hatch_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
