#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import logging
import time
import subprocess


logging.basicConfig(level=logging.INFO)

def extract_agent_wealth(model):
    return pd.Series([ a.wealth for a in model.schedule.agents ])
    

class MoneyAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        logging.info("Running agent {}! (currently ${})".format(
            self.unique_id, self.wealth))
        if self.wealth == 0:
            return
        other = self.random.choice(self.model.schedule.agents)
        if self == other:
            logging.info("Trading with myself!")
        other.wealth += 1
        self.wealth -= 1
        

class MoneyModel(Model):

    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.num_steps = 0
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
        self.datacollector = DataCollector(
            agent_reporters={"agent_wealth": "wealth"})

    def step(self):
        self.num_steps += 1
        logging.info("Iteration {}...".format(self.num_steps))
        self.datacollector.collect(self)
        self.schedule.step()

    def run(self, num_steps=50):
        for _ in range(num_steps):
            self.step()

m = MoneyModel(200)
m.run(100)

wealths = m.datacollector.get_agent_vars_dataframe()
max_wealth_ever = wealths.agent_wealth.max()
max_iter = wealths.index.get_level_values("Step").max()
subprocess.run("rm -f /tmp/wealth0??.png /tmp/animation.gif".split(" "))
for step in wealths.index.get_level_values("Step").unique():
    wealths.xs(step, level="Step").plot(kind="hist", density=True,
        bins=range(0,max_wealth_ever+1))
    plt.title("Iteration {} of {}".format(step+1, max_iter+1))
    plt.savefig("/tmp/wealth{:03d}.png".format(step))
    plt.close()
subprocess.run("convert -delay 25 -loop 1 /tmp/wealth0??.png /tmp/animation.gif".split(" "))

