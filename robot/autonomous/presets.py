from .modular import Modular, Target, GameObject
from trajectory_generator import Trajectory


class Rocket(Modular):
    target = Target.ROCKET


class Cargo(Modular):
    target = Target.CARGO


class Ball(Modular):
    game_object = GameObject.BALL


class Hatch(Modular):
    game_object = GameObject.HATCH


class RocketHatch(Rocket, Hatch):
    MODE_NAME = 'RocketHatch'


class RocketBall(Rocket, Ball):
    MODE_NAME = 'RocketBall'

class CargoHatch(Cargo, Hatch):
    MODE_NAME = 'CargoHatch'


class CargoBall(Cargo, Ball):
    MODE_NAME = 'CargoBall'
