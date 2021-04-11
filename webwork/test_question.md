---
title: Kinematics - Time, Velocity, and Speed
author: Urone et. al
date: January 2018
editor: Wynne Reichheld, April 30, 2018
source: https://github.com/openwebwork/webwork-open-problem-library
type: ''
tags:
- speed
- velocity
- displacement
outcomes:
- TBD
assets:
- TBD
---
# {{ vars.title }}

## Question Text

Problem Text TBD
from random import randrange
d1 = randrange(12,17,0.1)
d2 = randrange(2,4,0.1)
d3 = randrange(17,25,0.1)
t1 = randrange(2,3,0.1)
t2 = randrange(1,2,0.1)
t3 = randrange(5,6,0.1)

A1 = (d1)/(t1)
A2 = -(d2)/(t2)
A3 = (d3)/(t3)

A4 = (d1-d2+d3)/(t1+t2+t3)