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
  from sympy import *

  #Note. One may be tempted to "import sympy" instead of "from sympy import *". This will work with simple multiplication/division, addition, and subtraction however this makes the sin and cos require sympy.sin and sympy.cos, which is messy. 
  #Of course, if you are using "from numpy import *" as well, this will may cause errors, so use caution.
    
  # define or load names/items/objects
  names = pd.read_csv("data/names.csv")["Names"].tolist()
  manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()

  # store phrases etc
  data["vars"]["name"] = random.choice(names)
  data["vars"]["vehicle"] = random.choice(manual_vehicles)
  data["vars"]["title"] = "Centripetal Force"

  # Declare math symbols to be used by sympy
  mu_s, g , theta = symbols('mu_s g theta')

  # Describe the solution equation
  amax = g*(mu_s*cos(theta) - sin(theta))
  
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

A wood crate sits in the back of a truck. The coefficients of static and kinetic friction between the crate and the truck are $\mu_s$ and $\mu_k$ respectively. The truck starts moving up a slope with angle $\theta$. What is the maximum acceleration the truck can have without the crate slipping out the back, in terms of $\mu_s$, $\mu_k$, $g$, and $\theta$? Not all variables need to be used. 
Note: for $\mu_s$, enter "mu_s", for $\mu_k$, enter "mu_k", for $g$, enter "g", and for $\theta$, enter "theta".

## Answer Section
F_r =

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
