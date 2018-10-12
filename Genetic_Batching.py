import sys
import random
import collections
import copy
import pandas as pd
import numpy as np

import pdb


def find_batches(trades, ref_table, num_batches, num_iterations=5, pop_size=20, max_generations=50):
    t_dict = get_times(trades, ref_table)
    solution = GA_iterate(t_dict, num_batches, num_iterations, pop_size, max_generations)

    avg_time = float(sum(t_dict.values())) / num_batches
    print ("Best Case: " + str(avg_time) + "\nFound: " + str(solution[0]))
    return solution


#TODO: check on format of time reference table
def get_times(trades, ref_table):

    t_dict = collections.OrderedDict()

    trades = pd.read_csv('test_data.csv')
    trades = trades.values
    for trade in trades:
        t_dict[trade[0]] = trade[1]

    return t_dict


def GA_iterate(t_dict, num_batches, num_iterations, pop_size, max_generations):
    best_sol = (sys.maxint, None)
    for i in range(num_iterations):
        print("Beginning Iteration " + str(i))
        sol = GA(t_dict, num_batches, pop_size, max_generations)
        if best_sol[0] > sol[0]:
            best_sol = sol
    return best_sol


def GA(t_dict, num_batches, pop_size, max_generations):
    max_time = sys.maxint
    population = []
    solution = -1
    for i in range(pop_size):
        population.append(smart_init(t_dict, num_batches))
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
        population = mate(t_dict, population, num_batches)
        population = mutate(population, num_batches)
        i += 1

    # Select best
    for member, times in population:
        if max(times) < max_time:
            max_time = max(times)
            solution = member

    return max_time, solution


def smart_init(t_dict, num_batches):
    #avg_time = float(sum(t_dict.values())) / num_batches
    trades = t_dict.keys()
    mixed = copy.deepcopy(trades)
    random.shuffle(mixed)
    batches = [-1] * len(trades)
    times = [0] * num_batches
    for trade in mixed:
        idx = trades.index(trade)
        batch = times.index(min(times))
        times[batch] += t_dict[trade]
        batches[idx] = batch
    return batches, times


# def smart_init(t_dict, num_batches):
#     avg_time = float(sum(t_dict.values())) / num_batches
#     trades = t_dict.keys()
#     random.shuffle(trades)
#     batches = [[[], 0] for _ in range(num_batches)]
#     # TODO: optimize embedded for loop
#     open_batches = range(num_batches)
#     for trade in trades:
#         min = sys.maxint
#         min_b = None
#         time = t_dict[trade]
#         placed = False
#         i = 0
#         while not placed and i < num_batches:
#             if batches[i][1] + time <= avg_time:
#                 batches[i][0].append(trade)
#                 batches[i][1] += time
#                 placed = True
#             elif batches[i][1] < min:
#                 min_b = batches[i]
#             i += 1
#         min_b[0].append(trade)
#         min_b[1] += time
#     return batches


def mate(t_dict, population, num_batches):
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
        baby_times = get_all_times(t_dict, baby, num_batches)
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


def get_all_times(t_dict, batch, num_batches):
    times = [0] * num_batches
    for i in range(len(batch)):
        times[batch[i]] += t_dict[t_dict.keys()[i]]
    return times


# def get_time(t_dict, batch):
#     time = 0
#     for trade in batch:
#         time += t_dict[trade]
#
#     return time


sol = find_batches(trades=1, ref_table=1, num_batches=7, num_iterations=3, pop_size=30, max_generations=500)


