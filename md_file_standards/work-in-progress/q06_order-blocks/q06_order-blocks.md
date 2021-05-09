---
title: Match quantity to units
author: Firas Moosvi
source: original
template_version: 0.2
outcomes:
- LO.units.2301
- LO.units.2302
tags:
- units
- test
assets:
server: |
    import random
    import pandas as pd
    
    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()

    # store phrases etc
    data["vars"]["name"] = random.choice(names)

    # Distractors
    distractors = ["Volts", "Watts", "Joules", "Cubic Metres", "Kilograms"]
    random.shuffle(distractors)

    # define correct pairs
    data["params"]["part1"]["Velocity"] = "Metres per second, North"
    data["params"]["part1"]["Displacement"] = "Metres, North"
    data["params"]["part1"]["Speed"] = "Metres per second"
    data["params"]["part1"]["Distance"] = "Metres"
    data["params"]["part1"]["Time"] = "Seconds"
    data["params"]["part1"]["Distractors"] = distractors
part1:
  type: matching
  pl-options:
    allow-blank: true
---
# {{ vars.title }}

## Question Text

{{ vars.name }} is trying to create a table where the left side is the physical quantity, and the right side is its corresponding unit.

## Answer Section

Help {{ vars.name }} match the unit of measurement to the quantity?

| Quantity | Unit |
| -------- | ---- |
| {{ params.part1.Velocity }} | |
| {{ params.part1.Displacement }} | |
| {{ params.part1.Speed }} | |
| {{ params.part1.Distance }} | |
| {{ params.part1.Time }} | |
| {{ params.part1. }} | |
