"""

Simulação de dinâmica de clareiras em uma floresta.

"""

import mesa

from scheduler import RandomActivationByTypeFiltered
from agents import ForestPatch


def compute_sp1(model):
    agent_sp1 = [agent.sp1 for agent in model.schedule.agents]
    x = sorted(agent_sp1)
    y = sum(x)
    return int(y)

def compute_sp2(model):
    agent_sp2 = [agent.sp2 for agent in model.schedule.agents]
    x = sorted(agent_sp2)
    y = sum(x)
    return int(y)




class ForestModel(mesa.Model):
    """
    Forest gap dynamics
    """
    
    description = (
        "Modelo de simulação dinamica florestal. Versão 1.0.0. (Desenvolvido por Pedro Higuchi. Contato: higuchip@gmail.com)" 
    )

    def __init__(
        self,
        width=10,
        height=10,
        forest_regrowth_time=20,
        gap_chance=5,
        cyclone_frequency = 30
            ):
        """
        Create a new forest model with the given parameters.
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.forest_regrowth_time = forest_regrowth_time
        self.gap_chance = gap_chance
        self.cyclone_frequency = cyclone_frequency

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Sp1": compute_sp1,
                "Sp2": compute_sp2,
                "forest": lambda m: m.schedule.get_type_count(
                    ForestPatch, lambda x: x.fully_grown
                ),
            },
            
        )

        # Create Forest
        for agent, x, y in self.grid.coord_iter():

                fully_grown = True

                if fully_grown:
                    countdown = self.forest_regrowth_time
                else:
                    countdown = self.random.randrange(self.forest_regrowth_time)

                patch = ForestPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)



        self.running = True
        self.datacollector.collect(self)
        


    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)


        

    def run_model(self, step_count=200):

       
        for i in range(step_count):
            self.step()

       