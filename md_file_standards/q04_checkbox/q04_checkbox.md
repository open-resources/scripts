---
title: Vectors and Scalars
type: checkbox
author: Firas Moosvi
source: original
tags:
- kinematics
- test
outcomes:
- LO.kinematics.2305
- LO.kinematics.2304
assets:
server: |
    import random
    import pandas as pd

    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()

    # store phrases etc
    data["vars"]["name"] = random.choice(names)
    data["vars"]["title"] = "Vectors and Scalars"

    # define useful variables/lists
    vectors = ["displacement", "velocity", "acceleration", "momentum", "force", "lift", "drag", "thurst", "weight"]
    scalars = ["length", "area", "volume", "mass", "density", "pressure", "temperature", "energy", "entropy", "work", "power"]

    # Randomly select 2,3,4 scalars and shuffle the lists
    total_choices = 6
    num_scalars = random.choice([2,3,4])
    num_vectors = total_choices - num_scalars
    select = random.choice(["vectors","scalars"])

    # Create ans_choices
    ans_choices = ["ans{0}".format(i+1) for i in range(total_choices)]

    random.shuffle(scalars)
    random.shuffle(vectors)

    # define possible answers
    if select == "vectors":
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data["params"]["part1"][choice] = vectors.pop()
            data["correct_answer"]["part1"].append(choice)
            
        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data["params"]["part1"][choice] = scalars.pop()
            
    elif select == "scalars":
        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data["params"]["part1"][choice] = vectors.pop()
            data["correct_answer"]["part1"].append(choice)
            
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data["params"]["part1"][choice] = vectors.pop()
part1:
 type: checkbox
 pl-customizations:
   allow-blank: true
   partial-credit: true
   partial-credit-method: EDC
---
# {{ vars.title }}

## Question Text

{{ vars.name }} is given a list of physical quantities and has to identify all of the {{ params.select }}. Can you help?

## Answer Section

Select all the choices that apply.

Note: You will be awarded full marks only if you select all the correct choices, and none of the incorrect choices. Choosing incorrect choices as well as not choosing correct choices will result in deductions.

- {{ params.ans1}} 
- {{ params.ans2}} 
- {{ params.ans3}} 
- {{ params.ans4}} 
- {{ params.ans5}} 
- {{ params.ans6}}