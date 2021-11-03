

class cromosome:
    def __init__(self, id):
        self.id = id
        self.garbage = None
        self.garbage_block = None
        self.obfuscate = None
        self.scrambling = None
        self.heat = None
        self.punt_over = None
        self.punt_heat = None
        self.punt_tot = None

    def set_garbage(self, garbage, garbage_block):
        self.garbage = garbage
        self.garbage_block = garbage_block

    def set_obfuscate(self, obfuscate):
        self.obfuscate = obfuscate

    def set_scrambling(self, scrambling):
        self.scrambling = scrambling

    def set_heat(self, heat: int):
        self.heat = heat

    def set_punt_over(self, punt):
        if self.punt_over is None:
            self.punt_over = punt
            if self.punt_tot is None:
                self.punt_tot = punt
            else:
                self.punt_tot += punt
        else:
            self.punt_tot -= self.punt_over
            self.punt_over = punt
            self.punt_tot += self.punt_over

    def set_punt_heat(self, punt):
        if self.punt_heat is None:
            self.punt_heat = punt
            if self.punt_tot is None:
                self.punt_tot = punt
            else:
                self.punt_tot += punt
        else:
            self.punt_tot -= self.punt_heat
            self.punt_heat = punt
            self.punt_tot += self.punt_heat


class population:
    def __init__(self, n):
        self.individuals = []
        for i in range(n):
            self.individuals.append(cromosome(i))

    def classifica(self):
        classifica = []
        for i in self.individuals:
            classifica.append([int(i.punt_tot), int(i.id)])
        ordered = sorted(classifica, key=lambda x: x[0], reverse=True)
        return ordered