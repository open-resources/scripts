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

    # define correct answers
    data["correct_answers"]["part1"] = v*t
part1:
 type: number-input
 correct_answers: part1
 pl-options:
   allow-blank: true
   label: d
   suffix: m
   comparison: sigfig
   digits: 2
---
# {{ vars.title }}

## Question Text

{{ vars.name }} is traveling on {{ vars.vehicle }} at {{ params.v }} {{ vars.units }}.
How far does {{ vars.name }} travel in {{ params.t }} seconds, assuming they continue at the same velocity?

### Answer Section

Please enter in a numeric value in {{ vars.units }} to {{ vars.digits_after_decimal }} decimal places.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
