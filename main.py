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
    for i in range(n-1):
### potrzebna zmiana do większej ilości miast
        t = [1,2,3,4,5,6]
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
    # print(ind)

# generation = first_gen()
# print(generation)
# for i in range(n-1):
#     print(full_dist(generation[i]))
# print(crossover(generation[0],generation[1]))
# mutation(generation[0])
