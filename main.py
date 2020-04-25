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
n = 7
### prawdopodobieństwo mutacji
mutation_prob = 0.03
### ilość osobników w pokoleniu
size = 10
### liczba pokoleń
iterations = 20

def distance(a,b):
    x = cities[a]
    y = cities[b]
    d = math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
    return d

def full_dist(individual):
    d = 0
    list = individual
    for i in range(n):
        d += distance(list[i],list[i+1])
    return d

def first_gen():
    gen1 = []
    for i in range(size):
        t = list(range(1,n))
        # print(t)
        individual = [0]
        while len(t) > 0:
            r = random.choice(t)
            individual.append(r)
            t.remove(r)
        individual.append(0)
        gen1.append(individual)
    return gen1

def crossover(ind1, ind2):
    cut = random.randint(2,n-2)
    new1 = [0]
    new2 = [0]
    # print(ind1)
    # print(ind2)
    # print(cut)
    for i in range(1,n):
        #gdy znajdziemy wszystkie szukane liczby zanim przejrzymy całą ind2
        if len(new1) == cut+1:
            break
        elif ind1[i] in islice(ind2, cut+1, None):
            continue
        else:
            new1.append(ind1[i])
    for i in range(1,n):
        if len(new2) == cut+1:
            break
        elif ind2[i] in islice(ind1, cut+1, None):
            continue
        else:
            new2.append(ind2[i])
    slice2 = ind2[slice(cut+1, n+1)]
    slice1 = ind1[slice(cut+1, n+1)]
    new1 = new1 + slice2
    new2 = new2 + slice1
    # print(new1)
    # print(new2)
    return new1, new2

def mutation(ind):
    # print(ind)
    locuses = list(range(1,n))
    locus1 = random.choice(locuses)
    locuses.remove(locus1)
    locus2 = random.choice(locuses)
    # print(locus1)
    # print(locus2)
    x = ind[locus1]
    ind[locus1] = ind[locus2]
    ind[locus2] = x
    return ind

def roulette(generation):
    # print('pokolenie: ', generation)
    distances = []
    for i in range(size):
        a = full_dist(generation[i])
        distances.append(a)
    # print('dystanse: ',distances)
    roulette_tab = reciprocal(distances)
    # print('ruletka: ',roulette_tab)
    survivors = []
    for i in range(size):
        r = random.random()
        j = 0
        while r > roulette_tab[j]:
            j += 1
        #może by się przydało coś na wypadek wylosowania 1 gdy nie ma jej w tablicy akurat
        survivors.append(generation[j])
    # print('przetrwali: ',survivors)
    return survivors


def reciprocal(distances):
    # print('odległości: ', distances)
    maximum = max(distances)
    minimum = min(distances)
    reciprocal = [maximum-x+minimum for x in distances]
    # print('odwrócone: ',reciprocal)
    sum2 = sum(reciprocal)
    normalized = [x/sum2 for x in reciprocal]
    # print('znormalizowane: ',normalized)
    for i in range(1,size):
        normalized[i] += normalized[i-1]
    # print('ruletka: ', normalized)
    return normalized


generation = first_gen()
print('1 generacja: ',generation)
#to by wypadało zmienić bo brzydkie!
local_minimum = 50
for i in range(size):
    a = full_dist(generation[i])
    if a < local_minimum:
        local_minimum = a
for i in range(iterations):
    print('pokolenie: ', i)
    # print(generation)
    survivors = roulette(generation)
    # print('przetrwali: ',survivors)
    descendants = []
    for j in range(0,size,2):
        pair = crossover(survivors[j],survivors[j+1])
        for a in pair:
            descendants.append(a)
    for j in range(size):
        if random.random() <= mutation_prob:
            # print('MUTACJA!!!')
            mutation(descendants[j])
    # print('potomkowie: ', descendants)
    #to by wypadało zmienić bo brzydkie!
    x = 50
    for j in range(size):
        a = full_dist(descendants[j])
        if a < x:
            x = a
    print('minimum: ',x)
    if x < local_minimum:
        local_minimum = x
    generation = descendants
print('minimum lokalne: ', local_minimum)
