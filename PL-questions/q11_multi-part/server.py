import random
import pandas as pd
from collections import defaultdict
nested_dict = lambda: defaultdict(nested_dict)

def generate(data):
    
    data2 = nested_dict()
    
    # define or load names/items/objects
    names = pd.read_csv(data["options"]["client_files_course_path"]+"/data/names.csv")["Names"].tolist()
    manual_vehicles = pd.read_csv(data["options"]["client_files_course_path"]+"/data/manual_vehicles.csv")["Manual Vehicles"].tolist()
    
    # store phrases etc
    data2["params"]["vars"]["name"] = random.choice(names)
    data2["params"]["vars"]["vehicle"] = random.choice(manual_vehicles)
    data2["params"]["vars"]["title"] = "Distance travelled"
    data2["params"]["vars"]["units"] = "m/s"
    
    # define bounds of the variables
    v = random.randint(2,7)
    t = random.randint(5,10)
    
    # store the variables in the dictionary "params"
    data2["params"]["v"] = v
    data2["params"]["t"] = t
    
    ## Part 1
    
    # define correct answers
    data2["correct_answers"]["part1_ans"] = v*t
    
    ## Part 2
    
    # define possible answers
    data2["params"]["part2"]["ans1"]["value"] = 42
    data2["params"]["part2"]["ans1"]["correct"] = False
    
    data2["params"]["part2"]["ans2"]["value"] = v*t
    data2["params"]["part2"]["ans2"]["correct"] = True
    
    data2["params"]["part2"]["ans3"]["value"] = v+t
    data2["params"]["part2"]["ans3"]["correct"] = False
    
    data2["params"]["part2"]["ans4"]["value"] = v/t
    data2["params"]["part2"]["ans4"]["correct"] = False
    
    data2["params"]["part2"]["ans5"]["value"] = v-t
    data2["params"]["part2"]["ans5"]["correct"] = False
    
    data2["params"]["part2"]["ans6"]["value"] = 1.3*(v-t)
    data2["params"]["part2"]["ans6"]["correct"] = False
    
    # Update the data object with a new dict
    data.update(data2)
    