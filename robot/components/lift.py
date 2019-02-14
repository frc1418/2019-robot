import wpilib
from magicbot import will_reset_to
from magicbot import tunable
from networktables.util import ntproperty

from ctre.wpi_talonsrx import WPI_TalonSRX


class Lift:
    """
    Operate robot object-lifting mechanism.
    """
    lift_motor: WPI_TalonSRX
    lift_solenoid: wpilib.DoubleSolenoid

    _current_height = ntproperty('/components/lift/height', 0)

    lift_speed = will_reset_to(0)
    motion_constant = tunable(0.6)

    target_kp = tunable(0.00001)
    target_ki = tunable(0.00)
    target_kd = tunable(0.00)
    target_tolerance = tunable(100)
    previous_error = 0
    zero = 0

    ENCODER_TICKS_PER_REVOLUTION = 55000  # May not be real value, double check

    TARGETS = {
        11: 0,  # bottom hatch
        9: 800_000,  # middle hatch
        7: 2_000_000,  # top hatch

        12: 650_000,  # bottom cargo
        10: 1_450_000,  # middle cargo
        8: 2_250_000,  # top cargo
    }
    current_goal = 0

    def on_enable(self):
        """
        Prepare component for operation.
        """
        self.i_err = 0

    @property
    def current_ticks(self):
        """
        Get current position of lift in encoder ticks.
        """
        return self.lift_motor.getSelectedSensorPosition() - self.zero

    def approach(self) -> bool:
        """
        Adjusts the lift using PID to a given number of ticks.
        :returns: Whether robot has reached requested position
        """
        # Get distance to target
        tick_error = self.current_goal - self.current_ticks
        # print(f"tick_error: {tick_error}, target_ticks: {self.current_goal}, current ticks: {self.current_ticks}, zero: {self.zero}, speed: {self.lift_speed}")

        # Check if we're within range of target
        if abs(tick_error) > self.target_tolerance:
            # If we're not close enough, calculate our needed speed through PID
            self.i_err += tick_error
            self.lift_speed = self.target_kp * tick_error + self.target_ki * self.i_err + self.target_kd * (self.previous_error - tick_error) / 0.020

            self.previous_error = tick_error
            return False

        self.i_err = 0
        return True

    def target(self, target: int):
        """
        Use our PID to move to a given target.
        :param target: index of target to move toward.
        """
        self.current_goal = self.TARGETS[target]

    def move(self, speed: float):
        """
        Set the motor speed of the lift.
        :param speed: The requested speed, between -1 and 1.
        """
        self.lift_speed = speed

    def up(self):
        """
        Move lift upward.
        Used when controlling arm through buttons.
        """
        self.lift_speed = 1 * self.motion_constant

    def down(self):
        """
        Move lift downward.
        Used when controlling arm through buttons.
        """
        self.lift_speed = -1 * self.motion_constant

    @property
    def is_retracted(self):
        """
        Get whether robot hatch pistons are extended.
        """
        return self.lift_solenoid.get() == wpilib.DoubleSolenoid.Value.kReverse

    def forward(self):
        """
        Move lift forward with piston.
        """

        self.lift_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

    def back(self):
        """
        Move lift backward with piston.
        """
        self.lift_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

    def actuate(self):
        """
        Move lift forward or backward using piston.
        """
        if self.is_retracted:
            self.forward()
        else:
            self.back()

    def execute(self):
        """
        Run elevator motors.
        """
        self.lift_motor.set(self.lift_speed)
        self._current_height = self.current_ticks
