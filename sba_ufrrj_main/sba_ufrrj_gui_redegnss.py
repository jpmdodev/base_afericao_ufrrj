#utilidades
import sys
from datetime import date
from functools import partial
from os import getenv
from os import listdir
from os.path import isfile, join
import json
import webbrowser
#scripts
import tool1
#qt
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout, QApplication, QAction, QHBoxLayout, QDialog, QPlainTextEdit, QMessageBox, QFileDialog, QPushButton, QLabel, QGroupBox, QVBoxLayout, QWidget, QMainWindow, QTableWidget, QRadioButton, QComboBox, QLineEdit, QFormLayout, QTabWidget, QDockWidget, QHBoxLayout
from pyqtgraph import PlotWidget

#globais
projeto = ""
isantigo = False

#comandos
def novoProjeto(ferramenta1):
    global projeto
    global isantigo
    isantigo = False
    caminho = str(QFileDialog.getExistingDirectory(ferramenta1, "Crie uma pasta para salvar os arquivos do projeto!"))
    if(caminho == ''):
        ferramenta1.statusBar().showMessage('Diretório não selecionado!')
        return
    else:
        ferramenta1.statusBar().showMessage('Novo projeto criado!')
    projeto = caminho
    config = {}
    config['criacao'] = str(date.today())
    config['ferramenta1'] = []
    config['ferramenta1'].append({
        'injuncao': 'P',
        'injuncaoX': 0,
        'injuncaoY': 0,
        'injuncaoZ': 0, 
        'tolerancia': 0
    })
    config['ferramenta2'] = []
    config['ferramenta2'].append({
        'injuncao': 'P'
    })
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(config, outfile)
...
def antigoProjeto(ferramenta1):
    global projeto
    global isantigo
    caminho = str(QFileDialog.getExistingDirectory(ferramenta1, "Selecione o diretório do antigo projeto!"))
    if(caminho == ''):
        ferramenta1.statusBar().showMessage('Diretório não selecionado!')
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
        ferramenta1.statusBar().showMessage('O projeto foi carregado!')
        isantigo = True
...
def getCoordenadas(ferramenta1, widgetEntrada):
    caminho = QFileDialog.getOpenFileName(ferramenta1, "Selecione um arquivo de coordenadas!", getenv('HOME'), 'CSV(*.csv)')
    widgetEntrada.setText(caminho[0])
    ferramenta1.statusBar().showMessage("Arquivo de coordenadas selecionado!")
...
def getVetores(ferramenta1, widgetEntrada):
    caminho = QFileDialog.getOpenFileName(ferramenta1, "Selecione um arquivo de vetores!", getenv('HOME'), 'CSV(*.csv)')
    widgetEntrada.setText(caminho[0])
    ferramenta1.statusBar().showMessage("Arquivo de vetores selecionado!")
...
def carregarDados(widgetEntrada1, widgetEntrada2, widgetAba1, widgetAba2, widgetAba4, widgetLegenda, nome_injuncao, separador1, separador2):
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
        msg.setText("Erro ao carregar coordenadas!")
        msg.setInformativeText("Você deve selecionar um arquivo de coordenadas para carregar os dados.")
        msg.setWindowTitle("Carregar Coordenadas")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(separador1.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar coordenadas!")
        msg.setInformativeText("Você deve indicar o caractere delimitador.")
        msg.setWindowTitle("Carregar Coordenadas")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(widgetEntrada2.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar vetores!")
        msg.setInformativeText("Você deve selecionar um arquivo de vetores para carregar os dados.")
        msg.setWindowTitle("Carregar Vetores")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(separador2.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar vetores!")
        msg.setInformativeText("Você deve indicar o caractere delimitador.")
        msg.setWindowTitle("Carregar Vetores")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    tool1.lerCoordenadas(str(widgetEntrada1.text()), widgetAba1, projeto, nome_injuncao, separador1.text())
    tool1.lerVetores(str(widgetEntrada2.text()), widgetAba2, projeto, separador2.text())
    tool1.plotarPyQtGraph(projeto, widgetAba4, widgetLegenda)
...
def  ajustarDados(nome_injuncao, x_injuncao, y_injuncao, z_injuncao, tolerancia, tabela_resultados, texto_relatorio, aba):
    global projeto
    if(str(nome_injuncao.currentText()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Injunção")
        msg.setInformativeText("Forneça um ponto de injunção do ajustamento.")
        msg.setWindowTitle("Erro ao ajustar!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(y_injuncao.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Injunção")
        msg.setInformativeText("Coordenada Y da injunção não foi fornecida.")
        msg.setWindowTitle("Erro ao ajustar!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(x_injuncao.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Injunção")
        msg.setInformativeText("Coordenada X da injunção não foi fornecida.")
        msg.setWindowTitle("Erro ao ajustar!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(z_injuncao.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Injunção")
        msg.setInformativeText("Coordenada Z da injunção não foi fornecida.")
        msg.setWindowTitle("Erro ao ajustar!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(tolerancia.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Tolerância")
        msg.setInformativeText("A tolerância para o ajustamento não foi fornecida.")
        msg.setWindowTitle("Erro ao ajustar!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    tool1.ajustar(projeto, [str(nome_injuncao.currentText()), float(y_injuncao.text()), float(x_injuncao.text()), float(z_injuncao.text())], float(tolerancia.text()), tabela_resultados, texto_relatorio, aba)
    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
        data['ferramenta1'][0]['injuncao'] = str(nome_injuncao.currentText())
        data['ferramenta1'][0]['injuncaoY'] = float(y_injuncao.text())
        data['ferramenta1'][0]['injuncaoX'] = float(x_injuncao.text()) 
        data['ferramenta1'][0]['injuncaoZ'] = float(z_injuncao.text())  
        data['ferramenta1'][0]['tolerancia'] = float(tolerancia.text())
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(data, outfile)
...
def getDadosSalvos(widgetTabela1, widgetTabela2, widgetGrafico, widgetLegenda, widgetInjuncao, widgetX, widgetY, widgetZ, widgetTolerancia):
    global projeto
    tool1.lerCoordenadasSalvas(projeto, widgetTabela1, widgetInjuncao)
    tool1.lerVetoresSalvos(projeto, widgetTabela2)
    tool1.plotarPyQtGraph(projeto, widgetGrafico, widgetLegenda)
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
        index = widgetInjuncao.findText(data['ferramenta1'][0]['injuncao'], Qt.MatchFixedString)
        if index >= 0:
            widgetInjuncao.setCurrentIndex(index)
        widgetX.setText(str(data['ferramenta1'][0]['injuncaoX']))
        widgetY.setText(str(data['ferramenta1'][0]['injuncaoY']))
        widgetZ.setText(str(data['ferramenta1'][0]['injuncaoZ']))
        widgetTolerancia.setText(str(data['ferramenta1'][0]['tolerancia']))
...
def sobre():
    bloco = QGroupBox('Dados da Versão')
    layout = QGridLayout()
    bloco.setLayout(layout)

    label = QLabel('Ajustamento de Rede GNSS: ')
    versao = QLabel('v 0.0.1')
    layout.addWidget(label, 0, 0)
    layout.addWidget(versao, 0, 1)

    d = QDialog()
    vbox = QVBoxLayout()

    vbox.addWidget(bloco)

    d.setWindowTitle("Sobre a Ferramenta")
    d.setLayout(vbox)
    d.setWindowModality(Qt.ApplicationModal)
    d.exec_()
...
def tese():
    webbrowser.open('https://www.ibge.gov.br/geociencias/informacoes-sobre-posicionamento-geodesico/rede-geodesica.html')
...
"""
def getDatum():
    d = QDialog()

    pesquisa = QLineEdit()
    btn_pesquisa = QPushButton("Pesquisar")
    hbox = QHBoxLayout()        
    hbox.addWidget(pesquisa)
    hbox.addWidget(btn_pesquisa)

    lista = QListWidget()
    vbox = QVBoxLayout()
    vbox.addLayout(hbox)
    vbox.addWidget(lista)

    d.setWindowTitle("Selecione um Datum Horizontal")
    d.setLayout(vbox)
    d.setWindowModality(Qt.ApplicationModal)
    d.exec_()
...
"""
sag_gui_tool1 = QApplication(sys.argv)

ferramenta1 = QMainWindow()
ferramenta1.setWindowTitle("Ajustamento de Rede GNSS")
ferramenta1.setWindowIcon(QtGui.QIcon('4imgs/ferramenta1.png'))
ferramenta1.Width = 800
ferramenta1.height = int(0.618 * ferramenta1.Width)
ferramenta1.resize(ferramenta1.Width, ferramenta1.height)

#Menus
menu = ferramenta1.menuBar()
menu_arquivo = menu.addMenu('Arquivo')
menu_editar = menu.addMenu('Editar')
menu_ajuda = menu.addMenu('Ajuda')

#Acoes Arquivo
arquivoNovoProjeto = QAction(QtGui.QIcon('4imgs/novoprojeto.png'), 'Novo Projeto', ferramenta1)
cmdArquivoNovoProjeto = partial(novoProjeto, ferramenta1)
arquivoNovoProjeto.triggered.connect(cmdArquivoNovoProjeto)
arquivoAbrirProjeto = QAction(QtGui.QIcon('4imgs/abrirprojeto.png'), 'Abrir Projeto', ferramenta1)
cmdArquivoAbrirProjeto = partial(antigoProjeto, ferramenta1)
arquivoAbrirProjeto.triggered.connect(cmdArquivoAbrirProjeto)
menu_arquivo.addAction(arquivoNovoProjeto)
menu_arquivo.addAction(arquivoAbrirProjeto)

#Acoes Preferencias
editarPreferencias = QAction('Preferências', ferramenta1)
#arquivoNovoProjeto.triggered.connect(cmdArquivoNovoProjeto)
#arquivoExportar = QAction(QtGui.QIcon('abrirprojeto.png'), 'Exportar Dados', inicio)
#cmdArquivoExportar = partial(antigoProjeto, inicio)
#arquivoExportar.triggered.connect(cmdArquivoAbrirProjeto)
menu_editar.addAction(editarPreferencias)

#Acoes Ajuda
ajudaSobre = QAction(QtGui.QIcon(), 'Sobre', ferramenta1)
cmdAjudaSobre = partial(sobre)
ajudaSobre.triggered.connect(cmdAjudaSobre)
ajudaTese = QAction(QtGui.QIcon(), 'Teoria', ferramenta1)
cmdAjudaTese = partial(tese)
ajudaTese.triggered.connect(cmdAjudaTese)
menu_ajuda.addAction(ajudaSobre)
menu_ajuda.addAction(ajudaTese)

ferramenta1_layout = QHBoxLayout()

#Lateral Esquerda
lateral = QDockWidget('Entrada de Dados')
lateralWidget = QWidget()
lateral_layout = QVBoxLayout()

#Lateral Direita
"""
f = open('2tutoriais//tutorial_tool_1.html', 'r')
file_contents = f.read()
lateral2 = QDockWidget('Teoria')
lateral2Widget = QWidget()
lateral2_layout = QVBoxLayout()
teoria = QWebEngineView()
#teoria.textCursor().insertHtml(file_contents)
teoria.setHtml(file_contents)
#teoria.setReadOnly(True)
lateral2_layout.addWidget(teoria)
teoria.show()
"""

#Main
principal = QTabWidget()
tabela_coordenadas = QTableWidget()
tabela_vetores = QTableWidget()
tabela_resultados = QTableWidget()
texto_relatorio = QPlainTextEdit()

legendasWidget = QWidget()
grafico2grafico = PlotWidget()
grafico2 = QWidget()
grafico2Layout = QHBoxLayout()
grafico2Layout.addWidget(grafico2grafico)
grafico2Layout.addWidget(legendasWidget)
grafico2.setLayout(grafico2Layout)
grafico2grafico.setBackground('w')
grafico2grafico.setTitle("Rede GNSS")
grafico2grafico.showGrid(x=True, y=True)
grafico2grafico.setLabel('left', "N (m)")
grafico2grafico.setLabel('bottom', "E (m)")

grafico3grafico = PlotWidget()
grafico3 = QWidget()
grafico3Layout = QHBoxLayout()
grafico3Layout.addWidget(grafico3grafico)
grafico3.setLayout(grafico3Layout)
grafico3grafico.setBackground('w')
grafico3grafico.setTitle("Rede GNSS - Ajustada")
grafico3grafico.showGrid(x=True, y=True)
grafico3grafico.setLabel('left', "N (m)")
grafico3grafico.setLabel('bottom', "E (m)")

principal.addTab(tabela_coordenadas, "Coordenadas")
principal.addTab(tabela_vetores, "Vetores")
principal.addTab(grafico2, "Gráfico - Rede")
principal.addTab(tabela_resultados, "Coordenadas Ajustadas")
principal.addTab(texto_relatorio, "Relatório de Processamento")
principal.addTab(grafico3, "Gráfico - Rede Ajustada")

#Arquivo Coordenadas
bloco_coordenadas = QGroupBox("Arquivo de Coordenadas")
bloco_coordenadas_layout = QFormLayout()
caminho_coordenadas = QLineEdit()
caminho_coordenadas.setPlaceholderText('caminho do arquivo')
linha_caminho_coordenadas = QHBoxLayout()
#bloco_coordenadas_layout.addRow(QLabel("Caminho:"), caminho_coordenadas)
btn_caminho_coordenadas = QPushButton('...')
cmd_btn_coordenadas = partial(getCoordenadas, ferramenta1, caminho_coordenadas)
btn_caminho_coordenadas.clicked.connect(cmd_btn_coordenadas)
linha_caminho_coordenadas.addWidget(caminho_coordenadas)
linha_caminho_coordenadas.addWidget(btn_caminho_coordenadas)
bloco_coordenadas_layout.addRow(linha_caminho_coordenadas)
#bloco_coordenadas_layout.addRow(btn_caminho_coordenadas)
separador_coordenadas = QLineEdit()
bloco_coordenadas_layout.addRow("Caractere separador: ", separador_coordenadas)
#decimal_coordenadas = QCheckBox('Separador decimal é a vírgula')
#bloco_coordenadas_layout.addRow(decimal_coordenadas)
bloco_coordenadas.setLayout(bloco_coordenadas_layout)

#Arquivo Vetores
bloco_vetores = QGroupBox("Arquivo de Vetores")
bloco_vetores_layout = QFormLayout()
caminho_vetores = QLineEdit()
caminho_vetores.setPlaceholderText('caminho do arquivo')
linha_caminho_vetores = QHBoxLayout()
#bloco_vetores_layout.addRow(QLabel("Caminho:"), caminho_vetores)
btn_caminho_vetores = QPushButton('...')
cmd_btn_vetores = partial(getVetores, ferramenta1, caminho_vetores)
btn_caminho_vetores.clicked.connect(cmd_btn_vetores)
linha_caminho_vetores.addWidget(caminho_vetores)
linha_caminho_vetores.addWidget(btn_caminho_vetores)
bloco_vetores_layout.addRow(linha_caminho_vetores)
#bloco_vetores_layout.addRow(btn_caminho_vetores)
separador_vetores = QLineEdit()
bloco_vetores_layout.addRow("Caractere separador: ", separador_vetores)
#decimal_vetores = QCheckBox('Separador decimal é a vírgula')
#bloco_vetores_layout.addRow(decimal_vetores)
bloco_vetores.setLayout(bloco_vetores_layout)

#Datum
"""
bloco_datum = QGroupBox("Sistema de Coordenadas")
bloco_datum_layout = QFormLayout()

datum_projecao_edit = QLineEdit()
datum_projecao_edit.setPlaceholderText('Sistema de projeção')
datum_projecao = QHBoxLayout()
datum_projecao.addWidget(datum_projecao_edit)
btn_datum_projecao = QPushButton('...')
cmd_btn_datum_projecao = partial(getDatum)
btn_datum_projecao.clicked.connect(cmd_btn_datum_projecao)
datum_projecao.addWidget(btn_datum_projecao)
bloco_datum_layout.addRow(datum_projecao)

datum_datum_edit = QLineEdit()
datum_datum_edit.setPlaceholderText('Sistema de referência')
datum_datum = QHBoxLayout()
datum_datum.addWidget(datum_datum_edit)
btn_datum_datum = QPushButton('...')
cmd_btn_datum_projecao = partial(getDatum)
btn_datum_datum.clicked.connect(cmd_btn_datum_projecao)
datum_datum.addWidget(btn_datum_datum)
bloco_datum_layout.addRow(datum_datum)

bloco_datum_layout.addRow(QLabel("Elevação"))
geometrica = QRadioButton("Geométrica/Elipsoidal")
ortometrica = QRadioButton("Ortométrica/Geoidal")
geometrica.setChecked(True)
bloco_datum_layout.addRow(geometrica, ortometrica)
bloco_datum.setLayout(bloco_datum_layout)
"""

#Injuncao
bloco_injuncao = QGroupBox("Injunção")
bloco_injuncao_layout = QFormLayout()
nome_injuncao = QComboBox()
bloco_injuncao_layout.addRow(QLabel("Ponto:"), nome_injuncao)
x_injuncao = QLineEdit()
bloco_injuncao_layout.addRow(QLabel("X:"), x_injuncao)
y_injuncao = QLineEdit()
bloco_injuncao_layout.addRow(QLabel("Y:"), y_injuncao)
z_injuncao = QLineEdit()
bloco_injuncao_layout.addRow(QLabel("Z:"), z_injuncao)
#cmd_btn_vetores = partial(iniciaFerramenta1, inicio)
#btn_caminho_vetores.clicked.connect(cmd_btn_vetores)
absoluta = QRadioButton("Absoluta")
absoluta.setChecked(True)
absoluta.country = "Absoluta"
#radiobutton.toggled.connect(self.onClicked)
relativa = QRadioButton("Relativa")
relativa.country = "Relativa"
#radiobutton.toggled.connect(self.onClicked)
bloco_injuncao_layout.addRow(absoluta, relativa)
bloco_injuncao.setLayout(bloco_injuncao_layout)

#Tolerancia
bloco_tolerancia = QGroupBox("Tolerância")
bloco_tolerancia_layout = QFormLayout()
tolerancia = QLineEdit()
bloco_tolerancia_layout.addRow(QLabel("Tolerância:"), tolerancia)
bloco_tolerancia.setLayout(bloco_tolerancia_layout)

#btn carregar dados
btn_carregar_dados = QPushButton('Carregar Dados')
cmd_carregar_dados = partial(carregarDados, caminho_coordenadas, caminho_vetores, tabela_coordenadas, tabela_vetores, grafico2grafico, legendasWidget, nome_injuncao, separador_coordenadas, separador_vetores)
btn_carregar_dados.clicked.connect(cmd_carregar_dados)

#btn ajustar dados
btn_ajustar_dados = QPushButton('Ajustar Dados')
cmd_btn_ajustar = partial(ajustarDados, nome_injuncao, x_injuncao, y_injuncao, z_injuncao, tolerancia, tabela_resultados, texto_relatorio, grafico3grafico)
btn_ajustar_dados.clicked.connect(cmd_btn_ajustar)

lateral_layout.addWidget(bloco_coordenadas)
lateral_layout.addWidget(bloco_vetores)
#lateral_layout.addWidget(bloco_datum)
lateral_layout.addWidget(btn_carregar_dados)
lateral_layout.addWidget(bloco_injuncao)
lateral_layout.addWidget(bloco_tolerancia)
lateral_layout.addWidget(btn_ajustar_dados)

lateralWidget.setLayout(lateral_layout)
lateral.setWidget(lateralWidget)

#lateral2Widget.setLayout(lateral2_layout)
#lateral2.setWidget(lateral2Widget)

ferramenta1.setCentralWidget(principal)
ferramenta1.addDockWidget(Qt.LeftDockWidgetArea, lateral)
#ferramenta1.addDockWidget(Qt.RightDockWidgetArea, lateral2)
ferramenta1.setLayout(ferramenta1_layout)

ferramenta1.show()
sys.exit(sag_gui_tool1.exec_())