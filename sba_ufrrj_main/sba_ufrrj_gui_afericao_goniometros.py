#utilidades
import sys
from datetime import date
from functools import partial
from os import getenv
from os import listdir
from os.path import isfile, join
import json
#import serial.tools.list_ports
#scripts
import tool3
#qt
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout, QApplication, QAction, QHBoxLayout, QListWidget, QDialog, QCheckBox, QProgressBar, QPlainTextEdit, QMessageBox, QTextEdit, QFileDialog, QPushButton, QLabel, QGroupBox, QVBoxLayout, QWidget, QMainWindow, QTableWidget, QRadioButton, QComboBox, QLineEdit, QFormLayout, QTabWidget, QDockWidget, QHBoxLayout
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from pyqtgraph import PlotWidget, plot, GraphicsWidget, GraphicsWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

#globais
projeto = ""
isantigo = False

#comandos
def novoProjeto(ferramenta3):
    global projeto
    global isantigo
    isantigo = False
    caminho = str(QFileDialog.getExistingDirectory(ferramenta3, "Crie uma pasta para salvar os arquivos do projeto!"))
    if(caminho == ''):
        ferramenta3.statusBar().showMessage('Diretório não selecionado!')
        return
    else:
        ferramenta3.statusBar().showMessage('Novo projeto criado!')
    projeto = caminho
    config = {}
    config['criacao'] = str(date.today())
    config['ferramenta3'] = []
    config['ferramenta3'].append({
        'proprietario': '',
        'marca': '',
        'modelo': '',
        'serie': '',
        'precisao_angular_nominal': '',
        'operador': '',
        'anotador': '',
        'data': '',
        'horario_inicio': '',
        'horario_termino': '',
        'temperatura': '',
        'pressao': '',
        'desvio_padrao_exp_geral': ''
    })
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(config, outfile)
...
def antigoProjeto(ferramenta3):
    global projeto
    global isantigo
    caminho = str(QFileDialog.getExistingDirectory(ferramenta3, "Selecione o diretório do antigo projeto!"))
    if(caminho == ''):
        ferramenta3.statusBar().showMessage('Diretório não selecionado!')
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
        ferramenta3.statusBar().showMessage('O projeto foi carregado!')
        isantigo = True
...
def getAngulos(ferramenta3, widgetEntrada):
    caminho = QFileDialog.getOpenFileName(ferramenta3, "Selecione um arquivo de ângulos!", getenv('HOME'), 'CSV(*.csv)')
    widgetEntrada.setText(caminho[0])
    ferramenta3.statusBar().showMessage("Arquivo de ângulos selecionado!")
...
def carregarDados(widgetEntrada1, separador1, widgetAba1):
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
        msg.setText("Erro ao carregar ângulos!")
        msg.setInformativeText("Você deve selecionar um arquivo de ângulos para carregar os dados.")
        msg.setWindowTitle("Carregar Ângulos")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(separador1.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro ao carregar ângulos!")
        msg.setInformativeText("Você deve indicar o caractere delimitador.")
        msg.setWindowTitle("Carregar Ângulos")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    tool3.lerAngulos(str(widgetEntrada1.text()), projeto, widgetAba1, separador1)
...
def aferirDados(tabela, campo):
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
    tool3.calcular(projeto, tabela, campo)
...
def certificarDados(tabela):
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
    tool3.gerarRelatorio(projeto, tabela)
...
def salvarForm(proprietario, marca, modelo, serie, precisao, operador, anotador, editData, inicio, fim, temperatura, pressao):
    global projeto
    if(str(proprietario.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(marca.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(modelo.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(serie.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(precisao.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(operador.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(anotador.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(editData.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(inicio.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(fim.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(temperatura.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    if(str(pressao.text()) == ''):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Erro Formulário")
        msg.setInformativeText("O preenchimento dos campos do formulário é obrigatório.")
        msg.setWindowTitle("Erro ao salvar formulário!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return
    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
        data['ferramenta3'][0]['proprietario'] = str(proprietario.text())
        data['ferramenta3'][0]['marca'] = str(marca.text())
        data['ferramenta3'][0]['modelo'] = str(modelo.text())
        data['ferramenta3'][0]['serie'] = str(serie.text())
        data['ferramenta3'][0]['precisao_angular_nominal'] = str(precisao.text())
        data['ferramenta3'][0]['operador'] = str(operador.text())
        data['ferramenta3'][0]['anotador'] = str(anotador.text())
        data['ferramenta3'][0]['data'] = str(editData.text())
        data['ferramenta3'][0]['horario_inicio'] = str(inicio.text())
        data['ferramenta3'][0]['horario_termino'] = str(fim.text())
        data['ferramenta3'][0]['temperatura'] = str(temperatura.text())
        data['ferramenta3'][0]['pressao'] = str(pressao.text())
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(data, outfile)
...
def editarFormulario():

    bloco = QGroupBox('Dados de Aferição')
    layout = QGridLayout()
    bloco.setLayout(layout)

    labelProprietario = QLabel('Proprietário: ')
    editProprietario = QLineEdit()
    layout.addWidget(labelProprietario, 0, 0)
    layout.addWidget(editProprietario, 0, 1)

    labelMarca = QLabel('Marca do Equipamento: ')
    editMarca = QLineEdit()
    layout.addWidget(labelMarca, 1, 0)
    layout.addWidget(editMarca, 1, 1)

    labelModelo = QLabel('Modelo do Equipamento: ')
    editModelo = QLineEdit()
    layout.addWidget(labelModelo, 2, 0)
    layout.addWidget(editModelo, 2, 1)

    labelSerie = QLabel('Série do Equipamento: ')
    editSerie = QLineEdit()
    layout.addWidget(labelSerie, 3, 0)
    layout.addWidget(editSerie, 3, 1)

    labelPrecisao = QLabel('Precisão Angular Nominal (\"): ')
    editPrecisao = QLineEdit()
    layout.addWidget(labelPrecisao, 4, 0)
    layout.addWidget(editPrecisao, 4, 1)

    labelOperador = QLabel('Operador: ')
    editOperador = QLineEdit()
    layout.addWidget(labelOperador, 5, 0)
    layout.addWidget(editOperador, 5, 1)

    labelAnotador = QLabel('Anotador: ')
    editAnotador = QLineEdit()
    layout.addWidget(labelAnotador, 0, 2)
    layout.addWidget(editAnotador, 0, 3)

    labelData = QLabel('Data (dd/mm/aaaa): ')
    editData = QLineEdit()
    layout.addWidget(labelData, 1, 2)
    layout.addWidget(editData, 1, 3)

    labelInicio = QLabel('Horário de Início (hh:mm): ')
    editInicio = QLineEdit()
    layout.addWidget(labelInicio, 2, 2)
    layout.addWidget(editInicio, 2, 3)

    labelFim = QLabel('Horário de Término (hh:mm): ')
    editFim = QLineEdit()
    layout.addWidget(labelFim, 3, 2)
    layout.addWidget(editFim, 3, 3)

    labelTemperatura = QLabel('Temperatura (°C): ')
    editTemperatura = QLineEdit()
    layout.addWidget(labelTemperatura, 4, 2)
    layout.addWidget(editTemperatura, 4, 3)

    labelPressao = QLabel('Pressão (mmHg): ')
    editPressao = QLineEdit()
    layout.addWidget(labelPressao, 5, 2)
    layout.addWidget(editPressao, 5, 3)

    btn_salvar_form = QPushButton("Salvar Informações")
    cmd_salvar_form = partial(salvarForm, editProprietario, editMarca, editModelo, editSerie, editPrecisao, editOperador, editAnotador, editData, editInicio, editFim, editTemperatura, editPressao)
    btn_salvar_form.clicked.connect(cmd_salvar_form)
    layout.addWidget(btn_salvar_form, 6, 3)

    d = QDialog()
    vbox = QVBoxLayout()

    vbox.addWidget(bloco)

    d.setWindowTitle("Formulário")
    d.setLayout(vbox)
    d.setWindowModality(Qt.ApplicationModal)
    d.exec_()
...
#def recebeEstacao(porta, codigos, baudrate, textEdit):
#    print(codigos[porta.currentIndex()])
#    ser = serial.Serial(codigos[porta.currentIndex()])
#    ser.flushInput()
#    texto = ""
#    while True:
#        ser_bytes = ser.readline()
#        decoded_bytes = ser_bytes.decode("utf-8")
#        textEdit.setPlainText(texto)
#        texto+=decoded_bytes
#        texto+='\n'
#        print(decoded_bytes)
#        if not ser.inWaiting():
#            break
#    textEdit.setPlainText(texto)
#...
#def conectarEstacao():
#    nomes = []
#    codigos = []
#    for i in serial.tools.list_ports.comports():
#        print(i)
#        nomes.append(str(i).split(" - ")[1])
#        codigos.append(str(i).split(" - ")[0])
#    
#    bloco = QGroupBox('Dados de Conexão')
#    layout = QFormLayout()
#    bloco.setLayout(layout)
#
#    editPorta = QComboBox()
#    for n in nomes:
#        editPorta.addItem(n)
#    layout.addRow("Selecione uma porta:", editPorta)
#    editBaudrate = QLineEdit()
#    layout.addRow("Baudrate: ", editBaudrate)
#    leituras = QTextEdit()
#    layout.addRow(leituras)
#    btn_ler_dados = QPushButton("Receber Dados")
#    cmd_ler_dados = partial(recebeEstacao, editPorta, codigos, str(editBaudrate.text()), leituras)
#    btn_ler_dados.clicked.connect(cmd_ler_dados)
#    layout.addRow(btn_ler_dados)

#    d = QDialog()
#    vbox = QVBoxLayout()

#    vbox.addWidget(bloco)

#    d.setWindowTitle("Conectar Estação")
#    d.setLayout(vbox)
#    d.setWindowModality(Qt.ApplicationModal)
#    d.exec_()

#    print("Nomes COM ports: " + str(nomes))
#    print("Codigos COM ports: " + str(codigos))
#...
def  ajustarDados(tolerancia, tabela_resultados, texto_relatorio, aba):
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
    tool3.ajustar(projeto, [float(tolerancia.text())], tabela_resultados, texto_relatorio, aba)
    data = []
    with open(projeto+'/config.ajobs', 'r') as outfile:
        data = json.load(outfile)
        #data['ferramenta3'][0]['injuncao'] = str(nome_injuncao.currentText())
        #data['ferramenta3'][0]['injuncaoY'] = float(y_injuncao.text())
        #data['ferramenta3'][0]['injuncaoX'] = float(x_injuncao.text()) 
        #data['ferramenta3'][0]['injuncaoZ'] = float(z_injuncao.text())  
        data['ferramenta3'][0]['tolerancia'] = float(tolerancia.text())
    with open(projeto+'/config.ajobs', 'w') as outfile:
        json.dump(data, outfile)
...
def getDadosSalvos(widgetAba1):
    global projeto
    tool3.lerAngulosSalvos(projeto, widgetTabela1)
...

def imprimir(web):
    global projeto
    web.page().printToPdf(projeto+"/relatorio.pdf")
...

sag_gui_tool3 = QApplication(sys.argv)

ferramenta3 = QMainWindow()
ferramenta3.setWindowTitle("Aferir Ângulo Horizontal")
ferramenta3.setWindowIcon(QtGui.QIcon('4imgs/ferramenta2.png'))
ferramenta3.Width = 800
ferramenta3.height = int(0.618 * ferramenta3.Width)
ferramenta3.resize(ferramenta3.Width, ferramenta3.height)

menu = ferramenta3.menuBar()
menu_arquivo = menu.addMenu('Arquivo')
menu_editar = menu.addMenu('Editar')
menu_sobre = menu.addMenu('Sobre')

#Acoes Arquivo
arquivoNovoProjeto = QAction(QtGui.QIcon('4imgs/novoprojeto.png'), 'Novo Projeto', ferramenta3)
cmdArquivoNovoProjeto = partial(novoProjeto, ferramenta3)
arquivoNovoProjeto.triggered.connect(cmdArquivoNovoProjeto)
arquivoAbrirProjeto = QAction(QtGui.QIcon('4imgs/abrirprojeto.png'), 'Abrir Projeto', ferramenta3)
cmdArquivoAbrirProjeto = partial(antigoProjeto, ferramenta3)
arquivoAbrirProjeto.triggered.connect(cmdArquivoAbrirProjeto)
menu_arquivo.addAction(arquivoNovoProjeto)
menu_arquivo.addAction(arquivoAbrirProjeto)
menu_arquivo.addSeparator()

#Acoes Editar
editarPreferencias = QAction('Preferências', ferramenta3)
#arquivoNovoProjeto.triggered.connect(cmdArquivoNovoProjeto)
#arquivoExportar = QAction(QtGui.QIcon('abrirprojeto.png'), 'Exportar Dados', inicio)
#cmdArquivoExportar = partial(antigoProjeto, inicio)
#arquivoExportar.triggered.connect(cmdArquivoAbrirProjeto)
menu_editar.addAction(editarPreferencias)

ferramenta3_layout = QVBoxLayout()

lateral = QDockWidget('Ações')
lateralWidget = QWidget()
lateral_layout = QHBoxLayout()


#Main
principal = QTabWidget()
tabela_levantamento = QTableWidget()
tabela_resultados = QTableWidget()
texto_relatorio = QWebEngineView()


principal.addTab(tabela_levantamento, "Levantamento")
principal.addTab(tabela_resultados, "Resultados")
principal.addTab(texto_relatorio, "Relatório de Processamento")

#Arquivo Coordenadas
bloco_angulos = QGroupBox("Entrada de Dados")
bloco_angulos_layout = QFormLayout()
caminho_angulos = QLineEdit()
caminho_angulos.setPlaceholderText('caminho do arquivo')
linha_caminho_angulos = QHBoxLayout()
#bloco_angulos_layout.addRow(QLabel("Caminho:"), caminho_angulos)
btn_caminho_angulos = QPushButton('...')
cmd_btn_angulos = partial(getAngulos, ferramenta3, caminho_angulos)
btn_caminho_angulos.clicked.connect(cmd_btn_angulos)
linha_caminho_angulos.addWidget(caminho_angulos)
linha_caminho_angulos.addWidget(btn_caminho_angulos)
bloco_angulos_layout.addRow(linha_caminho_angulos)
#bloco_angulos_layout.addRow(btn_caminho_angulos)
separador_angulos = QLineEdit()
bloco_angulos_layout.addRow("Caractere separador: ", separador_angulos)
#decimal_coordenadas = QCheckBox('Separador decimal é a vírgula')
#bloco_angulos_layout.addRow(decimal_coordenadas)
bloco_angulos.setLayout(bloco_angulos_layout)

bloco_acoes = QGroupBox("Ações")
bloco_acoes_layout = QFormLayout()
bloco_acoes.setLayout(bloco_acoes_layout)
bloco_acoes.setMinimumWidth(250)

bloco_erro = QGroupBox("Erro Padrão Experimental")
bloco_erro_layout = QFormLayout()
erro_padrao = QLineEdit()
bloco_erro_layout.addRow("Erro Padrão Experimental ", erro_padrao)
"""
pic1 = QLabel()
pixmap1 = QtGui.QPixmap("imgs//capa.png")
pixmap1 = pixmap1.scaled(75, 75, Qt.KeepAspectRatio)
pic1.setPixmap(pixmap1)
pic1.setAlignment(Qt.AlignCenter)
"""
pic2 = QLabel()
pixmap2 = QtGui.QPixmap("4imgs//ufrrj.png")
pixmap2 = pixmap2.scaled(200, 75)
pic2.setPixmap(pixmap2)
pic2.setAlignment(Qt.AlignCenter)
bloco_erro_layout.addRow(pic2)
bloco_erro.setLayout(bloco_erro_layout)
bloco_erro.setMinimumWidth(200)

"""
#Arquivo Vetores
bloco_vetores = QGroupBox("Arquivo de Vetores")
bloco_vetores_layout = QFormLayout()
caminho_vetores = QLineEdit()
caminho_vetores.setPlaceholderText('caminho do arquivo')
linha_caminho_vetores = QHBoxLayout()
#bloco_vetores_layout.addRow(QLabel("Caminho:"), caminho_vetores)
btn_caminho_vetores = QPushButton('...')
cmd_btn_vetores = partial(getVetores, ferramenta3, caminho_vetores)
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
#cmd_btn_vetores = partial(iniciaferramenta3, inicio)
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
"""

#Tolerancia
bloco_tolerancia = QGroupBox("Tolerância")
bloco_tolerancia_layout = QFormLayout()
tolerancia = QLineEdit()
bloco_tolerancia_layout.addRow(QLabel("Tolerância:"), tolerancia)
bloco_tolerancia.setLayout(bloco_tolerancia_layout)

#btn carregar dados
btn_carregar_dados = QPushButton('Carregar do Arquivo')
cmd_carregar_dados = partial(carregarDados, caminho_angulos, separador_angulos, tabela_levantamento)
btn_carregar_dados.clicked.connect(cmd_carregar_dados)
bloco_angulos_layout.addRow(btn_carregar_dados)

arquivoImportarTexto = QAction(QtGui.QIcon('4imgs/importar.png'), 'Importar Arquivo de Texto', ferramenta3)
arquivoImportarTexto.triggered.connect(cmd_btn_angulos)
menu_arquivo.addAction(arquivoImportarTexto)

#btn conectar estacao
btn_conectar_estacao = QPushButton('Carregar da Estação')
#cmd_conectar_estacao = partial(conectarEstacao)
#btn_conectar_estacao.clicked.connect(cmd_conectar_estacao)
bloco_angulos_layout.addRow(btn_conectar_estacao)
arquivoImportarEstacao = QAction(QtGui.QIcon('4imgs/estacao.png'), 'Conectar Estação Total', ferramenta3)
#arquivoImportarEstacao.triggered.connect(cmd_btn_angulos)
menu_arquivo.addAction(arquivoImportarEstacao)
menu_arquivo.addSeparator()


#btn aferir
btn_form = QPushButton('Editar Formulário')
cmd_form = partial(editarFormulario)
btn_form.clicked.connect(cmd_form)
bloco_acoes_layout.addRow(btn_form)

#btn aferir
btn_aferir = QPushButton('Aferir')
cmd_aferir = partial(aferirDados, tabela_resultados, erro_padrao)
btn_aferir.clicked.connect(cmd_aferir)
bloco_acoes_layout.addRow(btn_aferir)

#btn aferir
btn_certificado = QPushButton('Gerar Certificado')
cmd_certificado = partial(certificarDados, texto_relatorio)
btn_certificado.clicked.connect(cmd_certificado)
bloco_acoes_layout.addRow(btn_certificado)

#btn conectar estacao
btn_imprimir = QPushButton('Imprimir')
cmd_btn_imprimir = partial(imprimir, texto_relatorio)
btn_imprimir.clicked.connect(cmd_btn_imprimir)
bloco_acoes_layout.addRow(btn_imprimir)
"""
#btn ajustar dados
btn_ajustar_dados = QPushButton('Ajustar Dados')
cmd_btn_ajustar = partial(ajustarDados, tolerancia, tabela_resultados, texto_relatorio, grafico3grafico)
btn_ajustar_dados.clicked.connect(cmd_btn_ajustar)
"""

lateral_layout.addWidget(bloco_angulos)
#lateral_layout.addWidget(bloco_vetores)
#lateral_layout.addWidget(bloco_datum)
#lateral_layout.addWidget(btn_carregar_dados)
#lateral_layout.addWidget(bloco_injuncao)
#lateral_layout.addWidget(bloco_tolerancia)
#lateral_layout.addWidget(btn_ajustar_dados)
lateral_layout.addWidget(bloco_acoes)
lateral_layout.addWidget(bloco_erro)
lateral_layout.addStretch()

lateralWidget.setLayout(lateral_layout)
lateral.setWidget(lateralWidget)


ferramenta3.setCentralWidget(principal)
ferramenta3.addDockWidget(Qt.TopDockWidgetArea, lateral)
ferramenta3.setLayout(ferramenta3_layout)

ferramenta3.show()
sys.exit(sag_gui_tool3.exec_())