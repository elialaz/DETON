from rvob.optimization.ga_structures import population
import numpy
import random


#traforma in binary
def to_bin(n):
    return bin(n).replace("0b", "")

#cambia uno 0 o 1 a caso
def change(x):
    temp_rand = random.randint(1, len(x)) - 1
    flip = str(x)
    flip_list = list(flip)
    if flip_list[temp_rand] == "0":
        flip_list[temp_rand] = "1"
    else:
        flip_list[temp_rand] = "0"
    #return del binario trasformato convertito in base 2, ergo decimale
    return int("".join(flip_list), 2)


def mutation(p: population, n_individuals, classifica):
    prima = True
    prob = 90 / n_individuals
    prob_temp = prob

    prob_now = prob
    for i in classifica:
        heat = p.individuals[i[1]].heat
        scrambling = p.individuals[i[1]].scrambling
        garbage = p.individuals[i[1]].garbage
        garbage_block = p.individuals[i[1]].garbage_block
        obfuscate = p.individuals[i[1]].obfuscate

        if prima:
            heat = to_bin(heat)
            scrambling = to_bin(scrambling)
            garbage = to_bin(garbage)
            garbage_block = to_bin(garbage_block)
            obfuscate = to_bin(obfuscate)

        for s in range(5):
            if prima:
                rand_prob = random.random() * 100
                if rand_prob < prob:
                    num = random.randint(1, 5)
                    if num == 1:
                        p.individuals[i[1]].heat = change(heat)
                    if num == 2:
                        p.individuals[i[1]].scrambling = change(scrambling)
                    if num == 3:
                        p.individuals[i[1]].garbage = change(garbage)
                    if num == 4:
                        p.individuals[i[1]].garbage_block = change(garbage_block)
                    if num == 5:
                        p.individuals[i[1]].obfuscate = change(obfuscate)
                prob_temp += prob
            else:
                num = numpy.random.random(1) * 100
                if num <= prob_now:
                    num2 = numpy.random.randint(1, 5)
                    if num2 == 1:
                        p.individuals[i[1]].heat = int(heat ^ numpy.random.randint(0, int(heat / 4)))
                    if num2 == 2:
                        p.individuals[i[1]].scrambling = int(scrambling ^ numpy.random.randint(0, 50))
                    if num2 == 3:
                        p.individuals[i[1]].garbage = int(garbage ^ numpy.random.randint(0, int(garbage)))
                    if num2 == 4:
                        p.individuals[i[1]].garbage_block = int(
                            garbage_block ^ numpy.random.randint(0, int(garbage_block)))
                    if num2 == 5:
                        p.individuals[i[1]].obfuscate = int(obfuscate ^ numpy.random.randint(0, 50))
                prob_now = prob_now + prob
