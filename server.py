import mesa

from agents import ForestPatch
from model import ForestModel


def forest_portrayal(agent):
    if agent is None:
        return

    portrayal = {}


    if type(agent) is ForestPatch:
        if agent.fully_grown:
            portrayal["Color"] = 'darkgreen'
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(forest_portrayal, 10, 10, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Sp1", "Color": "#666666"},
         {"Label": "Sp2", "Color": 'blue'},
            ]
)

model_params = {
     "title": mesa.visualization.StaticText("Parametros:"),
     "forest_regrowth_time": mesa.visualization.Slider("Tempo fechamento da clareira (anos)", 20, 1, 50),
     "gap_chance": mesa.visualization.Slider("Probabilidade de formação de clareira", 1, 1, 10),
     "cyclone_frequency": mesa.visualization.Slider("Frequencia de impacto cíclico", 30, 1, 100),
   
}

server = mesa.visualization.ModularServer(
    ForestModel, [canvas_element, chart_element], "Simulação Dinâmica Florestal v1", model_params
)
server.port = 8521