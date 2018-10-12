import sys
import random
import collections
import copy
import pandas as pd
import numpy as np


def find_batches(items, ref_table, num_batches, num_iterations=5, pop_size=20, max_generations=50):
    item_dict = get_times(items, ref_table)
    solution = GA_iterate(item_dict, num_batches, num_iterations, pop_size, max_generations)

    avg_time = float(sum(item_dict.values())) / num_batches
    print ("Best Case: " + str(avg_time) + "\nFound: " + str(solution[0]))
    return solution


def get_times(items, ref_table):

    item_dict = collections.OrderedDict()

    items = pd.read_csv('test_data.csv')
    items = items.values
    for item in items:
        item_dict[item[0]] = item[1]

    return item_dict


def GA_iterate(item_dict, num_batches, num_iterations, pop_size, max_generations):
    best_sol = (sys.maxint, None)
    for i in range(num_iterations):
        print("Beginning Iteration " + str(i))
        sol = GA(item_dict, num_batches, pop_size, max_generations)
        if best_sol[0] > sol[0]:
            best_sol = sol
    return best_sol


def GA(item_dict, num_batches, pop_size, max_generations):
    max_time = sys.maxint
    population = []
    solution = -1
    for i in range(pop_size):
        population.append(smart_init(item_dict, num_batches))
    i = 0
    no_movement = 0
    while i < max_generations and no_movement < 5:
        if not i % 50:
            best_fit = sys.maxint
            print("Generation " + str(i))
            for member, times in population:
                if max(times) < max_time:
                    best_fit = max(times)
            print("Current Best: " + str(best_fit))
        population = mate(item_dict, population, num_batches)
        population = mutate(population, num_batches)
        i += 1

    # Select best
    for member, times in population:
        if max(times) < max_time:
            max_time = max(times)
            solution = member

    return max_time, solution


def smart_init(item_dict, num_batches):
    #avg_time = float(sum(item_dict.values())) / num_batches
    items = item_dict.keys()
    mixed = copy.deepcopy(items)
    random.shuffle(mixed)
    batches = [-1] * len(items)
    times = [0] * num_batches
    for item in mixed:
        idx = items.index(item)
        batch = times.index(min(times))
        times[batch] += item_dict[item]
        batches[idx] = batch
    return batches, times


def mate(item_dict, population, num_batches):
    fitness = []
    for batches, times in population:
        fitness.append(max(times))
    #pdb.set_trace()
    #avg = sum(fitness) / float(len(fitness))
    avg = np.median(fitness)
    best = [population[i][0] for i in range(len(fitness)) if fitness[i] <= avg]
    new_pop = []
    random.shuffle(best)

    i = 0
    while len(new_pop) < len(population):
        mom = best[i%len(best)]
        dad = best[random.choice(range(len(best)))]
        baby = [mom[i] if random.random() < .5 else dad[i] for i in range(len(mom))]
        baby_times = get_all_times(item_dict, baby, num_batches)
        new_pop.append((baby, baby_times))
        i += 1

    return new_pop


def mutate(population, num_batches):
    for batches, times in population:
        if random.random() < 0.50:
            for i in range(len(batches)):
                if random.random() < 0.0005 and random.random() < 0.0005:
                    print("BM")
                    batches += [batches.pop(i)]
                elif random.random() < 0.001:
                    batches[i] = random.randint(0, num_batches-1)

    return population


def get_all_times(item_dict, batch, num_batches):
    times = [0] * num_batches
    for i in range(len(batch)):
        times[batch[i]] += item_dict[item_dict.keys()[i]]
    return times


sol = find_batches(items=1, ref_table=1, num_batches=7, num_iterations=3, pop_size=30, max_generations=500)


