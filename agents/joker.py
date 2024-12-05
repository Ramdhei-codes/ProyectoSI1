from mesa import Agent
class Joker(Agent):
    def __init__(self, pos, model, value):
        super().__init__(pos, model)
        self.pos = pos
        self.value = value
        
    def step(self):
        pass