from deton import execute
import argparse
from optimization.setup_popolation import setup_population
from os import path
from optimization.fitness import fitness


def get_args():
    parser = argparse.ArgumentParser(description="OPTIMIZATOR DETON")

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

def calc_fitness(p, id: int, overhead: int):
    rel = path.dirname(__file__)
    str1 = rel + '/metrics/data.txt'
    str2 = rel + '/metrics/data_metrics.txt'

    # execute the fitness on the cromosome
    fitness(p, id, str1, str2, overhead)

def run_gen(p, n_individuals, file: str, entry: str, overhead: int):

    # execution of deton and fitness on every cromosome
    for i in range(n_individuals):
        execute(file, entry, p.individuals[i].heat, p.individuals[i].scrambling, p.individuals[i].obfuscate, p.individuals[i].garbage, p.individuals[i].garbage_block, (path.dirname(__file__)+'/metrics/output.s'), False, True)
        calc_fitness(p, i, overhead)

    classifica = p.classifica()
    print(classifica)


def ga(overhead: int, file: str, entry: str):

    n_individuals = 100

    # setup the population
    population = setup_population(n_individuals)

    # running the generation and the fitness function
    i = True
    count = 0
    while (i and count <= 1000):
        run_gen(population, n_individuals, file, entry, overhead)




def main():
    args = get_args()

    input_file = args.File
    entry = args.e
    overhead = args.Overhead

    output = ga(overhead, input_file, entry)

    print(output)


if __name__ == "__main__":
    main()
