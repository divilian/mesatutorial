
import matplotlib.pyplot as plt
import numpy as np
from mesa import Agent, Model
from mesa.space import SingleGrid
import importlib
import logging

import boltzmann


class GridMoneyModel(boltzmann.MoneyModel):

    def __init__(self, N, width, height, max_iter):
        logging.debug("GridMoneyModel constructor.")
        super().__init__(N, agent_class=GridMoneyAgent)
        self.grid = SingleGrid(width, height, False)
        self.width = width
        self.height = height
        self.max_iter = max_iter   # (Solely used for plotting captions.)
        
        for a in self.schedule.agents:
            self.grid.place_agent(a, self.grid.find_empty())

    def step(self):
        super().step()
        agent_locs = np.zeros((self.grid.width, self.grid.height))
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if cell_content:
                agent_locs[x][y] = 1
        fig = plt.imshow(agent_locs, interpolation='nearest')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.title("Iteration {} of {}".format(self.num_steps, self.max_iter))
        plt.savefig("/tmp/agent_locs{:03d}.png".format(self.num_steps))
        plt.close()

    def __str__(self):
        return "{}x{} GridMoneyModel with {} agents.".format(self.width,
            self.height,self.num_agents)

    def __repr__(self):
        return "GridMoneyModel({},{},{})".format(self.num_agents, self.width,
            self.height)


class GridMoneyAgent(boltzmann.MoneyAgent):

    def __init__(self, agent_id, model):
        logging.debug("GridMoneyAgent constructor.")
        super().__init__(agent_id, model)

    def step(self):
        self.move()
        super().step()

    def give_money(self):
        # Different from tutorial: since we use a single grid, pass money to a
        # grid neighbor, not a fellow member of our grid cell (of which there
        # will be none).
        others = self.model.grid.get_cell_list_contents(
            self.model.grid.get_neighborhood(self.pos, moore=True,
            include_center=False))
        if len(others) == 0:
            logging.info("No one for agent {} to give to.".format(
                self.unique_id))
            return
        other = self.random.choice(others)
        logging.info("Agent {} gives to {}.".format(self.unique_id, other))
        if self == other:
            logging.critical("ERROR: Trading with myself!")
        other.wealth += 1
        self.wealth -= 1

    def move(self):
        possible_moves = [ c for c in self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)
            if self.model.grid.is_cell_empty(c) ]
            
        if len(possible_moves) == 0:
            logging.info("Nowhere for agent {} to move.".format(
                self.unique_id))
            return
        new_loc = self.random.choice(possible_moves)
        logging.info("Agent {} moving from {} to {}.".format(self.unique_id,
            self.pos, new_loc))
        self.model.grid.move_agent(self, self.random.choice(possible_moves))

    def __str__(self):
        return "GridMoneyAgent {}.".format(self.unique_id)

    def __repr__(self):
        return "GridMoneyAgent({},{})".format(self.unique_id,m.__repr__())

if __name__ == "__main__":
    max_iter = 100
    m = GridMoneyModel(50,12,12,max_iter)
    m.run(max_iter)
