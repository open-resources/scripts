---
title: Displacement of a Vehicle
topic: Kinematics(1D)
author: Jake Bobowski
source: 2012 Midterm 1 Q1 Section 002
template_version: 1.1
attribution: standard
outcomes:
- 4.1.1.0
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- PW
assets:
server: 
    imports: |
        import random as rd
        import pandas as pd
        import math
        import problem_bank_helpers as pbh
        import pathlib as pth
        import yaml
    generate: |
        # function for calculating the values based on the direction
        # the direction pairs north-south and east-west are stored in a list as [NS,EW]
        # c is the number of blocks moved in the direction passed to the function
        # north and east are considered positive (cartesian plane)
        def calcDir(direction, c, dirlist):
            if direction == 'north':
                dirlist[0] = dirlist[0] + c
            elif direction == 'south':
                dirlist[0] = dirlist[0] - c
            elif direction == 'east':
                dirlist[1] = dirlist[1] + c
            else: # west
                dirlist[1] = dirlist[1] - c

        data2 = pbh.create_data2()

        # define or load names/items/objects
        vehicles = pd.read_csv("data/vehicles.csv")["Vehicles"].tolist()

        # store phrases etc
        data2["params"]["vars"]["vehicle"] = rd.choice(vehicles)
        data2["params"]["vars"]["title"] = "Displacement of a Vehicle"
        data2["params"]["vars"]["units"] = "blocks"

        # define bounds of the variables
        c1 = rd.randint(2,100)
        c2 = rd.randint(2,100)
        c3 = rd.randint(2,100)

        # generate directions
        # some restrictions need to be applied:
        # two consecutive directions cannot be generated (it would not make sense)
        directions = ['north', 'south', 'east', 'west']

        dir1 = rd.choice(directions)

        directions2 = directions.copy()
        directions2.remove(dir1)
        dir2 = rd.choice(directions2)

        directions3 = directions.copy()
        directions3.remove(dir2)
        dir3 = rd.choice(directions3)

        # store the variables in the dictionary "params"
        data2["params"]["c1"] = c1
        data2["params"]["c2"] = c2
        data2["params"]["c3"] = c3
        data2["params"]["dir1"] = dir1
        data2["params"]["dir2"] = dir2
        data2["params"]["dir3"] = dir3


        # consider the pairs: (north-south) and (east-west) stored in a list as [NS, EW]
        # both values are initialised to 0
        # call the function to calculate values in the x-y direction
        dirlist = [0,0]

        calcDir(dir1, c1, dirlist)
        calcDir(dir2, c2, dirlist)
        calcDir(dir3, c3, dirlist)

        # caculate the magnitude
        mag = math.sqrt(dirlist[0]**2 + dirlist[1]**2)

        # define correct answers
        data2["correct_answers"]["part1_ans"] = mag
        
        # Update the data object with a new dict
        data.update(data2)
    prepare: |
        pass
    parse: |
        pass
    grade: |
        pass
part1:
  type: number-input
  pl-customizations:
    weight: 1
    allow-blank: true
    label: $\Delta r = $
    suffix: blocks
    comparison: sigfig
    digits: 2
---
# {{ params.vars.title }}

A {{ params.vars.vehicle }} moves {{ params.c1}} blocks due {{ params.dir1}}, {{ params.c2 }} blocks due {{ params.dir2}}, and another {{ params.c3 }} blocks due {{ params.dir3}}. 

## Question Text

Assume all blocks are of equal size. What is the magnitude of the {{ params.vars.vehicle }}'s displacement, start to finish?

### Answer Section

Please enter in a numeric value in {{ params.vars.units }}.

## pl-submission-panel

## pl-answer-panel

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
