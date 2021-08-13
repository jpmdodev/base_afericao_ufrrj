#utilidades
import sys
from datetime import date
from functools import partial
from os import getenv
from os import listdir
from os.path import isfile, join
import json
#scripts
import tool4d
#qt
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QAction, QHBoxLayout, QListWidget, QDialog, QCheckBox, QProgressBar, QPlainTextEdit, QMessageBox, QTextEdit, QFileDialog, QPushButton, QLabel, QGroupBox, QVBoxLayout, QWidget, QMainWindow, QTableWidget, QRadioButton, QComboBox, QLineEdit, QFormLayout, QTabWidget, QDockWidget, QHBoxLayout
from pyqtgraph import PlotWidget, plot, GraphicsWidget, GraphicsWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

#globais
projeto = ""
isantigo = False

#comandos
def novoProjeto(ferramenta4):
    global projeto
    global isantigo
    isantigo = False
    caminho = str(QFileDialog.getExistingDirectory(ferramenta4, "Crie uma pasta para salvar os arquivos do projeto!"))
    if(caminho == ''):
        ferramenta4.statusBar().showMessage('Diretório não selecionado!')
        return
    else:
        ferramenta4.statusBar().showMessage('Novo projeto criado!')
    projeto = caminho
    config = {}
    config['criacao'] = str(date.today())
    config['ferramenta4'] = []
    config['ferramenta4'].append({
        'fabricante': '',
        'modelo': '',
        'serie': '',
        'precisao_nominal_a': '',
        'precisao_nominal_b': '',
        'precisao_op_a': '',
        'precisao_op_b': '',
        'precisao_op_a_s': '',
        'precisao_op_b_s': '',
        'erro_indice': '',
    })
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(config, outfile)
...
def antigoProjeto(ferramenta4):
    global projeto
    global isantigo
    caminho = str(QFileDialog.getExistingDirectory(ferramenta4, "Selecione o diretório do antigo projeto!"))
    if(caminho == ''):
        ferramenta4.statusBar().showMessage('Diretório não selecionado!')
        return
    arquivos = [f for f in listdir(caminho) if isfile(join(caminho, f))]
    config = [f for f in arquivos if '.ajobs' in f]
    if(len(config)==0):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar o projeto!")
        msg.setInformativeText("O diretório indicado não contém um arquivo de projeto.")
        msg.setWindowTitle("Abrir Projeto")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    else:
        projeto = caminho
        ferramenta4.statusBar().showMessage('O projeto foi carregado!')
        isantigo = True
...
def getAmostra(ferramenta4, widgetEntrada):
    caminho = QFileDialog.getOpenFileName(ferramenta4, "Selecione um arquivo de distâncias!", getenv('HOME'), 'CSV(*.csv)')
    widgetEntrada.setText(caminho[0])
    ferramenta4.statusBar().showMessage("Arquivo de distâncias selecionado!")
...
def carregarAmostra(widgetEntrada1, separador1, widgetAba1, widgetAba2, am):
    global projeto
    if(projeto == ""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar dados!")
        msg.setInformativeText("Você deve criar um novo projeto antes de carregar os dados. Um projeto é responsável por salvar o progresso do processamento.")
        msg.setWindowTitle("Carregar dados")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(widgetEntrada1.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar distâncias!")
        msg.setInformativeText("Você deve selecionar um arquivo de distâncias para carregar os dados.")
        msg.setWindowTitle("Carregar Distâncias")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(separador1.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar distâncias!")
        msg.setInformativeText("Você deve indicar o caractere delimitador.")
        msg.setWindowTitle("Carregar Distâncias")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    tool4d.lerDistancias(str(widgetEntrada1.text()), projeto, widgetAba1, str(separador1.text()), am)
...
def plotarObs(widgetAba1):
    tool4d.plotarPyQtGraph(projeto, widgetAba1)
...
def salvarEspec(fab, modelo, serie, a, b):
    global projeto
    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
        data['ferramenta4'][0]['fabricante'] = str(fab.text())
        data['ferramenta4'][0]['modelo'] = str(modelo.text())
        data['ferramenta4'][0]['serie'] = str(serie.text())
        data['ferramenta4'][0]['precisao_nominal_a'] = str(a.text())
        data['ferramenta4'][0]['precisao_nominal_b'] = str(b.text())
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(data, outfile)
...
def processar(html, grafico):
    global projeto
    tool4d.calcular(projeto, grafico, html)
...

sag_gui_tool4 = QApplication(sys.argv)

ferramenta4 = QMainWindow()
ferramenta4.setWindowTitle("Aferição de Distanciômetros")
ferramenta4.setWindowIcon(QtGui.QIcon('4imgs/ferramenta1.png'))
ferramenta4.Width = 800
ferramenta4.height = int(0.618 * ferramenta4.Width)
ferramenta4.resize(ferramenta4.Width, ferramenta4.height)

menu = ferramenta4.menuBar()
menu_arquivo = menu.addMenu('Arquivo')
menu_editar = menu.addMenu('Editar')
menu_sobre = menu.addMenu('Sobre')

#Acoes Arquivo
arquivoNovoProjeto = QAction(QtGui.QIcon('4imgs/novoprojeto.png'), 'Novo Projeto', ferramenta4)
cmdArquivoNovoProjeto = partial(novoProjeto, ferramenta4)
arquivoNovoProjeto.triggered.connect(cmdArquivoNovoProjeto)
arquivoAbrirProjeto = QAction(QtGui.QIcon('4imgs/abrirprojeto.png'), 'Abrir Projeto', ferramenta4)
cmdArquivoAbrirProjeto = partial(antigoProjeto, ferramenta4)
arquivoAbrirProjeto.triggered.connect(cmdArquivoAbrirProjeto)
menu_arquivo.addAction(arquivoNovoProjeto)
menu_arquivo.addAction(arquivoAbrirProjeto)
menu_arquivo.addSeparator()

ferramenta4_layout = QHBoxLayout()

lateral = QDockWidget('Entrada de Dados')
lateralWidget = QWidget()
lateral_layout = QVBoxLayout()

#Main
principal = QTabWidget()
tabela_amostra1 = QTableWidget()
tabela_amostra2 = QTableWidget()

obs = QWidget()
graficoObs = PlotWidget()
obsLayout = QHBoxLayout()
obsLayout.addWidget(graficoObs)
obs.setLayout(obsLayout)
graficoObs.setBackground('w')
graficoObs.setTitle("Estações de Calibração")
graficoObs.showGrid(x=True, y=False)
graficoObs.setLabel('bottom', "Distâncias Observadas (m)")

tabela_resultados = QTableWidget()
texto_relatorio = QWebEngineView()

principal.addTab(tabela_amostra1, "Amostra 1")
principal.addTab(tabela_amostra2, "Amostra 2")
principal.addTab(obs, "Observações")
principal.addTab(tabela_resultados, "Resultados")
principal.addTab(texto_relatorio, "Relatório de Processamento")

#Arquivo Amostra1
bloco_amostra1 = QGroupBox("Amostra 1")
bloco_amostra1_layout = QFormLayout()
caminho_amostra1 = QLineEdit()
caminho_amostra1.setPlaceholderText('caminho do arquivo')
linha_caminho_amostra1 = QHBoxLayout()
#bloco_levantamento_layout.addRow(QLabel("Caminho:"), caminho_levantamento)
btn_caminho_amostra1 = QPushButton('...')
cmd_btn_amostra1 = partial(getAmostra, ferramenta4, caminho_amostra1)
btn_caminho_amostra1.clicked.connect(cmd_btn_amostra1)
linha_caminho_amostra1.addWidget(caminho_amostra1)
linha_caminho_amostra1.addWidget(btn_caminho_amostra1)
bloco_amostra1_layout.addRow(linha_caminho_amostra1)
#bloco_levantamento_layout.addRow(btn_caminho_levantamento)
separador_amostra1 = QLineEdit()
bloco_amostra1_layout.addRow("Caractere separador: ", separador_amostra1)
#decimal_coordenadas = QCheckBox('Separador decimal é a vírgula')
#bloco_levantamento_layout.addRow(decimal_coordenadas)
bloco_amostra1.setLayout(bloco_amostra1_layout)
#btn carregar amostra1
btn_carregar_amostra1 = QPushButton('Carregar do Arquivo')
cmd_carregar_amostra1 = partial(carregarAmostra, caminho_amostra1, separador_amostra1, tabela_amostra1, tabela_resultados, "1")
btn_carregar_amostra1.clicked.connect(cmd_carregar_amostra1)
bloco_amostra1_layout.addRow(btn_carregar_amostra1)

#Arquivo Amostra2
bloco_amostra2 = QGroupBox("Amostra 2")
bloco_amostra2_layout = QFormLayout()
caminho_amostra2 = QLineEdit()
caminho_amostra2.setPlaceholderText('caminho do arquivo')
linha_caminho_amostra2 = QHBoxLayout()
#bloco_levantamento_layout.addRow(QLabel("Caminho:"), caminho_levantamento)
btn_caminho_amostra2 = QPushButton('...')
cmd_btn_amostra2 = partial(getAmostra, ferramenta4, caminho_amostra2)
btn_caminho_amostra2.clicked.connect(cmd_btn_amostra2)
linha_caminho_amostra2.addWidget(caminho_amostra2)
linha_caminho_amostra2.addWidget(btn_caminho_amostra2)
bloco_amostra2_layout.addRow(linha_caminho_amostra2)
#bloco_levantamento_layout.addRow(btn_caminho_levantamento)
separador_amostra2 = QLineEdit()
bloco_amostra2_layout.addRow("Caractere separador: ", separador_amostra2)
#decimal_coordenadas = QCheckBox('Separador decimal é a vírgula')
#bloco_levantamento_layout.addRow(decimal_coordenadas)
bloco_amostra2.setLayout(bloco_amostra2_layout)
#btn carregar amostra2
btn_carregar_amostra2 = QPushButton('Carregar do Arquivo')
cmd_carregar_amostra2 = partial(carregarAmostra, caminho_amostra2, separador_amostra2, tabela_amostra2, tabela_resultados, "2")
btn_carregar_amostra2.clicked.connect(cmd_carregar_amostra2)
bloco_amostra2_layout.addRow(btn_carregar_amostra2)

#btn plotar
btn_plotar = QPushButton('Plotar Observações')
cmd_plotar = partial(plotarObs, graficoObs)
btn_plotar.clicked.connect(cmd_plotar)

#Espec
bloco_espec = QGroupBox("Especificações")
bloco_espec_layout = QFormLayout()
fabricante_espec = QLineEdit()
bloco_espec_layout.addRow(QLabel("Fabricante:"), fabricante_espec)
modelo_espec = QLineEdit()
bloco_espec_layout.addRow(QLabel("Modelo:"), modelo_espec)
serie_espec = QLineEdit()
bloco_espec_layout.addRow(QLabel("Série:"), serie_espec)
bloco_espec.setLayout(bloco_espec_layout)

#Precisão Nominal
bloco_precnom = QGroupBox("Precisão Nominal")
bloco_precnom_layout = QFormLayout()
a_precnom = QLineEdit()
bloco_precnom_layout.addRow(QLabel("a (mm):"), a_precnom)
b_precnom = QLineEdit()
bloco_precnom_layout.addRow(QLabel("b (ppm):"), b_precnom)
bloco_precnom.setLayout(bloco_precnom_layout)

#btn salvar
btn_espec = QPushButton('salvar')
cmd_espec = partial(salvarEspec, fabricante_espec, modelo_espec, serie_espec, a_precnom, b_precnom)
btn_espec.clicked.connect(cmd_espec)

#btn processar
btn_processar = QPushButton('Processar')
cmd_processar = partial(processar, texto_relatorio, graficoObs)
btn_processar.clicked.connect(cmd_processar)

#Lateral
lateral_layout.addWidget(bloco_amostra1)
lateral_layout.addWidget(bloco_amostra2)
lateral_layout.addWidget(btn_plotar)
lateral_layout.addWidget(bloco_espec)
lateral_layout.addWidget(bloco_precnom)
lateral_layout.addWidget(btn_espec)
lateral_layout.addWidget(btn_processar)

lateralWidget.setLayout(lateral_layout)
lateral.setWidget(lateralWidget)

#lateral2Widget.setLayout(lateral2_layout)
#lateral2.setWidget(lateral2Widget)

ferramenta4.setCentralWidget(principal)
ferramenta4.addDockWidget(Qt.LeftDockWidgetArea, lateral)
#ferramenta4.addDockWidget(Qt.RightDockWidgetArea, lateral2)
ferramenta4.setLayout(ferramenta4_layout)

ferramenta4.show()
sys.exit(sag_gui_tool4.exec_())