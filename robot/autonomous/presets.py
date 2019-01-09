from .modular import Modular


class Rocket(Modular):
    game_object = 'rocket'


class Ball(Modular):
    game_object = 'ball'


class Hatch(Modular):
    game_object = 'hatch'


class Cargo(Modular):
    target = 'cargo'


class RocketHatch(Rocket, Hatch):
    MODE_NAME = 'RocketHatch'


class RocketBall(Rocket, Ball):
    MODE_NAME = 'RocketBall'


class CargoHatch(Cargo, Hatch):
    MODE_NAME = 'CargoHatch'


class CargoBall(Cargo, Ball):
    MODE_NAME = 'CargoBall'
