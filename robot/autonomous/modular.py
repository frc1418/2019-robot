from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive

from magicbot import tunable
from networktables.util import ntproperty
from enum import Enum


class Target(Enum):
    ROCKET = 0
    CARGO = 1


class GameObject(Enum):
    HATCH = 0
    BALL = 1


class Position(Enum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class Modular(AutonomousStateMachine):
    """
    Modular autonomous.
    Should not be executed on its own.
    """
    DEFAULT = False

    drive: drive.Drive

    position = ntproperty('/autonomous/position', '')
    target = ntproperty('/autonomous/target', '')  # rocket or cargo ship
    game_object = ntproperty('/autonomous/game_object', '')  # hatch or ball

    def direction(self):
        """
        Return directional multiplier based on position.
        """
        if self.position == Position.LEFT:
            return -1
        elif self.position == Position.RIGHT:
            return 1
        # TODO: handle positions that are not left or right

    # Basic outline of autonomous steps (edit/add steps in future)
    @state(first=True)
    def start(self):
        """
        Perform any necessary beginning tasks.
        """
        self.next_state('off_platform')

    @state
    def off_platform(self):
        """
        Move forward off of the habitat.
        """
        self.next_state('forward')

    @state
    def forward(self):
        """
        Move forward to the desired location for either the cargo ship or rocket.
        """
        if self.target == Target.ROCKET:
            # self.drive.move(x)
            self.next_state('align_rocket')
        elif self.target == Target.CARGO:
            # self.drive.move(y)
            self.next_state('align_cargo')

    @state
    def align_rocket(self):
        """
        Align robot with rocket using vision processing.
        """
        self.next_state('park')

    @state
    def align_cargo(self):
        """
        Align robot with cargo ship opening using vision processing.
        """
        self.next_state('park')

    @state
    def park(self):
        """
        Park up to rocket to deliver game object.
        """
        if self.target == Target.ROCKET:
            # self.drive.move(x)
            if self.game_object == GameObject.HATCH:
                self.next_state('deliver_hatch_rocket')
            elif self.game_object == GameObject.BALL:
                self.next_state('deliver_ball_rocket')
        elif self.target == Target.CARGO:
            # self.drive.move(y)
            if self.game_object == GameObject.HATCH:
                self.next_state('deliver_hatch_rocket')
            elif self.game_object == GameObject.BALL:
                self.next_state('deliver_ball_rocket')
        # TODO: handle targets that are not hatch or rocket

    @state
    def deliver_hatch_rocket(self):
        """
        Insert a hatch into rocket.
        """
        pass

    @state
    def deliver_hatch_cargo(self):
        """
        Insert a hatch into cargo ship opening.
        """
        pass

    @state
    def deliver_ball_rocket(self):
        """
        Insert a ball into rocket.
        """
        pass

    @state
    def deliver_ball_cargo(self):
        """
        Insert  a ball into cargo ship opening.
        """
        pass

    # Add more states as needed
