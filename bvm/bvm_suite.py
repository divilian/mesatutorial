
import numpy as np
import pandas as pd
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from mesa.visualization.modules import NetworkModule
from StaticChartVisualization import StaticChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
import logging

from bvm import VoterAgent, SocialWorld, Opinion, iters_to_converge

class SocialWorldSuite(Model):

    def __init__(self, N1, N2, p, suite_size):

        logging.info("Initializing SocialWorldSuite({},{},{})...".format(
            N1,N2,p))
        
        self.p = p
        self.N1 = N1
        self.N2 = N2
        self.suite_size = suite_size
        self.running = True
        self.df = pd.DataFrame({"N":[],"itersToConverge":[]})


    def step(self):

        self.running = True

        fixed = {"p":self.p}
        variable = {"N": np.arange(self.N1,self.N2,10)}

        batch_run = BatchRunner(SocialWorld, variable, fixed,
            iterations=self.suite_size, max_steps=1000,
            model_reporters={
                "itersToConverge": iters_to_converge})
        batch_run.run_all()
        self.running = False
        self.df = batch_run.get_model_vars_dataframe()


    def run(self, num_steps=50):
        for _ in range(num_steps):
            self.step()


if __name__ == "__main__":

    N1 = UserSettableParameter("slider","Number of agents (low)",10,1,100,1)
    N2 = UserSettableParameter("slider","Number of agents (high)",140,1,200,1)

    p = UserSettableParameter("slider","ER edge probability (p)",.2,0.05,1,.05)

    suite_size = UserSettableParameter("slider","Suite size",20,5,100,1)

    time_to_converge = StaticChartModule(name="Average iterations to converge")

    server = ModularServer(SocialWorldSuite, [time_to_converge],
        "BVM", { "N1":N1, "N2":N2, "p":p, "suite_size":suite_size })
    server.port = 8081
    server.launch()
