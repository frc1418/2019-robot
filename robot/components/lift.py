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
    lift_switch: wpilib.DigitalInput
    lift_solenoid: wpilib.DoubleSolenoid

    _current_height = ntproperty('/components/lift/height', 0)

    lift_speed = will_reset_to(0)
    lift_forward = tunable(False)
    motion_constant = tunable(1.0)

    target_kp = tunable(0.00001)
    target_ki = tunable(0.0000000001)
    target_kd = tunable(0.00)
    target_tolerance = tunable(100)
    previous_error = 0
    zero = 0

    ENCODER_TICKS_PER_REVOLUTION = 55000  # May not be real value, double check

    targets = {
        11: -10000000,  # bottom hatch, go until hitting bottom TODO make this better
        9: 920_000,
        7: 1_870_000,  # top hatch

        12: 725_000,  # bottom cargo
        10: 1_590_000,  # middle cargo
        8: 2_310_000,  # top cargo
    }
    current_goal = 0
    current_target = 11
    correction_speed = tunable(10000)
    correction_deadband = tunable(0.2)

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
        print(f"tick_error: {tick_error}, target_ticks: {self.current_goal}, current ticks: {self.current_ticks}, zero: {self.zero}, speed: {self.lift_speed}, limited: {not self.lift_switch.get()}")

        # TODO: Fix inverted limit switch
        if not self.lift_switch.get():
            self.zero = self.lift_motor.getSelectedSensorPosition()
            if self.current_goal < 0:
                self.current_goal = 0
        # Check if we're within range of target
        if abs(tick_error) > self.target_tolerance:
            # If we're not close enough, calculate our needed speed through PID
            self.i_err += tick_error
            self.lift_speed = self.target_kp * tick_error + self.target_ki * self.i_err + self.target_kd * (self.previous_error - tick_error) / 0.020

            self.previous_error = tick_error
            return False

        self.i_err = 0
        return True

    def correct(self, magnitude: float):
        """
        Correct for offset on preset.
        :param magnitude: joystick input telling us how far to modify position.
        """
        print(f"Correction magnitude: {magnitude}, current target: {self.current_target}, current goal: {self.current_goal}")
        if magnitude > self.correction_deadband:
            self.targets[self.current_target] += int(magnitude * self.correction_speed)
            self.current_goal = self.targets[self.current_target]

    def target(self, target: int):
        """
        Use our PID to move to a given target.
        :param target: index of target to move toward.
        """
        self.current_target = target
        self.current_goal = self.targets[target]

    def move(self, speed: float):
        """
        Set the motor speed of the lift.
        :param speed: The requested speed, between -1 and 1.
        """
        print(f'Lift limit: {not self.lift_switch.get()}')
        if not self.lift_switch.get() and speed < 0:
            # TODO: This is a clumsy way to do it
            speed = 0
        self.current_goal = self.current_ticks
        self.lift_speed = speed

    @property
    def is_extended(self):
        """
        Get whether robot hatch pistons are extended.
        """
        return self.lift_solenoid.get() == wpilib.DoubleSolenoid.Value.kForward

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
        if self.is_extended:
            self.back()
        else:
            self.forward()

    def execute(self):
        """
        Run elevator motors.
        """
        self.lift_motor.set(self.lift_speed)
        self._current_height = self.current_ticks
        self.lift_forward = self.is_extended
