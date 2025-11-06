from PyQt5.QtWidgets import ( 
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QListWidget, QMessageBox, QFrame, QSizePolicy, QLineEdit, QGridLayout, 
    QStackedWidget, QComboBox, QSpacerItem, QCheckBox, QTableWidget, QTableWidgetItem
)

from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime 
import sys
import sqlite3
import os

THEME = {
    "fundo": "#50766A", 
    "texto": "#E1E4E6",
    "painel_lateral": "#7EA198",
    "texto_principal": "#FFFFFF",
    "botao": "#50766E",
    "botao_hover": "#133930",
    "texto_fila": "#FFFFFF",
    "planofundo": "#737B78",
}

class Tela_Principal(QWidget):
##conexao ao db
    def conectar_banco(self):
        try:
            conexao = sqlite3.connect('clinica_vidamais.db')
            cursor = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT NOT NULL UNIQUE,
                    telefone TEXT,
                    idade INTEGER
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medicos(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    crm TEXT NOT NULL UNIQUE,
                    area TEXT,
                    idade INTEGER
                )
            """)
            conexao.commit()
            return conexao, cursor
        
        except sqlite3.Error as e:
            print(f"ERRO: Não foi possível conectar/criar o DB: {e}")
            return None, None
##tela init onde abrange todos os widgets, com o principal
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CLINICA VIDA+ - SISTEMA DE GESTAO")
        self.setWindowIcon(QIcon('clinicavida.png'))
        self.resize(1000, 600)
        self.setStyleSheet(f"background-color: {THEME['planofundo']}")

        self.conexao, self.cursor = self.conectar_banco()
        if self.conexao is None:
             return 

        widget_central = QVBoxLayout(self)
        widget_central.setContentsMargins(0,0,0,0)
        widget_central.setSpacing(0)

        self.lista_fila_widget = QListWidget() 
        self.lista_fila_widget.setContentsMargins(0,0,0,0)
        
        self.lista_fila_widget.itemDoubleClicked.connect(self.remover_fila)

        parte_cima = QFrame()
        parte_cima.setStyleSheet(f"background-color: {THEME['fundo']}; color: {THEME['texto']}; margin: 15px; border-radius: 25px;") 
    
        parte_cima_layout = QHBoxLayout(parte_cima)
        parte_cima_layout.setContentsMargins(10,0,10,0)

        logo = QLabel("CLINICA VIDA+")
        logo.setFont(QFont("Times New Roman", 30, QFont.Bold))
        logo.setStyleSheet(f"color: {THEME['texto_principal']};")
        parte_cima_layout.addWidget(logo)
        parte_cima_layout.addStretch()

        widget_central.addWidget(parte_cima) 

        layout_cheio = QHBoxLayout()
        layout_cheio.setContentsMargins(15, 15, 15, 15)
        layout_cheio.setSpacing(15)

        self.painel_menu = QFrame()
        self.painel_menu.setFixedWidth(350)
        self.painel_menu.setStyleSheet(f"background-color: {THEME['painel_lateral']}; border-radius: 25px;")
        self.layout_menu = QVBoxLayout(self.painel_menu)
        self.layout_menu.setContentsMargins(10, 10, 10, 10)

        self.btn_cadastro = self.criar_botao_click("CADASTRO COMPLETO")
        self.btn_medicos = self.criar_botao_click("MEDICOS DISPONIVEIS")
        self.btn_estatisticas = self.criar_botao_click("DADOS PACIENTES")

        self.layout_menu.addWidget(self.btn_cadastro)
        self.layout_menu.addWidget(self.btn_medicos)
        self.layout_menu.addWidget(self.btn_estatisticas)
        self.layout_menu.addStretch()
        
        layout_cheio.addWidget(self.painel_menu) 

        self.stacked_widget = QStackedWidget()
        layout_cheio.addWidget(self.stacked_widget) 
        self.stacked_widget.addWidget(self.tela_inicial())
        self.idx_cadastro = self.stacked_widget.addWidget(self.criar_tela_cadastro())
        self.btn_cadastro.clicked.connect(self.mostrar_tela_cadastro)
        self.medicos_ui_cadastro = self.cadastro_medicos_ui()
        self.idx_cadastro_med = self.stacked_widget.addWidget(self.medicos_ui_cadastro) 
        self.medicos_ui_tabela = self.medicos_disponiveis() 
        self.idx_medicos = self.stacked_widget.addWidget(self.medicos_ui_tabela)
        self.btn_medicos.clicked.connect(self.mostrar_medicos_click)
        self.btn_medicos.clicked.connect(self.carregar_medicos)
        self.idx_dados = self.stacked_widget.addWidget(self.dados_pacientes())
        self.btn_estatisticas.clicked.connect(self.mostrar_tela_dados)
        self.btn_estatisticas.clicked.connect(self.carregar_pacientes)

        self.painel_fila = self.criar_fila()
        self.painel_fila.setFixedWidth(350)
        layout_cheio.addWidget(self.painel_fila) 
        widget_central.addLayout(layout_cheio)

##tela inicial pos init
    def tela_inicial(self):
        tela = QWidget()
        layout_tela = QVBoxLayout()
        tela.setLayout(layout_tela)
        layout_tela.addWidget(QLabel())
        return tela

##botao de click para a esqierda
    def criar_botao_click(self, text):
        botao = QPushButton(text)
        fonte = QFont("Times New Roman", 12, QFont.Bold) 
        botao.setFont(fonte)
        botao.setFixedHeight(150)
        botao.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['botao']};
                color : {THEME['texto']}; 
                border-radius: 15px;
                border: 3px solid {THEME['texto_fila']};
            }}
            QPushButton:hover{{
                background-color: {THEME['botao_hover']};
                color: {THEME['fundo']};
            }}
""")
        return botao

##criacao da fila (painel lateral)
    def criar_fila(self):
        painel = QFrame()

        painel.setStyleSheet(f"background-color: {THEME['painel_lateral']}; border-radius: 25px; padding: 10px;")
        painel_layout = QVBoxLayout(painel)
        
        titulo_painel = QLabel("FILA DE ATENDIMENTO")
        fonte = QFont("Times New Roman", 16, QFont.Bold)
        titulo_painel.setFont(fonte)
        titulo_painel.setStyleSheet(f"color: {THEME['texto']}; margin-bottom: 10px;")
        painel_layout.addWidget(titulo_painel, alignment=Qt.AlignCenter) 

        label_pacientes = QLabel("PACIENTES NA FILA")
        label_pacientes.setStyleSheet(f"color: {THEME['texto_fila']};")
        painel_layout.addWidget(label_pacientes)
        
        self.lista_fila_widget.setStyleSheet(f"background-color: {THEME['fundo']}; color: {THEME['texto_fila']}; border-radius: 25px; padding: 10px;")
        self.lista_fila_widget.setMinimumHeight(300)
        painel_layout.addWidget(self.lista_fila_widget)

        painel_layout.addStretch()

        return painel

##tela cadastro pos click no botao
    def criar_tela_cadastro(self):
        cadastro_tela = QWidget()
        layout_cadastro = QGridLayout()
        cadastro_tela.setLayout(layout_cadastro)

        self.nome_cadastro = QLabel("Nome Completo:")
        self.texto_nome = QLineEdit()
        self.cpf_cadastro = QLabel("CPF: ")
        self.texto_cpf = QLineEdit()
        self.telefone_cadastro = QLabel("Telefone:")
        self.texto_telefone = QLineEdit()
        self.idade_cadastro = QLabel("Idade:")
        self.texto_idade = QLineEdit()

        layout_cadastro.addWidget(self.idade_cadastro, 3,0)
        layout_cadastro.addWidget(self.texto_idade,3,1)
        layout_cadastro.addWidget(self.telefone_cadastro, 2,0)
        layout_cadastro.addWidget(self.texto_telefone, 2, 1)
        layout_cadastro.addWidget(self.cpf_cadastro, 1, 0)
        layout_cadastro.addWidget(self.texto_cpf, 1, 1)
        layout_cadastro.addWidget(self.nome_cadastro, 0, 0)
        layout_cadastro.addWidget(self.texto_nome, 0, 1)

        btn_salvar = QPushButton("Salvar Cadastro")
        btn_salvar.setFixedHeight(75)
        
        layout_cadastro.addWidget(btn_salvar, 5,0,1,2)
        layout_cadastro.addItem(QSpacerItem(20,40, QSizePolicy.Expanding), 5, 0)
        
        fonte = QFont("Times New Roman", 12, QFont.Bold)
        cadastro_tela.setFont(fonte)
        cadastro_tela.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['botao']};
                color : {THEME['texto']}; 
                border-radius: 15px;
                border: 3px solid {THEME['texto_fila']};
            }}
            QPushButton:hover{{
                background-color: {THEME['botao_hover']};
                color: {THEME['fundo']};
            }}
""")
        self.nome_cadastro.setFont(fonte)
        self.texto_nome.setFont(fonte)
        self.cpf_cadastro.setFont(fonte)
        self.texto_cpf.setFont(fonte)
        self.telefone_cadastro.setFont(fonte)
        self.texto_telefone.setFont(fonte)
        self.idade_cadastro.setFont(fonte)
        self.texto_idade.setFont(fonte)

        self.texto_telefone.setStyleSheet(f"color: {THEME['texto']};")
        self.telefone_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.nome_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.texto_nome.setStyleSheet(f"color: {THEME['texto']};")
        self.cpf_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.texto_cpf.setStyleSheet(f"color: {THEME['texto']};")
        self.texto_idade.setStyleSheet(f"color: {THEME['texto']};")
        self.idade_cadastro.setStyleSheet(f"color: {THEME['texto']};")

        btn_salvar.clicked.connect(self.validar_cadastro)
    
        return cadastro_tela

##index pra clicar no botao. 
    def mostrar_tela_cadastro(self):
        self.stacked_widget.setCurrentIndex(self.idx_cadastro)

##tela de dados paciente pos click
    def dados_pacientes(self):
        dados = QWidget()
        layout_dados = QGridLayout()
        dados.setLayout(layout_dados)

        self.tabela_pacientes = QTableWidget()
        self.tabela_pacientes.setColumnCount(4) 
        self.tabela_pacientes.setHorizontalHeaderLabels(
            [ "NOME", "CPF", "Telefone", "Idade"]
        )
        self.tabela_pacientes.setStyleSheet(f"""
            QTableWidget {{
                background-color: {THEME['fundo']}; 
                color: {THEME['texto_principal']}; 
                border-radius: 25px; 
                padding: 10px;
                gridline-color: {THEME['planofundo']};
            }}
            QHeaderView::section {{
                background-color: {THEME['botao_hover']};
                color: {THEME['texto_principal']};
                padding: 5px;
           }}
            QTableCornerButton::section{{
                background-color: {THEME['botao']};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
""")    
        self.tabela_pacientes.itemDoubleClicked.connect(self.confirmar_deletar_paciente)
        self.buscar_pacientes = QLabel("Buscar por Nome:")
        self.buscar_pacientes.setStyleSheet(f"color: {THEME['texto']};")
        self.buscar_pacientes_caixa = QLineEdit()
        self.buscar_pacientes_caixa.setStyleSheet(f"color: {THEME['texto']};")
        btn_buscar = QPushButton("BUSCAR PACIENTE")
        btn_buscar.setFixedHeight(75)
        btn_buscar.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['botao']};
                color: {THEME['texto']}; 
                border-radius: 10px;
            }}
            QPushButton:hover{{
                background-color: {THEME['botao_hover']};
            }}
        """)
        fonte = QFont("Times New Roman", 12, QFont.Bold)
        self.buscar_pacientes.setFont(fonte)
        btn_buscar.setFont(fonte)
        self.tabela_pacientes.setFont(fonte)
        self.buscar_pacientes_caixa.textChanged.connect(self.pesquisar) 

        layout_para_busca = QHBoxLayout()
        layout_para_busca.addWidget(self.buscar_pacientes)
        layout_para_busca.addWidget(self.buscar_pacientes_caixa)
        layout_para_busca.addWidget(btn_buscar)

        layout_dados.addLayout(layout_para_busca, 0, 0, 1, 3)
        layout_dados.addWidget(self.tabela_pacientes, 1, 0, 1, 3)
    
        enviar_fila = QPushButton("Enviar para a fila.")
        enviar_fila.setFixedHeight(75)
        enviar_fila.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['botao']};
                color: {THEME['texto']}; 
                border-radius: 10px;
            }}
            QPushButton:hover{{
                background-color: {THEME['botao_hover']};
            }}
        """)
        enviar_fila.setFont(fonte)

        layout_dados.addWidget(enviar_fila, 2, 0, 1, 1)
        enviar_fila.clicked.connect(self.enviar_para_fila)

        return dados

##index pra mostrar pos click
    def mostrar_tela_dados(self):
        self.stacked_widget.setCurrentIndex(self.idx_dados)

## Qmessagebox configurado pra simplificar o codigo
    def mostrar_aviso(self, titulo, mensagem):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(titulo)
        msg.setText(mensagem)
        
        cor_fundo_clara = THEME['fundo'] 
        cor_texto_claro = THEME['texto_principal'] 
        
        msg.setStyleSheet(f"""
            QMessageBox {{ 
            }}
            
            QLabel {{ 
                color: {cor_texto_claro}; 
                background-color: transparent; 
                min-width: 300px;
                padding: 10px; 
            }}
            QPushButton {{
                background-color: {THEME['botao']}; 
                color: {THEME['texto']}; 
            }}
        """)
        msg.exec_()

##cuidado com erros de cadastro (digitar numeros onde ficam letras)
    def validar_cadastro(self):
        nome = self.texto_nome.text()
        if not nome:
            self.mostrar_aviso( "Erro de Validacao", "O campo 'Nome Completo' esta vazio!")
            return
        if not nome.replace(" ", "").isalpha():
            self.mostrar_aviso("Erro de Validação", "O campo 'Nome Completo' deve conter apenas letras e espaços!")
            return
            
        idade_text = self.texto_idade.text()
        if idade_text:
            try:
                idade = int(idade_text) 
                if idade <= 0 or idade >= 125:
                    self.mostrar_aviso("ERRO", "A Idade deve ser maior que 0! ou menor que 125 e valida!")
                    return 
            except ValueError:
                self.mostrar_aviso( "Erro de Validacao!", "O Campo idade deve conter numeros inteiros validos!")
                return
            
        cpf_text = self.texto_cpf.text()
        
        if not cpf_text:
            self.mostrar_aviso("Erro de Validação", "O campo CPF é obrigatório e está vazio!")
            return
            
        try:
            int(cpf_text)
        except ValueError:
            self.mostrar_aviso("Erro de Validacao!", "O campo CPF deve haver somente numeros.")
            return
        
        telefone_text = self.texto_telefone.text()
        if telefone_text:
            try:
                int(telefone_text)
            except ValueError:
                self.mostrar_aviso( "Erro de Validacao","O campo Telefone deve haver somente numeros!")
                return 
        
        nome = self.texto_nome.text()
        cpf = self.texto_cpf.text()
        telefone = self.texto_telefone.text()
        idade = int(self.texto_idade.text()) if self.texto_idade.text() else None 
        self.salvar_paciente(nome, cpf, telefone, idade)

##inserir e salvar paciente no banco de dados sqlite
    def salvar_paciente(self, nome, cpf, telefone, idade):
        comando_sql = """
        INSERT INTO pacientes (nome, cpf, telefone, idade)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.cursor.execute(comando_sql, (nome, cpf, telefone, idade))
            self.conexao.commit()
            self.mostrar_aviso("Sucesso", "Paciente cadastrado com sucesso!")
            
            self.texto_nome.clear()
            self.texto_cpf.clear()
            self.texto_telefone.clear()
            self.texto_idade.clear()
        except sqlite3.IntegrityError:
            self.mostrar_aviso("Erro de cadastro","CPF Identico a outro.")
        except sqlite3.Error as e:
            self.mostrar_aviso("Erro no Banco de dados.", f"Ocorreu um erro ao salvar: {e}")

##carregar pacientes pos cadastro
    def carregar_pacientes(self):
        self.tabela_pacientes.setRowCount(0)
        buscar = self.buscar_pacientes_caixa.text().strip()
        try:
            if buscar:
                comando_sql = "SELECT nome, cpf, telefone, idade FROM pacientes WHERE nome LIKE ?"
                parametros_busca = (f'%{buscar}%',)
            else:
                comando_sql = "SELECT nome, cpf, telefone, idade FROM pacientes"
                parametros_busca = ()

            self.cursor.execute(comando_sql, parametros_busca)
            pacientes = self.cursor.fetchall()
            flags_nao_editavel = Qt.ItemIsSelectable | Qt.ItemIsEnabled 
            
            for linha_pac, linha_dados in enumerate(pacientes):
                self.tabela_pacientes.insertRow(linha_pac)
                for coluna_pac, dado in enumerate(linha_dados):
                    item = QTableWidgetItem(str(dado))
                    item.setFlags(flags_nao_editavel) 
                    self.tabela_pacientes.setItem(
                        linha_pac, coluna_pac, item
                    )

            self.tabela_pacientes.horizontalHeader().setStretchLastSection(True)

            self.pesquisar(self.buscar_pacientes_caixa.text()) 

        except sqlite3.Error as e:
            self.mostrar_aviso("Erro de Leitura", f"Erro ao buscar Pacientes {e}")

## carrega os medicos 
    def carregar_medicos(self):
        self.medicos_tabela.setRowCount(0)
        try:
            comando_sql = "SELECT nome, crm, area, idade FROM medicos"
            self.cursor.execute(comando_sql)
            dados_medicos = self.cursor.fetchall()
            
            flags_nao_editavel = Qt.ItemIsSelectable | Qt.ItemIsEnabled 

            for linha_indice, linha_dados in enumerate(dados_medicos):
                self.medicos_tabela.insertRow(linha_indice)
                for coluna_indice, dado in enumerate(linha_dados):
                    item = QTableWidgetItem(str(dado))
                    item.setFlags(flags_nao_editavel)
                    self.medicos_tabela.setItem(linha_indice, coluna_indice, item)

            self.medicos_tabela.horizontalHeader().setStretchLastSection(True)
        except sqlite3.Error as e:
            self.mostrar_aviso("Erro de Leitura", f"Erro ao buscar Médicos: {e}")

##pesquisa de pacientes por nome da tela_dados
    def pesquisar(self, texto_digitado):
        pesquisado = texto_digitado.lower()

        for linha in range(self.tabela_pacientes.rowCount()): 
            item_nome = self.tabela_pacientes.item(linha, 0)
            if item_nome is not None:
                nome_na_celula = item_nome.text().lower()
                if pesquisado in nome_na_celula:
                    self.tabela_pacientes.setRowHidden(linha, False) 
                else: 
                    self.tabela_pacientes.setRowHidden(linha, True) 

##algoritmo pra enviar o paciente pra fila apos apertar o botao
    def enviar_para_fila(self):
        selecionado = self.tabela_pacientes.selectedItems()
        if not selecionado:
            self.mostrar_aviso("Fila de atedimento", " Selecione um paciente na tabela")
            return
        
        paciente_selecionado = selecionado[0].row() 
        
        nome_paciente = self.tabela_pacientes.item(paciente_selecionado, 0).text()
        cpf_paciente = self.tabela_pacientes.item(paciente_selecionado, 1).text() 
        
        horario = QDateTime.currentDateTime().toString("hh:mm:ss")
        item_fila = f"[{horario}] NOME: {nome_paciente} CPF: {cpf_paciente}"
        self.lista_fila_widget.addItem(item_fila)

        self.mostrar_aviso("Fila de Atendimaento", f"{nome_paciente} adicionado a fila!")

##algoritmo para remover o paciente da fila 
    def remover_fila(self):
        item_selecionado = self.lista_fila_widget.currentItem()
        if item_selecionado:
            indice_da_linha = self.lista_fila_widget.row(item_selecionado)
            self.lista_fila_widget.takeItem(indice_da_linha) 
            self.mostrar_aviso("Fila", f"Paciente {item_selecionado.text()} removido da fila!")

##click botao medicos abrir o menu de medicos
    def medicos_disponiveis(self):
        medicos = QWidget()
        medicos_layout = QGridLayout()
        medicos.setLayout(medicos_layout)
        
        self.medicos_tabela = QTableWidget()
        self.medicos_tabela.setColumnCount(4)
        self.medicos_tabela.setHorizontalHeaderLabels(
            ["Nome", "CRM", "Area", "Idade" ]
        )
        self.medicos_tabela.setStyleSheet(f"""
            QTableWidget {{
                background-color: {THEME['fundo']}; 
                color: {THEME['texto_principal']}; 
                border-radius: 25px; 
                padding: 10px;
                gridline-color: {THEME['planofundo']};
            }}
            QHeaderView::section {{
                background-color: {THEME['botao_hover']};
                color: {THEME['texto_principal']};
                padding: 5px;
           }}
            QTableCornerButton::section{{
                background-color: {THEME['botao']};
            }}
            QTableWidget::item {{
                padding: 5px;
            }}
""")
        self.medicos_tabela.itemDoubleClicked.connect(self.confirmar_deletar_medico)
        btn_adicionar_medicos = QPushButton("Adicionar Medicos.")
        btn_adicionar_medicos.setFixedHeight(75)
        btn_adicionar_medicos.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['botao']};
                color: {THEME['texto']};
                border-radius: 10px;
            }}
            QPushButton:hover{{
                background-color: {THEME['botao_hover']};
            }}
""") 
        medicos_layout.addWidget(btn_adicionar_medicos, 2,0, 1, 3)
        btn_adicionar_medicos.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(self.idx_cadastro_med)) 

        medicos_layout.addWidget(self.medicos_tabela, 1, 0, 1, 3)

        return medicos

##click no botao de medigos index
    def mostrar_medicos_click(self):
        self.stacked_widget.setCurrentIndex(self.idx_medicos)

##pagina para cadastro de medicos 
    def cadastro_medicos_ui(self):
        cadastro_medicos_tela = QWidget()
        layout_cadastro_med = QGridLayout()
        cadastro_medicos_tela.setLayout(layout_cadastro_med)

        self.med_nome_cadastro = QLabel("Nome Completo:")
        self.med_texto_nome = QLineEdit()
        self.med_crm_cadastro = QLabel("Informe o CRM:")
        self.med_texto_crm = QLineEdit()
        self.med_area_cadastro = QLabel("Informe a Area do medico:")
        self.med_texto_area = QLineEdit()
        self.med_idade_cadastro = QLabel("Idade:")
        self.med_texto_idade = QLineEdit()

        layout_cadastro_med.addWidget(self.med_texto_nome, 0,1)
        layout_cadastro_med.addWidget(self.med_nome_cadastro,0, 0)
        layout_cadastro_med.addWidget(self.med_crm_cadastro, 1,0) 
        layout_cadastro_med.addWidget(self.med_texto_crm, 1,1) 
        layout_cadastro_med.addWidget(self.med_texto_area, 2, 1)
        layout_cadastro_med.addWidget(self.med_area_cadastro, 2, 0)
        layout_cadastro_med.addWidget(self.med_idade_cadastro, 3, 0)
        layout_cadastro_med.addWidget(self.med_texto_idade, 3, 1)

        btn_salvar_medico = QPushButton("Salvar Medico")
        btn_salvar_medico.setFixedHeight(75)
        layout_cadastro_med.addWidget(btn_salvar_medico, 5,0,1,2)
        layout_cadastro_med.addItem(QSpacerItem(20,40, QSizePolicy.Expanding), 5,0 )

        fonte = QFont("Times New Roman", 12, QFont.Bold)
        cadastro_medicos_tela.setFont(fonte)
        cadastro_medicos_tela.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['botao']};
                color : {THEME['texto']}; 
                border-radius: 15px;
                border: 3px solid {THEME['texto_fila']};
            }}
            QPushButton:hover{{
                background-color: {THEME['botao_hover']};
                color: {THEME['fundo']};
            }}
""")
        self.med_nome_cadastro.setFont(fonte)
        self.med_texto_nome.setFont(fonte)
        self.med_crm_cadastro.setFont(fonte)
        self.med_texto_crm.setFont(fonte) 
        self.med_area_cadastro.setFont(fonte)
        self.med_texto_area.setFont(fonte) 
        self.med_idade_cadastro.setFont(fonte)
        self.med_texto_idade.setFont(fonte)

        self.med_nome_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.med_texto_nome.setStyleSheet(f"color: {THEME['texto']};")
        self.med_crm_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.med_texto_crm.setStyleSheet(f"color: {THEME['texto']};")
        self.med_area_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.med_texto_area.setStyleSheet(f"color: {THEME['texto']};")
        self.med_idade_cadastro.setStyleSheet(f"color: {THEME['texto']};")
        self.med_texto_idade.setStyleSheet(f"color: {THEME['texto']};")

        btn_salvar_medico.clicked.connect(self.validar_medicos)

        return cadastro_medicos_tela

##validacao feita igual nos pacientes
    def validar_medicos(self):
        nome = self.med_texto_nome.text().strip()
        crm_text = self.med_texto_crm.text().strip() 
        area = self.med_texto_area.text().strip()
        idade_text = self.med_texto_idade.text().strip()
        
        if not nome:
            self.mostrar_aviso( "Erro de Validacao", "O campo 'Nome Completo' do Médico esta vazio!")
            return
        if not nome.replace(" ", "").isalpha():
            self.mostrar_aviso("Erro de Validação", "O campo 'Nome Completo' deve conter apenas letras e espaços!")
            return

        if not crm_text:
            self.mostrar_aviso("Erro de Validacao!", "O campo CRM deve ser preenchido.")
            return
        try: 
            int(crm_text)
        except ValueError:
            self.mostrar_aviso("Erro de Validacao!", "O campo CRM deve conter somente numeros")
            return
        
        if not area:
            self.mostrar_aviso("Erro de validacao", " O campo 'area' esta vazio")
            return
        if not area.replace(" ","").isalpha():
            self.mostrar_aviso("Erro de Validação", "O campo 'area' deve conter apenas letras e espaços!")
            return

        if idade_text:
            try:
                idade = int(idade_text) 
                if idade <= 0 or idade >= 125:
                    self.mostrar_aviso("ERRO", "A Idade deve ser maior que 0! ou menor que 125 e valida!")
                    return 
            except ValueError:
                self.mostrar_aviso( "Erro de Validacao!", "O Campo idade deve conter numeros inteiros validos!")
                return
        else:
             idade = None
        try:
            self.carregar_medicos()
        except:
            pass
        
        self.cadastrar_medicos(nome, crm_text, area, idade)

##cadastro de medicos no db
    def cadastrar_medicos(self, nome, crm, area, idade):
        medicos_sql = """
        INSERT INTO medicos (nome, crm, area, idade)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.cursor.execute(medicos_sql, (nome, crm, area, idade))
            self.conexao.commit()
            self.mostrar_aviso("Sucesso", f"{nome}, cadastrado com sucesso!")
            self.med_texto_nome.clear()
            self.med_texto_crm.clear()
            self.med_texto_area.clear()
            self.med_texto_idade.clear()
            self.stacked_widget.setCurrentIndex(self.idx_medicos)
            self.carregar_medicos() 
            
        except sqlite3.IntegrityError:
            self.mostrar_aviso("ERRO", "CRM Identico a outro médico já cadastrado.")
        except sqlite3.Error as e:
            self.mostrar_aviso("Erro no DB", f"Ocorreu erro ao salvar: {e}")
## duas funcoes iguais porem com algumas escritas diferentes
## onde as duas deletam um paciente ou medico com clique duplo
    def confirmar_deletar_paciente(self, item):
        row = item.row()
        nome = self.tabela_pacientes.item(row, 0).text()
        cpf = self.tabela_pacientes.item(row, 1).text()

        if self.mostrar_confirmacao(
            "Remover Paciente",
            f"Deseja remover o'{nome}')?"
        ):
            try:
                self.cursor.execute("DELETE FROM pacientes WHERE cpf = ?", (cpf,))
                self.conexao.commit()
                self.mostrar_aviso("Sucesso", f"Paciente {nome} removido.")
                self.carregar_pacientes()
            except sqlite3.Error as e:
                self.mostrar_aviso("Erro no DB", str(e))

    def confirmar_deletar_medico(self, item):
        row = item.row()
        nome = self.medicos_tabela.item(row, 0).text()
        crm = self.medicos_tabela.item(row, 1).text()

        if self.mostrar_confirmacao(
            "Remover Medico",
            f"Deseja remover '{nome}'?"
        ):
            try:
                self.cursor.execute("DELETE FROM medicos WHERE crm = ?", (crm,))
                self.conexao.commit()
                self.mostrar_aviso("Sucesso", f"Médico {nome} removido.")
                self.carregar_medicos()
            except sqlite3.Error as e:
                self.mostrar_aviso("Erro no DB", str(e))
## para as Qmessage box ficarem simplificadas
    def mostrar_confirmacao(self, titulo, mensagem):
        caixa = QMessageBox(self)
        caixa.setWindowTitle(titulo)
        caixa.setText(mensagem)

        caixa.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        caixa.setDefaultButton(QMessageBox.No)

        caixa.setStyleSheet(f"""
            QMessageBox {{
                background-color: {THEME['fundo']};
                color: {THEME['texto_principal']};
                font-size: 14px;
            }}
            QLabel {{
                color: {THEME['texto_principal']};
                background: transparent;
                padding: 5px;
                min-width: 260px;
            }}
            QPushButton {{
                background-color: {THEME['botao']};
                color: {THEME['texto']};
                padding: 6px 14px;
                border-radius: 37px;
            }}
            QPushButton:hover {{
                background-color: {THEME['botao']};
            }}
        """)

        resposta = caixa.exec_()
        return resposta == QMessageBox.Yes

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela_principal = Tela_Principal() 
    janela_principal.show()
    sys.exit(app.exec_())