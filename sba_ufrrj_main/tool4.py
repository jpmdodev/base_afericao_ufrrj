import pandas as pd
import csv
from utilidades import Conversoes
from functools import partial
import math as m
import json
#qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QFormLayout, QTableWidgetItem, QVBoxLayout, QDockWidget, QWidget
from PyQt5.QtGui import QColor
from pyqtgraph import TextItem

def gerarRelatorio(projeto, webview):
    planilha_angulos = pd.read_csv(projeto+'/ferramenta3_resultados.csv', sep=';')
    tabela = planilha_angulos.to_html(classes='')
    tabela1 = planilha_angulos.iloc[:30,:].to_html(classes='')
    tabela2 = planilha_angulos.iloc[30:,:].to_html(classes='')
    print(tabela)
    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
    
    teste = ''
    precisao_fornecida = float(data['ferramenta3'][0]['precisao_angular_nominal'])
    precisao_obtida = 2*float(data['ferramenta3'][0]['desvio_padrao_exp_geral'])
    if precisao_fornecida < precisao_obtida/2:
        teste = 'NÃO'
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

                    <h3>Relatório de Aferição Angular Horizontal de Estação Total</h3>
                    <p><b>Expedição:</b> Universidade Federal Rural do Rio de Janeiro - Rodovia BR 465, KM7, Seropédica-RJ, CEP:23890-000</p>
                    <p><b>Validade:</b> Este certificado é válidado por 1 ano a partir da data da observação em conformidade a norma NBR 13133/1994</p>

                    <h2>Equipamento sob calibração:</h2>
                    <BLOCKQUOTE>   
                    <p><b>Proprietário:</b> {data['ferramenta3'][0]['proprietario']}</p>
                    <p><b>Equipamento:</b> {data['ferramenta3'][0]['marca']}</p>        
                    <p><b>Modelo:</b> {data['ferramenta3'][0]['modelo']}</p>
                    <p><b>Série:</b> {data['ferramenta3'][0]['serie']}</p>
                    <p><b>Precisão angular nominal:</b> {data['ferramenta3'][0]['precisao_angular_nominal']}</p>
                    <p><b>Operador:</b> {data['ferramenta3'][0]['operador']}</p>
                    <p><b>Anotador:</b> {data['ferramenta3'][0]['anotador']}</p>
                    </BLOCKQUOTE>

                    <h2>Condições de Observação:</h2>
                    <BLOCKQUOTE>   
                    <p><b>Data:</b> {data['ferramenta3'][0]['data']}</p>
                    <p><b>Horário de início:</b> {data['ferramenta3'][0]['horario_inicio']}</p>        
                    <p><b>Horário de término:</b> {data['ferramenta3'][0]['horario_termino']}</p>
                    <p><b>Temperatura:</b> {data['ferramenta3'][0]['temperatura']}</p>
                    <p><b>Pressão atmosférica:</b> {data['ferramenta3'][0]['pressao']}</p>
                    </BLOCKQUOTE>
                
                    <h3>Resumo do Processo de Aferição</h3>
                    <p>As observações foram feitas no CAMPO DE PROVA da UFRRJ, cuja coleta e o ajustamento pelo Método dos Mínimos Quadrados foram efetuados em conformidade com a norma ISO 17.123-3 em seu teste completo.</p>
                    <p>Para efeito de aferição, adotou-se como referência a precisão angular nominal do equipamento formecida pelo fabricante.</p>

                    <h3>Resultados obtidos após ajustamento das observações angulares horizontais</h3>
                    
                    <table border="1">
                    <tr>
                    <td>Precisão nominal</td>
                    <td>{data['ferramenta3'][0]['precisao_angular_nominal']}</td>
                    </tr>
                    <tr>
                    <td>Desvio Padrão Experimental</td>
                    <td>{round(float(data['ferramenta3'][0]['desvio_padrao_exp_geral']), 1)}</td>
                    </tr>
                    <tr>
                    <td>Desvio Padrão Experimental (95%)</td>
                    <td>{2*round(float(data['ferramenta3'][0]['desvio_padrao_exp_geral']), 1)}</td>
                    </table>
                    <br>
                    <br>

                    <p>Comparando o desvio padrão determinado, com 95% de probabilidade, com a precisão angular nominal do
equipamento, observa se que o mesmo {teste} está em conformidade com a precisão angular nominal estabelecidade pelo
fabricante.</p>
                    <p>Certifica-se, portanto que, na presente data o equipamento {teste} atende a precisão pradronizada pelo fabricante.</p>

                </page>
                <page size="A4">
                <h3>Memorial de Cálculo</h3>
                {tabela1}
                </page>
                <page size="A4">
                <h3>Memorial de Cálculo</h3>
                {tabela2}
                </page>
            </body>
        </html>
    '''
    file = open(projeto+"/sample.html","w")
    file.write(relatorio)
    file.close()

    f = open(projeto+"/sample.html", 'r')
    file_contents = f.read()
    webview.setHtml(file_contents)
...
def calcular(projeto, tabela):
    planilha_distancias = pd.read_csv(projeto+'/ferramenta4_distancias.csv', sep=';')
    series = planilha_distancias["serie"].unique().tolist()
    series.sort()
    conjuntos = planilha_distancias["conjunto"].unique().tolist()
    conjuntos.sort()
    alvos = planilha_distancias["alvo"].unique().tolist()
    alvos.sort()

    print(series)
    print(conjuntos)
    print(alvos)

    medias_distancias = []
    for s in series:
        for a in alvos:
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['serie'] == s]
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['alvo'] == a]
            medias_distancias.append(subplanilha_distancias['distanciah'].mean())
    print(medias_distancias)
    
    diferencas = []
    cont = 0
    for s in series:
        #cont = 0
        for c in conjuntos:
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['serie'] == s]
            subplanilha_distancias = subplanilha_distancias.loc[subplanilha_distancias['conjunto'] == c]
            j = 0
            for i, row in subplanilha_distancias.iterrows():
                diferenca = float(row['distanciah']) - medias_distancias[cont+j]
                print(f'''{float(row['distanciah'])}-{medias_distancias[cont+j]}''')
                print(diferenca)
                diferenca = round(diferenca, 4)
                diferencas.append(diferenca)
                j+=1
        cont+=5
    planilha_distancias['diferenca'] = diferencas

    medias_diferencas = []
    for s in series:
        for c in conjuntos:
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['serie'] == s]
            subplanilha_distancias = subplanilha_distancias.loc[subplanilha_distancias['conjunto'] == c]
            medias_diferencas.append(round(subplanilha_distancias['diferenca'].mean(), 4))
    print(medias_diferencas)

    desvios = []
    cont = 0
    for s in series:
        #cont = 0
        for c in conjuntos:
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['serie'] == s]
            subplanilha_distancias = subplanilha_distancias.loc[subplanilha_distancias['conjunto'] == c]
            for i, row in subplanilha_distancias.iterrows():
                desvio = float(row['diferenca']) - medias_diferencas[cont]
                desvios.append(round(desvio, 8))
            cont+=1
    planilha_distancias['desvio'] = desvios

    soma_desvios = []
    for s in series:
        for c in conjuntos:
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['serie'] == s]
            subplanilha_distancias = subplanilha_distancias.loc[subplanilha_distancias['conjunto'] == c]
            soma_desvios.append(round(subplanilha_distancias['desvio'].sum(), 4)) 

    desvios_quadrados = []
    for d in desvios:
        desvios_quadrados.append(round(d*d,4))
    planilha_distancias['desvio2'] = desvios_quadrados

    soma_desvios_quadrados = []
    for s in series:
        for c in conjuntos:
            subplanilha_distancias = planilha_distancias.loc[planilha_distancias['serie'] == s]
            subplanilha_distancias = subplanilha_distancias.loc[subplanilha_distancias['conjunto'] == c]
            soma_desvios_quadrados.append(subplanilha_distancias['desvio2'].sum()) 
    print(soma_desvios_quadrados)

    controle = 0
    sum_quadrado_res = []
    desvio_padrao_exp = []
    while controle < len(soma_desvios_quadrados):
        sum_quadrado_res.append(soma_desvios_quadrados[controle]+soma_desvios_quadrados[controle+1]+soma_desvios_quadrados[controle+2])
        desvio_padrao_exp.append(m.sqrt((soma_desvios_quadrados[controle]+soma_desvios_quadrados[controle+1]+soma_desvios_quadrados[controle+2])/8))
        controle+=3

    print(desvio_padrao_exp)

    desvio_padrao_exp_geral = m.sqrt(sum(sum_quadrado_res)/32)
    print(desvio_padrao_exp_geral)

    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
        data['ferramenta4'][0]['desvio_padrao_exp_geral'] = str(desvio_padrao_exp_geral)
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(data, outfile)

    #campo.setText(str(desvio_padrao_exp_geral))

    planilha_distancias.to_csv(projeto+'/ferramenta4_resultados.csv', index=False, sep=';')
    with open(projeto+'/ferramenta4_resultados.csv', newline='') as csv_file:
        tabela.setRowCount(0)
        tabela.setColumnCount(11)
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


def lerDistancias(caminho, projeto, tabela, separador):
    planilha_distancias = pd.read_csv(caminho, sep=';')
    print(planilha_distancias)

    #calculando distancias
    dists = []
    for i, row in planilha_distancias.iterrows():
        dist_pd = row['pd']
        dist_pi = row['pi']
        dist = (dist_pd+dist_pi)/2
        dists.append(round(dist, 8))
    planilha_distancias['distanciah'] = dists
    planilha_distancias.to_csv(projeto+'/ferramenta4_distancias.csv', index=False, sep=';')

    with open(projeto+'/ferramenta4_distancias.csv', newline='') as csv_file:
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