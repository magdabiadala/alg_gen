import math
import random
from itertools import islice

### testowy zbiór miast i ich współrzędnych
Poznan = [52.4082663, 16.9335199]
Warszawa = [52.2319581,21.0067249]
Gdansk = [54.347629,18.6452324]
Krakow = [50.0619474,19.9368564]
Wroclaw = [51.1089776,17.0326689]
Torun = [53.0102721,18.6048094]
Zielona_Gora = [51.9383777,15.5050408]
cities = [Poznan, Warszawa, Gdansk, Krakow, Wroclaw, Torun, Zielona_Gora]
### liczba miast
number_of_cities = len(cities)
### prawdopodobieństwo mutacji
mutation_prob = 0.02
### ilość osobników w pokoleniu
generation_size = 70
### liczba pokoleń
number_of_generations = 100

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
    roulette_tab = reciprocal(distances)
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


def reciprocal(distances):
    # print('odległości: ', distances)
    maximum = max(distances)
    minimum = min(distances)
    # print("minimum: ", minimum)
    # print("maximum: ", maximum)

    ### TSTARSZA WERSJA FUNKCJI ###
    # za słabo promuje najlepsze osobniki

    # reciprocal = [maximum-x+minimum for x in distances]
    # print('odwrócone: ',reciprocal)
    # sum_of_reciprocal = sum(reciprocal)
    # normalized = [x/sum_of_reciprocal for x in reciprocal]
    # print('znormalizowane: ',normalized)

    ################################

    ######### NOWA WERSJA ##########
    # zdcydowanie bardziej promuje dobre osobniki

    reciprocal = [maximum-x+1 for x in distances]
    sum_of_reciprocal = sum(reciprocal)
    # print('odwrócone: ',reciprocal)
    # print("suma: ", sum_of_reciprocal)
    normalized = [x/sum_of_reciprocal for x in reciprocal]
    # print('znormalizowane: ',normalized)

    ################################

    for i in range(1,generation_size-1):
        normalized[i] += normalized[i-1]
    # wpisuję 1 ręcznie, bo czasem liczby nie sumowały się idealnie do 1 (niedokładność komputera)
    normalized[generation_size-1] = 1
    # print('ruletka: ', normalized)
    return normalized


generation = first_gen()
print('1 generacja: ',generation)
global_minimum = math.inf

# ta pętla liczy tylko najkrótszy dystans dla pierwszego pokolenia
for first_gen_individual in range(generation_size):
    distance_of_individual = full_dist(generation[first_gen_individual])
    if distance_of_individual < global_minimum:
        global_minimum = distance_of_individual

#właściwa pętla programu
for generation_index in range(number_of_generations):
    print('pokolenie numer: ', generation_index)
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
    # print('potomkowie: ', descendants)

    # NAJKRÓTSZA TRASA
    local_minimum = math.inf
    for each in range(generation_size):
        specific_distance = full_dist(descendants[each])
        if specific_distance < local_minimum:
            local_minimum = specific_distance
    print('minimum w pokoleniu: ',local_minimum)
    if local_minimum < global_minimum:
        global_minimum = local_minimum
    generation = descendants
print('minimum globalne: ', global_minimum)
