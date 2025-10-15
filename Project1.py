# SI 201 Project 1
# Your name: Rahma Musse
# Your student id: 31746890
# Your email: rmusse@umich.edu 
# Who or what you worked with on this homework (including generative AI like ChatGPT): 
# Amani(did calculate_body_flipper_to_mass_ratio function and test cases for that function) 
# Isa(did load_penguin and calculate_average_body_mass_species and test cases for the functions)
# I did the analyze_bill_ratio_mass_relation function and the test cases for that function)
# All worked on the write_results function together
# If you worked with generative AI also add a statement for how you used it. 
# e.g.: Used chatgpt to help debug and guide me on writing the function
# Asked Chatgpt hints for debugging and suggesting the general sturcture of the code




# Topic question: Is there a correlation between sex and penguin body mass?
# Description: Understand the relation of penguin part size (flipper and beak) to rest of the penguin mass and how it related to sex


import os
import csv 

def load_penguin(csv_file): 
    '''
    Reads the penguin csv file and returns it as a list of dictionaries - coverts keys that have numbered outputs into integers utilizing float to account for decimals
    Input: csv_file(string)
    Output: penguins(list of dictionaries)
    '''
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, csv_file)

    penguins = [] 
    numbered_keys = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']

    #opens the file and turns columns that are numbers into integers
    with open(full_path, newline='') as csv_file: 
        reader = csv.DictReader(csv_file)
        for row in reader: 
            for key in numbered_keys: 
                value = row.get(key, '')
                if value.strip() != '': 
                    try: 
                        row[key] = int(float(value))
                    except ValueError: 
                        row[key] = None
                else: 
                    row[key] = None
            penguins.append(row)
    return penguins


def calculate_average_body_mass_species(penguins): 
    '''
    Grouping the body masses by species and island and finding the averages of each (island, species)
    Input: csv_file(string)
    Output: avg_body_mass_dict(dictionary)
    '''
    
    data = {}
    for row in penguins: 
        island = row['island']
        species = row['species']
        body_mass = row['body_mass_g']
        
        if body_mass is None: 
            continue 
        if island not in data: 
            data[island] = {}
        if species not in data[island]: 
            data[island][species] = [] 

        data[island][species].append(body_mass)

    avg_body_mass_dict = {}
    highest_avg_mass = 0
    heaviest_species_island = None
    for island, species_dict in data.items(): 
        for species, masses in species_dict.items(): 
            avg_mass = sum(masses) / len(masses)
            avg_body_mass_dict[(island, species)] = avg_mass #calculation 1 - calculating the average mass for each species 

            if avg_mass > highest_avg_mass:
                highest_avg_mass = avg_mass #calculation 2 - calculating the highest average mass with associated species 
                heaviest_species_island = (island, species) 
    print(f"The average mass for (island, species) is: {avg_body_mass_dict}")
    print(f"The species with the highest average mass is: {heaviest_species_island} with a mass of {highest_avg_mass:.2f}g") 
    return avg_body_mass_dict, heaviest_species_island, highest_avg_mass

    


def calculate_body_flipper_to_mass_ratio(penguins, avg_body_mass_dict):
    '''
    Calculates the flipper-to-average-mass ratio for each penguin (using the above function avg mass) and then using that output, find the sex with the highest flipper-to-average-mass ratio
    Input: penguins (list of dicts) and avg_body_mass_dict (dictionary)
    Output: penguins_with_ratio and sex_highest_ratio
    '''
    penguins_with_ratio = []

    for penguin in penguins:
        island = penguin["island"]
        species = penguin["species"]

        if (island, species) not in avg_body_mass_dict:
            continue

        avg_mass = avg_body_mass_dict[(island, species)]

        if penguin["flipper_length_mm"] is not None:
            flipper_length = penguin["flipper_length_mm"]
            ratio = flipper_length / avg_mass
            penguin["ratio"] = ratio
            penguins_with_ratio.append(penguin)


    results_dict = {}
    for (island, species) in avg_body_mass_dict.keys():
        male_ratios = []
        female_ratios = []

        for penguin in penguins_with_ratio:
            if penguin["species"] == species and "sex" in penguin:
                if penguin["sex"] == "male":
                    male_ratios.append(penguin["ratio"])
                elif penguin["sex"] == "female":
                    female_ratios.append(penguin["ratio"])

        if len(male_ratios) > 0:
            male_avg = sum(male_ratios) / len(male_ratios)
        else:
            male_avg = None
        if len(female_ratios) > 0:
            female_avg = sum(female_ratios) / len(female_ratios)
        else:
            female_avg = None
        if male_avg is not None and female_avg is not None:
            if male_avg > female_avg:
                results_dict[species] = "male"
            else:
                results_dict[species] = "female"
        elif male_avg is not None:
            results_dict[species] = "male"
        elif female_avg is not None:
            results_dict[species] = "female"
        else:
            results_dict[species] = "unknown"  
            
        print(f"Sex with highest flipper-to-mass ratio: {results_dict[species]}")

    print("\nFinal results (species: sex):", results_dict)

    return results_dict


def analyze_bill_ratio_mass_relation(penguins, avg_body_mass_dict, sex_highest_ratio): 
    '''
    Analyzes how the average bill-length-depth-mass ratio relates to average body mass across species, island, and sex and compares that to see if its the same sex as highest_ratio (found in calculate_body_ratio)
    Input: penguins (list of dicts), avg_body_mass_dict (dictionary), sex_highest_ratio
    Output: bill_mass_relation (dictionary), sex_match (boolean)
    '''
    
    # Create an empty dictionary to hold grouped data.
    # The key will be (island, species, sex)
    # The value will be a list of all the bill ratios (bill_length / bill_depth)
    grouped_data = {}

    # Loop through every penguin in the list
    for row in penguins:
        island = row['island']
        species = row['species']
        sex = row['sex']
        bill_length = row['bill_length_mm']
        bill_depth = row['bill_depth_mm']
    
    # Skip this penguin if any of the important values are missing
        # (we can't divide by None or zero)
        if None in (island, species, sex, bill_length, bill_depth):
            continue
    # CALCULATION 1, finding average bill ratio
    # Calculate the bill ratio (length ÷ depth)
        bill_ratio = bill_length / bill_depth

    # Create a unique key for this (island, species, sex) group
        key = (island, species, sex)

        # Add the bill ratio to the right group in the dictionary
        if key not in grouped_data:
            grouped_data[key] = []  # if key not there yet, make a new empty list
        grouped_data[key].append(bill_ratio)

    # Create a second dictionary to store the average ratio per group
    bill_mass_relation = {}

    # Loop through each (island, species, sex) key and average its ratios
    for key, ratios in grouped_data.items():
        avg_ratio = sum(ratios) / len(ratios)
        bill_mass_relation[key] = avg_ratio


    # CALCULATION 2, now we’ll compare the bill ratios to the average body mass
    # and see if the sex with the highest flipper ratio matches the one with the highest bill ratio.

    # Create a new dictionary to store average bill ratios by species and sex.
    species_bill_ratio = {}

    # Go through each (island, species, sex) entry in our bill ratio data.
    for (island, species, sex), ratio in bill_mass_relation.items():
        # Skip this penguin if sex is missing or invalid
        if not sex or sex.lower() not in ['male', 'female']:
            continue
        # If this species isn’t in our dictionary yet, create it with male/female lists.
        if (island, species) not in species_bill_ratio:
            species_bill_ratio[species] = {'male': [], 'female': []}

        # Add the ratio value to the correct list (male or female).
        species_bill_ratio[species][sex.lower()].append(ratio)

    # Make another dictionary to store which sex has the higher average bill ratio.
    sex_with_highest_bill_ratio = {}

    # Go through each species to find who has the higher average ratio (male or female).
    for species, sex_data in species_bill_ratio.items():
        male_ratios = sex_data['male']
        female_ratios = sex_data['female']

        # Calculate the average for males and females (if data exists).
        male_avg = sum(male_ratios) / len(male_ratios) if len(male_ratios) > 0 else None
        female_avg = sum(female_ratios) / len(female_ratios) if len(female_ratios) > 0 else None

        # Compare them to find which sex has the higher average bill ratio.
        if male_avg is not None and female_avg is not None:
            # If both have data, pick whichever average is higher.
            if male_avg > female_avg:
                sex_with_highest_bill_ratio[species] = "male"
            else:
                sex_with_highest_bill_ratio[species] = "female"
        elif male_avg is not None:
            # If only male data exists, default to male.
            sex_with_highest_bill_ratio[species] = "male"
        elif female_avg is not None:
            # If only female data exists, default to female.
            sex_with_highest_bill_ratio[species] = "female"
        else:
            # If no data for either sex, mark as unknown.
            sex_with_highest_bill_ratio[species] = "unknown"

    # Now we compare this to the flipper ratio data (sex_highest_ratio).
    # We’ll count how many species have the same result for both bill ratio and flipper ratio.
    matches = 0
    total_species = 0

    for species, bill_sex in sex_with_highest_bill_ratio.items():
        if species in sex_highest_ratio:
            total_species += 1
            if bill_sex == sex_highest_ratio[species]:
                # If the sex matches for this species, add to match count.
                matches += 1

    # If every species matches, or at least one does, mark True.
    # If none match, mark False.
    sex_match = matches > 0 and matches == total_species

    # Print everything so you can see the results clearly.
    print("\n--- Bill Ratio vs Body Mass Relation ---")
    for species, sex in sex_with_highest_bill_ratio.items():
        print(f"{species}: Sex with higher average bill ratio = {sex}")
    print(f"\nDo the highest bill ratio sexes match the flipper ratio sexes? {sex_match}")

    # Return both results so they can be used later or written to a file.
    return bill_mass_relation, sex_match

