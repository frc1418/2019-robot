from networktables.util import ntproperty
from components import lift

from magicbot import StateMachine, state, timed_state, tunable


class MoveLift(StateMachine):
    lift: lift.Lift

    # TODO: better name
    terminal_angle = 0

    def seek(self):
        """
        Engage automation.
        """
        self.engage()

    @state(first=True, must_finish=True)
    def reposition(self, initial_call):
        """
        Turn to face tower.
        """
        if initial_call:
            self.terminal_position = self.lift.ticks + 3000  # FIXME: This is just an arbitrary value
        if self.lift.target(self.terminal_position):
            self.done()
