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

    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()
    manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()

    # store phrases etc
    data["params"]["vars"]["name"] = random.choice(names)
    data["params"]["vars"]["vehicle"] = random.choice(manual_vehicles)
    data["params"]["vars"]["title"] = "Distance travelled"
    data["params"]["vars"]["units"] = "m/s"
    data["params"]["vars"]["digits_after_decimal"] = 0

    # define bounds of the variables
    n = random.randint(2,100)

    # store the variables in the dictionary "params"
    data["params"]["n"] = n

    # define correct answers
    data["correct_answers"]["part1"] = int(n*10)
part1:
 type: number-input
 label: d
 pl-options:
   allow-blank: true
---
# {{ vars.title }}

## Question Text

{{ vars.name }} is on a {{ params.vars.vehicle }} trying to calculate the result of 10 x {{ params.n }} {{ params.vars.units }}.

## Answer Section

Please enter an integer value in {{ params.vars.units }}.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.