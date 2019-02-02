from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive, trajectory_follower


class Charge(AutonomousStateMachine):
    MODE_NAME = 'Charge'
    DEFAULT = True

    drive = drive.Drive
    lift = lift.Lift
    follower: trajectory_follower.TrajectoryFollower

    @state(first=True)
    def charge(self, initial_call):
        if initial_call:
            self.follower.follow_trajectory('cargo_ship')

        if not self.follower.is_following('cargo_ship'):
            self.next_state('place_hatch')  # If using mutliple states use self.next_state(name)

    @state()
    def move_lift(self):
        self.
