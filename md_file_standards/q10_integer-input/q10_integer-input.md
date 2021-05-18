---
title: Integer Math
topic: Math
author: Firas Moosvi
source: original
template_version: 0.2
outcomes:
- LO.multiplication.2305
- LO.multiplication.2304
tags:
- quiz
- homework
assets:
server: |
    import random
    import pandas as pd
    from collections import defaultdict
    nested_dict = lambda: defaultdict(nested_dict)

    # Start problem code

    data2 = nested_dict()

    # store phrases etc
    data2["params"]["vars"]["name"] = random.choice(names)
    data2["params"]["vars"]["vehicle"] = random.choice(manual_vehicles)
    data2["params"]["vars"]["title"] = "Integer Math"
    data2["params"]["vars"]["units"] = "m/s"

    # define bounds of the variables
    n = random.randint(2,100)

    # store the variables in the dictionary "params"
    data2["params"]["n"] = n

    # define correct answers
    data2["correct_answers"]["part1_ans"] = int(n*10)
    
    # Update the data object with a new dict
    data.update(data2)
part1:
  type: number-input
  label: $d=$
  pl-options:
    weight: 1
    allow-blank: true
---
# {{ params.vars.title }}

## Question Text

{{ params.vars.name }} is on a {{ params.vars.vehicle }} trying to calculate the result of 10 x {{ params.n }} {{ params.vars.units }}.

### Answer Section

Please enter an integer value in {{ params.vars.units }}.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.