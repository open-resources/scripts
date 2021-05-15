---
title: Symbolic Input 2 - Trig
topic: example
author: Michael Kudla
source: original
template_version: 0.1
outcomes:
tags:
- quiz
- homework
assets:
server: |
  import prairielearn as pl
  import sympy as sp

  # define or load names/items/objects
  names = pd.read_csv("data/names.csv")["Names"].tolist()
  vehicles = pd.read_csv("data/vehicles.csv")["Vehicles"].tolist()

  # store phrases etc
  data["params"]["vars"]["name"] = random.choice(names)
  data["params"]["vars"]["vehicle"] = random.choice(vehicles)

  # Declare math symbols to be used by sympy
  mu_s, g , theta = sp.symbols('mu_s g theta')

  # Describe the solution equation
  amax = g*(mu_s*sp.cos(theta) - sp.sin(theta))
  
  # Answer to fill in the blank input -- must be stored as JSON.
  data['correct_answers']['part1'] = pl.to_json(amax)

part1:
 type: symbolic-input
 units: 
 variables: mu_s, g , theta
 label: 
 pl-options:
   allow-blank: true
---
# {{ vars.title }}

## Question Text

{{ params.vars.name }} is driving a {{ params.vars.vehicle }} up a slope of angle $\theta$. 

There is a wooden crate in the back of the {{ params.vars.vehicle }} and the coefficients of static and kinetic friction between the crate and the {{ params.vars.vehicle }} are $\mu_s$ and $\mu_k$ respectively. 

If the {{ params.vars.vehicle }} starts moving, what is the maximum acceleration the {{ params.vars.vehicle }} can have without the crate slipping? You should provide a symbolic answer in terms of the following variables: $\mu_s$, $\mu_k$, $g$, and $\theta$.

Note that it may not be necessary to use every variable. For $\mu_s$, enter "mu_s", for $\mu_k$, enter "mu_k", for $g$, enter "g", and for $\theta$, enter "theta".

### Answer Section
F_r =

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
