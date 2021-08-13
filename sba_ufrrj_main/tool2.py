from sympy import symbols, diff
import pandas as pd
import numpy as np
import csv
from utilidades import azimute
from functools import partial
from scipy import stats
#qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QFormLayout, QTableWidgetItem, QVBoxLayout, QDockWidget, QWidget
from PyQt5.QtGui import QColor
from pyqtgraph import TextItem

def lerCoordenadas(caminho, tabela, tabela2, projeto, separador):
    planilha_coordenadas = pd.read_csv(caminho, sep=separador)
    planilha_coordenadas.to_csv(projeto+'/ferramenta2_coordenadas.csv', index=False, sep=separador)
    with open(projeto+'/ferramenta2_coordenadas.csv', newline='') as csv_file:
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
    #calculando azimutes
    campanhas = planilha_coordenadas["campanha"].unique().tolist()
    campanhas.sort()
    pontos = planilha_coordenadas["ponto"].unique().tolist()
    pontos.sort()
    azimutes = []
    cont_campanha = 1
    for c in campanhas:
        subplanilha_coordenadas = planilha_coordenadas.loc[planilha_coordenadas['campanha'] == c]
        for i, row in subplanilha_coordenadas.iterrows():
            linha = []
            row_de = subplanilha_coordenadas.loc[(subplanilha_coordenadas['ponto'] == 'P0')]
            row_ref = subplanilha_coordenadas.loc[(subplanilha_coordenadas['ponto'] == 'P1')]
            if(row['ponto'] != row_de.iloc[0]['ponto']):
                linha.append(c)
                linha.append('P0')
                linha.append(row['ponto'])
                linha.append(azimute(row_de.iloc[0]['x'], row_de.iloc[0]['y'], row['x'], row['y']))
                linha.append(azimute(row_de.iloc[0]['x'], row_de.iloc[0]['y'], row_ref.iloc[0]['x'], row_ref.iloc[0]['y']))
                az_ref = linha[3]-linha[4]
                if az_ref < 0:
                    az_ref+=360
                linha.append(az_ref)
                azimutes.append(linha)
        cont_campanha+=1
        if(cont_campanha >= len(pontos)):
            cont_campanha = 1
    planilha_azimutes = pd.DataFrame(azimutes,columns=['campanha', 'de','ate','azimute', 'azimute_referencia', 'diferenca'])
    planilha_azimutes.to_csv(projeto+'/ferramenta2_azimutes.csv', index=False, sep=";")
    with open(projeto+'/ferramenta2_azimutes.csv', newline='') as csv_file:
        tabela2.setRowCount(0)
        tabela2.setColumnCount(6)
        my_file = csv.reader(csv_file, delimiter=';')
        for row_data in my_file:
            row = tabela2.rowCount()
            tabela2.insertRow(row)
            if len(row_data) > 10:
                tabela2.setColumnCount(len(row_data))
            for column, stuff in enumerate(row_data):
                item = QTableWidgetItem(stuff)
                if row == 0:
                    item.setBackground(QColor(60,179,113))
                elif column == 0:
                    item.setBackground(QColor(144,238,144))
                tabela2.setItem(row, column, item)
...
def plotarPyQtGraph(projeto, aba, legendas):
    #vetores, coordenadas e campanhas
    planilha1 = pd.read_csv(projeto+'/ferramenta2_coordenadas.csv', sep=';')
    planilha2 = pd.read_csv(projeto+'/ferramenta2_azimutes.csv', sep=';')
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

    arcos = []
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
def ajustar(projeto, tolerancia, peso, tabela, texto):
    planilha1 = pd.read_csv('1dados/dados_azimutes.csv', sep=';')
    campanhas = planilha1["campanha"].unique().tolist()
    campanhas.sort()
    pontos = planilha1["ate"].unique().tolist()
    pontos.sort()

    simbolos = symbols('AzP1:%i'%(len(pontos)+1))
    
    print(simbolos)
    Lb = []
    equacoes = []
    cont_campanha = 0
    for c in campanhas:
        subPlanilha1 = planilha1.loc[planilha1['campanha'] == c]
        azimutes = subPlanilha1['diferenca'].tolist()
        i = cont_campanha+1
        num_azimutes = 0
        while num_azimutes != len(azimutes)-1:
            if i >= len(azimutes):
                i = 0
            resultado = azimutes[i] - azimutes[cont_campanha]
            if resultado < 0:
                obs = resultado + 360
                eq = simbolos[i] - simbolos[cont_campanha] + 360
            else:
                eq = simbolos[i] - simbolos[cont_campanha]
                obs = resultado
            equacoes.append(eq)
            Lb.append(obs)
            num_azimutes+=1
            i+=1
        cont_campanha+=1
    Lb = np.matrix(Lb).transpose()
    print('Lb')
    print(Lb)

    P = np.eye(len(Lb)) * peso
    print(P)

    
    subPlanilha1 = planilha1.loc[planilha1['campanha'] == 1]
    Xo = subPlanilha1['diferenca'].tolist()
    Xo.remove(0)

    n = len(Lb)
    u = len(Xo)

    Xo = np.matrix(Xo).transpose()
    print('Xo')
    print(Xo)
    Xa = Xo
    print('Xa')
    print(Xa)

    iteracao = 0
    correcao = 1
    while correcao > tolerancia:
        Lo = []
        for e in equacoes:
            subs = []
            i = 0
            while i < len(simbolos):
                if i != 0:
                    subs.append((simbolos[i], Xa[i-1,0]))
                    i+=1
                else:
                    subs.append((simbolos[i], 0))
                    i+=1
            print(subs)
            print(e.subs(subs))
            Lo.append(e.subs(subs))
        Lo = np.matrix(Lo).transpose()
        df = pd.DataFrame(data=Lo.astype(float))
        df.to_csv(projeto+'/ferramenta2_debug_Lo.csv', sep=';', header=False, float_format='%.4f', index=False)

        L = Lo - Lb
        df = pd.DataFrame(data=L.astype(float))
        df.to_csv(projeto+'/ferramenta2_debug_L.csv', sep=';', header=False, float_format='%.4f', index=False)
            
        A = []
        for e in equacoes:
            row = []
            i = 0
            while i < len(Xa):
                row.append(int(diff(e, simbolos[i+1]).evalf()))
                i+=1
            A.append(row)
        A = np.matrix(A)
        df = pd.DataFrame(data=A.astype(float))
        df.to_csv(projeto+'/ferramenta2_debug_A.csv', sep=';', header=False, float_format='%.4f', index=False)

        Xc = -np.linalg.inv(A.transpose()*P*A)*A.transpose()*P*L
        df = pd.DataFrame(data=Xc.astype(float))
        df.to_csv(projeto+'/ferramenta2_debug_Xc.csv', sep=';', header=False, float_format='%.4f', index=False)
        Xa = Xo + Xc
        df = pd.DataFrame(data=Xa.astype(float))
        df.to_csv(projeto+'/ferramenta2_debug_Xa.csv', sep=';', header=False, float_format='%.4f', index=False)
        Xo = Xa
        correcao = np.max(np.abs(Xc))
        print(correcao)
        iteracao = iteracao+1
        print(iteracao)

    relatorio = open(projeto+'/ferramenta2_relatorio.txt',"w")

    relatorio.write('Observações e Parâmetros\n-------------------------------\n')

    n = len(Lb)
    relatorio.write('Número de Observações (n) = '+str(n)+'\n')
    u = len(Xa)
    relatorio.write('Número de Parâmetros (u) = '+str(u)+'\n')

    relatorio.write('\nResíduos\n-------------------------------\n')

    v = A * Xc + L
    Vmax = np.max(np.abs(v))
    relatorio.write('Resíduo Máximo (Vmax) = '+str(Vmax)+'\n')
    Vmin = np.min(np.abs(v))
    relatorio.write('Resíduo Mínimo (Vmax) = '+str(Vmin)+'\n')
    Vmedio = np.mean(v)
    relatorio.write('Resíduo Médio (Vm) = '+str(Vmedio)+'\n')
    v = v.astype(float)
    Vdp = np.std(v)
    Rms = np.sqrt(np.sum(np.power(v, 2))/len(Lb))
    relatorio.write('Erro Médio Quadrático (RMSE) = '+str(Rms)+'\n')

    relatorio.write('\nAnálise do Ajustamento\n-------------------------------\n')
    chi_calc = v.transpose()*P*v
    print(chi_calc)
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
    spost = (v.transpose()*P*v)/(len(Lb)-len(Xa))
    relatorio.write('Sigma a posteriori = '+str(spost)+'\n')

    #Matriz Variancia-Covariancia dos Pârametros Ajustados
    MVC_Xa = spost[0,0]*np.linalg.inv(A.transpose()*P*A)
    df = pd.DataFrame(data=MVC_Xa.astype(float))
    df.to_csv(projeto+'/ferramenta2_debug_mvc_Xa.csv', sep=';', header=False, float_format='%.9f', index=False)
    
    #Precisão dos Parâmetros Ajustados
    PXa = np.sqrt(np.abs(np.diag(MVC_Xa)))
    print(PXa)

    #Tabela de ângulos Finais
    futureDf = []
    contador = 0
    while contador < len(pontos)-1:
        row = []
        row.append('P0')
        row.append(str(contador+1))
        row.append(Xa[contador, 0])
        row.append(PXa[contador])
        futureDf.append(row)
        contador+=1
    angulos_ajustados = pd.DataFrame (futureDf,columns=['De', 'Até', 'Azimute','Precisão'])
    angulos_ajustados.to_csv(projeto+'/ferramenta2_angulos_ajustados.csv', index=False, sep=";")
    
    """
    #Matriz Variancia-Covariancia das Observações
    MVC_La = spost[0,0]*(A*np.linalg.inv(A.transpose()*P*A)*A.transpose())
    df = pd.DataFrame(data=MVC_La.astype(float))
    df.to_csv(projeto+'/ferramenta2_debug_mvc_La.csv', sep=';', header=False, float_format='%.9f', index=False)

    #Precisão das Observações Ajustadas
    PLa = np.sqrt(np.abs(np.diag(MVC_La)))
    print(PLa)
    """

    with open(projeto+'/ferramenta2_angulos_ajustados.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(4)
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

    """
    num_estacoes = 0
    contador = 0
    while contador < (len(pontos)-1)*3:
        if(pontos[num_estacoes] == injuncao[0]):
            num_estacoes+=1
        elipse(MVC_Xa[contador+1, contador+1], MVC_Xa[contador, contador], MVC_Xa[contador, contador+1], Xa[contador+1], Xa[contador], aba)
        contador+=3
    """

    relatorio.close()
    relatorio = open(projeto+'/ferramenta2_relatorio.txt').read()
    texto.setPlainText(relatorio)

...