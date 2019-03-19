import magicbot
import wpilib
import wpilib.drive

from wpilib.buttons import JoystickButton
from robotpy_ext.control.button_debouncer import ButtonDebouncer
# from controllers import recorder
from components import drive, lift, hatch_manipulator, cargo_manipulator, climber, trajectory_follower
from automations import seek_target
from magicbot import tunable
from trajectory_generator import load_trajectories
import math

import navx
from ctre.wpi_talonsrx import WPI_TalonSRX


class Robot(magicbot.MagicRobot):
    # Automations
    # TODO: bad name
    seek_target: seek_target.SeekTarget

    # Controllers
    # recorder: recorder.Recorder

    # Components
    follower: trajectory_follower.TrajectoryFollower

    drive: drive.Drive
    lift: lift.Lift
    hatch_manipulator: hatch_manipulator.HatchManipulator
    cargo_manipulator: cargo_manipulator.CargoManipulator
    climber: climber.Climber

    ENCODER_PULSE_PER_REV = 1024
    WHEEL_DIAMETER = 0.5

    """
    manual_lift_control = tunable(True)
    stabilize = tunable(False)
    stabilizer_threshold = tunable(30)
    stabilizer_aggression = tunable(5)
    """

    """
    time = tunable(0)
    voltage = tunable(0)
    yaw = tunable(0)
    """

    def createObjects(self):
        """
        Initialize robot components.
        """
        # For using teleop in autonomous
        self.robot = self

        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.joystick_alt = wpilib.Joystick(2)

        # Buttons
        self.button_strafe_left = JoystickButton(self.joystick_left, 4)
        self.button_strafe_right = JoystickButton(self.joystick_left, 5)
        self.button_strafe_forward = JoystickButton(self.joystick_left, 3)
        self.button_strafe_backward = JoystickButton(self.joystick_left, 2)
        self.button_slow_rotation = JoystickButton(self.joystick_right, 4)

        self.button_lift_actuate = ButtonDebouncer(self.joystick_alt, 2)
        self.button_manual_lift_control = ButtonDebouncer(self.joystick_alt, 6)
        self.button_hatch_kick = JoystickButton(self.joystick_alt, 1)
        self.button_cargo_push = JoystickButton(self.joystick_alt, 5)
        self.button_cargo_pull = JoystickButton(self.joystick_alt, 3)
        self.button_cargo_pull_lightly = JoystickButton(self.joystick_alt, 4)
        self.button_climb_front = JoystickButton(self.joystick_right, 3)
        self.button_climb_back = JoystickButton(self.joystick_right, 2)

        self.button_target = JoystickButton(self.joystick_right, 8)

        # Drive motor controllers
        # ID SCHEME:
        #   10^1: 1 = left, 2 = right
        #   10^0: 0 = front, 5 = rear
        self.lf_motor = WPI_TalonSRX(10)
        self.lr_motor = WPI_TalonSRX(15)
        self.rf_motor = WPI_TalonSRX(20)
        self.rr_motor = WPI_TalonSRX(25)

        encoder_constant = (
            (1 / self.ENCODER_PULSE_PER_REV) * self.WHEEL_DIAMETER * math.pi
        )

        self.r_encoder = wpilib.Encoder(0, 1)
        self.r_encoder.setDistancePerPulse(encoder_constant)
        self.l_encoder = wpilib.Encoder(2, 3)
        self.l_encoder.setDistancePerPulse(encoder_constant)
        self.l_encoder.setReverseDirection(True)

        # Drivetrain
        self.train = wpilib.drive.MecanumDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)

        # Functional motors
        self.lift_motor = WPI_TalonSRX(40)
        self.lift_motor.setSensorPhase(True)
        self.lift_switch = wpilib.DigitalInput(4)
        self.lift_solenoid = wpilib.DoubleSolenoid(2, 3)
        self.hatch_solenoid = wpilib.DoubleSolenoid(0, 1)
        self.left_cargo_intake_motor = WPI_TalonSRX(35)
        # TODO: electricians soldered one motor in reverse.
        # self.left_cargo_intake_motor.setInverted(True)
        self.right_cargo_intake_motor = WPI_TalonSRX(30)
        """
        self.cargo_intake_motors = wpilib.SpeedControllerGroup(self.left_cargo_intake_motor,
                                                               self.right_cargo_intake_motor)
        """
        self.right_cargo_intake_motor.follow(self.left_cargo_intake_motor)
        self.front_climb_piston = wpilib.DoubleSolenoid(4, 5)
        self.back_climb_piston = wpilib.DoubleSolenoid(6, 7)

        # Tank Drivetrain
        """
        self.tank_train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                         wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))
        """

        # Load trajectories
        self.generated_trajectories = load_trajectories()

        # NavX
        self.navx = navx.AHRS.create_spi()
        self.navx.reset()

        # Utility
        # self.ds = wpilib.DriverStation.getInstance()
        # self.timer = wpilib.Timer()
        self.pdp = wpilib.PowerDistributionPanel(0)
        self.compressor = wpilib.Compressor()

        # Camera server
        wpilib.CameraServer.launch('camera/camera.py:main')
        wpilib.LiveWindow.disableAllTelemetry()

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        # self.time = int(self.timer.getMatchTime())
        # self.voltage = self.pdp.getVoltage()
        # self.yaw = self.navx.getAngle() % 360
        pass

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Call autonomous
        super().autonomous()

    def disabledInit(self):
        """
        Executed once right away when robot is disabled.
        """
        # Reset Gyro to 0
        self.navx.reset()

    def disabledPeriodic(self):
        """
        Executed periodically while robot is disabled.
        Useful for testing.
        """
        pass

    def teleopInit(self):
        """
        Executed when teleoperated mode begins.
        """
        self.lift.zero = self.lift_motor.getSelectedSensorPosition()
        self.lift.current_position = 5000000
        self.compressor.start()

    def teleopPeriodic(self):
        """
        Executed periodically while robot is in teleoperated mode.
        """
        # Read from joysticks and move drivetrain accordingly
        self.drive.move(x=-self.joystick_left.getY(),
                        y=self.joystick_left.getX(),
                        rot=self.joystick_right.getX(),
                        real=True,
                        slow_rot=self.button_slow_rotation.get())

        """
        self.drive.strafe(self.button_strafe_left.get(),
                          self.button_strafe_right.get(),
                          self.button_strafe_forward.get(),
                          self.button_strafe_backward.get())
        """

        """
        for button in range(7, 12 + 1):
            if self.joystick_alt.getRawButton(button):
                self.lift.target(button)
        """
        # if self.manual_lift_control:
        self.lift.move(-self.joystick_alt.getY())
        """
        else:
            # self.lift.correct(-self.joystick_alt.getY())
            # self.lift.approach()
            pass
        """
        """
        if self.button_manual_lift_control:
            # self.manual_lift_control = not self.manual_lift_control
            pass
        """

        if self.button_hatch_kick.get():
            self.hatch_manipulator.extend()
        else:
            self.hatch_manipulator.retract()

        if self.button_target.get():
            self.seek_target.seek()

        if self.button_lift_actuate.get():
            self.lift.actuate()

        if self.button_cargo_push.get():
            self.cargo_manipulator.push()
        elif self.button_cargo_pull.get():
            self.cargo_manipulator.pull()
        elif self.button_cargo_pull_lightly.get():
            self.cargo_manipulator.pull_lightly()

        if self.button_climb_front.get():
            self.climber.extend_front()
        else:
            self.climber.retract_front()
        if self.button_climb_back.get():
            self.climber.extend_back()
        else:
            self.climber.retract_back()

        """
        if self.stabilize:
            if abs(self.navx.getPitch()) > self.stabilizer_threshold:
                self.drive.move(self.navx.getPitch() / 180 * self.stabilizer_aggression, 0, 0)
        """


if __name__ == '__main__':
    wpilib.run(Robot)
