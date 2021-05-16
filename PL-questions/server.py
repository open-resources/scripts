import random
import pandas as pd

def generate(data):
	# define or load names/items/objects from server files
	names = pd.read_csv("data/names.csv")["Names"].tolist()
	manual_vehicles = pd.read_csv("data/manual_vehicles.csv")["Manual Vehicles"].tolist()
	
	# store phrases etc
	data["vars"]["name"] = random.choice(names)
	data["vars"]["vehicle"] = random.choice(manual_vehicles)
	data["vars"]["units"] = "m/s"
	data["vars"]["digits_after_decimal"] = 2
	
	# Randomize Variables
	v = random.randint(2,7)
	t = random.randint(5,10)
	
	# store the variables in the dictionary "params"
	data["params"]["v"] = v
	data["params"]["t"] = t
	
	# define possible answers
	data["params"]["part1"]["ans1"] = 42
	data["params"]["part1"]["ans2"] = v*t
	data["params"]["part1"]["ans3"] = v+t
	data["params"]["part1"]["ans4"] = v/t
	data["params"]["part1"]["ans5"] = v-t
	data["params"]["part1"]["ans6"] = 1.3*(v-t)
	
	# define correct answers
	data["correct_answers"]["part1"] = data["params"]["part1"]["ans1"]
