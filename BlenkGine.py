from os import listdir
from os.path import isfile, join
import importlib

project = input("Project folder name:")

eng = importlib.import_module(project + ".engine")

objects = [f for f in listdir(join(project,"objects")) if isfile(join(project,"objects", f))]
rooms = [f for f in listdir(join(project,"rooms")) if isfile(join(project,"rooms", f))]


obj = eng.getobjects(objects,project)
room = eng.getrooms(rooms,project)
pos = []

eng.engine(room,obj,pos)
