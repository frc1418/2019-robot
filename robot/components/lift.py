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
    # TODO: Use get() to find actual starting position of piston
    lift_forward = tunable(False)
    motion_constant = tunable(0.6)

    target_kp = tunable(0.0001)
    target_ki = tunable(0.00)
    target_kd = tunable(0.00)
    target_tolerance = tunable(100)
    previous_error = 0

    ENCODER_TICKS_PER_REVOLUTION = 12345  # FIXME: NOT THE REAL VALUE!

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
        return self.lift_motor.getSelectedSensorPosition()

    def target(self, target_ticks) -> bool:
        """
        Adjusts the lift using PID to a given number of ticks.

        :param target_ticks: Position in ticks desired.
        :returns: Whether robot has reached requested position
        """
        tick_error = target_ticks - self.current_ticks
        if abs(tick_error) > self.target_tolerance:
            self.i_err += tick_error
            self.lift_speed = self.target_kp * tick_error + self.target_ki * self.i_err + self.target_kd * (self.previous_error - tick_error) / 0.020

            self.previous_error = tick_error
            return False
        self.i_err = 0
        return True

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

    def actuate(self):
        """
        Move lift forward or backward using piston.
        """
        if self.lift_forward:
            self.back()
        else:
            self.forward()

    def forward(self):
        """
        Move lift forward with piston.
        """
        self.lift_forward = True

    def back(self):
        """
        Move lift backward with piston.
        """
        self.lift_forward = False

    def execute(self):
        """
        Run elevator motors.
        """
        print(self.lift_motor.getSelectedSensorPosition())
        self.lift_motor.set(self.lift_speed)
        self._current_height = self.current_ticks

        if self.lift_forward:
            self.lift_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        else:
            self.lift_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
