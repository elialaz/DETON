import numpy as nu
from rvob.optimization.ga_structures import population


def heat_ideal_determination(n: int):
    param = nu.random.uniform(30, 60, n)
    return param


def garbage_determination(n: int):
    param = nu.random.uniform(1, 200, n)
    return param


def garbage_block_size(n: int):
    param = nu.random.randint(3, 7, size=n)
    return param


def obfuscate_determination(n: int):
    param = nu.random.uniform(1, 200, n)
    return param


def scrambling_determination(n: int):
    param = nu.random.uniform(1, 200, n)
    return param


def setup_population(n_individuals: int):
    """
    Creating the starting population of the genetic algorithm
    @param n_individuals: number of individuals
    """
    new_population = population(n_individuals)
    ideal_heat = heat_ideal_determination(n_individuals)

    # setup heat in the new population
    for i in range(n_individuals):
        new_population.individuals[i].set_heat(int(ideal_heat[i]))

    # setup the garbage insertion value and the garbage block size
    garbage_range = garbage_determination(n_individuals)
    block_size = garbage_block_size(n_individuals)
    for i in range(n_individuals):
        new_population.individuals[i].set_garbage(int(garbage_range[i]), int(block_size[i]))

    # setup the obfuscate value
    obfuscate_range = obfuscate_determination(n_individuals)
    for i in range(n_individuals):
        new_population.individuals[i].set_obfuscate(int(obfuscate_range[i]))

    # setup the scrambling value
    scrambling_range = scrambling_determination(n_individuals)
    for i in range(n_individuals):
        new_population.individuals[i].set_scrambling(int(scrambling_range[i]))

    return new_population
