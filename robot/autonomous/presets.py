from .modular import Modular


class Rocket(Modular):
    target = Target.ROCKET


class Ball(Modular):
    target = Target.CARGO


class Hatch(Modular):
    game_object = Game_object.HATCH


class Cargo(Modular):
    game_object = Game_object.BALL


class RocketHatch(Rocket, Hatch):
    MODE_NAME = 'RocketHatch'


class RocketBall(Rocket, Ball):
    MODE_NAME = 'RocketBall'


class CargoHatch(Cargo, Hatch):
    MODE_NAME = 'CargoHatch'


class CargoBall(Cargo, Ball):
    MODE_NAME = 'CargoBall'
