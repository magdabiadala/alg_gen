import math
import random
from itertools import islice
import time
import statistics as stat


### testowy zbiór miast i ich współrzędnych
# Poznan = [52.4082663, 16.9335199]
# Warszawa = [52.2319581,21.0067249]
# Gdansk = [54.347629,18.6452324]
# Krakow = [50.0619474,19.9368564]
# Wroclaw = [51.1089776,17.0326689]
# Torun = [53.0102721,18.6048094]
# Zielona_Gora = [51.9383777,15.5050408]
# cities = [Poznan, Warszawa, Gdansk, Krakow, Wroclaw, Torun, Zielona_Gora]

### liczba miast
### number_of_cities
### prawdopodobieństwo mutacji
mutation_prob = 0.02
### ilość osobników w pokoleniu
generation_size = 10
### liczba pokoleń
number_of_generations = 10
### rodzaj ruletki
rec_fun = False


def distance(a,b):
    city_a = cities[a]
    city_b = cities[b]
    dist = math.sqrt((city_a[0]-city_b[0])**2 + (city_a[1]-city_b[1])**2)
    return dist

def full_dist(individual):
    full_distance = 0
    for city in range(number_of_cities):
        full_distance += distance(individual[city],individual[city+1])
    return full_distance

def first_gen():
    first_generation = []
    for individual in range(generation_size):
        list_of_numbers = list(range(1,number_of_cities))
        # print(list_of_numbers)
        individual = [0]
        while len(list_of_numbers) > 0:
            number = random.choice(list_of_numbers)
            individual.append(number)
            list_of_numbers.remove(number)
        individual.append(0)
        first_generation.append(individual)
    return first_generation

def crossover(individual1, individual2):
    cut = random.randint(2,number_of_cities-2)
    new1 = [0]
    new2 = [0]
    # print(individual1)
    # print(individual2)
    # print(cut)

    for city in range(1,number_of_cities):
        #gdy znajdziemy wszystkie szukane liczby zanim przejrzymy całą individual2
        if len(new1) == cut+1:
            break
        elif individual1[city] in islice(individual2, cut+1, None):
            continue
        else:
            new1.append(individual1[city])
    for city in range(1,number_of_cities):
        if len(new2) == cut+1:
            break
        elif individual2[city] in islice(individual1, cut+1, None):
            continue
        else:
            new2.append(individual2[city])
    slice2 = individual2[slice(cut+1, number_of_cities+1)]
    slice1 = individual1[slice(cut+1, number_of_cities+1)]
    new1 = new1 + slice2
    new2 = new2 + slice1
    # print(new1)
    # print(new2)
    return new1, new2

def mutation(individual):
    # print(individual)
    possible_locuses = list(range(1,number_of_cities))
    locus1 = random.choice(possible_locuses)
    possible_locuses.remove(locus1)
    locus2 = random.choice(possible_locuses)
    # print(locus1)
    # print(locus2)
    # zamiana 2 genów
    gene = individual[locus1]
    individual[locus1] = individual[locus2]
    individual[locus2] = gene
    return individual

def roulette(generation):
    # print('pokolenie: ', generation)
    distances = []
    for individual in range(generation_size):
        individual_distance = full_dist(generation[individual])
        distances.append(individual_distance)
    # print('dystanse: ',distances)
    roulette_tab = reciprocal(distances, rec_fun)
    # print('ruletka: ',roulette_tab)
    survivors = []
    for individual in range(generation_size):
        random_number = random.random()
        interval_number = 0
        while random_number > roulette_tab[interval_number]:
            interval_number += 1
        survivors.append(generation[interval_number])
    # print('przetrwali: ',survivors)
    return survivors


def reciprocal(distances, rec_fun):
    # print('odległości: ', distances)
    maximum = max(distances)
    minimum = min(distances)
    # print("minimum: ", minimum)
    # print("maximum: ", maximum)

    ### STARSZA WERSJA FUNKCJI ###
    # za słabo promuje najlepsze osobniki

    # reciprocal = [maximum-x+minimum for x in distances]
    # print('odwrócone: ',reciprocal)
    # sum_of_reciprocal = sum(reciprocal)
    # normalized = [x/sum_of_reciprocal for x in reciprocal]
    # print('znormalizowane: ',normalized)

    ################################

    ######### NOWA WERSJA ##########
    # zdcydowanie bardziej promuje dobre osobniki

    if rec_fun == True:
        reciprocal = [maximum-x+1 for x in distances]
        sum_of_reciprocal = sum(reciprocal)
        # print('odwrócone: ',reciprocal)
        # print("suma: ", sum_of_reciprocal)
        normalized = [x/sum_of_reciprocal for x in reciprocal]
    # print('znormalizowane: ',normalized)

    ################################

    ######## WERSJA Z 1/x ##########

    else:
        reciprocal = [1/x for x in distances]
        sum_of_reciprocal = sum(reciprocal)
        # print('odwrócone: ',reciprocal)
        # print("suma: ", sum_of_reciprocal)
        normalized = [(1/x)/sum_of_reciprocal for x in reciprocal]

    ################################

    for i in range(1,generation_size-1):
        normalized[i] += normalized[i-1]
    # wpisuję 1 ręcznie, bo czasem liczby nie sumowały się idealnie do 1 (niedokładność komputera)
    normalized[generation_size-1] = 1
    # print('ruletka: ', normalized)
    return normalized

def gen_alg():
    generation = first_gen()
    # print('1 generacja: ',generation)
    global_minimum = math.inf

    # ta pętla liczy tylko najkrótszy dystans dla pierwszego pokolenia
    for first_gen_individual in range(generation_size):
        distance_of_individual = full_dist(generation[first_gen_individual])
        if distance_of_individual < global_minimum:
            global_minimum = distance_of_individual

    #właściwa pętla programu
    for generation_index in range(number_of_generations):
        # print('pokolenie numer: ', generation_index)
        # print(generation)

        #RULETKA
        survivors = roulette(generation)
        # print('przetrwali: ',survivors)

        #KRZYŻOWANIE
        descendants = []
        for individual in range(0,generation_size,2):
            pair = crossover(survivors[individual],survivors[individual+1])
            for each in pair:
                descendants.append(each)
        # print('potomkowie: ', descendants)

        #MUTACJA
        for individual in range(generation_size):
            if random.random() <= mutation_prob:
                # print('MUTACJA!!!')
                mutation(descendants[individual])
        # print('potomkowie po mutacji: ', descendants)

        # NAJKRÓTSZA TRASA
        local_minimum = math.inf
        for each in range(generation_size):
            specific_distance = full_dist(descendants[each])
            if specific_distance < local_minimum:
                local_minimum = specific_distance
        # print('minimum w pokoleniu: ',local_minimum)
        if local_minimum < global_minimum:
            global_minimum = local_minimum
        generation = descendants
    return global_minimum

# otwarcie plików z współrzędnymi i wynikami
file = open("tsp_100_1", "r")
number = 0
cities = []
number_of_cities = int(file.readline())
for line in file:
    coords = line.split()
    coords = list(map(int, coords))
    cities.append(coords)
    number += 1
file_results = open("text_results.txt", "a")

# listy parametrów do przetestowania
mut = [0.06]
size = [60, 80]
iters = [20, 40, 80, 160, 320]
rec = [True]
# mut = [0.01, 0.02]
# size = [10, 20]
# iters = [5, 10]
# liczba testów w każdym z warunków
num_of_tests = 50
test_id = 1

for d in range(len(rec)):
    rec_fun = rec[d]
    for a in range(len(mut)):
        mutation_prob = mut[a]
        for b in range(len(size)):
            generation_size = size[b]
            for c in range(len(iters)):
                number_of_generations = iters[c]
                print("test numer: ", test_id)
                file_results.write(str(mutation_prob) + "," + str(generation_size) + "," + str(number_of_generations) + "," + str(rec_fun) + ",")
                for e in range(num_of_tests):
                    exec_times = []
                    best_individuals = []
                    start_time = time.time()
                    best = gen_alg()
                    exec_times.append(time.time() - start_time)
                    best_individuals.append(best)
                file_results.write(str(stat.mean(best_individuals)) + ",")
                file_results.write(str(stat.median(best_individuals)) + ",")
                file_results.write(str(stat.mean(exec_times)) + ",\n")
                test_id += 1
file_results.close()
