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
    print(cut)
    new1 = [0]
    new2 = new1
    # for i in range(cut+1):
    #     new1.append(0)
    # new2 = new1
    # print(new1)
    # print(new2)
### jest źle
    for i in range(1,n):
        if len(new1) == cut+1:
            break
        elif ind1[i] in islice(ind2, cut+1, None):
            continue
        else:
            new1.append(ind1[i])
    print(new1)



print(first_gen())
generation = first_gen()

for i in range(n-1):
    print(full_dist(generation[i]))

crossover(generation[0],generation[1])
