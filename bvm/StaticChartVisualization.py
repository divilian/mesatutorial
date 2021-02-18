
import json
from mesa.visualization.ModularVisualization import VisualizationElement


class StaticChartModule(VisualizationElement):

    package_includes = ["Chart.min.js"]
    local_includes = ["StaticChartModule.js"]

    def __init__(self, height=200, width=500, name="Data"):

        self.canvas_height = height
        self.canvas_width = width

        new_element = "new StaticChartModule({}, {}, '{}')"
        new_element = new_element.format(width, height, name)
        self.js_code = "elements.push(" + new_element + ");"
        print("self.js_code = {}".format(self.js_code))

    def render(self, model):
        return [ model.df.N.unique().tolist(),
            [ float(d) for d in 
                model.df.groupby("N").itersToConverge.mean().tolist()
            ]
        ]
