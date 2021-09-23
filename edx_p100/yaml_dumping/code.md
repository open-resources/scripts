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
        data2["params"]["part1"][choice]["correct"] = Truez

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