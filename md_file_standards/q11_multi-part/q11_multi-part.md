---
title: Distance travelled
topic: kinematics
author: Firas Moosvi
source: original
template_version: 0.2
outcomes:
- LO.kinematics.2305
- LO.kinematics.2304
tags:
- quiz
- homework
assets:
server: |
    import random
    import pandas as pd

    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()
    manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()

    # store phrases etc
    data["params"]["vars"]["name"] = random.choice(names)
    data["params"]["vars"]["vehicle"] = random.choice(manual_vehicles)
    data["params"]["vars"]["title"] = "Distance travelled"
    data["params"]["vars"]["units"] = "m/s"

    # define bounds of the variables
    v = random.randint(2,7)
    t = random.randint(5,10)

    # store the variables in the dictionary "params"
    data["params"]["v"] = v
    data["params"]["t"] = t

    # define possible answers
    data["params"]["part2"]["ans1"] = 42
    data["params"]["part2"]["ans2"] = v*t
    data["params"]["part2"]["ans3"] = v+t
    data["params"]["part2"]["ans4"] = v/t
    data["params"]["part2"]["ans5"] = v-t
    data["params"]["part2"]["ans6"] = 1.3*(v-t)

    # define correct answers
    data["correct_answers"]["part1"] = v*t
part1:
 type: number-input
 label: d
  pl-customizations:
   allow-blank: true
part2:
 type: multiple-choice  
  pl-customizations:
   allow-blank: true
---
# {{ params.vars.title }}

## Part 1

{{ vars.name }} is traveling on {{ vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ params.vars.units }}.

## Part 2

{{ params.vars.name }} is traveling on {{ vars.vehicle }} at {{ params.v }} {{ params.vars.units }}.
How far does {{ params.vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

- {{ params.part2.ans1}} {{ params.vars.units}} 
- {{ params.part2.ans2}} {{ params.vars.units}} 
- {{ params.part2.ans3}} {{ params.vars.units}} 
- {{ params.part2.ans4}} {{ params.vars.units}} 
- {{ params.part2.ans5}} {{ params.vars.units}} 
- {{ params.part2.ans6}} {{ params.vars.units}} 

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.