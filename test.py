import yaml

with open("Jewel\\wanted_mods.yaml") as f:
    a = yaml.load(f, Loader=yaml.FullLoader)


for i in a:
    print(i)
