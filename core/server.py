from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Choice
from agents.balloon import Balloon
from agents.bomb import Bomb
from agents.fire import Fire
from core.model import BombermanModel, NumberMarker
from agents.bomberman import Bomberman
from agents.rock import Rock
from agents.metal import Metal
from agents.joker import Joker

def bomberman_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}

    if isinstance(agent, NumberMarker):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "green"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["text"] = str(agent.number)
        portrayal["text_color"] = "black"
        return portrayal 

    if hasattr(agent, 'model') and agent.pos in agent.model.visited_numbers:
        portrayal["text"] = str(agent.model.visited_numbers[agent.pos])
        portrayal["text_color"] = "red"
    
    if isinstance(agent, Bomberman):
        portrayal["Shape"] = "assets/bomberman.png"

    elif isinstance(agent, Rock):
        portrayal["Shape"] = "assets/block.png"
    
    elif isinstance(agent, Metal):
        portrayal["Shape"] = "assets/metal.png"

    elif isinstance(agent, Balloon):
        portrayal["Shape"] = "assets/globe.png"

    elif isinstance(agent, Bomb):
        portrayal["Shape"] = "assets/bomb.png"

    elif isinstance(agent, Fire):
        portrayal["Shape"] = "assets/fire.png"
    
    elif isinstance(agent, Joker):
        portrayal["Shape"] = "assets/powerup.png"
    
    return portrayal

map_file = "data/mapaRam.txt"
model = BombermanModel(map_file, "BFS", "Manhattan")
grid = CanvasGrid(bomberman_portrayal, model.grid_width, model.grid_height, model.grid_width * 70, model.grid_height * 70)
algorithm_choice = Choice("Algoritmo de búsqueda", value="BFS", choices=["BFS", "DFS", "UCS", "BS", "HC", "A*", "AlphaBeta"])
heuristic_choice = Choice("Heurística", value="Manhattan", choices=["Manhattan", "Euclidiana"])
#cambiar el rango por 0
jokers_choice = Choice("Número de comodines", value=3, choices=list(range(1, 11)))
difficulty_choice = Choice("Dificultad", value=1, choices=[0,3,6])
server = ModularServer(BombermanModel, [grid], "Bomberman", {"map_file": map_file, "algorithm": algorithm_choice, 
                                                                   "heuristic": heuristic_choice, "jokers": jokers_choice, "alpha_beta_depth": difficulty_choice})
server.port = 8521
server.launch()
