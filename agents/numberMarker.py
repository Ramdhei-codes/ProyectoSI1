from mesa import Agent
class NumberMarker(Agent):
    def __init__(self, pos, model, number):
        super().__init__(pos, model)
        self.number = number
        self.has_power_item = False  # Inicializa sin ítem de poder, pero puede ser modificado al explotar una roca

    def step(self):
        pass 