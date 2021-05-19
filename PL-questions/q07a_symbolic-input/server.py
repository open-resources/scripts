import random    
import prairielearn as pl
import sympy
from collections import defaultdict
nested_dict = lambda: defaultdict(nested_dict)

def generate(data):
    
    data2 = nested_dict()
    
    # Declare math symbols to be used by sympy
    m, v, r = sympy.symbols('m v r')
    
    # Describe the solution equation
    F = m*v**2/r
    
    # Answer to fill in the blank input stored as JSON.
    data2['correct_answers']['part1_ans'] = pl.to_json(F)
    
    # Update the data object with a new dict
    data.update(data2)    
    