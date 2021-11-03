from deton import execute
import argparse
from optimization.setup_popolation import setup_population
from os import path
from optimization.fitness import fitness
from optimization.crossover import crossover


def get_args():
    parser = argparse.ArgumentParser(description="GENETIC OPTIMIZATION OF DETON")

    parser.add_argument(
        "Overhead",
        metavar="max overhead value",
        help="The maximum Overhead value wanted in % compared to the original file",
        default='50',
        type=int)

    parser.add_argument(
        "File",
        metavar="File path input",
        help="The path of the file in .json format to process",
        nargs='?',
        default='q',
        type=str)

    parser.add_argument(
        '-e', '-entry',
        metavar="File entry point",
        help="Entry point of the program to process",
        nargs='?',
        default='',
        const='',
        type=str)

    return parser.parse_args()


def run_gen(p, n_individuals, file: str, entry: str, overhead: int):
    rel = path.dirname(__file__)
    str1 = rel + '/metrics/data.txt'
    str2 = rel + '/metrics/data_metrics.txt'

    # execution of deton and fitness on every cromosome
    for i in range(n_individuals):
        execute(file, entry, p.individuals[i].heat, p.individuals[i].scrambling, p.individuals[i].obfuscate,
                p.individuals[i].garbage, p.individuals[i].garbage_block,
                (path.dirname(__file__) + '/metrics/output.s'), False, True)
        # execute the fitness on the cromosome
        fitness(p, i, str1, str2, overhead)


def ga(overhead: int, file: str, entry: str):
    n_individuals = 10
    generation = 200

    # setup the population
    population = setup_population(n_individuals)

    # running the generation and the fitness function
    i = True
    count = 0
    first = True
    useless_gen = 0
    while i and count <= generation:
        print("Starting generation " + str(count + 1) + " of maximum " + str(generation))
        run_gen(population, n_individuals, file, entry, overhead)
        classifica = population.classifica()

        # verify the improvements of this generation
        if first is True:
            first = False

            # saving the best cromosome data
            best_cromosome = population.individuals[classifica[0][1]]
        else:
            if population.individuals[classifica[0][1]].punt_tot < best_cromosome.punt_tot:
                useless_gen = useless_gen + 1
            else:
                improvements = ((population.individuals[classifica[0][1]].punt_tot - best_cromosome.punt_tot) / 400)
                best_cromosome = population.individuals[classifica[0][1]]
                if improvements <= 2:
                    useless_gen = useless_gen + 1

        # apply the crossover
        population = crossover(population, classifica, n_individuals)

        # apply the mutation on the new generation

        if (useless_gen == 50) or (best_cromosome.punt_tot > 19900):
            i = False
        count = count + 1

    return best_cromosome


def main():
    args = get_args()

    input_file = args.File
    entry = args.e
    overhead = args.Overhead

    # launch the genetic algorithm
    output = ga(overhead, input_file, entry)

    # print the best param obtained
    output.print_param()


if __name__ == "__main__":
    main()
