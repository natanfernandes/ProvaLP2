
total_cadeiras = 29
dados = []
nomes = []
QE = 12684

with open("eleicao.csv", encoding="utf-8") as f:
    f.readline()
    for line in f:
    	string_auxiliar = line.replace("\n", ";")
    	dados.append(string_auxiliar.split(";"))

    for i in dados:
    	print(i)
