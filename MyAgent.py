import random

class Agent:
    def __init__(self):
        self.SAFE_DISTANCE = 1.0
        self.TARGET_SPEED = 0.7
        self.TURN_THRESHOLD = 0.3
        
    def chooseAction(self, observations, possibleActions):

        lidar = observations['lidar']
        velocity = observations['velocity']
        observations['lidar'] = [float(f'{x:.2}') for x in lidar]

        left45 = lidar[0]
        left10 = lidar[1]
        center = lidar[2]
        right10 = lidar[3]
        right45 = lidar[4]
        
        direction = 'straight'
        if left45 < self.SAFE_DISTANCE or left10 < self.SAFE_DISTANCE:
            direction = 'right'
        elif right10 < self.SAFE_DISTANCE or right45 < self.SAFE_DISTANCE:
            direction = 'left'
        elif center < self.SAFE_DISTANCE * 1.5:
            if left45 + left10 > right10 + right45:
                direction = 'left'
            else:
                direction = 'right'
        
        speed = 'accelerate'
        if velocity == 0:
            speed = 'accelerate'
        elif velocity > self.TARGET_SPEED:
            speed = 'brake'
        elif min(lidar) < self.SAFE_DISTANCE * 1.2:
            speed = 'brake'
        elif min(lidar) < self.SAFE_DISTANCE * 1.5:
            speed = 'coast'
            
        return (direction, speed)
