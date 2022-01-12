import sys
import argparse

class Virus:
    pass

file = open(sys.argv[1])

def getGenome(name, file):
    name.header = file.readline()
    name.genome = []
    name.genome = file.readlines()

    name.genome2 = []
    name.g2str = ""

    for i in name.genome:
        name.genome2.append(i.rsplit("\n")[0])

    for i in name.genome2:
        name.g2str += i

    return name.g2str


getGenome(Virus, file)

print(len(Virus.g2str))
