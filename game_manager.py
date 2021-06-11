import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from env.env import SnakeEnv
from nn.agent import Agent
from nn.model import Model


def play_game():
    env = SnakeEnv()
    user_control = True

    state_shape = env.observation_space.shape
    nb_actions = env.action_space.nb_actions

    model = Model.build_model(state_shape, nb_actions, name='Snake-Model')
    weights_path = 'snake_model_weights.h5'
    weights_loading_try = 0


    while True:
        try:
            model.load_weights(weights_path)
            break

        except Exception:
            weights_loading_try += 1
            
            if weights_loading_try > 1:
                print('Unable to load model weights')
                print('---Quitting---')
                quit(1)


    while True:
        game_started = False
        state = env.reset()
        done = False

        while user_control and not game_started:
            user_actions, switch_mode = env.render(user_control=user_control)

            if switch_mode:
                user_control = not user_control

            if user_actions is not None and len(user_actions) > 0:
                for action in user_actions:
                    new_state, reward, done, info = env.step(action)
                    state = new_state
            
                game_started = True


        while not done:
            user_actions, switch_mode = env.render(user_control=user_control)

            if switch_mode:
                user_control = not user_control

            if user_control:
                if user_actions is not None and len(user_actions) > 0:
                    for action in user_actions:
                        new_state, reward, done, info = env.step(action)
                        state = new_state
                
                else:
                    new_state, reward, done, info = env.step(None)
                    state = new_state
            
            else:
                action = Agent.predict(model, state)
                new_state, reward, done, info = env.step(action)

    