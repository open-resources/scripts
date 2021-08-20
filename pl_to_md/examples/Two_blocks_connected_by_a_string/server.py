import random as rd
import problem_bank_helpers as pbh
from collections import defaultdict
nested_dict = lambda: defaultdict(nested_dict)

def generate(data):
    # Start problem code
    
    data2 = nested_dict()
    
    # store phrases etc
    data2["params"]["vars"]["title"] = 'Two Blocks Connected by a String'
    data2["params"]["vars"]["units"] = "N"
    
    # Define variables in case the image is randomized in the future.
    m1 = 1
    m2 = 1.2
    g = 9.81
    
    # store the variables in the dictionary "params".  
    data2["params"]["m1"] = m1
    
    # define possible answers
    # round in traditional way using pbh.roundp() and then convert to int
    data2["params"]["part1"]["ans1"]["value"] = int(pbh.roundp(m1*g, decimals = 0))     
    data2["params"]["part1"]["ans1"]["correct"] = False
    
    data2["params"]["part1"]["ans2"]["value"] = int(pbh.roundp(m2*g, decimals = 0))
    data2["params"]["part1"]["ans2"]["correct"] = True
    
    data2["params"]["part1"]["ans3"]["value"] = int(pbh.roundp(2*m2*g, decimals = 0))
    data2["params"]["part1"]["ans3"]["correct"] = False
    
    data2["params"]["part1"]["ans4"]["value"] = int(pbh.roundp(2*m1*g, decimals = 0))
    data2["params"]["part1"]["ans4"]["correct"] = False
    
    data2["params"]["part1"]["ans5"]["value"] = int(pbh.roundp(m2*g, decimals = 0)) + 1
    data2["params"]["part1"]["ans5"]["correct"] = False
    
    data2["params"]["part1"]["ans6"]["value"] = int(pbh.roundp(m2*g, decimals = 0)) - 1
    data2["params"]["part1"]["ans6"]["correct"] = False
    
    # Update the data object with a new dict
    data.update(data2)
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
