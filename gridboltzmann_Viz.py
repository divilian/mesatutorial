
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

from gridboltzmann import GridMoneyModel

def agent_portrayal(agent):
    if agent.wealth > 10:
        color = "red"
    elif agent.wealth > 0:
        color = "green"
    else:
        color = "gray"
    portrayal = {"Shape": "circle",
                 "Color": color,
                 "Filled": "true",
                 "Layer": 0,
                 "r": max(.05,min(1,agent.wealth/5)) }
    return portrayal


if __name__ == "__main__":
    N = 30
    width = 12
    height = 12

    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)
    chart = ChartModule([{"Label":"Gini", "Color":"Green"}],
        data_collector_name="datacollector")
    interest_rate = UserSettableParameter("slider", "Interest Rate (Brandon)",
        0, 0, .1, .01)
    ubi = UserSettableParameter("slider", "UBI $ (Justin)", 0, 0, 10, .1)

    server = ModularServer(GridMoneyModel, [grid,chart],
        "Grid Boltzmann",
        { "N":N, "width":width, "height":height, "max_iter":100,
        "int_rate":interest_rate, "ubi":ubi })
    server.port = 8081
    server.launch()
