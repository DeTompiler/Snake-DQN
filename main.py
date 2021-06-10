from env.env import SnakeEnv
import time
import numpy as np

env = SnakeEnv()

# state = env.reset()
for i in range(1):
    done = False
    state = env.reset()
    while not done:
        actions = env.render(user_control=True)
        # new_state, reward, done, info = env.step(env.action_space.sample())
        if actions is not None and len(actions) > 0:
            for action in actions:
                new_state, reward, done, info = env.step(action)
                state = new_state
                print(reward, done, info, end='\r')
            
        else:
            new_state, reward, done, info = env.step(None)
            state = new_state
            print(reward, done, info, end='\r')


env.close()