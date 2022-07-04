import math

def direction_reward(waypoints, closest_waypoints, heading, speed):
    reward = 1
    # DIRECTION_THRESHOLD = 

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]))

    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

     # Penalize the reward if the difference is too large, reward if can turn around fast
    if track_direction > 2: # Turning corner award
        if direction_diff < 15 and speed > 2:
            reward = 1
        elif direction_diff < 15:
            reward = 0.8
        elif direction_diff < 20 and speed > 2:
            reward = 0.6
        elif direction_diff < 20:
            reward = 0.3
        else:
            reward = 1e-3
    else: # Straightline award
        if direction_diff < 15 and speed > 3:
            reward = 1
        if direction_diff < 15 and speed > 2:
            reward = 0.8
        elif direction_diff < 15:
            reward = 0.6
        elif direction_diff < 20 and speed > 2:
            reward = 0.5
        elif direction_diff < 20:
            reward = 0.3
        else:
            reward = 1e-3

    return reward

#def completion_reward(steps, progress):
#    return_reward = progress/100
#    return return_reward

def completion_reward(steps, progress):
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    # Assume 15steps / second, takes 12 seconds to finish each lap
    TOTAL_NUM_STEPS = 15*12

    # Initialize the reward with typical value
    reward = 0

    # Give additional reward if the car pass every 100 steps faster than expected
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0

    return float(reward)

def reward_function(params):
    ALPHA = 2

    MAX_SPEED=4.0
    
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    is_offtrack = params['is_offtrack']
    all_wheels_on_track = params['all_wheels_on_track']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    
    # Strongly discourage going off track
    if is_offtrack:
        reward = 1e-3
        return float(reward)

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward = 1e-3
        return float(reward)

    # Base reward (Nothing)
    reward = 1e-3

    # Reward if near the center, penalize more if deivate from the centre
    reward += (1 - (distance_from_center/(track_width/2))**(1/2))**ALPHA

    # Speed reward
    # reward += 2*speed/MAX_SPEED

    # Reward if the direction is correct
    reward += 3*direction_reward(waypoints, closest_waypoints, heading, speed)**ALPHA

    # Reward if complete more
    reward += completion_reward(steps, progress)**ALPHA

    return float(reward)

