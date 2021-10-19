#===================================================================================================#
'''
Versão 1.2
Autor: Victor S. Teixeira
LinkedIn: https://www.linkedin.com/in/victor-s-teixeira-022a5717b
e-mail: unieviteixeira@fei.edu.br

Sobre: 
Esse programa identifica qual processo termodinâmico ocorreu através dos dados 
de pressão e volume iniciais e finais e calcula os valores de trabalho(W), calor envolvido(Q)
e variação de energia interna(ΔEi).
Obs.: Essa é a atualização da versão 1.1 do programa. Agora é possível trabalhar com gases ideiais monoatômicos, diatômicos e poliatômicos.

Quaisquer dúvidas entre em contato com o desenvolvedor.
'''
#===================================================================================================#

from numpy import log as ln

print("="*60)
print("\033[1m CÁLCULO E IDENTIFICAÇÃO DE PROCESSOS TERMODINÂMICOS \033[0m".center(65))

#Informações
print("="*60)
print("\033[1;31mInserir os valores de pressão e\nvolume em notação científica!!!\033[0m")
print("Exemplo:\nPara \033[1;32m5.0x10^5\033[0m inserir \033[1;32m5.0e5\033[0m\nPara \033[1;32m3.4x10^-3\033[0m inserir \033[1;32m3.4e-3\033[0m")
print("="*60)
print("Constante γ:")
print("Monoatômico = 1.67\nDiatômico   = 1.4\nPoliatômico = 1.33")
#Entrada de valores
print('='*60)
gama = float(input("γ = "))
Pi   = float(input("Insira o valor da pressão inicial (x10^5 Pa): "))
Pf   = float(input("Insira o valor da pressão final (x10^5 Pa): "))
Vi   = float(input("Insira o valor do volume inicial (x10^-3 m³): ")) 
Vf   = float(input("Insira o valor do volume final (x10^-3 m³): "))
print('='*60)



#Variáveis auxiliares para o processo isobárico
Pt = Pf - Pi
Vt = Vf - Vi 

#Variáveis auxiliares para identificação do processo adiabático
P1 = Pi * (Vi ** gama)
P1 = round(P1, 3)
P2 = Pf * (Vf ** gama)
P2 = round(P2, 3)

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


#Identificando se é um processo isotérmico
if Pi * Vi == Pf * Vf or Pi * Vi <= Pf * Vf or Pi * Vi >= Pf * Vf  :
    if Pi * Vi <= Pf * Vf and ((100 * ((Pf * Vf) - (Pi * Vi)))/(Pf * Vf)) < 1:
        print("Processo termodinâmico: Isotérmico")     
        W = Pf * Vf * ln((Vf / Vi))
        Ei = 0
        print("W = {:.2f}J".format(W))
        print("Q = {:.2f}J".format(W))
        print("ΔEi =", Ei, "J")
        print('='*60)

    elif Pi * Vi >= Pf * Vf and ((100 * ((Pi * Vi) - (Pf * Vf)))/(Pi * Vi)) < 1:
        print("Processo termodinâmico: Isotérmico")     
        W = Pf * Vf * ln((Vf / Vi))
        Ei = 0
        print("W = {:.2f}J".format(W))
        print("Q = {:.2f}J".format(W))
        print("ΔEi =", Ei, "J")
        print('='*60)

    elif Pi * Vi == Pf * Vf:
        print("Processo termodinâmico: Isotérmico")     
        W = Pf * Vf * ln((Vf / Vi))
        Ei = 0
        print("W = {:.2f}J".format(W))
        print("Q = {:.2f}J".format(W))
        print("ΔEi =", Ei, "J")
        print('='*60)

#Identificando o processo adiabático
if P1 == P2 or P1 <= P2 or P1 >= P2:
    if P1 <= P2 and ((((100 *((P2 - P1))) / P2 )) < 1) and ((((100 *((P2 - P1))) / P2 )) > 0):
        print("Processo termodinâmico: Adiabático")
        W = ((Pi * Vi) - (Pf * Vf)) / (1 - gama)
        Ei = -W
        print("W = {:.2f}J".format(W))
        print("Q =", 0, "J")
        print("ΔEi = {:.2f}J".format(Ei))
        print('='*60)

    elif P1 >= P2 and ((((100 *((P1 - P2))) / P1 )) < 1) and ((((100 *((P1 - P2))) / P1 )) > 0):
        print("Processo termodinâmico: Adiabático")
        W = ((Pi * Vi) - (Pf * Vf)) / (1 - gama)
        Ei = -W
        print("W = {:.2f}J".format(W))
        print("Q =", 0, "J")
        print("ΔEi = {:.2f}J".format(Ei))
        print('='*60)
        
    elif P1 == P2:
        print("Processo termodinâmico: Adiabático")
        W = ((Pi * Vi) - (Pf * Vf)) / (1 - gama)
        Ei = -W
        print("W = {:.2f}J".format(W))
        print("Q =", 0, "J")
        print("ΔEi = {:.2f}J".format(Ei))
        print('='*60)

#Identificando se é um processo isocórico
if Vi == Vf:

        print("Processo termodinâmico: Isocórico") 
        Q = cv * (Pf - Pi) * Vf
        print("W = ", 0, "J")
        print("Q = {:.3f}J".format(Q))
        print("ΔEi = {:.3f}J".format(Q))
        print('='*60)

#Identificando se é um processo isobárico
if Pi == Pf:
    
        Pt = Pf
        print("Processo termodinâmico: Isobárico") 
        W = Pt * Vt 
        Q = cp * W
        Ei = cv * Pt * Vt 
        print("W = ", W, "J")
        print("Q =", Q, "J")
        print("ΔEi =", Ei, "J")
        print('='*60)
