---
title: Distance travelled
topic: Kinematics
author: Firas Moosvi
template_version: 0.2
source: original

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
    data["correct_answers"]["ans1a"] = 4
    data["correct_answers"]["ans1"] = v*t
    data["correct_answers"]["ans2"] = v+t
    data["correct_answers"]["ans3"] = v/t
    data["correct_answers"]["ans4"] = v-t
    data["correct_answers"]["ans5"] = 1.3*(v-t)
    
 # Part 1
    data["part1"]["title"]  = "Friction"
    
part1:
 type: multiple-choice  
 choices: ans1, ans2, ans3, ans4  
 answer: ans1  
 units: m/s
 pl-options:
   allow-blank: true
part2:
  pl-options:
  allow-blank: true
  type: multiple-choice  
  choices: ans1, ans2, ans3, ans4  
  answer: ans1a  
  units: m/s
---

<!-- Titlte -->

## Friction

a friction question








