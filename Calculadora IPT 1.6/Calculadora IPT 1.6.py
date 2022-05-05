#===================================================================================================#
'''
Calculadora para Identificação de Processos Termodinâmicos

Versão 1.6
Autor: Victor S. Teixeira
LinkedIn: https://www.linkedin.com/in/victor-s-teixeira-022a5717b
e-mail: unieviteixeira@fei.edu.br

Sobre: 
Esse programa identifica qual processo termodinâmico ocorreu através dos dados 
de pressão e volume iniciais e finais e calcula os valores de trabalho(W), calor envolvido(Q)
e variação de energia interna(ΔEi). Além disso ele plota o diagrama PxV e permite que o usuário descubra a constante adiabática, 
permitindo que o mesmo saiba se o gás em questão é mono, poli ou diatômico.

Obs.: Essa é a atualização da versão 1.6 do programa. Foram corrigidos alguns bugs, adicionada uma rotina para tratamento de erros 
e altereção na rotina que determina se o usuário vai ou não continuar utilizando o programa. Além disso foi implementada uma função 
que permite que o usuário descubra a constante adiabática.

Quaisquer dúvidas, bugs ou problemas durante a execução do programa entre em contato com o desenvolvedor.
'''

#==============================================BIBLIOTECA============================================#


from numpy import log as ln 
import numpy as np
import plotly.express as pl

#===========================FUNÇÃO 0: IDENTIFICAR SE O USUÁRIO TEM OU NÃO VALOR DE GAMA===========================#

def valor_gama():
    print("Obs.: A segunda opção é feita especificamente para ciclos\ntermodinâmicos ou em casos onde você tem um processo\nadiabático para ser usado como referência, dito isso\ndos primeiros valores de entrada devem ser de um adiabático!")
    print("")
    x = str(input('Você tem o valor de gama [S/N]? ')).strip().upper()
    
    while x not in 'SsNn':
        print("Responda apenas com 'S' par sim ou 'N' para não!!!")
        x = str(input('Você tem o valor de gama [S/N]? '))

    if x == 'S':
        n = 0
        return n

    elif x == 'N':   
        n = 1 
        return n

#===========================FUNÇÃO 1: ENTRADA DE VALORES(COM O VALOR DE GAMA)===========================#

def entrada_de_valores_com_gama():
    
#ENTRADA DE VALORES

        try:  
            print('='*60)
            g = float(input("γ = "))
            pi   = float(input("Insira o valor da pressão inicial: "))
            pf   = float(input("Insira o valor da pressão final: "))
            vi   = float(input("Insira o valor do volume inicial: ")) 
            vf   = float(input("Insira o valor do volume final: "))
            print('='*60)
        
        except Exception as  erro:
            print('='*60)
            print("Um dos valores inseridos não é um número,\nnão será possível realizar os cálculos.\nInsira os valores novamente!")
            entrada_de_valores_com_gama()



#Enfia os valores de entradaoara a função  "identifica_processo()"
        identifica_processo(g, pi, pf, vi, vf)

#===========================FUNÇÃO 2: IDENTIFICAÇÃO DOS PROCESSOS (COM O VALOR DE GAMA)===========================#

def identifica_processo(gama, Pi, Pf, Vi, Vf):

    #VARIÁVEIS AUXILIARES: ISOBÁRICO

            Pt = Pf - Pi
            Vt = Vf - Vi 

    #VARIÁVEIS AUXILIARES: ADIABÁICO

            P1 = Pi * (Vi ** gama)
            P1 = round(P1, 3)
            P2 = Pf * (Vf ** gama)
            P2 = round(P2, 3)

    #CONDIÇÃO PARA DIFERENCIAR OS VALORES DE CP E CV COM BASE NO TIPO DE GÁS

            if gama == 1.67 or gama == 1.4 or gama == 1.33:
                if gama == 1.67:
                    cv = (3/2)
                    cp = (5/2)

                elif gama == 1.4:
                    cv = (5/2)
                    cp = (7/2)

                elif gama == 1.33:
                    cv = 3
                    cp = 4   

     #IDENTIFICAÇÃO: ISOCÓRICO

            if Vi == Vf:

                processo = "Isocórico"

     #IDENTIFICAÇÃO: ISOBÁRICO

            elif Pi == Pf:  

                processo = "Isobárico"  
    
     #ANÁLISE: ISOTÉRMICO OU ADIABÁTICO?

            E_adi, Erro_isot = erro_percentual(P1, P2, Pi, Vi, Pf, Vf)
            
            if (Pi * Vi <= Pf * Vf) or (Pi * Vi >= Pf * Vf) or (P1 <= P2) or (P1 >= P2):

               if E_adi <= 10 or Erro_isot <= 10: 
               
                                    
                #ERRO PERCENTUAL: RESULTADOS
                  print("ADIABÁTICO: PERCENTUAL DE ERRO PiVi^γ = PfVf^γ: {:.5f}%".format(E_adi))
                  print("ISOTÉRMICO: PERCENTUAL DE ERRO Pi.Vi = Pf.Vf: {:.5f}%".format(Erro_isot))
                  print()
                  print("Com  base nesses dados qual é o processo?")
                  print()
                  resp1 = isotermico_ou_adiabatico() 

                  if resp1 == '1':

                    #IDENTIFICAÇÃO: ADIABÁTICO

                        processo = "Adiabático"
                 
                  if resp1 == '2':             
                                
                    #IDENTIFICAÇÃO: ISOTÉRMICO

                        processo = "Isotérmico"
              
            
     
     #Envia os dados para a função do respectivo processo

            if processo == "Isocórico":

               isocorico(Pi, Pf, Vi, Vf, cv)

            
            elif processo == "Isobárico":

                isobárico(Pi, Pf, Vi, Vf, cv, cp, Pt, Vt)

            elif processo == "Isotérmico":

                isotermico(Pi, Pf, Vi, Vf)    
            
            elif processo == "Adiabático":

                adiabatico(gama, Pi, Pf, Vi, Vf)

#===========================FUNÇÃO 3: CALCULA O PERCENTUAL DE ERRO PARA ISOTÉRMICO E ADIABÁTICO===========================#

def erro_percentual(p1, p2, PI, VI, PF, VF):

    #PERCENUAL DE ERRO: ADIABÁTICO
         
    if p1 >  p2:

        maior1 = p1 
        menor1 = p2
    
    elif p1 < p2:

        maior1 = p2  
        menor1 = p1  

    else:

        maior1 = p1
        menor1 = p2     

    Erro1 = (100 *((maior1 - menor1))) / maior1

    #PERCENTUAL DE ERRO: ISOTÉRMICO
    
    PV1 = PI * VI
    PV2 = PF * VF
    
    if  PV1 > PV2:

        maior2 = PV1
        menor2 = PV2
    
    elif  PV1 < PV2:

        maior2 = PV2
        menor2 = PV1
   
    else:

        maior2 = PV1
        menor2 = PV2

    Erro2 = (100 *((maior2 - menor2))) / maior2

    return Erro1, Erro2            

#===========================FUNÇÃO 5: VERIFICA SE O USUÁRIO SELECIONOU O ISOTÉRMICO OU ADIABÁTICO===========================#
def isotermico_ou_adiabatico():
    
    print('''
[1] Adiabático
[2] Isotérmico
            ''') 
    print('='*60)

    RESP = str(input("Qual opção deseja? "))

    print('='*60)

    while RESP not in ['1', '2']: 

        print("INSIRA APENAS '1' OU '2' !!!")
        RESP = input("Qual opção deseja? ")
        print('='*60)

    return RESP             

#===========================FUNÇÃO 6: PROCESSO ISOCÓRICO===========================#
def isocorico(Pi1, Pf1, Vi1, Vf1, cv1):

    #Cálculos: Trabalho, calor envolvido, variação de energia interna

    W = 0
    Q = cv1 * (Pf1 - Pi1) * Vf1
    Ei = Q

    #Resultado dos cálculos e nome do processo

    print("Processo termodinâmico: Isocórico") 
    print("W = {:.3f}J".format(W))
    print("Q = {:.3f}J".format(Q))
    print("ΔEi = {:.3f}J".format(Ei))
    print('='*60)

    #Diagrama PxV

    dd_x = [Vi1, Vf1]
    dd_y = [Pi1, Pf1]

    img = pl.line(x = dd_x, y = dd_y, title = "DIAGRAMA PxV: ISOCÓRICO", height = 400, width = 600, line_shape = 'spline')
    img.update_yaxes(title= 'PRESSÃO',title_font_color ='black', exponentformat = "power", ticks= 'outside', tickfont_color ='black')
    img.update_xaxes(title= 'VOLUME',title_font_color ='black', exponentformat = "power",  ticks = 'outside', tickfont_color ='black')
    img.show()

#VERIFICA SE O USUÁRIO QUER OU NÃO CONTINUAR USANDO A CALCULADORA

    calcular_novamente()

#===========================FUNÇÃO 6: PROCESSO ISOBÁRICO===========================#
def isobárico(Pi1, Pf1, Vi1, Vf1, cv1, cp1, Pt1, Vt1):

    #Cálculos: Trabalho, calor envolvido, variação de energia interna

    Pt1 = Pf1
    W = Pt1 * Vt1
    Q = cp1 * W
    Ei = cv1 * Pt1 * Vt1

    #Resultado dos cálculos e nome do processo

    print("Processo termodinâmico: Isobárico") 
    print("W = {:.3f}J".format(W))
    print("Q = {:.3f}J".format(Q))
    print("ΔEi = {:.3f}J".format(Ei))
    print('='*60)

    #Diagrama PxV

    dd_x = [Vi1, Vf1]
    dd_y = [Pi1, Pf1]

    img = pl.line(x = dd_x, y = dd_y, title = "DIAGRAMA PxV: ISOBÁRICO", height = 400, width = 600, line_shape = 'spline')
    img.update_yaxes(title= 'PRESSÃO',title_font_color ='black', exponentformat = "power", ticks= 'outside', tickfont_color ='black')
    img.update_xaxes(title= 'VOLUME',title_font_color ='black', exponentformat = "power",  ticks = 'outside', tickfont_color ='black')
    img.show()

#VERIFICA SE O USUÁRIO QUER OU NÃO CONTINUAR USANDO A CALCULADORA

    calcular_novamente()

#===========================FUNÇÃO 7: PROCESSO ISOTÉRMICO===========================#
def isotermico(Pi1, Pf1, Vi1, Vf1):

    #Cálculos: Trabalho, calor envolvido, variação de energia interna

    W = Pf1 * Vf1 * ln((Vf1 / Vi1))
    Q = W
    Ei = 0

    #Resultado dos cálculos e nome do processo

    print("Processo termodinâmico: Isotérmico") 
    print("W = {:.3f}J".format(W))
    print("Q = {:.3f}J".format(Q))
    print("ΔEi = {:.3f}J".format(Ei))
    print('='*60)

    #Diagrama PxV
    k = Pi1 * Vi1
   
    if Pi1 > Pf1:
      pr = np.arange(Pi1, Pf1, (Pf1-Pi1) / 20)

    else:
      pr = np.arange(Pf1, Pi1, (Pi1-Pf1) / 20)

    vl = k / pr

    img = pl.line(x = vl, y = pr, title = "DIAGRAMA PxV: ISOTÉRMICO", height = 400, width = 600, line_shape = 'spline')
    img.update_yaxes(title= 'PRESSÃO',title_font_color ='black', exponentformat = "power", ticks= 'outside', tickfont_color ='black')
    img.update_xaxes(title= 'VOLUME',title_font_color ='black', exponentformat = "power",  ticks = 'outside', tickfont_color ='black')
    img.show()

#VERIFICA SE O USUÁRIO QUER OU NÃO CONTINUAR USANDO A CALCULADORA

    calcular_novamente()

#===========================FUNÇÃO 8: PROCESSO ADIABÁTICO===========================#
def adiabatico(gama1, Pi1, Pf1, Vi1, Vf1):

    #Cálculos: Trabalho, calor envolvido, variação de energia interna

    W = (((Pi1 * Vi1) - (Pf1 * Vf1)) / (gama1 - 1))
    Q = 0
    Ei = -W
    #Resultado dos cálculos e nome do processo

    print("Processo termodinâmico: Adiabático") 
    print("W = {:.3f}J".format(W))
    print("Q = {:.3f}J".format(Q))
    print("ΔEi = {:.3f}J".format(Ei))
    print('='*60)

    #Diagrama PxV
    k = Pi1 * (Vi1 ** gama1)

    if Pi1 > Pf1:
      pr = np.arange(Pi1, Pf1, (Pf1-Pi1) / 20)

    else:
      pr = np.arange(Pf1, Pi1, (Pi1-Pf1) / 20)
    
    vl = k /pr 

    img = pl.line(x = vl, y = pr, title = "DIAGRAMA PxV: ADIABÁTICO", height = 400, width = 600, line_shape = 'spline')
    img.update_yaxes(title= 'PRESSÃO',title_font_color ='black', exponentformat = "power", ticks= 'outside', tickfont_color ='black')
    img.update_xaxes(title= 'VOLUME',title_font_color ='black', exponentformat = "power",  ticks = 'outside', tickfont_color ='black')
    img.show()

#VERIFICA SE O USUÁRIO QUER OU NÃO CONTINUAR USANDO A CALCULADORA

    calcular_novamente()

#===========================FUNÇÃO 9:ENTRADA DE VALORES SEM GAMA===========================#

def entrada_de_valores_sem_gama():   
 
    try:  

        print('='*60)
        pi   = float(input("Insira o valor da pressão inicial: "))
        pf   = float(input("Insira o valor da pressão final: "))
        vi   = float(input("Insira o valor do volume inicial: ")) 
        vf   = float(input("Insira o valor do volume final: "))
        print('='*60)
    
    except Exception as  erro:
        print('='*60)
        print("Um dos valores inseridos não é um número,\nnão será possível realizar os cálculos.\nInsira os valores novamente!")
        entrada_de_valores_sem_gama()



#Enfia os valores de entradaoara a função  "identifica_processo()"
    descobre_gama(pi, pf, vi, vf)

#===========================FUNÇÃO 10: DESCOBRE O VALOR DE GAMA========================#
def descobre_gama(pi1, pf1, vi1, vf1):

  P = (pi1/pf1)
  V = (vf1/vi1)

  mono = 1.67 * 0.05
  dia = 1.4 * 0.05
  poli = 1.33 * 0.05

  gama = ln(P) / ln(V)

  if gama >= (1.67  * (1 - mono)) and gama <= (1.67 * (1 + mono)) or  gama == 1.67:

      print("γ = {}".format(1.67))
      print("Você está trabalhando com um gás monoatômico!")
      print('='*60)
      r = calcular_com_gama()

      if r == 0:
        entrada_de_valores_com_gama2(1.67)

      elif r == 1:
    
        print("CALCULADORA ENCERRADA!!!")
        print('='*60)
        

  elif gama >= (1.4  * (1 - dia)) and gama <= (1.4 * (1 + dia)) or  gama == 1.4:

      print("γ = {}".format(1.4)) 
      print("Você está trabalhando com um gás diatômico!")
      print('='*60)
      r = calcular_com_gama()

      if r == 0:
        entrada_de_valores_com_gama2(1.4)


      elif r == 1:
    
        print("CALCULADORA ENCERRADA!!!")
        print('='*60)
        

  elif gama >= (1.33  * (1 - poli)) and gama <= (1.33 * (1 + poli)) or gama == 1.33:

      print("γ = {}".format(1.33)) 
      print("Você está trabalhando com um gás politômico!")
      print('='*60)
      r = calcular_com_gama()

      if r == 0:
        entrada_de_valores_com_gama2(1.33)

      
      elif r == 1:
    
        print("CALCULADORA ENCERRADA!!!")
        print('='*60)

  else:

      print("Os valores de entrada não condizem com um processo adiabático\nportanto não foi possível descobrir o valor de gama!")
      print("Insira novos valores que atendam o requisitado.")
      entrada_de_valores_sem_gama()

#===========================FUNÇÃO 11: VERIFICA SE O USUÁRIO QUER CALCULAR OUTRO PROCESSO COM 'γ'===========================#
def calcular_com_gama():
    x = str(input('Você deseja utilizar "γ" para calcular outro processo? [S/N] ')).strip().upper()
    
    while x not in 'SsNn':
        print("Responda apenas com 'S' par sim ou 'N' para não!!!")
        x = str(input('Você deseja utilizar "γ" para calcular outro processo? [S/N] '))

    if x == 'S':
        n = 0
        return n

    elif x == 'N':   
        n = 1 
        return n
#===========================FUNÇÃO 12: ENTRADA DE VALORES(COM O VALOR DE GAMA) 2===========================#

def entrada_de_valores_com_gama2(g1):
    
#ENTRADA DE VALORES
        g = g1

        try:  
            print('='*60)          
            pi   = float(input("Insira o valor da pressão inicial: "))
            pf   = float(input("Insira o valor da pressão final: "))
            vi   = float(input("Insira o valor do volume inicial: ")) 
            vf   = float(input("Insira o valor do volume final: "))
            print('='*60)
        
        except Exception as  erro:
            print('='*60)
            print("Um dos valores inseridos não é um número,\nnão será possível realizar os cálculos.\nInsira os valores novamente!")
            entrada_de_valores_com_gama()



#Enfia os valores de entradaoara a função  "identifica_processo()"
        identifica_processo(g, pi, pf, vi, vf)
 
#===========================FUNÇÃO 13: VERIFICA SE O USUÁRIO QUER CONINUAR CALCULANDO===========================#

def calcular_novamente():

   print('''
[1] Fazer outro cálculo
[2] Encerrar calculadora
            ''') 
   print('='*60)

   RESP = str(input("Qual opção deseja? "))

   while RESP not in ['1', '2']: 

        print("INSIRA APENAS '1' OU '2' !!!")
        RESP = input("Qual opção deseja? ")
        
   if RESP == '1':
     print('='*60)
     vg = valor_gama()

     if vg == 0:
      entrada_de_valores_com_gama()

     if vg == 1:
       entrada_de_valores_sem_gama() 


   elif RESP == '2':
      print('='*60)
      print("CALCULADORA ENCERRADA!!!")
      print('='*60)
      


#===========================PROGRAMA PRINCIPAL: INFORMAÇÕES===========================#

print("="*60)
print("\033[1m CÁLCULO E IDENTIFICAÇÃO DE PROCESSOS TERMODINÂMICOS \033[0m".center(65))
print("="*60)
print("\033[1;31mEm algumas situações é melhor inserir os\nvalores de pressão e volume em notação científica!!!\033[0m")
print("Exemplo:\nPara \033[1;32m5.0x10^5 Pa\033[0m inserir \033[1;32m5.0e5\033[0m\nPara \033[1;32m3.4x10^-3 m³\033[0m inserir \033[1;32m3.4e-3\033[0m")
print("="*60)
print("Constante γ:")
print("Monoatômico = 1.67\nDiatômico   = 1.4\nPoliatômico = 1.33")
print("="*60)

vg = valor_gama()

if vg == 0:
  entrada_de_valores_com_gama()
   
if vg == 1:
  entrada_de_valores_sem_gama()   