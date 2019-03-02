import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class HatchManipulator:
    """
    Operate robot object-lifting mechanism.
    """
    hatch_solenoid: wpilib.DoubleSolenoid

    def on_enable(self):
        """
        Called when robot is enabled.
        """
        self.position = self.hatch_solenoid.get()
        self.retract()

    def extend(self):
        """
        Extend hatch pistons.
        """
        self.requested_position = wpilib.DoubleSolenoid.Value.kForward

    def retract(self):
        """
        Retract hatch pistons.
        """
        self.requested_position = wpilib.DoubleSolenoid.Value.kReverse

    def execute(self):
        """
        Run component.
        """
        # TODO: Reimplement extended tunable
        if self.requested_position != self.position:
            self.position = self.requested_position
            self.hatch_solenoid.set(self.position)
