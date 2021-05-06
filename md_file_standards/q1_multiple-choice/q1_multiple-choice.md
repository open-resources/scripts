---
title: Distance travelled
topic: Kinematics
author: Firas Moosvi
template_version: 0.1
source: original
pl-options:
  allow-blank: true
tags:
- Firas Moosvi
- test
- 2305
- 2304
assets:
server: |
    import random
    import pandas as pd

    # define or load names/items/objects from server files
    names = pd.read_csv("/serverFilesCourse/names.csv")["Names"].tolist()
    manual_vehicles = pd.read_csv("./serverFilesQuestion/manual_vehicles.csv")["Manual Vehicles"].tolist()

    # store phrases etc
    data["vars"]["name"] = random.choice(names)
    data["vars"]["vehicle"] = random.choice(manual_vehicles)
    data["vars"]["units"] = "m/s"
    data["vars"]["digits_after_decimal"] = 2

    # define bounds of the variables
    v = random.randint(2,7)
    t = random.randint(5,10)

    # store the variables in the dictionary "params"
    data["params"]["v"] = v
    data["params"]["t"] = t

    # define possible answers
    data["answers"]["ans1a"] = 4
    
    data["answers"]["ans1"] = v*t
    data["answers"]["ans2"] = v+t
    data["answers"]["ans3"] = v/t
    data["answers"]["ans4"] = v-t
    data["answers"]["ans5"] = 1.3*(v-t)

part2:
  type: multiple-choice  
  choices: ans1, ans2, ans3, ans4  
  answer: ans1  
  units: m/s
...

<!-- Titlte -->

## Part 1
  question text
---
### Answer Section
part1:
  type: numeric  
  answer: ans1a  
  units: m
<!-- multiple choice -->
... 
## Part 2

<!-- numeric -->
What is 2m + 2m?
### Answer Choice

This will get removed in Graham's script (if this is a numeric input)



## Multiple-choice follow-up

{{vars.name}} is traveling on {{vars.vehicle}} at {{params.v}} {{vars.units}}.
How far does {{vars.name}} travel in {{params.t}} seconds, assuming they continue at the same velocity?





