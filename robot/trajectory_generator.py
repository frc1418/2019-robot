import os
import pickle
import pathfinder as pf
import wpilib
import typing


WHEELBASE_WIDTH = 1.83  # In feet
TRAJECTORY_DIRECTORY = 'trajectories'
PICKLE_FILE = os.path.join(os.path.dirname(__file__), TRAJECTORY_DIRECTORY, 'trajectories.pickle')
MAX_GENERATION_VELOCITY = 4
MAX_GENERATION_ACCELERATION = 20
MAX_GENERATION_JERK = 40

trajectories = {
    "diagonal_higher": [
        pf.Waypoint(0, 0, 0),  # Waypoints are relative to first, so start at 0, 0, 0
        pf.Waypoint(15, 8, 0)
    ],
    "cargo_ship": [
        pf.Waypoint(0, 0, 0),
        pf.Waypoint(7.33, 0, 0)
    ],
    "left-side": [
        pf.Waypoint(0, 0, 0),
        pf.Waypoint(8.33, 6.25, 0)
    ],
    "diagonal": [
        pf.Waypoint(0, 0, 0),  # Waypoints are relative to first, so start at 0, 0, 0
        pf.Waypoint(15, 5, 0)
    ],
    "charge": [
        pf.Waypoint(0, 0, 0),
        pf.Waypoint(10, 0, 0)
    ]
}


def load_trajectories():
    """
    Either generate and write trajectories if in a sim or read them if on the robot.
    """
    if wpilib.RobotBase.isSimulation():
        generated_trajectories = _generate_trajectories()
        _write_trajectories(generated_trajectories)
    else:
        with open(PICKLE_FILE, 'rb') as f:
            generated_trajectories = pickle.load(f)

    return generated_trajectories


def _write_trajectories(trajectories):
    """
    Write trajectories dictionary to a file.
    :param trajectories: The trajectory dict to write.
    """
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(trajectories, f)


def _generate_trajectories():
    """
    Generate trajectory from waypoints.
    """
    generated_trajectories = {}

    for trajectory_name, trajectory in trajectories.items():
        generated_trajectory = pf.generate(
            trajectory,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            dt=0.02,  # 20ms
            max_velocity=MAX_GENERATION_VELOCITY,      # These are in ft/sec and
            max_acceleration=MAX_GENERATION_ACCELERATION,  # set the units for distance to ft.
            max_jerk=MAX_GENERATION_JERK
        )[1]  # The 0th element is just info

        modifier = pf.modifiers.TankModifier(generated_trajectory).modify(WHEELBASE_WIDTH)

        generated_trajectories[trajectory_name] = (
            modifier.getLeftTrajectory(),
            modifier.getRightTrajectory()
        )

    if wpilib.RobotBase.isSimulation():
        from pyfrc.sim import get_user_renderer

        renderer = get_user_renderer()
        if renderer:
            renderer.draw_pathfinder_trajectory(modifier.getLeftTrajectory(), '#0000ff', offset=(-0.9, 0))
            renderer.draw_pathfinder_trajectory(modifier.source, '#00ff00', show_dt=True)
            renderer.draw_pathfinder_trajectory(modifier.getRightTrajectory(), '#0000ff', offset=(0.9, 0))

    return generated_trajectories
