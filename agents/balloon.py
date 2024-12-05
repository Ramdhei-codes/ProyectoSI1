from mesa import Agent
from agents.bomberman import Bomberman
from agents.numberMarker import NumberMarker
import random

class Balloon(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos

    def move(self):
        if self.pos is None:
            return  

        # Si el algoritmo seleccionado es Alfa-Beta, calcula el mejor movimiento
        if self.model.algorithm == "AlphaBeta" and self.model.alpha_beta_depth > 0:
            print(f"ALFA BETA {self.model.alpha_beta_depth}")
            bomberman = next(agent for agent in self.model.schedule.agents if isinstance(agent, Bomberman))
            best_move = self.model.run_search_algorithm(self.pos, bomberman.pos, is_balloon=True)
            
            if best_move:
                self.model.grid.move_agent(self, best_move)
                self.check_collision(best_move)
            return

        # Movimiento aleatorio si no es Alfa-Beta
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        valid_steps = [pos for pos in possible_steps if self.is_valid_step(pos)]    

        if valid_steps:
            new_position = random.choice(valid_steps)
            self.model.grid.move_agent(self, new_position)
            self.check_collision(new_position)

    def is_valid_step(self, pos):
        """Determina si un paso es válido para el globo."""
        cell_contents = self.model.grid.get_cell_list_contents(pos)
        return all(isinstance(obj, NumberMarker) or self.model.grid.is_cell_empty(pos) or isinstance(obj, Bomberman) for obj in cell_contents)

    def check_collision(self, new_position):
        """Verifica colisiones entre el globo y Bomberman."""
        bomberman = next(agent for agent in self.model.schedule.agents if isinstance(agent, Bomberman))

        # Verificar intercambio de posiciones con Bomberman (colisión alternada)
        if (self.model.previous_positions.get(bomberman) == new_position and
            self.model.previous_positions.get(self) == bomberman.pos):
            print("Colisión alternada entre globo y Bomberman.")
            self.model.reset_game()
            return

        # Verificar colisión directa
        if self.pos == bomberman.pos or bomberman.pos == new_position:
            print("Colisión directa entre globo y Bomberman.")
            self.model.reset_game()

    def step(self):
        """Actualiza la posición previa y realiza el movimiento."""
        self.model.update_previous_position(self, self.pos)
        self.move()
