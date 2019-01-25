from networktables.util import ntproperty
from components import drive

from magicbot import StateMachine, state
# TODO: Use this to automate shooting process at the end and things like that
# from automations import
from magicbot import tunable


class SeekTarget(StateMachine):
    drive: drive.Drive
    # TODO: define automations too

    # TODO: use better name
    yaw = ntproperty('/PiData/yawToTarget', 0)

    @state(first=True, must_finish=True)
    def align(self, initial_call):
        """
        Turn to face tower.
        """
        # TODO: This is a very bad way to run it
        self.drive.move(0.3, 0, self.yaw / 10)
        if self.yaw == 0:
            self.done()
