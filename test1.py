import ujson
from collections import OrderedDict 

with open("Inverted_Index/barrel0.json") as f:
    onj = ujson.load(f)
    for key in onj["cbdcs"].values():
        print(key)
