from networktables.util import ntproperty
from components import lift

from magicbot import StateMachine, state, timed_state, tunable


class SeekTarget(StateMachine):
    lift: lift.Lift

    # TODO: better name
    terminal_angle = 0

    def seek(self):
        """
        Engage automation.
        """
        self.engage()

    @state(first=True, must_finish=True)
    def align(self, initial_call):
        """
        Turn to face tower.
        """
        if initial_call:
            self.terminal_position = self.lift.ticks + 3000
        if self.drive.align(self.terminal_angle):
            self.next_state('advance')
