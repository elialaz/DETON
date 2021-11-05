from rvob.optimization.ga_structures import population
import numpy


def mutation(p: population, n_individuals, classifica):
    prob = 90 / n_individuals

    prob_now = prob
    for i in classifica:
        heat = p.individuals[i[1]].heat
        scrambling = p.individuals[i[1]].scrambling
        garbage = p.individuals[i[1]].garbage
        garbage_block = p.individuals[i[1]].garbage_block
        obfuscate = p.individuals[i[1]].obfuscate

        for s in range(5):
            num = numpy.random.random(1) * 100
            if num <= prob_now:
                num2 = numpy.random.randint(1, 5)
                if num2 == 1:
                    p.individuals[i[1]].heat = int(heat ^ numpy.random.randint(0, int(heat/4)))
                if num2 == 2:
                    p.individuals[i[1]].scrambling = int(scrambling ^ numpy.random.randint(0, 50))
                if num2 == 3:
                    p.individuals[i[1]].garbage = int(garbage ^ numpy.random.randint(0, int(garbage)))
                if num2 == 4:
                    p.individuals[i[1]].garbage_block = int(garbage_block ^ numpy.random.randint(0, int(garbage_block)))
                if num2 == 5:
                    p.individuals[i[1]].obfuscate = int(obfuscate ^ numpy.random.randint(0, 50))

            prob_now = prob_now + prob
