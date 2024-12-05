from mesa import Agent
import random

class Rock(Agent):
    def __init__(self, pos, model, has_power_item=False, has_exit=False):
        super().__init__(pos, model)
        self.pos = pos
        self.has_exit = has_exit
        self.has_power_item = has_power_item
        
    def step(self):
        pass
