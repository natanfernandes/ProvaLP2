total_cadeiras              = 29    #total de vagas a serem preenchidas
dados                       = []    #todos os dados retirados do arquivo
partidos_coligacoes         = {}    #todos os partidos/coligações do arquivo
votos_validos               = 0     #total de votos válidos
vagas_por_coligacao         = {}    #total de vagas por cada coligação
qe                          = 0     #quociente eleitoral calculado do arquivo
QE                          = 12684  #quociente eleitoral passado pelo professor
vagas_residuais_recebidas   = {}    #recebe os partidos e as vagas residuais de cada
media_por_partido           = {}    #guarda as médias de cada partido no cálculo da média
politicos_por_partido       = {}
votos_por_politico          = {}
politicos_por_numero        = {}


#Calcula o partido que obteve maior média para receber a vaga residual
def calcula_maior_media(partidos_coligacoes,vagas_por_coligacao,vagas_residuais_recebidas):
    maior_media         = 0
    lista_valores = {}
    for partido in partidos_coligacoes:
        media_por_partido[partido] = float(partidos_coligacoes[partido])/float(vagas_por_coligacao[partido]+vagas_residuais_recebidas[partido]+1)
        lista_valores[partido] = media_por_partido[partido] 
    return max(lista_valores,key=lista_valores.get)

#Lê o arquivo e o formata
with open("eleicao.csv", encoding="utf-8") as f:
    f.readline()
    for line in f:
    	string_auxiliar = line.replace("\n", ";")
    	dados.append(string_auxiliar.split(";"))

    #Conta os votos válidos, e conta todos os partidos diferentes e seus votos
    for dado in dados:
        votos_validos += int(dado[3])
        votos_por_politico[dado[1]] = int(dado[3])
        politicos_por_partido[dado[1]] = dado[2]
        politicos_por_numero[dado[1]] = dado[0]
        if(dado[2] not in partidos_coligacoes):
            partidos_coligacoes[dado[2]] = 0
            vagas_residuais_recebidas[dado[2]] = 0
        if(dado[2] in partidos_coligacoes):
            partidos_coligacoes[dado[2]] += int(dado[3])
        
   
    #Faz o cálculo do quociente eleitoral, quantidade de vagas por coligação e a quantidade
    # de vagas residuais
    qe                  = votos_validos//total_cadeiras	
    vagas_por_coligacao = {x:int(partidos_coligacoes[x])//qe for x in partidos_coligacoes}
    vagas_normais       = sum(vagas_por_coligacao.values())
    vagas_residuais     = total_cadeiras - vagas_normais
    
    
    #Designa as vagas residuais para cada partido 
    aux                 = 0
    while(aux < vagas_residuais):
        partido_recebe_vaga                              = calcula_maior_media(partidos_coligacoes,vagas_por_coligacao,vagas_residuais_recebidas)
        vagas_residuais_recebidas[partido_recebe_vaga]  += 1
        aux                                             += 1

    for politico1,politico2 in zip(votos_por_politico,politicos_por_partido):
        if(politico1 == politico2):
            votos_por_politico[politico1] = [politicos_por_numero[politico1],politico1,politicos_por_partido[politico1],votos_por_politico[politico1]]
    
    #Junta a quantidade final de vagas por patido/coligação, vagas normais e residuais
    for coligacao1,coligacao2 in zip(vagas_por_coligacao,vagas_residuais_recebidas):
        if(coligacao1 == coligacao2):
            vagas_por_coligacao[coligacao1] += vagas_residuais_recebidas[coligacao2]
        
    lista_candidatos_ordenada = sorted(votos_por_politico.items(), key=lambda x:x[1][3],reverse= True)
    lista_mais_votados = []
    for coligacao in vagas_por_coligacao:
        for i in range(0,len(lista_candidatos_ordenada)):
            if(coligacao == lista_candidatos_ordenada[i][1][2]):
                if(vagas_por_coligacao[coligacao] > 0):
                    lista_mais_votados.append(lista_candidatos_ordenada[i][1])
                    vagas_por_coligacao[coligacao] -= 1
    
    lista_mais_votados_ordenada = sorted(lista_mais_votados,key=lambda x:x[3], reverse=True)    

    with open('eleicao.tsv', 'w',encoding="utf-8") as f:
        for i in range(0,len(lista_mais_votados_ordenada)):    
            f.write(str(lista_mais_votados_ordenada[i][0] + " " + lista_mais_votados_ordenada[i][1] + " " + lista_mais_votados_ordenada[i][2] + " " + str(lista_mais_votados_ordenada[i][3]) + "\n"))

    