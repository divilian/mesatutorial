#!/usr/bin/env python3

from mesa import Agent, Model
from mesa.time import RandomActivation
import logging

logging.basicConfig(level=logging.INFO)

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

    def step(self):
        self.num_steps += 1
        logging.info("Iteration {}...".format(self.num_steps))
        self.schedule.step()

    def run(self, num_steps=50):
        for _ in range(num_steps):
            self.step()

m = MoneyModel(10)
m.run()
