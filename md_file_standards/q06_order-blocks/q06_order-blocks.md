---
title: Match quantity to units
type: matching
author: Firas Moosvi
source: original
tags:
- units
- test
outcomes:
- LO.units.2301
- LO.units.2302
assets:
server: |
    import random
    import pandas as pd

    # define the data dictionary
    data = {"params":{},
            "vars":{}}
    
    # define or load names/items/objects
    names = pd.read_csv("data/names.csv")["Names"].tolist()

    # store phrases etc
    data["vars"]["name"] = random.choice(names)

    # define correct pairs
    data["params"]["Velocity"] = "Metres per second, North"
    data["params"]["Displacement"] = "Metres, North"
    data["params"]["Speed"] = "Metres per second"
    data["params"]["Distance"] = "Metres"
    data["params"]["Time"] = "Seconds"
    data["params"]["Distractors"] = ["Volts", "Watts", "Joules", "Cubic Metres", "Kilograms"]
---
# {{ vars.title }}

## Question Text

{{ vars.name }} is trying to create a table where the left side is the physical quantity, and the right side is its corresponding unit.

## Answer Section

Help {{ vars.name }} match the unit of measurement to the quantity?