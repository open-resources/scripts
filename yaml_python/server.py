def generate(data):
  import random

  # define bounds of the variables
  v = random.randint(2,7)
  t = random.randint(5,10)

  # store the variables in the dictionary "params"
  data["params"]["a"] = v
  data["params"]["b"] = t

  # define possible answers
  data["params"]["ans"] = v*t
  data["params"]["ans1"] = v+t
  data["params"]["ans2"] = v/t
  data["params"]["ans3"] = v-t
