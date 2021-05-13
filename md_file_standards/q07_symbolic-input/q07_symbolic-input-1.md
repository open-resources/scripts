---
title: Symbolic Input
topic: example
author: MIchael Kudla
source: original
template_version: 0.1
outcomes:
tags:
- quiz
- homework
assets:
server: |
    import random    
    import prairielearn as pl
    import sympy
    
    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()
    manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()

    # store phrases etc
    data["vars"]["name"] = random.choice(names)
    data["vars"]["vehicle"] = random.choice(manual_vehicles)
    data["vars"]["title"] = "Distance travelled"
    data["vars"]["units"] = "m/s"
    data["vars"]["digits_after_decimal"] = 2

    # Declare math symbols to be used by sympy
    m, v, r = sympy.symbols('m v r')

    # define correct answers
    # Describe the solution equation
    F = m*v**2/r
    # Answer to fill in the blank input stored as JSON.
    data['correct_answers']['part1'] = pl.to_json(F)

    
part1:
 type: symbolic-input
 units: 
 variables: m,v,r
 label: 
 pl-options:
   allow-blank: true
---
# {{ vars.title }}

## Question Text

Write the centripetal force $F_r$ in terms of mass $m$, velocity $v$, and radius $r$.

## Answer Section

F_r =

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
