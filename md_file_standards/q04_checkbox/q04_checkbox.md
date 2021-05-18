---
title: Vectors and Scalars
topic: Vectors
author: Firas Moosvi
source: original
template_version: 0.2
outcomes:
- LO.kinematics.2305
- LO.kinematics.2304
tags:
- kinematics
- test
assets:
server: |
    import random
    import pandas as pd
    from collections import defaultdict
    nested_dict = lambda: defaultdict(nested_dict)

    # Start problem code

    data2 = nested_dict()

    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()

    # store phrases etc
    data2["params"]["vars"]["name"] = random.choice(names)

    # define useful variables/lists
    vectors = ["displacement", "velocity", "acceleration", "momentum", "force", "lift", "drag", "thurst", "weight"]
    scalars = ["length", "area", "volume", "mass", "density", "pressure", "temperature", "energy", "entropy", "work", "power"]

    # Randomly select 2,3,4 scalars and shuffle the lists
    total_choices = 6
    num_scalars = random.choice([2,3,4])
    num_vectors = total_choices - num_scalars
    select = random.choice(["vectors","scalars"])

    data2["params"]["choice"] = select

    # Create ans_choices
    ans_choices = ["ans{0}".format(i+1) for i in range(total_choices)]

    random.shuffle(scalars)
    random.shuffle(vectors)

    # define possible answers
    if select == "vectors":
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = vectors.pop()
            data2["params"]["part1"][choice]["correct"] = True

        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = scalars.pop()
            data2["params"]["part1"][choice]["correct"] = False

    elif select == "scalars":
        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = scalars.pop()
            data2["params"]["part1"][choice]["correct"] = True
            
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = vectors.pop()
            data2["params"]["part1"][choice]["correct"] = False

    # Update the data object with a new dict
    data.update(data2)
part1:
  type: checkbox
  pl-customizations:
    weight: 1
    partial-credit: true
    partial-credit-method: EDC
---
# {{ params.vars.title }}

## Question Text

{{ params.vars.name }} is given a list of physical quantities and has to identify all of the {{ params.choice }}. Can you help?

### Answer Section

Select all the choices that apply.

Note: You will be awarded full marks only if you select all the correct choices, and none of the incorrect choices. Choosing incorrect choices as well as not choosing correct choices will result in deductions.

- {{ params.part1.ans1}} 
- {{ params.part1.ans2}} 
- {{ params.part1.ans3}} 
- {{ params.part1.ans4}} 
- {{ params.part1.ans5}} 
- {{ params.part1.ans6}}

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
