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

    _front_cache = None
    _back_cache = None

    def on_enable(self):
        """
        Component setup
        """
        self._front_cache = None
        self._back_cache = None

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
        self.back_extended = False

    def execute(self):
        """
        Run component.
        """
        if self.front_extended:
            front = wpilib.DoubleSolenoid.Value.kForward
        else:
            front = wpilib.DoubleSolenoid.Value.kReverse

        if self.back_extended:
            back = wpilib.DoubleSolenoid.Value.kForward
        else:
            back = wpilib.DoubleSolenoid.Value.kReverse

        # only update the solenoid when a change is asked for
        # .. this isn't like a motor, there's no watchdog

        if front != self._front_cache:
            self._front_cache = front
            self.front_climb_piston.set(front)

        if back != self._back_cache:
            self._back_cache = back
            self.back_climb_piston.set(back)
