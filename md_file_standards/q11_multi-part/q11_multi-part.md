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
 units: m/s
 label: d
 pl-options:
   allow-blank: true
part2:
 type: multiple-choice  
 units: m/s
 pl-options:
   allow-blank: true
---
# {{ vars.title }}

## Part 1

{{ vars.name }} is traveling on {{ vars.vehicle }} at {{ params.v }} {{ vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ vars.units }} to {{ vars.digits_after_decimal }} decimal places.

## Part 2

{{ vars.name }} is traveling on {{ vars.vehicle }} at {{ params.v }} {{ vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

- {{ params.part2.ans1}} {{ vars.units}} 
- {{ params.part2.ans2}} {{ vars.units}} 
- {{ params.part2.ans3}} {{ vars.units}} 
- {{ params.part2.ans4}} {{ vars.units}} 
- {{ params.part2.ans5}} {{ vars.units}} 
- {{ params.part2.ans6}} {{ vars.units}} 

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.