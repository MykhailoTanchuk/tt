import sys
from os import path
from output_utils import print_data, print_population_timetables, print_timetable_as_table
from db_and_export.database_utils import (
    export_data_to_db,
    import_data_from_db,
    create_database_schema,
    export_timetable_to_txt
)
from data import Data
from genetic_algorithm import GenAlg
from population import Population

# Algorithm parameters
POPULATION_SIZE = 50
MUTATION_RATE = 0.15
CROSSOVER_RATE = 0.7
TOURNAMENT_SELECTION_SIZE = 5
NUMB_OF_ELITE_TIMETABLES = 2
MAX_GENERATIONS = 100

DATABASE_PATH = 'db_and_export/timetable_database.db'
EXPORT_FILE_PATH = 'db_and_export/final_timetable.txt'

def run() -> None:
    # Step 1: Create db_and_export schema
    create_database_schema(DATABASE_PATH)
    print(f"Database schema created at path {DATABASE_PATH}")

    # Step 2: Export data to the db_and_export
    data = Data()
    export_data_to_db(data, DATABASE_PATH)
    print("Data exported to the db_and_export.")

    # Step 3: Import data from the db_and_export
    data = import_data_from_db(DATABASE_PATH)
    print("Data imported from the db_and_export.")

    generation_number = 0
    FITNESS_FUNCTION = "gaps" # can also be "combined", "conflicts"

    # Step 4: Set up and run genetic algorithm
    genetic_algorithm = GenAlg(
        data=data,
        num_elite_timetables=NUMB_OF_ELITE_TIMETABLES,
        crossover_rate=CROSSOVER_RATE,
        mutation_rate=MUTATION_RATE,
        tournament_size=TOURNAMENT_SELECTION_SIZE,
        fitness_function=FITNESS_FUNCTION
    )

    population = Population(size=POPULATION_SIZE, data=data).sort_by_fitness()

    # Initial output
    print_data(data=data)
    print_population_and_best_timetable(population, data, generation_number)
    print("START")

    # Main evolution loop
    while population.timetables[0].fitness != 1.0 and generation_number < MAX_GENERATIONS:
        generation_number += 1
        population = genetic_algorithm.evolve(population=population, generation_number=generation_number).sort_by_fitness()

        # Output current generation and best solution fitness
        print(f"Generation {generation_number}: Best fitness = {population.timetables[0].fitness}")

        print_population_and_best_timetable(population, data, generation_number)

    # Determine the best timetable
    best_timetable = population.timetables[0]

    # Check for successful completion
    if best_timetable.fitness == 1.0:
        print(f"Solution found in {generation_number + 1} generations.")
    else:
        print(f"Reached maximum generations ({MAX_GENERATIONS}) without an optimal solution.")

    print_population_and_best_timetable(population, data, generation_number)

    # Step 5: Export the best timetable to a text file
    export_timetable_to_txt(best_timetable, EXPORT_FILE_PATH)
    print(f"Timetable exported to file {EXPORT_FILE_PATH}")

def print_population_and_best_timetable(population, data, generation_number: int) -> None:
    """Displays information about the current generation and the best timetable."""
    print_population_timetables(population=population, generation_number=generation_number)
    print_timetable_as_table(data=data, timetable=population.timetables[0], generation=generation_number)

if __name__ == '__main__' and __package__ is None:
    sys.path.insert(0, path.dirname(path.abspath(__file__)))
    run()
