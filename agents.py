import mesa

class ForestPatch(mesa.Agent):
    """
    Trecho de floresta, com duas espécies (sp1 e sp2), que são distribuídas de forma aleatória.
    Sp1: Tardia, com crescimento populacional em condição de dossel fechado e reduçãoo em clareira.
    Sp2: Pioneira, com crescimento populacional em condição de dossel aberto e redução em de sub-bosque.
    Mundaças populacionais em função da dinâmica de clareira e disturbios cíclicos de grande proporcoes
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Create a new forest patch.
        Args:
            fully_grown: (boolean) Whether the patch of forest is closed or not
            countdown: Time for the gap to be fully closed again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos
       
        
        self.sp1 = self.random.randrange(10) # Tamanho inicial da populacao sp1
        self.sp2 = self.random.randrange(10) # Tamanho inicial da populacao sp2

        self.cyclone = True # Disturbio ciclico
        self.cyclone_countdown = 0


    def step(self):
        
        if not self.fully_grown:
            if self.countdown <= 0:
                self.fully_grown = True
                self.countdown = self.model.forest_regrowth_time
            else:
                self.countdown -= 1

        
         ### Formacao de clareiras

        
        if self.fully_grown:
            if self.random.random() < (self.model.gap_chance/1000): # probabilidade de clareira
                self.fully_grown = False
                self.countdown = self.model.forest_regrowth_time
                self.sp1 = self.random.randrange(10) # Se formou clareira, tamanho inicial da populacao sp1
                self.sp2 = self.random.randrange(10) # Se formou clareira, tamanho inicial da populacao sp2

        # Dinamica de comunidade

        if self.fully_grown:      
            if self.sp1 < 11:
                self.sp1 += 1 # Se dossel fechado, aumenta a populacao sp1
            if self.sp2 >= 1:
                self.sp2 -= 1 # Se dossel fechado, diminui a populacao sp2

        else:
            if self.sp2 < 11:
                self.sp2 += 1 # Se esta clareira esta aberta, aumenta a populacao sp2
            if self.sp1 >= 1:    
                self.sp1 -= 1 # Se esta clareira esta aberta, diminui a populacao sp1

        


        # Distúrbio cíclico

        if self.cyclone == True:
            self.cyclone_countdown +=1
            if self.cyclone_countdown == self.model.cyclone_frequency:
                self.cyclone_countdown = 0
                if self.random.random() < 0.3: # probabilidade de clareira
                    self.fully_grown = False


