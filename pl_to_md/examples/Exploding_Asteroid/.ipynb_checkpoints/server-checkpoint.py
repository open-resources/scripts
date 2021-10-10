import random
import pandas as pd
import problem_bank_helpers as pbh
from collections import defaultdict
nested_dict = lambda: defaultdict(nested_dict)

def generate(data):
    # Start problem code
    
    data2 = nested_dict()
    
    # define or load names/items/objects
    names = pd.read_csv(data["options"]["client_files_course_path"]+"/data/names.csv")["Names"].tolist()
    
    # store phrases etc
    data2["params"]["vars"]["title"] = 'Exploding Asteroid'
    data2["params"]["vars"]["name"] = random.choice(names)
    data2["params"]["vars"]["name2"] = random.choice(names)
    
    # define useful variables/lists
    
    # create list of answers and shuffle
    answers = [
    "The momentum vectors they use to describe each of the two asteroid pieces will be the same.", 
    "The total momentum vectors they use to describe the asteroid system (both pieces) will be the same.", 
    "The CHANGE in the momentum vector they determine for each piece of the asteroid before and after the explosion will be the same.", 
    "The FORCE vector they determine that each piece of the asteroid felt during the explosion will be the same.", 
    "The final velocity vectors they use to describe the two asteroid pieces will be the same.", 
    "The final speeds they measure for the two asteroid pieces will be the same.", 
    "They will both agree on how much kinetic energy each of the asteroid pieces has.", 
    "They will both agree on how the kinetic energy of each of the pieces has changed.", 
    "They will both agree on how the TOTAL kinetic energy of the system has changed.", 
    "They will both agree on how the internal energy of the system has changed."
    ]
    
    correct_answers = [
        "The momentum vectors they use to describe each of the two asteroid pieces will be the same.", 
        "The total momentum vectors they use to describe the asteroid system (both pieces) will be the same.",
        "The final velocity vectors they use to describe the two asteroid pieces will be the same.",
        "The final speeds they measure for the two asteroid pieces will be the same.", 
        "They will both agree on how much kinetic energy each of the asteroid pieces has.", 
    ]
    
    random.shuffle(answers)
    
    # Create ans_choices
    num_choices = 6
    
    for i,this_answer in enumerate(random.sample(answers,num_choices)):
        
        choice = f"ans{i+1}"
        
        data2["params"]["part1"][choice]["value"] = this_answer
    
        if this_answer in correct_answers:
            data2["params"]["part1"][choice]["correct"] = False
        else:
            data2["params"]["part1"][choice]["correct"] = True
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass    
    
