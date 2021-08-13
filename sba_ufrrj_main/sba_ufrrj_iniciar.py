#utilidades
import sys
from datetime import date
import json
from functools import partial
from os import listdir
from os.path import isfile, join
import subprocess
#scripts
#import sag_gui_tool1
#import sag_gui_tool3
#import sag_gui_tool2
#qt
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QFileDialog, QAction, QGroupBox, QApplication, QWidget, QMainWindow, QPushButton, QVBoxLayout, QMessageBox

#globais
projeto = ""
isantigo = False

#comandos
def novoProjeto(inicio):
    global projeto
    global isantigo
    isantigo = False
    caminho = str(QFileDialog.getExistingDirectory(inicio, "Crie uma pasta para salvar os arquivos do projeto!"))
    if(caminho == ''):
        inicio.statusBar().showMessage('Diretório não selecionado!')
        return
    else:
        inicio.statusBar().showMessage('Novo projeto criado!')
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
def antigoProjeto(inicio):
    global projeto
    global isantigo
    caminho = str(QFileDialog.getExistingDirectory(inicio, "Selecione o diretório do antigo projeto!"))
    if(caminho == ''):
        inicio.statusBar().showMessage('Diretório não selecionado!')
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
        inicio.statusBar().showMessage('O projeto foi carregado!')
        isantigo = True
...
def iniciaFerramenta1(inicio):
    subprocess.call('sag_gui_tool1.exe')
...
def iniciaFerramenta2(inicio):
    subprocess.call('sag_gui_tool2.exe')
...
def iniciaFerramenta3(inicio):
    subprocess.call('sag_gui_tool3.exe')
...
def iniciaFerramenta4(inicio):
    subprocess.call('sag_gui_tool4.exe')
...


#criacao do aplicativo principal
sag_launcher = QApplication(sys.argv)

inicio = QMainWindow()
inicio.setWindowTitle("Sistema Base de Aferição UFRRJ")
inicio.setWindowIcon(QtGui.QIcon('4imgs//capa.png'))
inicio.width = 400
inicio.height = int(0.618 * inicio.width)
inicio.resize(inicio.width, inicio.height)

"""
menu = inicio.menuBar()
menu_arquivo = menu.addMenu('Arquivo')
menu_ajuda = menu.addMenu('Ajuda')
menu_sobre = menu.addMenu('Sobre')

#Acoes Arquivo
arquivoNovoProjeto = QAction(QtGui.QIcon('novoprojeto.png'), 'Novo Projeto', inicio)
cmdArquivoNovoProjeto = partial(novoProjeto, inicio)
arquivoNovoProjeto.triggered.connect(cmdArquivoNovoProjeto)

arquivoAbrirProjeto = QAction(QtGui.QIcon('abrirprojeto.png'), 'Abrir Projeto', inicio)
cmdArquivoAbrirProjeto = partial(antigoProjeto, inicio)
arquivoAbrirProjeto.triggered.connect(cmdArquivoAbrirProjeto)

menu_arquivo.addAction(arquivoNovoProjeto)
menu_arquivo.addAction(arquivoAbrirProjeto)
"""

ferramentas = QGroupBox(inicio)
inicio.setCentralWidget(ferramentas)

ferramenta1 = QPushButton(QtGui.QIcon('4imgs//ferramenta1.png'), 'Ajustamento de Rede GNSS')
cmdFerramenta1 = partial(iniciaFerramenta1, inicio)
ferramenta1.clicked.connect(cmdFerramenta1)


ferramenta2 = QPushButton(QtGui.QIcon('4imgs//ferramenta2.png'), 'Ângulo Padrão')
cmdFerramenta2 = partial(iniciaFerramenta2, inicio)
ferramenta2.clicked.connect(cmdFerramenta2)

ferramenta3 = QPushButton(QtGui.QIcon('4imgs//ferramenta3.png'), 'Aferição de Goniômetros')
cmdFerramenta3 = partial(iniciaFerramenta3, inicio)
ferramenta3.clicked.connect(cmdFerramenta3)

ferramenta4 = QPushButton(QtGui.QIcon('4imgs//ferramenta4.png'), 'Aferição de Distanciômetros')
cmdFerramenta4 = partial(iniciaFerramenta4, inicio)
ferramenta4.clicked.connect(cmdFerramenta3)

texto = QLabel('Selecione uma ferramenta!')
texto.setAlignment(Qt.AlignCenter)

ferramentas_layout = QVBoxLayout()
pic = QLabel(inicio)
pixmap = QtGui.QPixmap("4imgs//capa.png")
pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
pic.setPixmap(pixmap)
pic.setAlignment(Qt.AlignCenter)
ferramentas_layout.addWidget(pic)
ferramentas_layout.addWidget(texto)
ferramentas_layout.addWidget(ferramenta1)
ferramentas_layout.addWidget(ferramenta2)
ferramentas_layout.addWidget(ferramenta3)
ferramentas_layout.addWidget(ferramenta4)
ferramentas.setLayout(ferramentas_layout)

inicio.statusBar().showMessage('SBA_UFRRJ - versão: 0.0.1')
inicio.show()

sys.exit(sag_launcher.exec_())