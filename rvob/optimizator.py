from deton import execute
import argparse
from optimization.setup_popolation import setup_population
from os import path
from optimization.fitness import fitness
from optimization.crossover import crossover
from optimization.mutation import mutation
import matplotlib.pyplot as plt
from multiprocessing import Process

global bench


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

    parser.add_argument(
        '-b', '-bench',
        help="Run benchmark file",
        nargs='?',
        default=False,
        type=bool)

    parser.add_argument(
        '-s', '-stats',
        help="Print stats and plot",
        nargs='?',
        default=False,
        type=bool)

    parser.add_argument(
        '-i', '-individuals',
        help="Number of individuals in every generation",
        nargs='?',
        default=int(20),
        type=int)

    parser.add_argument(
        '-g', '-generation',
        help="Maximum number of generation executed",
        nargs='?',
        default=int(200),
        type=int)

    return parser.parse_args()


def run_gen(p, n_individuals, file: str, entry: str, overhead: int, lenght_before: int):
    rel = path.dirname(__file__)
    process = []

    # execution of deton in multiprocessing
    for i in range(n_individuals):
        out = rel + '/metrics/output' + str(i) + '.s'

        # noinspection PyTypeChecker
        t = Process(target=execute,
                    args=[file, entry, p.individuals[i].heat, p.individuals[i].scrambling, p.individuals[i].obfuscate,
                          p.individuals[i].garbage, p.individuals[i].garbage_block,
                          out, False, True, str(i)])
        t.start()
        process.append(t)

    # wait all the process end
    for t in process:
        t.join()

    # execution of the fitness function
    for i in range(n_individuals):
        str1 = rel + '/metrics/data' + str(i) + '.txt'
        str2 = rel + '/metrics/data_metrics' + str(i) + '.txt'
        str3 = rel + '/metrics/output' + str(i) + '.s'
        fitness(p, i, str1, str2, str3, overhead, lenght_before)


def ga(overhead: int, file: str, entry: str, lenght_before: int, stats: bool, n_individuals: int, generation: int):
    plot = []
    rel = path.dirname(__file__)
    name = file

    # add bench path
    if bench:
        file = rel + '/benchmark/benchmark_file/' + file + '.json'

    # setup the population
    population = setup_population(n_individuals)

    # running the generation and the fitness function
    i = True
    count = 0
    first = True
    useless_gen = 0
    best_cromosome = 0
    while i and count <= generation:
        print("Starting generation " + str(count + 1) + " of maximum " + str(generation))
        run_gen(population, n_individuals, file, entry, overhead, lenght_before)
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
                improvements = ((population.individuals[classifica[0][1]].punt_tot - best_cromosome.punt_tot) / 300)
                best_cromosome = population.individuals[classifica[0][1]]
                if improvements <= 0.5:
                    useless_gen = useless_gen + 1
        if stats:
            plot.append(int(best_cromosome.punt_tot))

        # apply the crossover
        population = crossover(population, classifica, n_individuals)

        # apply the mutation on the new generation
        mutation(population, n_individuals, classifica)

        if (useless_gen == 20) or (best_cromosome.punt_tot > 19900):
            i = False
        count = count + 1

    if stats:
        plt.title(name)
        plt.xlabel("Generations")
        plt.ylabel("Fitness Points")
        plt.plot(plot)
        plt.show()

    return best_cromosome


def main():
    global bench
    args = get_args()
    benchmarks = [('bubblesort', ''), ('crc_32', ''), ('dijkstra_small', ''), ('fibonacci', ''),
                  ('matrixMul', ''), ('patricia', 'bit'), ('quickSort', ''), ('sha', 'sha_transform'), ('bitarray', 'alloc_bit_array'), ('idea', 'mulInv'),
                  ('Sha512String', ''), ('rsa', 'mpi_add'), ('aes', '')]
    subtest = [('bubblesort', ''), ('dijkstra_small', ''), ('fibonacci', ''), ('matrixMul', ''), ('patricia', 'bit'), ('quickSort', ''), ('sha', 'sha_transform'), ('bitarray', 'alloc_bit_array'), ('idea', 'mulInv'),
                  ('Sha512String', ''), ('rsa', 'mpi_add'), ('aes', '')]

    input_file = args.File
    entry = args.e
    overhead = args.Overhead
    bench = args.b
    count = 50
    stats = args.s
    n_indi = args.i
    gen = args.g

    if bench:
        for i in subtest:
            # Get the lenght of the original file
            execute(path.dirname(__file__) + '/benchmark/benchmark_file/' + i[0] + '.json', i[1], 0, 0, 0, 0, 0, (path.dirname(__file__) + '/metrics/output.s'), False, False, '00')
            num_lines = sum(1 for line in open((path.dirname(__file__) + '/metrics/output.s')))

            # launch the genetic algorithm
            output = ga(overhead, i[0], i[1], num_lines, stats, n_indi, gen)

            execute(path.dirname(__file__) + '/benchmark/benchmark_file/' + i[0] + '.json', i[1], output.heat, output.scrambling, output.obfuscate, output.garbage,
                    output.garbage_block,
                    (path.dirname(__file__) + '/metrics/output.s'), False, True, count)
            count = count + 1
            num_lines_2 = sum(1 for line in open((path.dirname(__file__) + '/metrics/output.s')))

            # print the best param obtained
            output.print_param()
            if stats:
                # print the overhead
                print(" Overhead: " + str(int(((num_lines_2 - num_lines) / num_lines) * 100)))

    else:
        # Get the lenght of the original file
        execute(input_file, entry, 0, 0, 0, 0, 0, (path.dirname(__file__) + '/metrics/output.s'), False, False)
        num_lines = sum(1 for line in open((path.dirname(__file__) + '/metrics/output.s')))

        # launch the genetic algorithm
        output = ga(overhead, input_file, entry, num_lines, stats, n_indi, gen)

        execute(input_file, entry, output.heat, output.scrambling, output.obfuscate, output.garbage,
                output.garbage_block,
                (path.dirname(__file__) + '/metrics/output.s'), False, True)
        num_lines_2 = sum(1 for line in open((path.dirname(__file__) + '/metrics/output.s')))

        # print the best param obtained
        output.print_param()
        if stats:
            # print the overhead
            print(" Overhead: " + str(int(((num_lines_2-num_lines)/num_lines)*100)))


if __name__ == "__main__":
    main()
