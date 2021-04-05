---
title: 8.kappa
author: edX Physics 100 Team
source: https://github.com/open-resources/edx_bank
type: mc
tags:
- TBD
outcomes:
- TBD
assets:
- TBD
server: |
  import random

  # define or load names/items/objects

  # store phrases etc

  # define bounds of the variables

  ga = 9.8
  gb = 0.1*random.randint(40, 80)
  a = 1.5
  sol = ga+a-gb
  c2 = ga+a+gb
  c3 = ga+a
  c4 = ga-gb

  # store the variables in the dictionary params

  # define possible answers

  data['params']['ans1'] = sol
  data['params']['correct_answer'] = sol
  data['params']['ans2'] = c2
  data['params']['ans3'] = c3
  data['params']['ans4'] = c4
---
# {{ vars.title }}

## Question Text

8) During an inter-planetary experiment, a bathroom scale is placed on two elevators located in two different planets. Planet A (Earth) has a constant of gravity g_A = {{ga m/s^2 and planet B has a constant of gravity g_B = {{gb m/s^2. During the experiment, the elevator on Earth starts from rest and is accelerated upwards at a rate of $a m/s^2. If the scale reading for an astronaut during her way up in the elevator is the same in both planets, what is the magnitude of the elevator's acceleration (in m/s^2) on planet B? Note: the elevator on planet B is also accelerating upwards. 

## Answer Section

- {{ sol }}
- {{ c2 }}
- {{ c3 }}
- {{ c4 }}
