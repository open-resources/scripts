---
title: Symbolic Input
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
    import random    
    import prairielearn as pl
    import sympy
    
    # Declare math symbols to be used by sympy
    m, v, r = sympy.symbols('m v r')

    # Describe the solution equation
    F = m*v**2/r
    
    # Answer to fill in the blank input stored as JSON.
    data['correct_answers']['part1'] = pl.to_json(F)
    
part1:
 type: symbolic-input
 label: $F_r = $
 pl-options:
   allow-blank: false
---
# {{ vars.title }}

## Question Text

Write the centripetal force $F_r$ in terms of the mass $m$, velocity $v$, and radius $r$.

## Answer Section

F_r =

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
