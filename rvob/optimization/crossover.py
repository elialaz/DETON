from rvob.optimization.ga_structures import population


def reproduction(gen1: int, gen2: int, old, new, count):
    heat1 = old.individuals[gen1].heat
    heat2 = old.individuals[gen2].heat
    scrambling1 = old.individuals[gen1].scrambling
    scrambling2 = old.individuals[gen2].scrambling
    garbage1 = old.individuals[gen1].garbage
    garbage2 = old.individuals[gen2].garbage
    garbage_block1 = old.individuals[gen1].garbage_block
    garbage_block2 = old.individuals[gen2].garbage_block
    obfuscate1 = old.individuals[gen1].obfuscate
    obfuscate2 = old.individuals[gen2].obfuscate

    # set the first child
    new.individuals[count].set_heat(heat1)
    new.individuals[count].set_garbage(garbage1, garbage_block1)
    new.individuals[count].set_obfuscate(obfuscate2)
    new.individuals[count].set_scrambling(scrambling1)

    # set the second child
    count = count + 1
    new.individuals[count].set_heat(heat1)
    new.individuals[count].set_garbage(garbage1, garbage_block1)
    new.individuals[count].set_obfuscate(obfuscate1)
    new.individuals[count].set_scrambling(scrambling2)

    # set the third child
    count = count + 1
    new.individuals[count].set_heat(heat2)
    new.individuals[count].set_garbage(garbage2, garbage_block2)
    new.individuals[count].set_obfuscate(obfuscate1)
    new.individuals[count].set_scrambling(scrambling2)

    # set the four child
    count = count + 1
    new.individuals[count].set_heat(heat2)
    new.individuals[count].set_garbage(garbage2, garbage_block2)
    new.individuals[count].set_obfuscate(obfuscate2)
    new.individuals[count].set_scrambling(scrambling1)

    return count


def crossover(p: population, classifica, n_individuals: int):
    first_reproduction_cromosome = int((n_individuals / 100) * 10)
    second_reproduction_cromosome = int((n_individuals / 100) * 20) + 1
    third_reproduction_cromosome = int(n_individuals - first_reproduction_cromosome) - 1
    old_population = p
    new_population = population(n_individuals)

    # starting the crossover procedure
    count = 0
    for i in range(n_individuals):
        if (i < first_reproduction_cromosome) and (count < n_individuals):
            new_population.individuals[count].set_scrambling(old_population.individuals[classifica[i][1]].scrambling)
            new_population.individuals[count].set_garbage(old_population.individuals[classifica[i][1]].garbage,
                                                          old_population.individuals[classifica[i][1]].garbage_block)
            new_population.individuals[count].set_heat(old_population.individuals[classifica[i][1]].heat)
            new_population.individuals[count].set_obfuscate(old_population.individuals[classifica[i][1]].obfuscate)
            count = count + 1
        if (i < second_reproduction_cromosome) and (count < n_individuals - 4):
            gen1 = classifica[i][1]
            gen2 = classifica[i+1][1]
            count = reproduction(gen1, gen2, old_population, new_population, count)
            count = count + 1
        if i > third_reproduction_cromosome:
            new_population.individuals[count].set_scrambling(old_population.individuals[classifica[i][1]].scrambling)
            new_population.individuals[count].set_garbage(old_population.individuals[classifica[i][1]].garbage,
                                                          old_population.individuals[classifica[i][1]].garbage_block)
            new_population.individuals[count].set_heat(old_population.individuals[classifica[i][1]].heat)
            new_population.individuals[count].set_obfuscate(old_population.individuals[classifica[i][1]].obfuscate)
            count = count + 1

    return new_population
