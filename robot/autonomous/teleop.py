import magicbot


class TeleopSandstorm:
    """
    Run teleop mode during autonomous.
    """
    MODE_NAME = "Teleoperated"
    DEFAULT = True

    robot: magicbot.MagicRobot

    def on_enable(self):
        """
        """
        pass

    def on_disable(self):
        """
        """
        pass

    def on_iteration(self, _time_elapsed):
        """
        Run teleop loop.
        :param _time_elapsed: time since beginning of autonomous mode.
        """
        self.robot.teleopPeriodic()
