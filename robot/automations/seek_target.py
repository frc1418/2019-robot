from networktables.util import ntproperty
from components import drive

from magicbot import StateMachine, state, timed_state
# TODO: Use this to automate shooting process at the end and things like that
# from automations import
from magicbot import tunable


class SeekTarget(StateMachine):
    drive: drive.Drive
    # TODO: define automations too

    yaw = ntproperty('/vision/target_yaw', 0)

    def seek(self):
        """
        Engage automation.
        """
        # self.engage()
        self.drive.move(0.3, self.yaw / 20, self.yaw / 20)

    @timed_state(first=True, duration=1, must_finish=True)
    def align(self, initial_call):
        """
        Turn to face tower.
        """
        # TODO: This is a very bad way to run it
        # self.drive.move(0.3, 0, self.yaw / 10)
        # self.drive.move(0, 0, 0.5)
        if self.yaw == 0:
            self.done()
