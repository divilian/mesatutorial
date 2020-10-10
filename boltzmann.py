
from mesa import Agent, Model
from mesa.time import RandomActivation

class MoneyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        print("Running agent {}! (currently ${})".format(self.unique_id,
            self.wealth))
        

class MoneyModel(Model):
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

m = MoneyModel(10)
m.step()
