from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.bomberman import Bomberman
from agents.numberMarker import NumberMarker
from agents.rock import Rock
from agents.metal import Metal
from agents.balloon import Balloon
from utils.search_algorithms import (breadth_first_search, depth_first_search, uniform_cost_search,
                                      beam_search, manhattan_distance, euclidean_distance, 
                                      hill_climbing, a_star_search, alpha_beta_search, bomberman_heuristic,
                                      balloon_heuristic)
import random
class BombermanModel(Model):
    def __init__(self,  map_file, algorithm, heuristic, jokers=3, alpha_beta_depth=0):
        super().__init__()
        self.map_file = map_file
        self.grid_width, self.grid_height = self.get_map_dimensions(map_file)
        self.grid = MultiGrid(self.grid_width, self.grid_height, torus=False)
        self.schedule = RandomActivation(self)
        self.visited_numbers = {}
        self.previous_positions = {}
        self.algorithm = algorithm  
        self.heuristic = heuristic
        self.jokers = jokers  # Añadir esta línea
        self.joker_count = 0  # Contador para controlar los comodines
        self.alpha_beta_depth = alpha_beta_depth  
        self.running = True
        self.exit_position = None 
        self.export_file = "game_states.txt"
        
        # Crear archivo vacío para exportar estados
        with open(self.export_file, "w") as f:
            f.write("Estados de juego en pre-orden:\n")

        self.load_map(map_file)
    
    def record_state(self, position, heuristic_value=None):
        """
        Registra el estado en un archivo de texto en preorden.
        
        Args:
            position (tuple): La posición actual de Bomberman.
            heuristic_value (float, optional): Valor de la heurística (solo para algoritmos informados).
        """
        with open(self.export_file, "a", encoding="utf-8") as f:
            if heuristic_value is not None:
                f.write(f"Posición: {position}, Heurística: {heuristic_value}\n")
            else:
                f.write(f"Posición: {position}\n")

    def get_map_dimensions(self, map_file):
        with open(map_file, "r") as f:
            lines = f.readlines()
            height = len(lines)
            width = len(lines[0].strip().split(','))
        return width, height

    def load_map(self, map_file):
        with open(map_file, "r") as f:
            lines = f.readlines()
            bomberman_position = None 
            valid_positions = []  
            balloon_positions = []
            rock_positions = []

            for y, line in enumerate(reversed(lines)): 
                elements = line.strip().split(',')
                for x, elem in enumerate(elements):
                    if elem == "C_b":  
                        bomberman_position = (x, y)
                    elif elem == "C":
                        valid_positions.append((x, y))
                    elif elem == "C_g":
                        balloon_positions.append((x, y))
                    elif elem == "R":
                        rock_positions.append((x, y))  # Agregar la posición a rock_positions
                    elif elem == "R_s":
                        rock = Rock((x, y), self, has_exit=True)
                        self.exit_position = (x, y)
                        self.grid.place_agent(rock, (x, y))
                        self.schedule.add(rock)
                    elif elem == "M":
                        metal = Metal((x, y), self)
                        self.grid.place_agent(metal, (x, y))
                        
            # Seleccionar posiciones aleatorias para los comodines
            joker_positions = random.sample(rock_positions, min(self.jokers, len(rock_positions)))
          
            # Colocar las rocas, asignando comodines aleatoriamente
            for pos in rock_positions:
                has_power_item = pos in joker_positions
                rock = Rock(pos, self, has_power_item=has_power_item)
                self.grid.place_agent(rock, pos)
                self.schedule.add(rock)

            for balloon_position in balloon_positions:
                balloon = Balloon(balloon_position, self)
                self.grid.place_agent(balloon, balloon_position)
                self.schedule.add(balloon)

            if not balloon_positions:
                self.add_balloons(3)

            if not bomberman_position:
                if valid_positions:
                    bomberman_position = random.choice(valid_positions)
                else:
                    raise ValueError("No hay posiciones válidas en el mapa para colocar a Bomberman.")

            bomberman = Bomberman(bomberman_position, self)
            self.grid.place_agent(bomberman, bomberman_position)
            self.schedule.add(bomberman)


    def place_agent_number(self, pos, number):
        """
            Marca una casilla en el mapa con un número que representa el orden en que fue visitada.

            Args:
                pos (tuple): La posición en la grilla.
                number (int): El número que representa el orden de la visita.
        """
        self.visited_numbers[pos] = number
        self.grid.place_agent(NumberMarker(pos, self, number), pos)

    def step(self):
        self.schedule.step()

    def run_search_algorithm(self, start, goal, is_balloon=False):
        if self.algorithm == "AlphaBeta":
            heuristic_func = balloon_heuristic if is_balloon else bomberman_heuristic
            return alpha_beta_search(
                start, goal, self, depth=5,
                is_maximizing=not is_balloon,
                heuristic=heuristic_func,  # Pasar la heurística seleccionada
                record_state=self.record_state,
                pruned_nodes=0
            )[0]  # Solo devolver la posición óptima

        heuristic_func = manhattan_distance if self.heuristic == "Manhattan" else euclidean_distance

        if self.algorithm == "BFS":
            return breadth_first_search(start, goal, self, record_state=self.record_state)
        elif self.algorithm == "DFS":
            return depth_first_search(start, goal, self, record_state=self.record_state)
        elif self.algorithm == "UCS":
            return uniform_cost_search(start, goal, self, record_state=self.record_state)
        elif self.algorithm == "BS":
            return beam_search(start, goal, self, heuristic=heuristic_func, record_state=self.record_state)
        elif self.algorithm == "HC":
            return hill_climbing(start, goal, self, heuristic=heuristic_func, record_state=self.record_state)
        elif self.algorithm == "A*":
            return a_star_search(start, goal, self, heuristic=heuristic_func, record_state=self.record_state)
        
    def get_heuristic(self, pos1, pos2):
        """
        Calcula la heurística en función de la selección del usuario.
        """
        if self.heuristic == "Manhattan":
            return manhattan_distance(pos1, pos2)
        elif self.heuristic == "Euclidiana":
            return euclidean_distance(pos1, pos2)
        
    def add_balloons(self, count):
          for _ in range(count):
            # Buscar una posición válida aleatoria (C)
            while True:
                x = random.randrange(self.grid_width)
                y = random.randrange(self.grid_height)
                if self.grid.is_cell_empty((x, y)):  # Verificar si es un camino libre
                    balloon = Balloon((x, y), self)
                    self.grid.place_agent(balloon, (x, y))
                    self.schedule.add(balloon)
                    break

    def update_previous_position(self, agent, new_position):
        self.previous_positions[agent] = new_position

    def reset_game(self):      
        self.__init__(self.map_file, self.algorithm, self.heuristic, self.jokers) 

    def finish_game(self):
        """Detiene el juego al finalizar."""
        print("¡Juego detenido! Bomberman ha alcanzado la salida.")
        self.running = False 