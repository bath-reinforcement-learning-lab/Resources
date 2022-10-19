# -*- coding: utf-8 -*-

"""
This will be the environment file which will have an open-ai gym style 
discrete version of metaworld. 
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Normal
import random
from matplotlib import pyplot as plt
from metaworld.envs import (ALL_V2_ENVIRONMENTS_GOAL_OBSERVABLE,
                                ALL_V2_ENVIRONMENTS_GOAL_HIDDEN)
import gym
import gym.spaces as spaces
import stable_baselines3
import os
import pickle

from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.results_plotter import plot_results
from stable_baselines3.common.noise import NormalActionNoise
from stable_baselines3.common.callbacks import BaseCallback

class record_decisions(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq:
    :param log_dir: Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: Verbosity level.
    """
    def __init__(self, check_freq: int, log_dir: str, verbose: int = 1):
        super(record_decisions, self).__init__(verbose)
        self.log_dir = log_dir

    def _on_step(self) -> bool:
        if disc_env.done == True:
            self.logger.record("decisions_made", disc_env.decisions_made)
            return True
        else:
            return False

class discreteMetaWorld:
    metadata = {'render.modes': ['human']} # this is required but does nought
    
    def __init__(self, cont_env):
        """ This will only make a discrete environment for each task 
        so if you need to run ML10 for example this needs to be 
        inside the loop and each task env should be fed here 
        """
        super(discreteMetaWorld, self).__init__()
        # 11 discrete to get a nice 0.2 step
        self.action_space = spaces.MultiDiscrete([11, 11, 11, 11]) 
        self.observation_space = spaces.Box(np.array(
            [-0.525, 0.348, -0.0525, -1.,
            -np.inf, -np.inf, -np.inf, 
            -np.inf, -np.inf, -np.inf,
            -np.inf, -np.inf, -np.inf,
            -np.inf, -np.inf, -np.inf,
            -np.inf, -np.inf, -0.525,
            0.348, -0.0525, -1., -np.inf,
            -np.inf, -np.inf, -np.inf,
            -np.inf, -np.inf, -np.inf,
            -np.inf, -np.inf, -np.inf,
            -np.inf, -np.inf, -np.inf,
            -np.inf, 0., 0., 0.]),
            np.array(
            [0.525, 1.025, 0.7, 1.,
            np.inf, np.inf, np.inf, 
            np.inf, np.inf, np.inf,
            np.inf, np.inf, np.inf,
            np.inf, np.inf, np.inf,
            np.inf, np.inf, 0.525,
            1.025, 0.7, 1., np.inf,
            np.inf, np.inf, np.inf,
            np.inf, np.inf, np.inf,
            np.inf, np.inf, np.inf,
            np.inf, np.inf, np.inf,
            np.inf, 0., 0., 0.], np.float32))
        self.cont_env = cont_env
        self.obs = self.reset()
        self.decisions_list = []
        self.decisions_made = 0
        self.rewards_list = []
        self.rewards = 0
        self.length_list = []
        self.steps = 0
    
    def step(self, actions):
        cont_actions = self.disc_to_cont(actions)
        self.decisions_made += 1
        self.steps += 1 # for now this is the same as decisions - work needed for options 
        self.obs, self.reward, self.done, self.info = self.cont_env.step(cont_actions)
        self.rewards += self.reward
        
        if self.steps == 499: # this stops us hitting the maximum steps
            print(" hit max steps ")
            self.done = True
        
        elif self.done == True:
            print("done before max steps!")
        
        if self.done == True:
            self.decisions_list.append(self.decisions_made)
            self.rewards_list.append(self.rewards)
            self.length_list.append(self.steps)
            self.reset()
    
        return self.obs, self.reward, self.done, self.info
    
    def reset(self):
        self.decisions_made = 0
        self.rewards = 0
        self.steps = 0
        return self.cont_env.reset()
    
    def render(self):
        self.cont_env.render()
    
    def close(self):
        pass
    
    def disc_to_cont(self, actions):
        """Turns the actions from the discrete agent to cont for original MW"""
        cyther_dict = {0:-1.0, 1:-0.8, 2:-0.6, 3:-0.4, 4:-0.2, 5:0.0, 6:0.2,
                       7:0.4, 8:0.6, 9:0.8, 10:1.0}
        
        a1 = cyther_dict[actions[0]]
        a2 = cyther_dict[actions[1]]
        a3 = cyther_dict[actions[2]]
        a4 = cyther_dict[actions[3]]
        
        new_actions = np.array([a1, a2, a3, a4])
        
        return new_actions
        
        
        
if __name__ == "__main__":
    
    coffee_button_goal_observable_cls = ALL_V2_ENVIRONMENTS_GOAL_OBSERVABLE["drawer-close-v2-goal-observable"]
    cont_env = coffee_button_goal_observable_cls(seed=5)
    
    log_dir = "./PPO_ABC_prim"
    os.makedirs(log_dir, exist_ok = True)
    
    tag = "draw_close"
    recording_folder = "./test_records"
    
    try:
        os.makedirs(recording_folder)
    except:
        pass # hacky
    
    runs = 5
    for run in range(runs):
        print("starting run ", run)
        disc_env = discreteMetaWorld(cont_env)
        model = stable_baselines3.PPO('MlpPolicy', disc_env, tensorboard_log=log_dir,
                                      device="cuda")
        model.learn(total_timesteps=2000000, callback=record_decisions)
        
        pickle.dump(disc_env.decisions_list, open("{}/{}_{}_decisions".format(recording_folder, 
                                                                     tag, run), "wb"))
        
        pickle.dump(disc_env.rewards_list, open("{}/{}_{}_reward".format(recording_folder,
                                                                    tag, run), "wb"))
        
        print(disc_env.rewards_list)
        
        pickle.dump(disc_env.length_list, open("{}/{}_{}_length".format(recording_folder,
                                                               tag, run), "wb"))