#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import random

sudoku_1 = pd.read_csv("Soduku1.csv",header = None)
sudoku_1 = sudoku_1.fillna(0.0)
sudoku_1 = sudoku_1.astype(int)

array_og = np.array(sudoku_1.values)

def generate_grid(array1, start, stop):
    grid_1, grid_2, grid_3 = [], [], []
    for i in range(start, stop):
        for j in range(0, 9):
            if j in [0, 1, 2]:
                grid_1.append(array1[i][j])
            elif j in [3, 4, 5]:
                grid_2.append(array1[i][j])
            else:
                grid_3.append(array1[i][j])
    return grid_1, grid_2, grid_3

def check_grids(array, grids_all, start, stop):
    counter = start
    for j in range(start, stop):
        for k in range(0, 3):
            if array[j][k] == 0:
                x = random.randint(1, 9)
                while x in grids_all[counter]:
                    x = random.randint(1, 9)
                array[j][k] = x

        for k in range(3, 6):
            if array[j][k] == 0:
                x = random.randint(1, 9)
                while x in grids_all[counter+1]:
                    x = random.randint(1, 9)
                array[j][k] = x

        for k in range(6, 9):
            if array[j][k] == 0:
                x = random.randint(1, 9)
                while x in grids_all[counter+2]:
                    x = random.randint(1, 9)
                array[j][k] = x
    return array

def fitness(puzzle):
    size = len(puzzle)
    duplicates = 0

    for row in range(size):
        if len(set(puzzle[row])) != size:
            duplicates += size - len(set(puzzle[row]))

    for col in range(size):
        if len(set(puzzle[:, col])) != size:
            duplicates += size - len(set(puzzle[:, col]))

    return duplicates

def selection(population):
    selected_population = []
    selection_criteria = 0.2
    length = len(population)
    selected = int(selection_criteria * length)
    
    for i in range(selected):
        selected_population.append(population[i])

    a = random.choice(selected_population)
    b = random.choice(selected_population)

    return a if fitness(a) < fitness(b) else b

def crossover(parent1, parent2):
    row_idx = random.randint(0, 8)
    col_idx = random.randint(0, 8)

    parent1[row_idx][col_idx:], parent2[row_idx][col_idx:] = parent2[row_idx][col_idx:], parent1[row_idx][col_idx:]

    return parent1, parent2

def mutation(solution, mutation_rate):
    mutated_solution = solution.copy()

    for i in range(9):
        for j in range(9):
            if random.random() < mutation_rate:
                mutated_solution[i][j] = random.randint(1, 9)

    return mutated_solution

def generate_population(array1, sudoku_1, population_size):
    population = []
    grids_all = []
    grid1, grid2, grid3 = generate_grid(array1, 0, 3)
    grid4, grid5, grid6 = generate_grid(array1, 3, 6)
    grid7, grid8, grid9 = generate_grid(array1, 6, 9)
    grids = [grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9]
    grids_all = np.array(grids)

    for n in range(population_size):
        array_og = np.array(sudoku_1.values)
        array1 = check_grids(array_og, grids_all, 0, 3)
        array1 = check_grids(array_og, grids_all, 3, 6)
        array1 = check_grids(array_og, grids_all, 6, 9)
        population.append(array1)

    return population

def sorting(population):
    sorted_population = []
    fitness_values = np.array([fitness(solution) for solution in population])
    sorted_indices = np.argsort(fitness_values)

    for i in range(len(sorted_indices)):
        sorted_population.append(population[sorted_indices[i]])

    return sorted_population

population_size = 15000
mutation_rate = 0.05
max_generations = 200
target_fitness = 1

generation = 0
found_solution = False

population = generate_population(array_og, sudoku_1, population_size)

while generation < max_generations and not found_solution:
    generation += 1
    sorted_population = sorting(population)

    new_population = []

    for _ in range(population_size // 2):
        parent1 = selection(sorted_population)
        parent2 = selection(sorted_population)

        crossover_child1, crossover_child2 = crossover(parent1, parent2)

        mutated_child1 = mutation(crossover_child1, mutation_rate)
        mutated_child2 = mutation(crossover_child2, mutation_rate)

        new_population.extend([mutated_child1, mutated_child2])

    population = new_population

    best_solution = sorted_population[0]
    best_fitness = fitness(best_solution)

    if best_fitness < target_fitness:
        found_solution = True

    print(f"Generation: {generation}, Best Fitness: {best_fitness}")

if found_solution:
    print("\n Orignial puzzle:")
    print(array_og)
    print("\n Found a solution with fitness less than 1:")
    print(best_solution)
else:
    print("\n Could not find a solution with fitness less than 1 within the given generations.")


# In[ ]:




