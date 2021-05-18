---
title: Centripetal Motion
topic: centripetal motion
author: Michael Kudla
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
    import prairielearn as pl
    import sympy
    from collections import defaultdict
    nested_dict = lambda: defaultdict(nested_dict)

    # Start problem code

    data2 = nested_dict()

    # Declare math symbols to be used by sympy
    m, v, r = sympy.symbols('m v r')

    # Describe the solution equation
    F = m*v**2/r
    
    # Answer to fill in the blank input stored as JSON.
    data['correct_answers']['part1'] = pl.to_json(F)
    
part1:
 type: symbolic-input
 label: $F_r = $
 pl-customizations:
   allow-blank: false
---
# {{ vars.title }}

## Question Text

Write the centripetal force $F_r$ in terms of the mass $m$, velocity $v$, and radius $r$.

## Answer Section

{{ substitutions.part1.label }}

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
