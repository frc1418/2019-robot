from networktables.util import ntproperty
from components import drive

from magicbot import StateMachine, state
# TODO: Use this to automate shooting process at the end and things like that
# from automations import
from magicbot import tunable


class SeekTarget(StateMachine):
    drive: drive.Drive
    # TODO: define automations too

    yaw = ntproperty('/vision/target_yaw', 0)
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
        self.yaw = 90
        if initial_call:
            self.terminal_angle = self.drive.angle + self.yaw
        if self.drive.align(self.terminal_angle):
            self.done()
