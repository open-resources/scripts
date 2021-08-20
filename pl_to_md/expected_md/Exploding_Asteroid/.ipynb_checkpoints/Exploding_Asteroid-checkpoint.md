---
title: Exploding Asteroid
topic: Energy
author: Jake Bobowski
source: Final 2016 Q6
template_version: 1.0
attribution: standard
outcomes:
- 8.2.1.1
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- AK
assets:
server: 
    imports: |
        import random
        import pandas as pd
        import problem_bank_helpers as pbh
        from collections import defaultdict
        nested_dict = lambda: defaultdict(nested_dict)
    generate: |
        # Start problem code

        data2 = nested_dict()

        # define or load names/items/objects
        names = pd.read_csv("data/names.csv")["Names"].tolist()

        # store phrases etc
        data2["params"]["vars"]["title"] = 'Exploding Asteroid'
        data2["params"]["vars"]["name"] = random.choice(names)
        data2["params"]["vars"]["name2"] = random.choice(names)

        # define useful variables/lists

        # create list of answers and shuffle
        answers = [
        "The momentum vectors they use to describe each of the two asteroid pieces will be the same.", 
        "The total momentum vectors they use to describe the asteroid system (both pieces) will be the same.", 
        "The CHANGE in the momentum vector they determine for each piece of the asteroid before and after the explosion will be the same.", 
        "The FORCE vector they determine that each piece of the asteroid felt during the explosion will be the same.", 
        "The final velocity vectors they use to describe the two asteroid pieces will be the same.", 
        "The final speeds they measure for the two asteroid pieces will be the same.", 
        "They will both agree on how much kinetic energy each of the asteroid pieces has.", 
        "They will both agree on how the kinetic energy of each of the pieces has changed.", 
        "They will both agree on how the TOTAL kinetic energy of the system has changed.", 
        "They will both agree on how the internal energy of the system has changed."
        ]

        correct_answers = [
            "The momentum vectors they use to describe each of the two asteroid pieces will be the same.", 
            "The total momentum vectors they use to describe the asteroid system (both pieces) will be the same.",
            "The final velocity vectors they use to describe the two asteroid pieces will be the same.",
            "The final speeds they measure for the two asteroid pieces will be the same.", 
            "They will both agree on how much kinetic energy each of the asteroid pieces has.", 
        ]

        random.shuffle(answers)

        # Create ans_choices
        num_choices = 6

        for i,this_answer in enumerate(random.sample(answers,num_choices)):
            
            choice = f"ans{i+1}"
            
            data2["params"]["part1"][choice]["value"] = this_answer

            if this_answer in correct_answers:
                data2["params"]["part1"][choice]["correct"] = False
            else:
                data2["params"]["part1"][choice]["correct"] = True
    prepare: |
        pass
    parse: |
        pass
    grade: |
        pass    
part1:
  type: checkbox
  pl-customizations:
    weight: 1
    partial-credit: true
    partial-credit-method: EDC
---
# {{ params.vars.title }}

## Question Text

{{ params.vars.name }} and {{ params.vars.name2 }} are both standing in their space ships, each one moving with a constant (but different) velocity. They carefully watch and measure, from their two space ships, an asteroid exploding into two parts. When they compare their final numbers, which of their numbers will agree?

### Answer Section

Select all the choices that apply.

Note: You will be awarded full marks only if you select all the correct choices, and none of the incorrect choices. Choosing incorrect choices as well as not choosing correct choices will result in deductions.

- {{ params.part1.ans1.value }} 
- {{ params.part1.ans2.value }} 
- {{ params.part1.ans3.value }} 
- {{ params.part1.ans4.value }} 
- {{ params.part1.ans5.value }} 
- {{ params.part1.ans6.value }}

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
