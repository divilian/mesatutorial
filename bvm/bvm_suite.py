
# Things I don't know how to get Mesa to do out of the box:
# - a "double slider" (or whatever it's called) in UserSettableParameter
# - show a meaningful progress bar as the suite executes (i.e., update the text
# in SocialWorldSuite.msg while the BatchRunner is executing).

import numpy as np
import pandas as pd
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from mesa.visualization.modules import NetworkModule, TextElement
from StaticChartVisualization import StaticChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
import logging

from bvm import VoterAgent, SocialWorld, Opinion, iters_to_converge

class SocialWorldSuite(Model):

    def __init__(self, N1, N2, Nstep, p, suite_size):

        logging.info("Initializing SocialWorldSuite({},{},{})...".format(
            N1,N2,p))
        
        self.p = p
        self.N1 = N1
        self.N2 = N2
        self.Nstep = Nstep
        self.msg = "Ready"
        self.suite_size = suite_size
        self.running = True
        self.df = pd.DataFrame({"N":[],"itersToConverge":[]})
        self.msg_printed = False


    def step(self):

        param_vals = np.arange(self.N1, self.N2+self.Nstep, self.Nstep)
        self.running = True
        if not self.msg_printed:
            self.msg=("Running {} sims for each of {} param values " +
                "({} total)...").format(self.suite_size, 
                len(param_vals), self.suite_size * len(param_vals))
            self.msg_printed = True
            return

        fixed = {"p":self.p}
        variable = {"N": param_vals}

        batch_run = BatchRunner(SocialWorld, variable, fixed,
            iterations=self.suite_size, max_steps=1000,
            model_reporters={
                "itersToConverge": iters_to_converge})
        batch_run.run_all()
        self.running = False
        self.msg="Done."
        self.df = batch_run.get_model_vars_dataframe()


    def run(self, num_steps=50):
        for _ in range(num_steps):
            self.step()


class StatusMessage(TextElement):
    def render(self, model):
        return model.msg


if __name__ == "__main__":

    N1 = UserSettableParameter("slider","Number of agents (low)",10,10,100,10)
    N2 = UserSettableParameter("slider","Number of agents (high)",100,10,200,10)
    Nstep = UserSettableParameter("slider","Number of agents (step)",10,1,20,1)

    p = UserSettableParameter("slider","ER edge probability (p)",.2,0.05,1,.05)

    msg = StatusMessage()

    suite_size = UserSettableParameter("slider","Suite size",20,5,100,1)

    time_to_converge = StaticChartModule(name="Average iterations to converge")

    server = ModularServer(SocialWorldSuite, [time_to_converge, msg],
        "BVM", { "N1":N1, "N2":N2, "Nstep":Nstep, "p":p,
         "suite_size":suite_size })
    server.port = 8081
    server.launch()
