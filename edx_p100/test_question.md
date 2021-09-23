---
title: 7.sigma
topic: undefined
author: edX Physics 100 Team
source: https://github.com/open-resources/edx_bank
attribution: standard
outcomes: undefined
difficulty: Average
randomization: undefined
tags: undefined
assets: undefined
server:
  imports: |-
    import random
    import problem_bank_helpers as pbh
  generate: |-
    data2 = pbh.create_data2()


    # store phrases etc


    a = 35
    r = 0.1*random.randint(5, 15)
    tin = random.randint(18, 22)
    tout = 5
    nperson = 2
    pperson = 80
    sola = round(a*(tin-tout)/r-nperson*pperson, 2)
    pheater = 500
    eff = 0.5
    hours = random.randint(5, 9)
    days = 5*random.randint(10, 14)
    cost = 0.12
    solb = round(pheater*hours*days*3600/eff/3.6e6*cost, 2)

    # store the variables in the dictionary params


    # Update the data object with a new dict
    data.update(data2)
  prepare: pass
  parse: pass
  grade: pass
part1:
  type: numeric
  pl-customizations:
    weight: 1
---
# {{ vars.title }}

## Question Text

7a) Consider a room in a house that has composite walls with an R_{tot} = {{ r\text{ }} m}^2\text{K/W}.
The total cross sectional area of the walls is {{ a }} m^2.
During winter, the temperature outside the room is T_{out} = {{ tout^\circ\text{C}. }}
Calculate the power (in W) of a heater that is required to keep the room's temperature constant at {{ tin^oC }} if the room is going to be occupied by {{ nperson }} people.
Assume that the radiative power emitted by a person is {{ pperson }} W.


## Answer Section

The answer is: {{ sola }}.The answer is: {{ sola }}.

## pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.

## pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.Recall the concept of efficiency: If the heater was 100% efficient all of the energy consumed by the heater would go into heating the room. 