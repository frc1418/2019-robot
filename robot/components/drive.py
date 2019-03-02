import wpilib
import wpilib.drive
import navx
from magicbot import will_reset_to
from magicbot import tunable


class Drive:
    """
    Handle robot drivetrain.
    All drive interaction must go through this class.
    """

    train: wpilib.drive.MecanumDrive
    # tank_train: wpilib.drive.DifferentialDrive
    navx: navx.AHRS

    y = will_reset_to(0)
    x = will_reset_to(0)
    rot = will_reset_to(0)

    y_multiplier = (1.0)
    x_multiplier = (1.0)
    rot_multiplier = (0.9)
    slow_rot_multiplier = (0.3)

    strafe_y_multiplier = (0.5)
    strafe_x_multiplier = (0.5)

    left_speed = will_reset_to(0)
    right_speed = will_reset_to(0)
    mecanum = will_reset_to(True)

    align_kp = (0.99)
    align_ki = (0.20)
    align_kd = (0.00)
    align_tolerance = (1)
    align_max_rot = (.3)
    previous_error = 0

    def __init__(self):
        self.enabled = False

    def setup(self):
        """
        Configure drivetrain at start.
        """
        pass

    def on_enable(self):
        """
        Prepare component for operation.
        """
        self.i_err = 0

    def move(self, x: float, y: float, rot: float, real: bool = False, slow_rot: bool = False):
        """
        Move robot.
        :param x: Speed of motion in the FORWARD AXIS. [-1..1]
        :param y: Speed of motion in the LEFT-RIGHT AXIS. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        :param real: Is a real driver at the controls? Hence, should drive constants be accounted for?
        :param slow_rot: Should we slow down rotation for alignment?
        """
        if real:
            x *= self.x_multiplier
            y *= self.y_multiplier
            rot *= self.rot_multiplier
        if slow_rot:
            rot *= self.slow_rot_multiplier
        self.x = x
        self.y = y
        self.rot = rot

    def strafe(self, left: bool, right: bool, forward: bool, backward: bool):
        """
        Move finely, i.e. when aligning to a target.
        :param left: Move left?
        :param right: Move right?
        :param forward: Move forward?
        :param backward: Move backward?
        """
        if left or right or forward or backward:
            self.x = 0
            self.y = 0

            if left:
                self.y -= 1
            if right:
                self.y += 1
            if forward:
                self.x += 1
            if backward:
                self.x -= 1

            self.x *= self.strafe_x_multiplier
            self.y *= self.strafe_y_multiplier

    def move_tank(self, left_speed: float, right_speed: float):
        """
        Move using the differential drive object
        :param left_speed: The speed of the left side of the drivetrain
        :param right_speed: The speed of the right side of the drivetrain
        """
        self.left_speed = left_speed
        self.right_speed = right_speed
        self.mecanum = False

    @property
    def angle(self):
        """
        Get current angle of robot.
        """
        return self.navx.getYaw()

    def align(self, target_angle) -> bool:
        """
        Adjusts the robot so that it points at a particular angle.

        :param target_angle: Angle to point at, in degrees
        :returns: Whether robot has reached requested angle
        """
        angle_error = target_angle - self.angle
        print(f"angle_error: {angle_error}, target_angle: {target_angle}, current angle: {self.angle}")
        # Ensure that robot turns the quickest direction to get to the desired angle
        if angle_error > 180:
            angle_error -= 360
        if abs(angle_error) > self.align_tolerance:
            self.i_err += angle_error
            self.rot = self.align_kp * angle_error + self.align_ki * self.i_err + self.align_kd * (self.previous_error - angle_error) / 0.020
            self.rot = max(min(self.align_max_rot, self.rot), -self.align_max_rot)

            self.previous_error = angle_error
            return False
        self.i_err = 0
        return True

    def execute(self):
        """
        Handle driving.
        """
        self.train.driveCartesian(self.y, self.x, self.rot)
        """
        if self.mecanum:
            self.train.driveCartesian(self.y, self.x, self.rot)
            self.tank_train.feed()
        else:
            self.tank_train.tankDrive(self.left_speed, self.right_speed)
            self.train.feed()
        """
