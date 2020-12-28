
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from gridboltzmann import GridMoneyModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": agent.wealth/5 }
    return portrayal


if __name__ == "__main__":
    N = 30
    width = 12
    height = 12

    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

    server = ModularServer(GridMoneyModel, [grid], "Grid Boltzmann",
        { "N":N, "width":width, "height":height, "max_iter":100 })
    server.port = 8521
    server.launch()
