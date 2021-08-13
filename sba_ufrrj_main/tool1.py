#utilidades
from functools import partial
import pandas as pd
import numpy as np
from sympy import symbols, diff
import csv
from scipy import stats
import math as m
#qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QFormLayout, QTableWidgetItem, QVBoxLayout, QDockWidget, QWidget
from PyQt5.QtGui import QColor
from pyqtgraph import TextItem
class Conversoes:
    """
        Classe construída para conversão de unidades angulares.
    """
    @staticmethod
    def rad_para_grdec(ang):
        """
            Recebe um ângulo em radianos e retorna seu valor em graus decimais.
        """
        return ang * 180.0 / m.pi
        ...
    
    @staticmethod
    def rad_para_grsex(ang):
        """
            Recebe um ângulo em radianos e retorna uma string no formato
            sexagesimal.
        """
        conv = Conversoes
        aux_ang = conv.rad_para_grdec(ang)
        gr = int(aux_ang)
        aux_minutes = (aux_ang - gr) * 60
        minutes = int(aux_minutes)
        seconds = round((aux_minutes - minutes) * 60, 0)
        grsex = str(gr)+"g"+str(minutes)+"m"+str(seconds)+'s'
        return grsex
        ...
    
    @staticmethod
    def grsex_para_rad(ang):
        """
            Recebe uma string no formato sexagesimal e retorna o valor do
            ângulo em radianos.
        """
        aux_gr = ang.split("g")[0]
        gr = float(aux_gr)
        aux_minutes = ang.split("g")[1].split("m")[0]
        minutes = float(aux_minutes)
        aux_seconds = ang.split("m")[1].split('s')[0]
        seconds = float(aux_seconds)
        return (gr + minutes/60 + seconds/3600) * m.pi / 180
        ...
        
    @staticmethod
    def grsex_para_grdec(ang):
        """
            Recebe uma string no formato sexagesimal e retorna o valor do
            ângulo em graus decimais.
        """
        conv = Conversoes
        return conv.rad_para_grdec(conv.grsex_para_rad(ang))
        ...

    @staticmethod    
    def grdec_para_rad(ang):
        """
            Recebe um ângulo em graus decimais e retorna seu valor em radianos.
        """
        return ang * m.pi / 180
        ...

    @staticmethod
    def grdec_para_grsex(ang):
        """
            Recebe um ângulo em graus decimais e retorna uma string no formato
            sexagesimal.
        """
        conv = Conversoes
        return conv.rad_para_grsex(conv.grdec_para_rad(ang))
        ...
        
    @staticmethod
    def seg_para_grdec(seg):
        """
            Recebe os segundos no formato decimal e retorna em graus decimais.
        """
        return seg/3600
        ...     
...
def lerCoordenadas(caminho, tabela, projeto, injuncao, separador):
    planilha = pd.read_csv(caminho, sep=separador)
    planilha.to_csv(projeto+'/ferramenta1_coordenadas.csv', index=False, sep=";")
    pontos = planilha["ponto"].unique().tolist()
    pontos.sort()
    with open(projeto+'/ferramenta1_coordenadas.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(6)
        my_file = csv.reader(csv_file, delimiter=';')
        for row_data in my_file:
            row = tabela.rowCount()
            tabela.insertRow(row)
            if len(row_data) > 10:
                tabela.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                if row == 0:
                    item.setBackground(QColor(60,179,113))
                elif column == 0:
                    item.setBackground(QColor(144,238,144))
                tabela.setItem(row, column, item)
    for p in pontos:
        injuncao.addItem(p)
def lerCoordenadasSalvas(projeto, tabela, injuncao):
    planilha = pd.read_csv(projeto+'/ferramenta1_coordenadas.csv', sep=';')
    pontos = planilha["ponto"].unique().tolist()
    pontos.sort()
    with open(projeto+'/ferramenta1_coordenadas.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(6)
        my_file = csv.reader(csv_file, delimiter=';')
        for row_data in my_file:
            row = tabela.rowCount()
            tabela.insertRow(row)
            if len(row_data) > 10:
                tabela.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                if row == 0:
                    item.setBackground(QColor(60,179,113))
                elif column == 0:
                    item.setBackground(QColor(144,238,144))
                tabela.setItem(row, column, item)
    for p in pontos:
        injuncao.addItem(p)
...
def lerVetores(caminho, tabela, projeto, separador):
    planilha = pd.read_csv(caminho, sep=separador)
    planilha.to_csv(projeto+'/ferramenta1_vetores.csv', sep=";", index=False)
    with open(projeto+'/ferramenta1_vetores.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(7)
        my_file = csv.reader(csv_file, delimiter=';')
        for row_data in my_file:
            row = tabela.rowCount()
            tabela.insertRow(row)
            if len(row_data) > 10:
                tabela.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                if row == 0:
                    item.setBackground(QColor(60,179,113))
                elif column == 0:
                    item.setBackground(QColor(144,238,144))
                tabela.setItem(row, column, item)
...
def lerVetoresSalvos(projeto, tabela):
    with open(projeto+'/ferramenta1_vetores.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(7)
        my_file = csv.reader(csv_file, delimiter=';')
        for row_data in my_file:
            row = tabela.rowCount()
            tabela.insertRow(row)
            if len(row_data) > 10:
                tabela.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                if row == 0:
                    item.setBackground(QColor(60,179,113))
                elif column == 0:
                    item.setBackground(QColor(144,238,144))
                tabela.setItem(row, column, item)
...
def plotarPyQtGraph(projeto, aba, legendas):
    #vetores, coordenadas e campanhas
    planilha1 = pd.read_csv(projeto+'/ferramenta1_coordenadas.csv', sep=';')
    planilha2 = pd.read_csv(projeto+'/ferramenta1_vetores.csv', sep=';')
    campanhas = planilha2["campanha"].unique().tolist()
    #print(campanhas)
    #configurando grafico
    vetores = []
    for c in campanhas:
        subPlanilha2 = planilha2.loc[planilha2['campanha'] == c]
        camp = []
        for i, row in subPlanilha2.iterrows():
            row_ate = planilha1.loc[(planilha1['campanha'] == row['campanha']) & (planilha1['ponto'] == row['ate'])]
            row_de = planilha1.loc[(planilha1['campanha'] == row['campanha']) & (planilha1['ponto'] == row['de'])]
            xs = [row_de.iloc[0]['x'], row_ate.iloc[0]['x']]
            ys = [row_de.iloc[0]['y'], row_ate.iloc[0]['y']]
            camp.append(aba.plot(xs, ys))
        vetores.append(camp)
    pontos = []
    for c in campanhas:
        subPlanilha1 = planilha1.loc[planilha1['campanha'] == c]
        #print(subPlanilha1)
        #print(subPlanilha1['x'])
        #print(subPlanilha1['y'])
        pontos.append(aba.plot(subPlanilha1['x'].tolist(), subPlanilha1['y'].tolist(), pen=None, symbol='o'))
    #print(vetores)

    aba.setAspectLocked()
    for i, row in planilha1.iterrows():
        text = TextItem("("+row['ponto']+", "+str(row['x'])+", "+str(row['y'])+", "+str(row['campanha'])+")", anchor=(0.5, -1.0))
        aba.addItem(text)
        text.setPos(row['x'], row['y'])

    #legandas vetores
    linhas = []
    for c in campanhas:
        checkbox = QCheckBox('Campanha '+str(c))
        checkbox.setChecked(True)
        linhas.append(checkbox)
    def checkState(plt, check, desenhos):
        if check.isChecked():
            for desenho in desenhos:
                plt.addItem(desenho)
        else:
            for desenho in desenhos:
                plt.removeItem(desenho)
    layout = QFormLayout()
    labelVetores = QLabel(text='Vetores')
    layout.addRow(labelVetores)
    comandos = []
    i = 0
    for l in linhas:
        comandos.append(partial(checkState, aba, l, vetores[i]))
        l.stateChanged.connect(comandos[i])
        layout.addRow(l)
        i+=1

    #legendas pontos
    linhasPontos = []
    for c in campanhas:
        checkbox = QCheckBox('Campanha '+str(c))
        checkbox.setChecked(True)
        linhasPontos.append(checkbox)
    def checkStatePontos(plt, check, desenhos):
        if check.isChecked():
            plt.addItem(desenhos)
        else:
            plt.removeItem(desenhos)
    labelPontos = QLabel(text='Pontos')
    layout.addRow(labelPontos)
    comandosPontos = []
    i = 0
    for l in linhasPontos:
        comandosPontos.append(partial(checkStatePontos, aba, l, pontos[i]))
        l.stateChanged.connect(comandosPontos[i])
        layout.addRow(l)
        i+=1

    
    legendas.setLayout(layout)
...
def elipse(varX, varY, covarXY, oX, oY, aba):
    conv = Conversoes()
    M = m.sqrt(4*covarXY**2+(varX-varY)**2)
    varMax = (varX+varY+M)/2
    varMin = (varX+varY-M)/2
    a = m.sqrt(varMax)
    b = m.sqrt(varMin)
    if(covarXY == 0):
        if(varX >= varY):
            t = 0
        else:
            t = 90
    else:
        if(varX == varY):
            if(covarXY > 0):
                t = 45
            else:
                t = 135
        else:
            t2 = conv.rad_para_grdec(m.atan(abs(2*covarXY/(varX-varY))))
            if(covarXY > 0):
                if(varX > varY):
                    t = t2/2
                else:
                    t = (180-t2)/2
            else:
                if(varX < varY):
                    t = (180+t2)/2
                else:
                    t = (360-t2)/2
    N = 60
    theta = np.linspace(0, 2*m.pi, N)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    X = x * np.cos(conv.grdec_para_rad(t)) - y * np.sin(conv.grdec_para_rad(t))
    Y = x * np.sin(conv.grdec_para_rad(t)) + y * np.cos(conv.grdec_para_rad(t))
    X = X + oX
    Y = Y + oY
    X = X.tolist()
    Y = Y.tolist()
    aba.plot(X[0], Y[0], pen=(255, 0, 0))
    aba.setAspectLocked()
    #print([a, b, t])
    return [a, b, t]
...
def ajustar(projeto, injuncao, tolerancia, tabela, texto, aba):
    #vetores, coordenadas, campanhas e pontos
    planilha1 = pd.read_csv(projeto+'/ferramenta1_coordenadas.csv', sep=';')
    planilha2 = pd.read_csv(projeto+'/ferramenta1_vetores.csv', sep=';')
    campanhas = planilha2["campanha"].unique().tolist()
    campanhas.sort()
    pontos = planilha1["ponto"].unique().tolist()
    pontos.sort()

    #montando vetor Lb e sLb
    Lb=[]
    sLb=[]
    for c in campanhas:
        subPlanilha2 = planilha2.loc[planilha2['campanha'] == c]
        for i, row in subPlanilha2.iterrows():
            row_ate = planilha1.loc[(planilha1['campanha'] == row['campanha']) & (planilha1['ponto'] == row['ate'])]
            row_de = planilha1.loc[(planilha1['campanha'] == row['campanha']) & (planilha1['ponto'] == row['de'])]
            if(row_ate.iloc[0]['ponto'] == injuncao[0]):
                dy = row_ate.iloc[0]['y'] - row_de.iloc[0]['y'] - injuncao[1]
                dx = row_ate.iloc[0]['x'] - row_de.iloc[0]['x'] - injuncao[2]
                dz = row_ate.iloc[0]['z'] - row_de.iloc[0]['z'] - injuncao[3]
            elif(row_de.iloc[0]['ponto'] == injuncao[0]):
                dy = row_ate.iloc[0]['y'] - row_de.iloc[0]['y'] + injuncao[1]
                dx = row_ate.iloc[0]['x'] - row_de.iloc[0]['x'] + injuncao[2]
                dz = row_ate.iloc[0]['z'] - row_de.iloc[0]['z'] + injuncao[3]
            else:
                dy = row_ate.iloc[0]['y'] - row_de.iloc[0]['y']
                dx = row_ate.iloc[0]['x'] - row_de.iloc[0]['x']
                dz = row_ate.iloc[0]['z'] - row_de.iloc[0]['z']
            Lb.append(dy)
            Lb.append(dx)
            Lb.append(dz)
            sLb.append(row['dpy'])
            sLb.append(row['dpx'])
            sLb.append(row['dpz'])

    #Calculando matriz P (Peso)
    P = np.diag(np.power(sLb, -2))
    P = P*5E-02

    df = pd.DataFrame(data=P.astype(float))
    df.to_csv(projeto+'/debug_p.csv', sep=';', header=False, float_format='%.11f', index=False)

    #Criando variaveis simbolicas
    simbolicos_x = symbols('XP0:%i'%len(pontos))
    simbolicos_y = symbols('YP0:%i'%len(pontos))
    simbolicos_z = symbols('ZP0:%i'%len(pontos))

    #Criando funcoes simbolicas
    funcoes = []
    for i, row in planilha2.iterrows():
        indice_ate = int(row['ate'][1])
        indice_de = int(row['de'][1])
        if(row['ate'] == injuncao[0]):
            dy = simbolicos_y[indice_ate] - simbolicos_y[indice_de] - injuncao[1]
            dx = simbolicos_x[indice_ate] - simbolicos_x[indice_de] - injuncao[2]
            dz = simbolicos_z[indice_ate] - simbolicos_z[indice_de] - injuncao[3]
        elif(row['de'] == injuncao[0]):
            dy = simbolicos_y[indice_ate] - simbolicos_y[indice_de] + injuncao[1]
            dx = simbolicos_x[indice_ate] - simbolicos_x[indice_de] + injuncao[2]
            dz = simbolicos_z[indice_ate] - simbolicos_z[indice_de] + injuncao[3]
        else:
            dy = simbolicos_y[indice_ate] - simbolicos_y[indice_de]
            dx = simbolicos_x[indice_ate] - simbolicos_x[indice_de]
            dz = simbolicos_z[indice_ate] - simbolicos_z[indice_de]
        funcoes.append(dy)
        funcoes.append(dx)
        funcoes.append(dz)

    #Montando matriz A
    A = []
    for f in funcoes:
        row = []
        i = 0
        while i < len(pontos):
            if(int(injuncao[0][1])!=i):    
                row.append(int(diff(f, simbolicos_y[i]).evalf()))
                row.append(int(diff(f, simbolicos_x[i]).evalf()))
                row.append(int(diff(f, simbolicos_z[i]).evalf()))
                i+=1
            else:
                i+=1
        A.append(row)

    Lb = np.matrix(Lb).transpose()
    df = pd.DataFrame(data=Lb.astype(float))
    df.to_csv(projeto+'/debug_lb.csv', sep=';', header=False, float_format='%.4f', index=False)
    A = np.matrix(A)
    df = pd.DataFrame(data=A.astype(float))
    df.to_csv(projeto+'/debug_a.csv', sep=';', header=False, float_format='%.4f', index=False)
    N = A.transpose()*P*A
    df = pd.DataFrame(data=N.astype(float))
    df.to_csv(projeto+'/debug_n.csv', sep=';', header=False, float_format='%.4f', index=False)
    U = A.transpose()*P*Lb
    df = pd.DataFrame(data=U.astype(float))
    df.to_csv(projeto+'/debug_u.csv', sep=';', header=False, float_format='%.4f', index=False)
    Xa = np.linalg.inv(N)*U
    df = pd.DataFrame(data=Xa.astype(float))
    df.to_csv(projeto+'/debug_xa.csv', sep=';', header=False, float_format='%.4f', index=False)

    relatorio = open(projeto+'/ferramenta1_relatorio.txt',"w")

    relatorio.write('Observações e Parâmetros\n-------------------------------\n')

    n = len(Lb)
    relatorio.write('Número de Observações (n) = '+str(n)+'\n')
    u = len(Xa)
    relatorio.write('Número de Parâmetros (u) = '+str(u)+'\n')

    relatorio.write('\nResíduos\n-------------------------------\n')

    V = A * Xa - Lb
    Vmax = np.max(np.abs(V))
    relatorio.write('Resíduo Máximo (Vmax) = '+str(Vmax)+'\n')
    Vmin = np.min(np.abs(V))
    relatorio.write('Resíduo Mínimo (Vmax) = '+str(Vmin)+'\n')
    Vmedio = np.mean(V)
    relatorio.write('Resíduo Médio (Vm) = '+str(Vmedio)+'\n')
    Vdp = np.std(V)
    Rms = np.sqrt(np.sum(np.power(V, 2))/len(Lb))
    relatorio.write('Erro Médio Quadrático (RMSE) = '+str(Rms)+'\n')
    
    relatorio.write('\nAnálise do Ajustamento\n-------------------------------\n')
    chi_calc = V.transpose()*P*V
    relatorio.write('Qui calculado (Qc) = '+str(chi_calc)+'\n')
    chi_teorico1 = stats.chi2.ppf(0.025, len(Lb) - len(Xa))
    relatorio.write('Qui teórico inferior (Qt1) = '+str(chi_teorico1)+'\n')
    chi_teorico2 = stats.chi2.ppf(0.975, len(Lb) - len(Xa))
    relatorio.write('Qui teórico superior (Qt2) = '+str(chi_teorico2)+'\n')
    if chi_calc > chi_teorico1 and chi_calc < chi_teorico2:
        relatorio.write('... Qt1 < Qc < Qt2 => Hipótese básica foi aceita!\n')
    else:
        relatorio.write('... => Hipótese básica rejeitada!\n')
        
    if np.abs(Rms) < tolerancia:
        relatorio.write('... => Os resíduos estão dentro da tolerância!\n')
    else:
        relatorio.write('... => Os resíduos estão fora da tolerância!\n')
    spost = (V.transpose()*P*V)/(len(Lb)-len(Xa))
    relatorio.write('Sigma a posteriori = '+str(spost)+'\n')

    #Matriz Variancia-Covariancia dos Pârametros Ajustados
    MVC_Xa = spost[0,0]*np.linalg.inv(A.transpose()*P*A)
    df = pd.DataFrame(data=MVC_Xa.astype(float))
    df.to_csv(projeto+'/debug_mvc_xa.csv', sep=';', header=False, float_format='%.9f', index=False)
    #Precisão dos Parâmetros Ajustados
    PXa = np.sqrt(np.abs(np.diag(MVC_Xa)))

    #Tabela de Coordenadas Finais
    futureDf = []
    contador = 0
    num_estacoes = 0
    while contador < (len(pontos)-1)*3:
        row = []
        if(pontos[num_estacoes] == injuncao[0]):
            num_estacoes+=1
        row.append(pontos[num_estacoes])
        row.append(Xa[contador, 0])
        row.append(Xa[contador+1, 0])
        row.append(Xa[contador+2, 0])
        row.append(PXa[contador])
        row.append(PXa[contador+1])
        row.append(PXa[contador+2])
        futureDf.append(row)
        contador+=3
        num_estacoes+=1
    coordenadas_ajustadas = pd.DataFrame (futureDf,columns=['Ponto', 'Ya','Xa','Za', 'Py', 'Px', 'Pz'])
    coordenadas_ajustadas.to_csv(projeto+'/ferramenta1_coordenadas_ajustadas.csv', index=False, sep=";")
    aba.plot(coordenadas_ajustadas['Xa'].tolist(), coordenadas_ajustadas['Ya'].tolist(), pen=None, symbol='o')
    aba.plot([injuncao[2]], [injuncao[1]], pen=None, symbol='+')
    text = TextItem("(Injunção"", "+str(injuncao[2])+", "+str(injuncao[2])+")", anchor=(0.5, -1.0))
    aba.addItem(text)
    text.setPos(injuncao[2], injuncao[1])
    for i, row in coordenadas_ajustadas.iterrows():
        text = TextItem("("+row['Ponto']+", "+str(row['Xa'])+", "+str(row['Ya'])+")", anchor=(0.5, -1.0))
        aba.addItem(text)
        text.setPos(row['Xa'], row['Ya'])
    
    with open(projeto+'/ferramenta1_coordenadas_ajustadas.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(7)
        my_file = csv.reader(csv_file, delimiter=';')
        for row_data in my_file:
            row = tabela.rowCount()
            tabela.insertRow(row)
            if len(row_data) > 10:
                tabela.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                if row == 0:
                    item.setBackground(QColor(60,179,113))
                elif column == 0:
                    item.setBackground(QColor(144,238,144))
                tabela.setItem(row, column, item)
    #Tabela de Coordenadas Finais

    num_estacoes = 0
    contador = 0
    while contador < (len(pontos)-1)*3:
        if(pontos[num_estacoes] == injuncao[0]):
            num_estacoes+=1
        elipse(MVC_Xa[contador+1, contador+1], MVC_Xa[contador, contador], MVC_Xa[contador, contador+1], Xa[contador+1], Xa[contador], aba)
        contador+=3

    relatorio.close()
    relatorio = open(projeto+'/ferramenta1_relatorio.txt').read()
    texto.setPlainText(relatorio)

#ajustar('C:\\Users\\jpmdo\\Desktop\\P900', ['P1', 7480944.663, 633837.652, 10.934], 0.004)