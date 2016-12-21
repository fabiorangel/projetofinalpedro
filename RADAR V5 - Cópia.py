import csv
import os
from datetime import datetime
from Tkinter import *
import matplotlib.pyplot as plt
import ttk
from scipy import stats


endereco = "C:\RADAR V2\BASE\ENTRADA\BASE VERSAO 3.csv"

#ABRE OS ARQUIVOS DE ENTRADA E SAÍDA E ESCREVE O CABEÇALHO DO ARQUIVO DE SAIDA FILTRO
arquivo_entrada_vendas = open (endereco)
arquivo_saida_usuario = open("C:\RADAR V2\BASE\SAIDA\SAIDA TESTE.csv",'w')
arquivo_saida_filtro = open("C:\RADAR V2\BASE\SAIDA\SAIDA FILTRO.csv",'w')
arquivo_saida_filtro.write('ID_LINHA,REGIAO,FILIAL,GERENCIA,SUPERVISOR,VENDEDOR,GRUPO,EMPRESA,ESTABELECIMENTO,CLIENTE,PRODUTO,UF,SEGMENTO_4,PRODUTO_NIVEL_1,PRODUTO_NIVEL_2,PRODUTO_NIVEL_3,PRODUTO_NIVEL_4,MES_1,MES_2,MES_3,MES_4,MES_5,MES_6,MES_7,MES_8,MES_9,MES_10,MES_11,MES_12,MES_13,MES_14,MES_15,MES_16,MES_17,MES_18,MES_19,MES_20,MES_21,MES_22,MES_23,MES_24,MES_25,MES_26,MES_27,MES_28,MES_29,MES_30,MES_31,MES_32,MES_33,MES_34,MES_35,MES_36,MES_37,MES_38,MES_39,MES_40,MES_41,MES_42,MES_43,MES_44,MES_45,MES_46,MES_47,MES_48,MES_49,MES_50,MES_51,MES_52,MES_53,MES_54,MES_55,MES_56,MES_57,MES_58,MES_59,MES_60,MES_61,MES_62,MES_63,MES_64,MES_65,MES_66,MES_67,MES_68,MES_69,MES_70,MES_71,MES_72\n')

#LÊ O ARQUIVO DE ENTRADA E TRANSFORMA ELE EM UMA LISTA
reader = csv.reader(arquivo_entrada_vendas)
MEUS_DADOS_vendas= list(reader)

# conta a quantidade de registro da base de clientes

tamanho_da_base=0
for line in MEUS_DADOS_vendas:
    tamanho_da_base=tamanho_da_base+1

# DIMENSIONA O VETOR DE DADOS E CRIA AS VARIÁVEIS PARA CALCULAR O ERRO

soma_erro58 = 0
soma_erro59 = 0
denominador_erro = 0
vetor_dados = [0]*60

# PREENCHE O VETOR DE DADOS DE COMPRAS
h = 0
for line in MEUS_DADOS_vendas[1:]:
    for i in range(len(line [17:77])):
        vetor_dados[i] = float(line [17:77][i])

    

# identifica clientes que ja foram perdidos (passaram os ultimos doze meses sem comprar) E A MAIOR VENDA DO ÚLTIMO ANO
    modelo = 0
    comeco = 0
    acumula_ultimo_ano = 0.0
    maior_ultimo_ano = 0
    for dado in vetor_dados[48:60]:
        acumula_ultimo_ano = acumula_ultimo_ano + dado
        if dado > maior_ultimo_ano:
            maior_ultimo_ano = dado
    if acumula_ultimo_ano == 0.0:
        modelo = "CLIENTE PERDIDO"
        alerta58 = "PRETO"
        alerta59 = "PRETO"
        arquivo_saida_usuario.write(modelo+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + modelo + '\n')

    
    else:

# DEFINE O COMEÇO (local onde aparece o primeiro valor diferente de zero)

        for dado in vetor_dados:
            if dado == 0.0:
                comeco = comeco+1
            else:
                break
        
# IDENTIFICA CLIENTES QUE PARARAM DE COMPRAR POR MAIS DE DOZE MESES E VOLTARAM DEPOIS. O INÍCIO DA SÉRIE DE COMPRAS DESSES CLIENTES SERÁ NA PRIMEIRA COMPRA APÓS A AUSÊNCIA.
        soma_12 = 0.0
        for a in range(comeco,48):
            soma_12 = vetor_dados[a]+vetor_dados[a+1]+vetor_dados[a+2]+vetor_dados[a+3]+vetor_dados[a+4]+vetor_dados[a+5]+vetor_dados[a+6]+vetor_dados[a+7]+vetor_dados[a+8]+vetor_dados[a+9]+vetor_dados[a+10]+vetor_dados[a+11]
            if soma_12 == 0.0:
                comeco = a+12
        if comeco >= 48:
            alerta58 = "AZUL"
            alerta59 = "AZUL"
            modelo = "CLIENTE NOVO"
            arquivo_saida_usuario.write(modelo+'\n')
            arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + modelo + '\n')


# IDENTIFICA O MENOR VALOR COMPRADO POR CADA CLIENTE
        menor = 10000000000000000000000000000000000000000000
        for dado in vetor_dados[comeco:58]:
            if dado < menor:
                menor = dado



# IDENTIFICA O TAMANHO DOS PERÍODOS QUE O CLIENTE PASSA SEM COMPRAR NADA
        ultimo_buraco = 0
        for dado in vetor_dados[60:comeco:-1]:
            if dado == 0.0:
                ultimo_buraco = ultimo_buraco + 1
            else:
                break

        buraco = 0
        maior_buraco = 0
        for dado in vetor_dados[comeco:60-ultimo_buraco]:
            if dado == 0.0:
                buraco = buraco + 1
            if buraco > maior_buraco:
                maior_buraco = buraco
            if dado != 0.0:
                buraco = 0
        
# ENCAIXA CADA CLIENTE EM UM MODELO DE COMPRA DE ACORDO COM O DESVIO PADRÃO DAS DIFERENÇAS MÓVEIS.
# UM CLIENTE SÓ SERÁ ENCAIXADO EM UM MODELO MAIOR OU IGUAL A 7 SE O TEMPO EM MESES DESDE QUE ELE COMEÇOU A COMPRAR FOR MAIOR OU IGUAL AO DOBRO DO TAMANHO DO MODELO.
                
    if modelo != 'CLIENTE PERDIDO' and modelo != "CLIENTE NOVO":

        vetor_diferenca_1= [0]*60
        vetor_diferenca_2= [0]*60
        vetor_diferenca_3= [0]*60
        vetor_diferenca_4= [0]*60
        vetor_diferenca_5= [0]*60
        vetor_diferenca_6= [0]*60
        vetor_diferenca_7= [0]*60
        vetor_diferenca_8= [0]*60
        vetor_diferenca_9= [0]*60
        vetor_diferenca_10= [0]*60
        vetor_diferenca_11= [0]*60
        vetor_diferenca_12= [0]*60

        variabilidade_minima = 100000000000000000000
        somadif1 = 0
        somadif2 = 0
        somadif3 = 0
        somadif4 = 0
        somadif5 = 0
        somadif6 = 0
        somadif7 = 0
        somadif8 = 0
        somadif9 = 0
        somadif10 = 0
        somadif11 = 0
        somadif12 = 0
        
        somadif1quadrado = 0
        somadif2quadrado = 0
        somadif3quadrado = 0
        somadif4quadrado = 0
        somadif5quadrado = 0
        somadif6quadrado = 0
        somadif7quadrado = 0
        somadif8quadrado = 0
        somadif9quadrado = 0
        somadif10quadrado = 0
        somadif11quadrado = 0
        somadif12quadrado = 0


        for j in range(comeco+1, 60):
            vetor_diferenca_1[j] = vetor_dados[j] - vetor_dados[j-1]

        denominador = 0
        for k in range(comeco+1,58):
            somadif1 = somadif1 + vetor_diferenca_1[k]
            somadif1quadrado = somadif1quadrado + vetor_diferenca_1[k]**2
            denominador = denominador+1
        mediadif1 = somadif1/denominador
        dp1 = ((somadif1quadrado/denominador) - mediadif1**2)**0.5
        if dp1*1.25 < variabilidade_minima:
            variabilidade_minima = dp1
            modelo='MM1'
    


        for j in range(comeco+2, 60):
            vetor_diferenca_2[j] = vetor_dados[j] - vetor_dados[j-2]

        denominador = 0
        for k in range(comeco+2,58):
            somadif2 = somadif2 + vetor_diferenca_2[k]
            somadif2quadrado = somadif2quadrado + vetor_diferenca_2[k]**2
            denominador = denominador+1
        mediadif2 = somadif2/denominador
        dp2 = ((somadif2quadrado/denominador) - mediadif2**2)**0.5
        if dp2*1.25 < variabilidade_minima:
            variabilidade_minima = dp2
            modelo='MM2'



        for j in range(comeco+3, 60):
            vetor_diferenca_3[j] = vetor_dados[j] - vetor_dados[j-3]

        denominador = 0
        for k in range(comeco+3,58):
            somadif3 = somadif3 + vetor_diferenca_3[k]
            somadif3quadrado = somadif3quadrado + vetor_diferenca_3[k]**2
            denominador = denominador+1
        mediadif3 = somadif3/denominador
        dp3 = ((somadif3quadrado/denominador) - mediadif3**2)**0.5 
        if dp3*1.25 < variabilidade_minima:
            variabilidade_minima = dp3
            modelo='MM3'



        for j in range(comeco+4, 60):
            vetor_diferenca_4[j] = vetor_dados[j] - vetor_dados[j-4]

        denominador = 0
        for k in range(comeco+4,58):
            somadif4 = somadif4 + vetor_diferenca_4[k]
            somadif4quadrado = somadif4quadrado + vetor_diferenca_4[k]**2
            denominador = denominador+1
        mediadif4 = somadif4/denominador
        dp4 = ((somadif4quadrado/denominador) - mediadif4**2)**0.5
        if dp4*1.25 < variabilidade_minima:
            variabilidade_minima = dp4
            modelo='MM4'



        for j in range(comeco+5, 60):
            vetor_diferenca_5[j] = vetor_dados[j] - vetor_dados[j-5]

        denominador = 0
        for k in range(comeco+5,58):
            somadif5 = somadif5 + vetor_diferenca_5[k]
            somadif5quadrado = somadif5quadrado + vetor_diferenca_5[k]**2
            denominador = denominador+1
        mediadif5 = somadif5/denominador
        dp5 = ((somadif5quadrado/denominador) - mediadif5**2)**0.5
        if dp5*1.25 < variabilidade_minima:
            variabilidade_minima = dp5
            modelo='MM5'



        for j in range(comeco+6, 60):
            vetor_diferenca_6[j] = vetor_dados[j] - vetor_dados[j-6]

        denominador = 0
        for k in range(comeco+6,58):
            somadif6 = somadif6 + vetor_diferenca_6[k]
            somadif6quadrado = somadif6quadrado + vetor_diferenca_6[k]**2
            denominador = denominador+1
        mediadif6 = somadif6/denominador
        dp6 = ((somadif6quadrado/denominador) - mediadif6**2)**0.5
        if dp6*1.25 < variabilidade_minima:
            variabilidade_minima = dp6
            modelo='MM6'



        if len(range(comeco, 60))>=14:
            for j in range(comeco+7, 60):
                vetor_diferenca_7[j] = vetor_dados[j] - vetor_dados[j-7]

            denominador = 0
            for k in range(comeco+7,58):
                somadif7 = somadif7 + vetor_diferenca_7[k]
                somadif7quadrado = somadif7quadrado + vetor_diferenca_7[k]**2
                denominador = denominador+1
            mediadif7 = somadif7/denominador
            dp7 = ((somadif7quadrado/denominador) - mediadif7**2)**0.5
            if dp7*1.25 < variabilidade_minima:
                variabilidade_minima = dp7
                modelo='MM7'



        if len(range(comeco, 60))>=16:
            for j in range(comeco+8, 60):
                vetor_diferenca_8[j] = vetor_dados[j] - vetor_dados[j-8]

            denominador = 0
            for k in range(comeco+8,58):
                somadif8 = somadif8 + vetor_diferenca_8[k]
                somadif8quadrado = somadif8quadrado + vetor_diferenca_8[k]**2
                denominador = denominador+1
            mediadif8 = somadif8/denominador
            dp8 = ((somadif8quadrado/denominador) - mediadif8**2)**0.5
            if dp8*1.25 < variabilidade_minima:
                variabilidade_minima = dp8
                modelo='MM8'



        if len(range(comeco, 60))>=18:
            for j in range(comeco+9, 60):
                vetor_diferenca_9[j] = vetor_dados[j] - vetor_dados[j-9]

            denominador = 0
            for k in range(comeco+9,58):
                somadif9 = somadif9 + vetor_diferenca_9[k]
                somadif9quadrado = somadif9quadrado + vetor_diferenca_9[k]**2
                denominador = denominador+1
            mediadif9 = somadif9/denominador
            dp9 = ((somadif9quadrado/denominador) - mediadif9**2)**0.5
            if dp9*1.25 < variabilidade_minima:
                variabilidade_minima = dp9
                modelo='MM9'



        if len(range(comeco, 60))>=20:
            for j in range(comeco+10, 60):
                vetor_diferenca_10[j] = vetor_dados[j] - vetor_dados[j-10]

            denominador = 0
            for k in range(comeco+10,58):
                somadif10 = somadif10 + vetor_diferenca_10[k]
                somadif10quadrado = somadif10quadrado + vetor_diferenca_10[k]**2
                denominador = denominador+1
            mediadif10 = somadif10/denominador
            dp10 = ((somadif10quadrado/denominador) - mediadif10**2)**0.5
            if dp10*1.25 < variabilidade_minima:
                variabilidade_minima = dp10
                modelo='MM10'


        if len(range(comeco, 60))>=22:
            for j in range(comeco+11, 60):
                vetor_diferenca_11[j] = vetor_dados[j] - vetor_dados[j-11]

            denominador = 0
            for k in range(comeco+11,58):
                somadif11 = somadif11 + vetor_diferenca_11[k]
                somadif11quadrado = somadif11quadrado + vetor_diferenca_11[k]**2
                denominador = denominador+1
            mediadif11 = somadif11/denominador
            dp11 = ((somadif11quadrado/denominador) - mediadif11**2)**0.5
            if dp11*1.25 < variabilidade_minima:
                variabilidade_minima = dp11
                modelo='MM11'


        if len(range(comeco, 60))>=24:
            for j in range(comeco+12, 60):
                vetor_diferenca_12[j] = vetor_dados[j] - vetor_dados[j-12]

            denominador = 0
            for k in range(comeco+12,58):
                somadif12 = somadif12 + vetor_diferenca_12[k]
                somadif12quadrado = somadif12quadrado + vetor_diferenca_12[k]**2
                denominador = denominador+1
            mediadif12 = somadif12/denominador
            dp12 = ((somadif12quadrado/denominador) - mediadif12**2)**0.5
            if dp12*1.25 < variabilidade_minima:
                variabilidade_minima = dp12
                modelo='MM12'


# DIMENSIONANDO OS VETORES DAS PROJEÇÕES.

    vetor_projecao_estacionario = [0]*72
    vetor_projecao_linear = [0]*72
    projecao = [0]*60
    melhor_projecao = 0*72
    vetor_z1 = [0]*60
    vetor_z2 = [0]*60


# PARÂMETROS A SEREM DEFINIDOS MANUALMENTE PARA AJUSTAR OS ALARMES

    mao = 1
    mvo = 1.5


# CALCULA A PROJEÇÃO DA SÉRIE DE ACORDO COM O MODELO DEFINIDO ACIMA.
# DE TODAS AS POSSÍVEIS COMBINAÇÕES DE ALFA, BETA E GAMA, ELEGE A MELHOR (AQUELA QUE TEM O MENOR EPAM).
# SE UM DOS DOIS ÚLTIMOS DADOS DA SÉRIE FOR MENOR QUE A PROJEÇÃO MENOS O DESVIO PADRÃO MULTIPLICADO PELA CONSTANTE DE AJUSTE, O ALERTA SERÁ ACIONADO.
# APÓS FAZER AS PROJEÇÕES, CALCULA-SE TAMBÉM A TENDÊNCIA DA SÉRIE ATRAVÉS DO TESTE DOS SINAIS.

    if modelo=='MM1':

        s = 1
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto])/s
        zbarra_fim = (vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,20,1):
            alfa = alfa/100.0
            for beta in range (1,20,1):
                beta = beta/100.0
                for gama in range (1,20,1):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1 
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca + 1
    

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma = 0
                        somaquadrado = 0
                        denominador = 0
                        for j in range(57,comeco+resto-1,-1):
                            soma = soma + vetor_dados[j]
                            somaquadrado = somaquadrado + vetor_dados[j]**2
                            denominador = denominador+1
                        media = soma/denominador
                        dp = ((somaquadrado/denominador) - media**2)**0.5
                        cv = 100*dp/media

                        if cv < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*(((somaquadrado/denominador) - media**2)**0.5) or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*(((somaquadrado/denominador) - media**2)**0.5) or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'
                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+1]) - ma*(((somaquadrado/denominador) - media**2)**0.5) or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+1]) - mv*(((somaquadrado/denominador) - media**2)**0.5) or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+1]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+1]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+1]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+1]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+1]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+1]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+1]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+1]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+1]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+1]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+1]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+1])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+1])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+1])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+1])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+1])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+1])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+1])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+1])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+1])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+1])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+1])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+1])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+1])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+1])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+1])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+1])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+1])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+1])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+1])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+1])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+1])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+1])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+1])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+1])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+1])


        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0

        
        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_1[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'
                    
        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')



    if modelo=='MM2':

        s = 2
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1])/s
        zbarra_fim = (vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,20,2):
            alfa = alfa/100.0
            for beta in range (1,20,2):
                beta = beta/100.0
                for gama in range (1,20,2):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1 
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(56,comeco+resto-1,-2):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(57,comeco+resto-1,-2):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+1]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+2]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+1]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+2]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+1]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+2]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+1]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+2]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+1]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+2]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+1])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+2])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+1])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+2])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+1])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+2])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+1])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+2])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+1])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+2])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+1])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+1])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+2])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+1])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+2])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+1])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+2])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+1])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+2])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+1])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+2])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+1])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+2])


        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_2[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM3':

        s = 3
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2])/s
        zbarra_fim = (vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,30,2):
            alfa = alfa/100.0
            for beta in range (1,30,2):
                beta = beta/100.0
                for gama in range (1,30,2):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca=multiplicador_diferenca+1
                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(55,comeco+resto-1,-3):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(56,comeco+resto-1,-3):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+1]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+2]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+3]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+1]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+2]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+3]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+1]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+2]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+3]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+1])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+2])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+3])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+1])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+2])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+3])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+1])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+2])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+3])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+1])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+1])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+2])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+3])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+1])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+2])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+3])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+1])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+2])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+3])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+1])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+2])


        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_3[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM4':

        s = 4
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3])/s
        zbarra_fim = (vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,30,2):
            alfa = alfa/100.0
            for beta in range (1,30,2):
                beta = beta/100.0
                for gama in range (1,30,2):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca=multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(54,comeco+resto-1,-4):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(55,comeco+resto-1,-4):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+1]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+2]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+3]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+4]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+1]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+2]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+3]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+4]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+1])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+2])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+3])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+4])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+1])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+2])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+3])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+4])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+1])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+1])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+2])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+3])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+4])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+1])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+2])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+3])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+4])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+1])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+2])

        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_4[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM5':

        s = 5
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4])/s
        zbarra_fim = (vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,30,2):
            alfa = alfa/100.0
            for beta in range (1,30,2):
                beta = beta/100.0
                for gama in range (1,30,2):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(53,comeco+resto-1,-5):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(54,comeco+resto-1,-5):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+1]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+2]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+3]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+4]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+5]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+1]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+2]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+1])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+2])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+3])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+4])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+5])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+1])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+2])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+3])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+1])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+2])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+3])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+4])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+5])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+1])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+2])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+3])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+4])

        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0

        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_5[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM6':

        s = 6
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5])/s
        zbarra_fim = (vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,40,4):
            alfa = alfa/100.0
            for beta in range (1,40,4):
                beta = beta/100.0
                for gama in range (1,40,4):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(52,comeco+resto-1,-6):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(53,comeco+resto-1,-6):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/(media59 + 0.0000000000000000001)

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+1]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+2]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+3]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+4]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+5]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+6]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+1])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+2])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+3])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+4])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+5])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+6])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+1])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+1])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+2])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+3])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+4])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+5])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+6])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+1])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+2])

        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0

        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_6[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM7':


        s = 7
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5] + vetor_dados[comeco+resto + 6])/s
        zbarra_fim = (vetor_dados[53] + vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,50,5):
            alfa = alfa/100.0
            for beta in range (1,50,5):
                beta = beta/100.0
                for gama in range (1,50,5):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(51,comeco+resto-1,-7):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/(media58 + 0.0000000000000000001)

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(52,comeco+resto-1,-7):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/(media59 + 0.0000000000000000001)

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+7]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+1]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+2]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+3]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+4]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+5]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+7])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+1])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+2])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+3])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+4])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+5])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+6])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+7])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+1])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+2])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+3])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+4])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+5])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+6])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+7])

        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0

        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_7[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM8':                
        s = 8
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5] + vetor_dados[comeco+resto + 6] + vetor_dados[comeco+resto + 7])/s
        zbarra_fim = (vetor_dados[52] + vetor_dados[53] + vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,50,5):
            alfa = alfa/100.0
            for beta in range (1,50,5):
                beta = beta/100.0
                for gama in range (1,50,5):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(50,comeco+resto-1,-8):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/(media58 + 0.0000000000000000001)

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(51,comeco+resto-1,-8):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+7]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+8]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+1]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+2]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+3]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+4]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+7])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+8])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+1])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+2])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+3])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+4])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+5])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+7])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+8])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+1])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+2])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+3])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+4])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+5])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+6])

        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0

        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_8[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM9':


        s = 9
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5] + vetor_dados[comeco+resto + 6] + vetor_dados[comeco+resto + 7] + vetor_dados[comeco+resto + 8])/s
        zbarra_fim = (vetor_dados[51] + vetor_dados[52] + vetor_dados[53] + vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,50,5):
            alfa = alfa/100.0
            for beta in range (1,50,5):
                beta = beta/100.0
                for gama in range (1,50,5):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca=multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(49,comeco+resto-1,-9):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(50,comeco+resto-1,-9):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+7]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+8]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+9]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+1]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+2]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+3]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+7])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+8])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+9])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+1])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+2])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+3])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+4])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+7])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+8])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+9])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+1])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+2])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+3])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+4])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+5])


        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_9[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM10':


        s = 10
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5] + vetor_dados[comeco+resto + 6] + vetor_dados[comeco+resto + 7] + vetor_dados[comeco+resto + 8] + vetor_dados[comeco+resto + 9])/s
        zbarra_fim = (vetor_dados[50] + vetor_dados[51] + vetor_dados[52] + vetor_dados[53] + vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,90,5):
            alfa = alfa/100.0
            for beta in range (1,90,5):
                beta = beta/100.0
                for gama in range (1,90,5):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca=multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(48,comeco+resto-1,-10):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(49,comeco+resto-1,-10):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+7]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+8]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+9]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+10]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+1]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+2]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+7])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+8])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+9])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+10])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+1])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+2])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+3])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+7])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+8])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+9])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+10])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+1])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+2])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+3])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+4])


        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_10[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM11':


        s = 11
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5] + vetor_dados[comeco+resto + 6] + vetor_dados[comeco+resto + 7] + vetor_dados[comeco+resto + 8] + vetor_dados[comeco+resto + 9] + vetor_dados[comeco+resto + 10])/s
        zbarra_fim = (vetor_dados[49] + vetor_dados[50] + vetor_dados[51] + vetor_dados[52] + vetor_dados[53] + vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,90,5):
            alfa = alfa/100.0
            for beta in range (1,90,5):
                beta = beta/100.0
                for gama in range (1,90,5):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca = multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(47,comeco+resto-1,-11):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58


                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(48,comeco+resto-1,-11):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/(media59 + 0.0000000000000000001)

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+7]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+8]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+9]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+10]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+11]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+1]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+7])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+8])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+9])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+10])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+11])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+1])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+2])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+7])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+8])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+9])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+10])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+11])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+1])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+2])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+3])


        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_11[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >=0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    if modelo=='MM12':

                
        s = 12
        k = len(vetor_dados[comeco:])/s
        resto = len(vetor_dados[comeco:])%s
        vetor_b0 = [0]*60
        vetor_b1 = [0]*60
        efeito_sazonal = [0]*60
        zbarra_comeco = (vetor_dados[comeco+resto] + vetor_dados[comeco+resto + 1] + vetor_dados[comeco+resto + 2] + vetor_dados[comeco+resto + 3] + vetor_dados[comeco+resto + 4] + vetor_dados[comeco+resto + 5] + vetor_dados[comeco+resto + 6] + vetor_dados[comeco+resto + 7] + vetor_dados[comeco+resto + 8] + vetor_dados[comeco+resto + 9] + vetor_dados[comeco+resto + 10] + vetor_dados[comeco+resto + 11])/s
        zbarra_fim = (vetor_dados[48] + vetor_dados[49] + vetor_dados[50] + vetor_dados[51] + vetor_dados[52] + vetor_dados[53] + vetor_dados[54] + vetor_dados[55] + vetor_dados[56] + vetor_dados[57] + vetor_dados[58] + vetor_dados[59])/s

        melhor_projecao = [0]*72
        melhor_alfa = 0.01
        melhor_beta = 0.01
        melhor_gama = 0.01
        menor_epam = 1000000000000000000000000000000000000000000000000000000000
        for alfa in range (1,90,5):
            alfa = alfa/100.0
            for beta in range (1,90,5):
                beta = beta/100.0
                for gama in range (1,90,5):
                    gama = gama/100.0
                    diferenca = 0
                    denominador = 0
                    vetor_b1[comeco+resto+s-1] = (zbarra_fim - zbarra_comeco)/((k-1)*s)
                    vetor_b0[comeco+resto+s-1] = vetor_dados[comeco+resto] + vetor_b1[comeco+resto+s-1]*s/2
                    for j in range (comeco+resto, comeco+resto+s):
                        efeito_sazonal[j] = vetor_dados[j] - (vetor_b0[comeco+resto+s-1] - ((s - (j-comeco+resto+1))*vetor_b1[comeco+resto+s-1]))
                    multiplicador_diferenca = comeco+resto+s+1
                    for j in range (comeco+resto+s, 60):
                        vetor_b0[j] = alfa*(vetor_dados[j]-efeito_sazonal[j-s]) + (1-alfa)*(vetor_b0[j-1]+vetor_b1[j-1])
                        vetor_b1[j] = beta*(vetor_b0[j] - vetor_b0[j-1]) + (1-beta)*vetor_b1[j-1]
                        efeito_sazonal[j] = gama*(vetor_dados[j] - vetor_b0[j]) + (1 - gama)*efeito_sazonal[j-s]
                        projecao[j] = vetor_b0[j-1]+vetor_b1[j-1]+efeito_sazonal[j-s]
                        diferenca = diferenca + multiplicador_diferenca**2*abs((projecao[j] - vetor_dados[j])/(vetor_dados[j] + 0.0000000000000001))
                        denominador = denominador+multiplicador_diferenca**2
                        multiplicador_diferenca=multiplicador_diferenca+1

                    epam = 100*diferenca/denominador
                    if epam < menor_epam:
                        melhor_alfa = alfa
                        melhor_beta = beta
                        melhor_gama = gama
                        menor_epam = epam
                        for j in range (comeco+resto+s, 60):
                            melhor_projecao[j]=projecao[j]

                        soma58 = 0
                        somaquadrado58 = 0
                        denominador58 = 0
                        for j in range(46,comeco+resto-1,-12):
                            soma58 = soma58 + vetor_dados[j]
                            somaquadrado58 = somaquadrado58 + vetor_dados[j]**2
                            denominador58 = denominador58+1
                        media58 = soma58/denominador58
                        dp58 = ((somaquadrado58/denominador58) - media58**2)**0.5
                        cv58 = 100*dp58/media58

                        soma59 = 0
                        somaquadrado59 = 0
                        denominador59 = 0
                        for j in range(47,comeco+resto-1,-12):
                            soma59 = soma59 + vetor_dados[j]
                            somaquadrado59 = somaquadrado59 + vetor_dados[j]**2
                            denominador59 = denominador59+1
                        media59 = soma59/denominador59
                        dp59 = ((somaquadrado59/denominador59) - media59**2)**0.5
                        cv59 = 100*dp59/media59

                        if cv58 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo
                            
                        alerta58 = 'VERDE'
                        if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - ma*dp58 or vetor_dados[58] < menor or ultimo_buraco-1 > maior_buraco:
                            alerta58 = 'AMARELO'
                            if vetor_dados[58] < (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1]) - mv*dp58 or vetor_dados[58] < menor/2 or ultimo_buraco-1 > maior_buraco + 1:
                                alerta58 = 'VERMELHO'
                                if ultimo_buraco - 1 > maior_buraco + 3:
                                    alerta58 = 'PRETO'

                        if cv59 < 5:
                            ma = 2
                            mv = 2.5
                        else:
                            ma = mao
                            mv = mvo

                        alerta59 = 'VERDE'
                        if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - ma*dp59 or vetor_dados[59] < menor or ultimo_buraco > maior_buraco:
                            alerta59 = 'AMARELO'
                            if vetor_dados[59] < (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2]) - mv*dp59 or vetor_dados[59] < menor/2 or ultimo_buraco > maior_buraco + 1:
                                alerta59 = 'VERMELHO'
                                if ultimo_buraco > maior_buraco + 3:
                                    alerta59 = 'PRETO'


                            
                        if alerta58 == 'VERDE' and alerta59 == 'VERDE' or alerta58 == 'AMARELO' and alerta59 == 'VERDE':
                            melhor_projecao [60] = vetor_b0[59] + vetor_b1[59]*1 + efeito_sazonal[59-s+1]
                            melhor_projecao [61] = vetor_b0[59] + vetor_b1[59]*2 + efeito_sazonal[59-s+2]
                            melhor_projecao [62] = vetor_b0[59] + vetor_b1[59]*3 + efeito_sazonal[59-s+3]
                            melhor_projecao [63] = vetor_b0[59] + vetor_b1[59]*4 + efeito_sazonal[59-s+4]
                            melhor_projecao [64] = vetor_b0[59] + vetor_b1[59]*5 + efeito_sazonal[59-s+5]
                            melhor_projecao [65] = vetor_b0[59] + vetor_b1[59]*6 + efeito_sazonal[59-s+6]
                            melhor_projecao [66] = vetor_b0[59] + vetor_b1[59]*7 + efeito_sazonal[59-s+7]
                            melhor_projecao [67] = vetor_b0[59] + vetor_b1[59]*8 + efeito_sazonal[59-s+8]
                            melhor_projecao [68] = vetor_b0[59] + vetor_b1[59]*9 + efeito_sazonal[59-s+9]
                            melhor_projecao [69] = vetor_b0[59] + vetor_b1[59]*10 + efeito_sazonal[59-s+10]
                            melhor_projecao [70] = vetor_b0[59] + vetor_b1[59]*11 + efeito_sazonal[59-s+11]
                            melhor_projecao [71] = vetor_b0[59] + vetor_b1[59]*12 + efeito_sazonal[59-s+12]

                        if alerta58 == 'VERDE' and alerta59 == 'VERMELHO' or alerta58 == 'VERDE' and alerta59 == 'AMARELO':
                            melhor_projecao [59] = (vetor_b0[58] + vetor_b1[58]*1 + efeito_sazonal[58-s+1])
                            melhor_projecao [60] = (vetor_b0[58] + vetor_b1[58]*2 + efeito_sazonal[58-s+2])
                            melhor_projecao [61] = (vetor_b0[58] + vetor_b1[58]*3 + efeito_sazonal[58-s+3])
                            melhor_projecao [62] = (vetor_b0[58] + vetor_b1[58]*4 + efeito_sazonal[58-s+4])
                            melhor_projecao [63] = (vetor_b0[58] + vetor_b1[58]*5 + efeito_sazonal[58-s+5])
                            melhor_projecao [64] = (vetor_b0[58] + vetor_b1[58]*6 + efeito_sazonal[58-s+6])
                            melhor_projecao [65] = (vetor_b0[58] + vetor_b1[58]*7 + efeito_sazonal[58-s+7])
                            melhor_projecao [66] = (vetor_b0[58] + vetor_b1[58]*8 + efeito_sazonal[58-s+8])
                            melhor_projecao [67] = (vetor_b0[58] + vetor_b1[58]*9 + efeito_sazonal[58-s+9])
                            melhor_projecao [68] = (vetor_b0[58] + vetor_b1[58]*10 + efeito_sazonal[58-s+10])
                            melhor_projecao [69] = (vetor_b0[58] + vetor_b1[58]*11 + efeito_sazonal[58-s+11])
                            melhor_projecao [70] = (vetor_b0[58] + vetor_b1[58]*12 + efeito_sazonal[58-s+12])
                            melhor_projecao [71] = (vetor_b0[58] + vetor_b1[58]*13 + efeito_sazonal[58-s+1])


                        if alerta58 == 'VERMELHO' and alerta59 == 'VERMELHO' or alerta58 == 'VERMELHO' and alerta59 == 'AMARELO' or alerta58 == 'AMARELO' and alerta59 == 'VERMELHO' or alerta58 == 'AMARELO' and alerta59 == 'AMARELO' or alerta58 == 'VERMELHO' and alerta59 == 'VERDE':
                            melhor_projecao [58] = (vetor_b0[57] + vetor_b1[57]*1 + efeito_sazonal[57-s+1])
                            melhor_projecao [59] = (vetor_b0[57] + vetor_b1[57]*2 + efeito_sazonal[57-s+2])
                            melhor_projecao [60] = (vetor_b0[57] + vetor_b1[57]*3 + efeito_sazonal[57-s+3])
                            melhor_projecao [61] = (vetor_b0[57] + vetor_b1[57]*4 + efeito_sazonal[57-s+4])
                            melhor_projecao [62] = (vetor_b0[57] + vetor_b1[57]*5 + efeito_sazonal[57-s+5])
                            melhor_projecao [63] = (vetor_b0[57] + vetor_b1[57]*6 + efeito_sazonal[57-s+6])
                            melhor_projecao [64] = (vetor_b0[57] + vetor_b1[57]*7 + efeito_sazonal[57-s+7])
                            melhor_projecao [65] = (vetor_b0[57] + vetor_b1[57]*8 + efeito_sazonal[57-s+8])
                            melhor_projecao [66] = (vetor_b0[57] + vetor_b1[57]*9 + efeito_sazonal[57-s+9])
                            melhor_projecao [67] = (vetor_b0[57] + vetor_b1[57]*10 + efeito_sazonal[57-s+10])
                            melhor_projecao [68] = (vetor_b0[57] + vetor_b1[57]*11 + efeito_sazonal[57-s+11])
                            melhor_projecao [69] = (vetor_b0[57] + vetor_b1[57]*12 + efeito_sazonal[57-s+12])
                            melhor_projecao [70] = (vetor_b0[57] + vetor_b1[57]*13 + efeito_sazonal[57-s+1])
                            melhor_projecao [71] = (vetor_b0[57] + vetor_b1[57]*14 + efeito_sazonal[57-s+2])

        for i in range(len(melhor_projecao[58:])):
            if melhor_projecao[i] < 0:
                melhor_projecao[i] = 0


        if alerta58 == 'PRETO' and alerta59 == 'PRETO':
            tendencia = 'CLIENTE PERDIDO'

        if alerta58 == 'AZUL' and alerta59 == 'AZUL':
            tendencia = 'CLIENTE NOVO'

        if alerta58 != 'PRETO' or alerta59 != 'PRETO':
            if alerta58 != 'AZUL' or alerta59 != 'AZUL':

                mais = 0
                for i in vetor_diferenca_12[48:]:
                    if i > 0:
                        mais+=1

                teste = stats.binom.cdf(mais, 12, 0.5, loc=0)
                
            
                if teste >= 0.95:
                    tendencia = 'CRESCENTE'

                if teste <= 0.07:
                    tendencia = 'DECRESCENTE'

                if teste >= 0.07 and teste <= 0.95:
                    tendencia = 'NEUTRA'

        arquivo_saida_usuario.write(modelo + ';' + alerta58 + ';' + alerta59 + ';' + str(melhor_alfa).replace('.',',') + ';'+ str(melhor_beta).replace('.',',') + ';'+ str(melhor_gama).replace('.',',') + ';' + str(dp).replace('.',',') + ';' + str(mv*dp).replace('.',',') + '\n'+'serie; '+str(vetor_dados).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n'+'projecao; '+str(melhor_projecao).replace("'","").replace('[','').replace(']','').replace(',',';').replace('.',',')+'\n')
        arquivo_saida_filtro.write(str(line).replace("'","").replace('[','').replace(']','') + ',' + str(melhor_projecao[-12:]).replace("'","").replace('[','').replace(']','') + ',' + alerta58 + ',' + alerta59 + ',' + tendencia + '\n')

    h+=1
    print h, modelo




arquivo_saida_filtro.close()
arquivo_saida_usuario.close()
arquivo_entrada_vendas.close()
