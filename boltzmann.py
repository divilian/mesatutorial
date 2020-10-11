#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import logging
import time
import subprocess
import sys


logging.basicConfig(level=logging.WARNING)

def compute_gini(model):
    w = sorted([a.wealth for a in model.schedule.agents])
    N = model.num_agents
    B = sum(wi * (N-i) for i,wi in enumerate(w)) / (N*sum(w))
    return (1 + (1/N) - 2*B)


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
        self.running = True   # could set this to stop prematurely

    def step(self):
        self.num_steps += 1
        logging.info("Iteration {}...".format(self.num_steps))
        self.datacollector.collect(self)
        self.schedule.step()

    def run(self, num_steps=50):
        for _ in range(num_steps):
            self.step()


if len(sys.argv) <= 1:
    print("Usage: boltzmann.py single|batch.")
    sys.exit(1)

if sys.argv[1] == "single":

    # Single simulation run.
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
    subprocess.run("convert -delay 15 -loop 1 /tmp/wealth0??.png /tmp/animation.gif".split(" "))
    print("Output in /tmp/animation.gif.")

else:

    # Batch simulation run.
    fixed_params = {} 
    variable_params = {"N": range(5,100) }

    batch_run = BatchRunner(MoneyModel,
        variable_params,
        fixed_params,
        iterations=10,
        max_steps=50,
        model_reporters={"Gini": compute_gini})

    batch_run.run_all()

    run_data = batch_run.get_model_vars_dataframe()
    run_data.head()
    plt.scatter(run_data.N, run_data.Gini)
    plt.ylim((0,1))
    plt.xlabel("Number of agents")
    plt.ylabel("Gini coefficient")
    plt.savefig("/tmp/Gini_scatter.png")
    plt.close()
    print("Output in /tmp/Gini_scatter.png.")
