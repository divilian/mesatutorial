
import numpy as np
from mesa.visualization.modules import NetworkModule
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

from bvm import VoterAgent, SocialWorld, Opinion

def network_portrayal(G):

    def node_color(agent):
        return "red" if agent.opinion == Opinion.RED else "blue"

    portrayal = {}
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": node_color(agent),
            "tooltip": "id: {}<br>state: {}".format(
                agent.unique_id, str(agent.opinion)
            ),
        }
        for (_, agent) in G.nodes.data("agent")
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": "black",
            "width": 2
        }
        for (source, target) in G.edges
    ]

    return portrayal



if __name__ == "__main__":

    N = UserSettableParameter("slider","Number of agents (N)",20,1,100,1)

    p = UserSettableParameter("slider","ER edge probability (p)",.2,0.05,1,.05)

    net = NetworkModule(network_portrayal, 300, 400, library="d3")

    frac_red = ChartModule([{"Label":"FracRed",
        "Color":"Red"}], data_collector_name="datacollector")

    server = ModularServer(SocialWorld, [net, frac_red],
        "BVM",
        { "N":N, "p":p })
        
    server.port = 8081
    server.launch()
