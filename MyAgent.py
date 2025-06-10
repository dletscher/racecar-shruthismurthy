# What I am trying to achieve here is for the race car to stay in the middle of the track. It should not drift closer to the walls. 
# It works by assigning a reward for each possible action.
# I tried this approach as the actions are rewarded based on the sensors, and the action with the highest reward is chosen. 
# It ensures safe and center-track driving. It also understands the walls and adjusts the speed.
# It works for all tracks. It is better on bigger tracks and slightly slower on smaller tracks.


import random

class Agent:
    def __init__(self):
        self.safe_distance = 0.2
        self.center_clear_low = 3.5
        self.center_clear_high = 5.0
        self.wall_soft = 0.1
        self.wall_hard = 0.25
        self.min_speed = 0.1
        self.max_speed = 1.35

    def chooseAction(self, observations, possible_actions):
        lidar = observations['lidar']
        velocity = observations['velocity']

        left, mid_left, center, mid_right, right = lidar
        wall = left - right  # more space on left = positive, more space on right = negative

        reward = {action: 0 for action in possible_actions}

        if velocity < self.min_speed:
            reward[('straight', 'accelerate')] += 10

        if self.center_clear_low < center < self.center_clear_high:
            reward[('straight', 'accelerate')] += 8

        if left < self.safe_distance:
            reward[('right', 'coast')] += 10
        if right < self.safe_distance:
            reward[('left', 'coast')] += 10

        if wall > self.wall_hard:
            reward[('left', 'brake')] += 8
        elif wall > self.wall_soft:
            reward[('left', 'accelerate')] += 5
        elif wall < -self.wall_hard:
            reward[('right', 'brake')] += 8
        elif wall < -self.wall_soft:
            reward[('right', 'accelerate')] += 5

        if velocity >= self.max_speed:
            reward[('straight', 'coast')] += 6

        if not any(reward.values()):
            return ('straight', 'coast')

        return max(reward.items(), key=lambda x: x[1])[0]
