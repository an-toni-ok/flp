import random
import json
import warnings
import dataclasses
import numpy as np
from deap import algorithms, base, creator, tools
from deap.tools import cxTwoPoint, cxOrdered
from deap.benchmarks.tools import hypervolume

from digital_twins import Area, MStep, MachineType, Machine, Operator, ProductionSystem

warnings.filterwarnings('ignore')

def decode_json(file):
    with open(file, 'r') as j:
        data = json.load(j)
    areas = [Area(**area, restricted=False) for area in data['areas']]
    areas.extend([Area(**area, restricted=True) for area in data['restricted_areas']])
    step_list = [MStep(order=i, **step) for i, step in enumerate(data['production_steps'])]
    machine_list = []
    for machine in data['machines']:
        machine_type = MachineType(machine['name'], machine['technologies'], machine['hourly_rate'], machine['investment_cost'],
                                   machine['additional_machine_time'], machine['x_dimension'], machine['y_dimension'])
        machine_list.append(machine_type)
    return step_list, machine_list, data['hourly_operator_cost'], data['target_cycle_time'], areas

def encode_json(systems):
    output = []
    for system in systems:
        system_dict = {'machines': [], 'operators': [], 'objectives': {}, 'cycle_time': system.cycle_time}
        for machine in system.machine_list:
            machine_dict = dataclasses.asdict(machine)
            machine_dict['production_steps'] = machine_dict.pop('mstep_list')
            machine_dict['production_steps'] = [mstep['order'] for mstep in machine_dict['production_steps']]
            machine_dict['assigned_operator'] = machine_dict.pop('operator')
            machine_dict['assigned_operator'] = machine_dict['assigned_operator']
            system_dict['machines'].append(machine_dict)
        for operator in system.operator_list:
            operator_dict = {}
            operator_dict['assigned_machines'] = [machine.id for machines in operator.machine_list]
            operator_dict['work_content'] = operator.work_content
            operator_dict['cycle_time'] = operator.cycle_time
            system_dict['operators'].append(operator_dict)
        system_dict['objectives'] = {'invest': system.investment_cost,
                                     'cost_per_part': system.cost_per_part,
                                     'used_area': system.used_area,
                                     'number_operators': system.number_operators}
        output.append(system_dict)
    return output

def optimization(step_list: list, machine_list: list, hourly_rate_operators: float, target_cycle_time: int,
                 areas: list, max_operators: int = 5,
                 hyperparameters: dict = {'generations': 250, 'pop_size': 200, 'prob_mutation': 0.3, 'prob_crossover': 1.}) -> list[list]:

    print('START OPTIMIZATION')
    # Define global variables
    MACHINE_TYPES = machine_list
    PRODUCTION_STEPS = step_list
    MAX_OPERATORS = max_operators
    HOURLY_RATE_OPERATORS = hourly_rate_operators
    AREAS = areas
    CYCLE_TIME = target_cycle_time

    # Define helper functions
    def create_system(individual):
        machine_list = []
        operator_list = []
        index = 0
        for machine_type_index, operator in zip(individual[0], individual[1]):
            machine_type = MACHINE_TYPES[machine_type_index]
            machine = Machine(machine_type.name, index, machine_type)
            machine.mstep_list = [PRODUCTION_STEPS[index]]
            machine.operator = operator
            machine_list.append(machine)
            index += 1
        
        # Create operator objects
        operators = individual[1]
        operator_list = []
        for i in list(set(operators)):
            indices = []
            for j, operator in enumerate(operators):
                if i == operator:
                    indices.append(j)
            operator_machines = []
            for index in indices:
                operator_machines.append(machine_list[index])
            operator_list.append(Operator(i, HOURLY_RATE_OPERATORS, operator_machines))

        system = ProductionSystem(CYCLE_TIME, None, AREAS, machine_list, operator_list,
                                  first_corner=individual[2][0], second_corner=individual[2][1])
        return system

    def genetic_algorithm(generations: int, pop_size: int,
                      prob_crossover: float, prob_mutation: float) -> list:
        creator.create('Objective', base.Fitness, weights=(-1., -1.))
        creator.create('Individual', list, fitness=creator.Objective)
        toolbox = base.Toolbox()
                
        def create_ind(ind_class) -> object:
            """
            Function to create an individual representing a valid solution.
            :param ind_class: class of individual of the DEAP framework
            :return: instance of an individual
            """
            machine_list = []
            operator_list = []
            for step in PRODUCTION_STEPS:
                machine_list.append(random.choice(range(0, len(MACHINE_TYPES))))
                operator_list.append(random.choice(range(0, MAX_OPERATORS)))
            # define positions of corners in the U-layout
            corners = []
            for i in range(0, 2):
                corners.append(random.choice(range(0, len(machine_list)+1)))
            corners.sort()
            # build genome
            individual = [machine_list, operator_list, corners]
            return ind_class(individual)

        def mutate(individual) -> object:
            def mutate_machine_type(individual):
                """
                Change the type of one machine.
                """
                index = random.choice(range(len(individual[0])))
                new_type = random.choice(range(len(MACHINE_TYPES)))
                individual[0][index] = new_type
                return individual
            
            def mutate_operators(individual):
                operator = random.choice(range(0, len(individual[1])))
                if individual[1][operator] == 0:
                    individual[1][operator] = 1
                elif individual[1][operator] == MAX_OPERATORS:
                    individual[1][operator] = MAX_OPERATORS - 1
                else:
                    number = random.choice([-1, 1])
                    individual[1][operator] = individual[1][operator] + number
                return individual
            
            def mutate_corners(individual):
                machine_types = individual[0]
                index = random.choice(range(0, len(individual[2])))
                if individual[2][index] == 0:
                    if individual[2][index] < len(machine_types):
                        individual[2][index] = 1
                elif individual[2][index] == len(machine_types):
                    if individual[2][index] > 0:
                        individual[2][index] = len(machine_types) - 1
                else:
                    number = random.choice([-1, 1])
                    individual[2][index] = individual[2][index] + number
                individual[2].sort()
                return individual

            if random.random() < 1 / 2:
                individual = mutate_machine_type(individual)
            if random.random() < 1 / 2:
                individual = mutate_operators(individual)
            if random.random() < 1 / 2:
                individual = mutate_corners(individual)
            return (individual,)
        

        def crossover(ind1: list, ind2: list) -> tuple[list, list]:
            """
            Crossover of two individuals.
            :param ind1: Individual 1
            :param ind2: Individual 2
            :return: two new individuals
            """
            cx_index = random.randrange(1, len(ind1[0]))
            new_machines1 = ind2[0][:cx_index] + ind1[0][cx_index:]
            new_machines2 = ind1[0][:cx_index] + ind2[0][cx_index:]
            new_operators1 = ind2[1][:cx_index] + ind1[1][cx_index:]
            new_operators2 = ind1[1][:cx_index] + ind2[1][cx_index:]
            new_corners1 = ind2[2][:1] + ind1[2][1:]
            new_corners1.sort()
            new_corners2 = ind1[2][:1] + ind2[2][1:]
            new_corners2.sort()
            ind1[0] = new_machines1
            ind1[1] = new_operators1
            ind1[2] = new_corners1
            ind1[0] = new_machines2
            ind2[1] = new_operators2
            ind2[2] = new_corners2
            return (ind1, ind2)

        def evaluate(individual, system: object = None) -> tuple[float]:
            """
            Evaluate the individual and return the fitness values without scaling and penalty.
            :param individual: Individual for evaluation
            :param system: Already constructed production system object
            :return: fitness values
            """
            # Minimize operator numbers to range(0, num_operators)
            map_dict = {}
            current_num = 0
            for op in individual[1]:
                if op not in map_dict.keys():
                    map_dict[op] = current_num
                    current_num += 1
            individual[1] = [map_dict[op] for op in individual[1]]
            # create line object if not passed as argument
            if system is None:
                system = create_system(individual)
            system.evaluate()
            cost_per_part = system.cost_per_part
            invest = system.investment_cost
            return (invest, cost_per_part)
        
        def scale(fitness: tuple[float], magnitudes: list[float]) -> tuple[float]:
            """
            Scale the fitness values to a magnitude of 1.
            :param fitness: unscaled fitness of an indiviual
            :param magnitudes: precalculated magnitudes of each fitness dimension
            :return: scaled fitness
            """
            scaled_fitness = np.divide(fitness, magnitudes).tolist()
            return tuple(scaled_fitness)
        
        def penalize(system: object, fitness: tuple[float]) -> tuple[float]:
            """
            Add penalties to the scaled fitness values if any constraint is violated.
            :param system: Instance of production system of the current evaluation
            :param fitness: scaled fitness without penalty
            :return: fitness with penalty
            """
            penalty = 0
            if (system.cycle_time > system.target_cycle_time):
                penalty += 10 + 1 * (system.cycle_time - system.target_cycle_time)
            if system.crossing_operators:
                penalty += 10
            return tuple([i + penalty for i in fitness])
        
        def scale_evaluate(individual, magnitudes: list[float]) -> tuple[float]:
            """
            Evaluate the individual and return the fitness values with scaling and penalty.
            :param individual: Individual for evaluation
            :param magnitudes: precalculated magnitudes of each fitness dimension
            :return: fitness values
            """
            system = create_system(individual)
            fitness = evaluate(individual, system)
            return penalize(system, scale(fitness, magnitudes))

        def customMuPlusLambda(population, toolbox, mu, mutpb, ngen,
                                stats=None, halloffame=None, verbose=__debug__):
            r"""This is the :math:`(\mu + \lambda)` evolutionary algorithm.

            :param population: A list of individuals.
            :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                            operators.
            :param mu: The number of individuals to select for the next generation.
            :param lambda\_: The number of children to produce at each generation.
            :param mutpb: The probability that an offspring is produced by mutation.
            :param ngen: The number of generation.
            :param stats: A :class:`~deap.tools.Statistics` object that is updated
                        inplace, optional.
            :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                            contain the best individuals, optional.
            :param verbose: Whether or not to log the statistics.
            :returns: The final population
            :returns: A class:`~deap.tools.Logbook` with the statistics of the
                    evolution.

            The algorithm takes in a population and evolves it in place using the
            :func:`varAnd` function. It returns the optimized population and a
            :class:`~deap.tools.Logbook` with the statistics of the evolution. The
            logbook will contain the generation number, the number of evaluations for
            each generation and the statistics if a :class:`~deap.tools.Statistics` is
            given as argument. The *cxpb* and *mutpb* arguments are passed to the

            This function expects :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
            :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
            registered in the toolbox. This algorithm uses the :func:`varOr`
            variation.
            """
            logbook = tools.Logbook()
            logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in population if not ind.fitness.valid]
            # get magnitudes of the unscaled fitness values for scaling
            magnitudes = [100000, 100]
            # get scaled and penalized fitness values
            scaled_fitnesses = toolbox.map(toolbox.evaluate, invalid_ind, [magnitudes] * len(invalid_ind))

            for ind, fit in zip(invalid_ind, scaled_fitnesses):
                ind.fitness.values = fit

            if halloffame is not None:
                halloffame.update(population)

            record = stats.compile(population) if stats is not None else {}
            logbook.record(gen=0, nevals=len(invalid_ind), **record)
            if verbose:
                print(logbook.stream)

            # Begin the generational process
            for gen in range(1, ngen + 1):
                # Vary the population
                def generate_offspring(population, toolbox, mutpb):
                    pop = [toolbox.clone(ind) for ind in population]
                    offspring = []
                    # Apply crossover and mutation on the offspring
                    for i in range(0, len(pop)// 2):
                        p1 = tools.sortNondominated(random.sample(pop, 2), 1, True)[0][0]
                        p2 = tools.sortNondominated(random.sample(pop, 2), 1, True)[0][0]
                        offspring1, offspring2 = toolbox.mate(p1, p2)
                        del offspring1.fitness.values, offspring2.fitness.values
                        offspring.append(offspring1)
                        offspring.append(offspring2)

                    for i in range(len(offspring)):
                        if random.random() < mutpb:
                            offspring[i], = toolbox.mutate(offspring[i])
                            del offspring[i].fitness.values

                    return offspring
                
                # offspring = algorithms.varAnd(population, toolbox, cxpb, mutpb)
                offspring = generate_offspring(population, toolbox, mutpb)
                # Evaluate the individuals with an invalid fitness
                invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
                fitnesses = toolbox.map(toolbox.evaluate, invalid_ind, [magnitudes] * len(invalid_ind))
                for ind, fit in zip(invalid_ind, fitnesses):
                    ind.fitness.values = fit

                # Update the hall of fame with the generated individuals
                if halloffame is not None:
                    halloffame.update(offspring)

                # Select the next generation population
                population[:] = toolbox.select(population + offspring, mu)

                # Update the statistics with the new population
                record = stats.compile(population) if stats is not None else {}
                logbook.record(gen=gen, nevals=len(invalid_ind), **record)
                if verbose:
                    print(logbook.stream)

            return population, logbook
        
        # hypervolume function for statistics
        def hyper(population):
            front = tools.sortNondominated(population, len(population), first_front_only=True)
            return hypervolume(front[0], [50, 50])

        # Register all the needed functions at the deap toolbox
        toolbox.register('create_individual', create_ind, creator.Individual)
        toolbox.register('create_population', tools.initRepeat, list, toolbox.create_individual)
        toolbox.register('mutate', mutate)
        toolbox.register('evaluate', scale_evaluate)
        toolbox.register('mate', crossover)
        toolbox.register('select', tools.selNSGA2)
        # Register statistics
        stats = tools.Statistics()
        stats.register("hypervolume", hyper)

        population = toolbox.create_population(n=pop_size) # create start population
        pop, log = customMuPlusLambda(population, toolbox, pop_size,
                                      prob_mutation, generations, stats=stats, verbose=True)
        return pop

    solutions = []
    solutions.extend(genetic_algorithm(**hyperparameters))
    # Sort all the collected solutions with non-dominated sorting
    fronts = tools.sortNondominated(solutions, len(solutions))
    results = [create_system(ind) for ind in fronts[0]]
    for system in results:
        system.evaluate()
    return (results)

def run_optimization(file):
    data = decode_json(file)
    results = optimization(*data)
    return encode_json(results)