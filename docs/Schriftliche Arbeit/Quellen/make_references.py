inp = open("sources")

dic = {}

lines = inp.readlines()

for line in range((len(lines) + 1)//4):
    url = lines[line * 4 + 0][:-1]
    desc = lines[line * 4 + 1][:-1]
    date = lines[line * 4 + 2][:-1]

    dic.update({line: {"desc": desc, "url": url, "date": date}})

print(dic)

out = ""

# \item \href{https}{\emph{Wiki}} Abgerufen: 01.01.2022


for i in dic:
    # out += "\\item \\url{" + dic[i]['url'] + "}\n\\emph{" + dic[i]['desc'] + "}\nAbgerufen: " + dic[i]['date'] + "\n\n"
    out += "\\bibitem{"+str(i+1)+"}\n"+"\\url{" + dic[i]['url'] + "} \\emph{" + dic[i]['desc'] + "}\nAbgerufen: " + dic[i]['date'] + "\n\n"

print(out)