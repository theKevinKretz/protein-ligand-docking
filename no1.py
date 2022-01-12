class virus():
    pass

file = open("sequences/SARS-CoV-2/sequence.fasta")

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

# l = virus.g2str.split()

print(len(getGenome(virus, file)))

#print(virus.g2str.lower())
print(len(virus.g2str))