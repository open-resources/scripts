---
title: Vectors and Scalars
topic: Template
author: Firas Moosvi
source: original
template_version: 1.1
attribution: standard
outcomes:
- 6.1.1.0
- 6.1.1.1
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- unknown
assets:
server: 
    imports: |
        import random;random.seed(111)
        import pandas as pd
        import problem_bank_helpers as pbh
    generate: |
        data2 = pbh.create_data2()

        # define or load names/items/objects
        names = pd.read_csv("data/names.csv")["Names"].tolist()

        # store phrases etc
        data2["params"]["vars"]["title"] = 'Vectors and Scalars'
        data2["params"]["vars"]["name"] = random.choice(names)

        # define useful variables/lists
        vectors = ["displacement", "velocity", "acceleration", "momentum", "force", "lift", "drag", "thurst", "weight"]
        scalars = ["length", "area", "volume", "mass", "density", "pressure", "temperature", "energy", "entropy", "work", "power"]

        # Randomly select 2,3,4 scalars and shuffle the lists
        total_choices = 6
        num_scalars = random.choice([2,3,4])
        num_vectors = total_choices - num_scalars
        select = random.choice(["vectors","scalars"])

        data2["params"]["choice"] = select

        # Create ans_choices
        ans_choices = ["ans{0}".format(i+1) for i in range(total_choices)]

        random.shuffle(scalars)
        random.shuffle(vectors)

        # define possible answers
        if select == "vectors":
            for i in range(num_vectors):
                choice = ans_choices.pop(0)
                data2["params"]["part1"][choice]["value"] = vectors.pop()
                data2["params"]["part1"][choice]["correct"] = True

            for i in range(num_scalars):
                choice = ans_choices.pop(0)
                data2["params"]["part1"][choice]["value"] = scalars.pop()
                data2["params"]["part1"][choice]["correct"] = False

        elif select == "scalars":
            for i in range(num_scalars):
                choice = ans_choices.pop(0)
                data2["params"]["part1"][choice]["value"] = scalars.pop()
                data2["params"]["part1"][choice]["correct"] = True
                
            for i in range(num_vectors):
                choice = ans_choices.pop(0)
                data2["params"]["part1"][choice]["value"] = vectors.pop()
                data2["params"]["part1"][choice]["correct"] = False

        # Update the data object with a new dict
        data.update(data2)
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

{{ params.vars.name }} is given a list of physical quantities and has to identify all of the {{ params.choice }}. Can you help?

### Answer Section

Select all the choices that apply.

Note: You will be awarded full marks only if you select all the correct choices, and none of the incorrect choices. Choosing incorrect choices as well as not choosing correct choices will result in deductions.

- {{ params.part1.ans1.value}} 
- {{ params.part1.ans2.value}} 
- {{ params.part1.ans3.value}} 
- {{ params.part1.ans4.value}} 
- {{ params.part1.ans5.value}} 
- {{ params.part1.ans6.value}}

## pl-submission-panel

Everything here will get inserted directly into the pl-submission-panel element at the end of the `question.html`.

## pl-answer-panel

Everything here will get inserted directly into an pl-answer-panel element at the end of the `question.html`.

## Rubric

This should be hidden from students until after the deadline.

## Solution

This should never be revealed to students.

## Comments

These are random comments associated with this question.
---
title: Vectors and Scalars
topic: Template
author: Firas Moosvi
source: original
template_version: 1.1
attribution: standard
outcomes:
- 6.1.1.0
- 6.1.1.1
difficulty:
- undefined
randomization:
- undefined
taxonomy:
- undefined
tags:
- unknown
assets: null
server:
  imports: |
    import random;random.seed(111)
    import pandas as pd
    import problem_bank_helpers as pbh
  generate: "data2 = pbh.create_data2()\n\n# define or load names/items/objects\n\
    names = pd.read_csv(\"data/names.csv\")[\"Names\"].tolist()\n\n# store phrases\
    \ etc\ndata2[\"params\"][\"vars\"][\"title\"] = 'Vectors and Scalars'\ndata2[\"\
    params\"][\"vars\"][\"name\"] = random.choice(names)\n\n# define useful variables/lists\n\
    vectors = [\"displacement\", \"velocity\", \"acceleration\", \"momentum\", \"\
    force\", \"lift\", \"drag\", \"thurst\", \"weight\"]\nscalars = [\"length\", \"\
    area\", \"volume\", \"mass\", \"density\", \"pressure\", \"temperature\", \"energy\"\
    , \"entropy\", \"work\", \"power\"]\n\n# Randomly select 2,3,4 scalars and shuffle\
    \ the lists\ntotal_choices = 6\nnum_scalars = random.choice([2,3,4])\nnum_vectors\
    \ = total_choices - num_scalars\nselect = random.choice([\"vectors\",\"scalars\"\
    ])\n\ndata2[\"params\"][\"choice\"] = select\n\n# Create ans_choices\nans_choices\
    \ = [\"ans{0}\".format(i+1) for i in range(total_choices)]\n\nrandom.shuffle(scalars)\n\
    random.shuffle(vectors)\n\n# define possible answers\nif select == \"vectors\"\
    :\n    for i in range(num_vectors):\n        choice = ans_choices.pop(0)\n   \
    \     data2[\"params\"][\"part1\"][choice][\"value\"] = vectors.pop()\n      \
    \  data2[\"params\"][\"part1\"][choice][\"correct\"] = True\n\n    for i in range(num_scalars):\n\
    \        choice = ans_choices.pop(0)\n        data2[\"params\"][\"part1\"][choice][\"\
    value\"] = scalars.pop()\n        data2[\"params\"][\"part1\"][choice][\"correct\"\
    ] = False\n\nelif select == \"scalars\":\n    for i in range(num_scalars):\n \
    \       choice = ans_choices.pop(0)\n        data2[\"params\"][\"part1\"][choice][\"\
    value\"] = scalars.pop()\n        data2[\"params\"][\"part1\"][choice][\"correct\"\
    ] = True\n        \n    for i in range(num_vectors):\n        choice = ans_choices.pop(0)\n\
    \        data2[\"params\"][\"part1\"][choice][\"value\"] = vectors.pop()\n   \
    \     data2[\"params\"][\"part1\"][choice][\"correct\"] = False\n\n# Update the\
    \ data object with a new dict\ndata.update(data2)\n"
  prepare: 'pass

    '
  parse: 'pass

    '
  grade: 'pass

    '
part1:
  type: checkbox
  pl-customizations:
    weight: 1
    partial-credit: true
    partial-credit-method: EDC
substitutions:
  params:
    vars:
      title: Vectors and Scalars
      name: Maya
    choice: scalars
    part1:
      ans1:
        value: mass
        correct: true
      ans2:
        value: temperature
        correct: true
      ans3:
        value: work
        correct: true
      ans4:
        value: drag
        correct: false
      ans5:
        value: weight
        correct: false
      ans6:
        value: lift
        correct: false
---
# {{ params.vars.title }}
## Question Text

{{ params.vars.name }} is given a list of physical quantities and has to identify all of the {{ params.choice }}. Can you help?

### Answer Section

Select all the choices that apply.

Note: You will be awarded full marks only if you select all the correct choices, and none of the incorrect choices. Choosing incorrect choices as well as not choosing correct choices will result in deductions.

- {{ params.part1.ans1.value}}
- {{ params.part1.ans2.value}}
- {{ params.part1.ans3.value}}
- {{ params.part1.ans4.value}}
- {{ params.part1.ans5.value}}
- {{ params.part1.ans6.value}}
## Rubric

This should be hidden from students until after the deadline.
## Solution

This should never be revealed to students.
## Comments

These are random comments associated with this question.

## Attribution

Problem is licensed under the [CC-BY-NC-SA 4.0 license](https://creativecommons.org/licenses/by-nc-sa/4.0/).<br> ![The Creative Commons 4.0 license requiring attribution-BY, non-commercial-NC, and share-alike-SA license.](https://raw.githubusercontent.com/firasm/bits/master/by-nc-sa.png)
