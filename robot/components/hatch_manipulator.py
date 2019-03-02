import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class HatchManipulator:
    """
    Operate robot object-lifting mechanism.
    """

    hatch_solenoid: wpilib.DoubleSolenoid

    position = will_reset_to(wpilib.DoubleSolenoid.Value.kReverse)
    extended = tunable(False)

    _extend_position = wpilib.DoubleSolenoid.Value.kForward
    _retract_position = wpilib.DoubleSolenoid.Value.kReverse

    _cached_position = None

    def on_enable(self):
        """
        Component setup
        """
        self._cached_position = None

    @property
    def is_extended(self):
        """
        Get whether robot hatch pistons are extended.
        """
        return self._cached_position == self._extend_position

    @property
    def is_retracted(self):
        """
        Get whether robot hatch pistons are retracted.
        """
        return self._cached_position == self._retract_position

    def extend(self):
        """
        Extend hatch pistons.
        """
        self.position = self._extend_position

    def retract(self):
        """
        Retract hatch pistons.
        """
        self.position = self._retract_position

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
        # only update the solenoid when a change is asked for
        # .. this isn't like a motor, there's no watchdog
        if self._cached_position != self.position:
            self._cached_position = self.position
            self.extended = self.is_extended
            self.hatch_solenoid.set(self.position)
