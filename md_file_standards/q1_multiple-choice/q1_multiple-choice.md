---
title: Distance travelled
type: multiple-choice
author: Firas Moosvi
template_version: 0.1
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

    # define the data dictionary
    data = {"params":{},
            "vars":{}}
    
    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()
    manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()

    # store phrases etc
    data["vars"]["name"] = random.choice(names)
    data["vars"]["vehicle"] = random.choice(manual_vehicles)
    data["vars"]["title"] = "Distance travelled"
    data["vars"]["units"] = "m/s"
    data["vars"]["digits_after_decimal"] = 2

    # define bounds of the variables
    v = random.randint(2,7)
    t = random.randint(5,10)

    # store the variables in the dictionary "params"
    data["params"]["v"] = v
    data["params"]["t"] = t

    # define possible answers
    data["params"]["ans1"] = v*t
    data["params"]["ans2"] = v+t
    data["params"]["ans3"] = v/t
    data["params"]["ans4"] = v-t
    data["params"]["ans5"] = 1.3*(v-t)
    data["params"]["correct_answer"] = "ans1"
---
# {{ vars.title }}

## Question Text

{{ vars.name }} is traveling on {{ vars.vehicle }} at {{ params.v }} {{ vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

## Part A

Here is any instructions specific for this part

### Answer Section

- {{ params.ans1}} {{ vars.units}} 
- {{ params.ans2}} {{ vars.units}} 
- {{ params.ans3}} {{ vars.units}} 
- {{ params.ans4}} {{ vars.units}} 
- {{ params.ans5}} {{ vars.units}} 

## Part B

More instructions

### Answer Section

- {{ params.ans1}} {{ vars.units}} 
- {{ params.ans2}} {{ vars.units}} 
- {{ params.ans3}} {{ vars.units}} 
- {{ params.ans4}} {{ vars.units}} 
- {{ params.ans5}} {{ vars.units}} 

