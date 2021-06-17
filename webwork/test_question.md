---
title: Kinematics - Falling Objects
author: Urone et. al
date: March 2018
editor: Wynne Reichheld, 22 June 2018
source: https://github.com/openwebwork/webwork-open-problem-library
type: ''
tags:
- gravity
- acceleration
- velocity
- distance
outcomes:
- TBD
assets:
- TBD
---
# {{ vars.title }}

## Question Text

Problem Text TBD
from random import randrange
d = randrange(50,100,0.1)

A1 = 4.9
A2 = sqrt((2)*(9.8)*(d))
A3 = (d)-(1/2)*(9.8)*(((sqrt((2)*(d)/(9.8)))-1)**(2))