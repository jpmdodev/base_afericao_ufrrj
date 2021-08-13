import pandas as pd
import numpy as np
from sympy import symbols, diff
import csv
from scipy import stats
import math as m
import json
#qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QFormLayout, QTableWidgetItem, QVBoxLayout, QDockWidget, QWidget
from PyQt5.QtGui import QColor
from pyqtgraph import TextItem

def lerDistancias(caminho, projeto, tabela, separador, am):
    planilha_distancias = pd.read_csv(caminho, sep=separador)
    planilha_distancias.to_csv(projeto+'/ferramenta4_amostra'+am+'.csv', index=False, sep=';')

    with open(projeto+'/ferramenta4_amostra'+am+'.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(3)
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

def plotarPyQtGraph(projeto, aba):
    #vetores, coordenadas e campanhas
    amostra1 = pd.read_csv(projeto+'/ferramenta4_amostra1.csv', sep=';')
    #amostra1 = pd.read_csv(projeto, sep=';')
    amostra2 = pd.read_csv(projeto+'/ferramenta4_amostra2.csv', sep=';')
    estacoes = amostra1["de"].unique().tolist()
    xis = amostra1.loc[amostra1['de'] == 1]['distancia'].unique().tolist()
    yo1 = -15
    yo2 = -50
    yi = 50

    #configurando grafico
    vetores = []
    conte = 0
    for e in estacoes:
        subAmostra = amostra1.loc[amostra1['de'] == e]
        yi+=yo2
        camp = []
        for i, row in subAmostra.iterrows():
            dist = row['distancia']
            if conte == 0:
                xs = [0, dist]
            else:
                xs = [xis[conte-1], xis[conte-1]+dist]
            ys = [yi, yi]
            camp.append(aba.plot(xs, ys, pen ='r', symbol ='t2', symbolPen ='r', symbolBrush =(255, 0, 0), symbolSize = 7))
            text = TextItem("E"+str(int(row['de']))+"-E"+str(int(row['ate']))+", "+str(round(row['distancia'], 2))+"m", anchor=(0,0.5))
            aba.addItem(text)
            if conte == 0:
                text.setPos(dist, yi)
            else:
                text.setPos(xis[conte-1]+dist, yi)
            yi+=yo1
        vetores.append(camp)
        conte+=1

    aba.setAspectLocked()

def ajustar(amostra, precisao):
    planilha = pd.read_csv(amostra, sep=';')
    estacoes = planilha["de"].unique().tolist()
    estacoes.sort()
    num = len(estacoes)+1

    simbolicos = symbols('D_1_2:%i'%(num+1))
    print(simbolicos)
    ind = symbols("A00")

    Lb=[]
    sLb=[]
    eqs=[]
    for e in estacoes:
        subPlanilha = planilha.loc[planilha['de'] == e]
        for i, row in subPlanilha.iterrows():
            de = int(row['de'])
            ate = int(row['ate'])
            d = row['distancia']
            #s = row['precisao']
            Lb.append(d)
            #sLb.append(s)
            if de == 1:
                eq = simbolicos[ate-2] + ind
                eqs.append(eq)
            else:
                eq = simbolicos[ate-2] - simbolicos[de-2] + ind
                eqs.append(eq)

    A = []
    for eq in eqs:
        row = []
        i = 0
        while i < num:
            if i == num-1:  
                row.append(int(diff(eq, ind).evalf()))
            else:
                row.append(int(diff(eq, simbolicos[i]).evalf()))
            i+=1
        A.append(row)
    P = np.identity(len(Lb))
    Lb = np.matrix(Lb).transpose()
    A = np.matrix(A)
    N = A.transpose()*P*A
    U = A.transpose()*P*Lb
    Xa = np.linalg.inv(N)*U
    V = A * Xa - Lb
    Vdp = np.std(V)
    q = np.sqrt((V.transpose()*V)[0,0])

    gl = len(Lb) - (len(simbolicos) + 1)
    chi = stats.chi2.ppf(0.95, gl)
    chid = precisao*np.sqrt(chi/gl)

    fd = stats.f.ppf(0.975, gl, gl)
    fe = 1/fd

    td = stats.t.ppf(0.975, gl)

    s = np.sqrt(q**2/gl)
    sA00 = s/np.sqrt(len(Lb)-1)
    return (q, s, sA00, chid, fe, fd, 0, sA00*td, Xa)

def calcular(projeto, aba_grafico, aba_relatorio):
    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
    ajuste1 = ajustar(projeto+'/ferramenta4_amostra1.csv', float(data['ferramenta4'][0]['precisao_nominal_a']))
    ajuste2 = ajustar(projeto+'/ferramenta4_amostra1.csv', float(data['ferramenta4'][0]['precisao_nominal_a']))
    print(ajuste1)

    distancias_corrigidas = np.array(ajuste1[8], dtype=float)
    print(distancias_corrigidas)
    yo1 = -15
    yi=100
    cont = 1
    for d in distancias_corrigidas:
        print(d)
        xs = [0, d[0]]
        ys = [yi, yi]
        aba_grafico.plot(xs, ys, pen ='g', symbol ='t2', symbolPen ='g', symbolBrush =(0, 255, 0), symbolSize = 7)
        text = TextItem("E"+str(cont)+"-E"+str(cont+1)+", "+str(round(d[0], 2))+"m", anchor=(0,0.5))
        aba_grafico.addItem(text)
        text.setPos(d, yi)
        yi+=yo1
        cont+=1

    if 0 < ajuste1[0] and ajuste1[0] <= ajuste1[3]:
        teste1 = 'APROVADO'
    else:
        teste1 = 'REPROVADO'
    rel = ajuste1[0]**2/ajuste2[0]**2
    if ajuste1[4] < rel and rel <= ajuste1[5]:
        teste2 = 'APROVADO'
    else:
        teste2 = 'REPROVADO'
    css = '''
        <style>
        H1 {
            font-family: Georgia, serif;
            font-size: 14px;
            font-weight: bold;
            color: #006600;
            letter-spacing: 1.4px;
            border-bottom: solid 1px #006600;
            text-transform: uppercase;
        }
        H2 {
            font-family: Georgia, serif;
            font-size: 12px;
            font-weight: normal;
            letter-spacing: 1.2px;
            color: #009900;
        }
        H3 {
            font-family: Georgia, serif;
            font-size: 12px;
            font-weight: normal;
            letter-spacing: 1.2px;
            color: #009900;
            text-align: center;
            border-bottom: solid 1px #006600;
        }
        P, BLOCKQUOTE {
            font-family: Verdana;
            font-size: 9px;
            color: #555555;
            line-height: 1.5;
            letter-spacing: .25px;
        }
        BLOCKQUOTE {
            font-family: Georgia, serif;
            font-style: italic;
            color: #444444;
            letter-spacing: 1.25px;
            line-height: 1.5;
            background: #EEEEEE;
            padding: 5px;
            margin: auto 15px;
        }
        A {
            color: #006600;
        }
        ABBR {
            border-bottom: dotted 1px #006600;
        }
        body {
  background: rgb(204,204,204); 
}
page {
  background: white;
  display: block;
  margin: 0 auto;
  margin-bottom: 0.5cm;
  box-shadow: 0 0 0.5cm rgba(0,0,0,0.5);
}
page[size="A4"] {  
  width: 21cm;
  height: 29.7cm; 
}
page[size="A4"][layout="landscape"] {
  width: 29.7cm;
  height: 21cm;  
}
page[size="A3"] {
  width: 29.7cm;
  height: 42cm;
}
page[size="A3"][layout="landscape"] {
  width: 42cm;
  height: 29.7cm;  
}
page[size="A5"] {
  width: 14.8cm;
  height: 21cm;
}
page[size="A5"][layout="landscape"] {
  width: 21cm;
  height: 14.8cm;  
}
@media print {
  body, page {
    margin: 0;
    box-shadow: 0;
  }
}
table {
  border-collapse: collapse;
  width: 75%;
margin-left: auto;
  margin-right: auto;
}

th, td {
            font-family: Verdana;
            font-size: 9px;
            color: #555555;
            line-height: 1.5;
            letter-spacing: .25px;
  text-align: left;
  padding: 8px;
}
        </style>
    '''
    relatorio = f'''
        <html>
            <head>
            {css}
            </head>
            <body>
                <page size="A4">
                    <h1>Universidade Federal Rural do Rio de Janeiro</h1>
                    <h2>Instituto de Tecnologia - Departamento de Engenharia</h2>
                    <h2>Engenharia de Agrimensura e Cartográfica</h2>

                    <h3>Relatório de Aferição de Distância Horizontal de Estação Total</h3>
                    <p><b>Expedição:</b> Universidade Federal Rural do Rio de Janeiro - Rodovia BR 465, KM7, Seropédica-RJ, CEP:23890-000</p>
                    <p><b>Validade:</b> Este certificado é válidado por 1 ano a partir da data da observação em conformidade a norma NBR 13133/1994</p>

                    <h2>Equipamento sob calibração:</h2>
                    <BLOCKQUOTE>
                    <p><b>Equipamento:</b> {data['ferramenta4'][0]['fabricante']}</p>        
                    <p><b>Modelo:</b> {data['ferramenta4'][0]['modelo']}</p>
                    <p><b>Série:</b> {data['ferramenta4'][0]['serie']}</p>
                    <p><b>Precisão linear nominal:</b> {data['ferramenta4'][0]['precisao_nominal_a']}</p>
                    </BLOCKQUOTE>

                    <h2>Precisão Operacional:</h2>
                    <BLOCKQUOTE>
                    <p><b>a:</b> {round(float(ajuste1[8][0]), 2)}</p>        
                    <p><b>b:</b> {round(float(ajuste1[8][1]), 2)}</p>
                    </BLOCKQUOTE>
                
                    <h3>Resumo do Processo de Aferição</h3>
                    <p>As observações foram feitas no CAMPO DE PROVA da UFRRJ, cuja coleta e o ajustamento pelo Método dos Mínimos Quadrados foram efetuados em conformidade com a norma ISO 17.123-3 em seu teste completo.</p>
                    <p>Para efeito de aferição, adotou-se como referência a precisão linear nominal do equipamento formecida pelo fabricante.</p>

                    <h3>Resultados obtidos após ajustamento das observações lineares</h3>
                    
                    <table border="1">
                    <tr>
                    <td>Precisão nominal</td>
                    <td>{data['ferramenta4'][0]['precisao_nominal_a']}</td>
                    </tr>
                    <tr>
                    <td>Desvio Padrão Experimental</td>
                    <td>{round(float(ajuste1[0]), 2)}</td>
                    </tr>
                    </table>
                    <br>
                    <br>

                    <h3>Teste estatístico (Incerteza de Medição)</h3>
                    
                    <table border="1">
                    <tr>
                    <td>Precisão nominal</td>
                    <td>{data['ferramenta4'][0]['precisao_nominal_a']}</td>
                    </tr>
                    <tr>
                    <td>Precisão experimental</td>
                    <td>{round(float(ajuste1[0]), 2)}</td>
                    </tr>
                    <tr>
                    <td>Teste1: </td>
                    <td>0</td>
                    <td>{round(float(ajuste1[0]), 2)}</td>
                    <td>{round(float(ajuste1[3]), 2)}</td>
                    <td>{teste1}</td>
                    </tr>
                    <tr>
                    <td>Teste2: </td>
                    <td>{round(float(ajuste1[4]), 2)}</td>
                    <td>{round(ajuste1[0]**2/ajuste2[0]**2, 2)}</td>
                    <td>{round(float(ajuste1[5]), 2)}</td>
                    <td>{teste2}</td>
                    </tr>
                    </table>
                    <br>
                    <br>

                    <p>Comparando o desvio padrão determinado, com 95% de probabilidade, com a precisão linear nominal do
equipamento, observa se que o mesmo está {teste1} em conformidade com a precisão linear nominal estabelecidade pelo
fabricante.</p>
                    <p>Certifica-se, portanto que, na presente data o equipamento está {teste1} em relação à precisão pradronizada pelo fabricante.</p>
            </body>
        </html>
    '''
    file = open(projeto+"/sample.html","w")
    file.write(relatorio)
    file.close()

    f = open(projeto+"/sample.html", 'r')
    file_contents = f.read()
    aba_relatorio.setHtml(file_contents)
#print(ajustar('dados_dist_teste.csv', 6, 1))
#plotarPyQtGraph('dados_dist_teste.csv', 6)

