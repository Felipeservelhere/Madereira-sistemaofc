import subprocess
import sys
import json
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from fpdf import FPDF
from datetime import datetime

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ['PyQt5', 'fpdf']

# Check and install required packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        install(package)

class ProdutosDialog(QtWidgets.QDialog):
    def __init__(self, produtos, on_edit, on_delete):
        super().__init__()
        self.setWindowTitle("Produtos Registrados")
        self.setGeometry(200, 200, 400, 300)  # Window size
        self.on_edit = on_edit
        self.on_delete = on_delete

        layout = QtWidgets.QVBoxLayout(self)

        if not produtos:
            layout.addWidget(QtWidgets.QLabel("Nenhum produto registrado."))
        else:
            self.produtos_list = QtWidgets.QListWidget()
            for produto in produtos:
                self.produtos_list.addItem(produto["descricao"])
            layout.addWidget(self.produtos_list)

            # Buttons for editing and deleting
            btn_layout = QtWidgets.QHBoxLayout()
            self.btn_edit = QtWidgets.QPushButton("Editar Produto")
            self.btn_edit.clicked.connect(self.edit_selected_product)
            btn_layout.addWidget(self.btn_edit)

            self.btn_delete = QtWidgets.QPushButton("Excluir Produto")
            self.btn_delete.clicked.connect(self.delete_selected_product)
            btn_layout.addWidget(self.btn_delete)

            layout.addLayout(btn_layout)

        self.setLayout(layout)

    def edit_selected_product(self):
        selected_items = self.produtos_list.selectedItems()
        if selected_items:
            selected_product = selected_items[0].text()
            self.on_edit(selected_product)
            self.accept()  # Close the dialog

    def delete_selected_product(self):
        selected_items = self.produtos_list.selectedItems()
        if selected_items:
            selected_product = selected_items[0].text()
            reply = QtWidgets.QMessageBox.question(self, 'Confirmar Exclusão',
                                                   f"Tem certeza que deseja excluir o produto '{selected_product}'?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.on_delete(selected_product)
                QtWidgets.QMessageBox.information(self, "Sucesso", f"Produto '{selected_product}' excluído com sucesso!")
                self.accept()  # Close the dialog after deletion

class ClientesDialog(QtWidgets.QDialog):
    def __init__(self, clientes, on_edit, on_delete):
        super().__init__()
        self.setWindowTitle("Clientes Registrados")
        self.setGeometry(200, 200, 400, 300)  # Window size
        self.on_edit = on_edit
        self.on_delete = on_delete

        layout = QtWidgets.QVBoxLayout(self)

        if not clientes:
            layout.addWidget(QtWidgets.QLabel("Nenhum cliente registrado."))
        else:
            self.clientes_list = QtWidgets.QListWidget()
            for cliente in clientes:
                self.clientes_list.addItem(cliente["nome"])
            layout.addWidget(self.clientes_list)

            # Buttons for editing and deleting
            btn_layout = QtWidgets.QHBoxLayout()
            self.btn_edit = QtWidgets.QPushButton("Editar Cliente")
            self.btn_edit.clicked.connect(self.edit_selected_client)
            btn_layout.addWidget(self.btn_edit)

            self.btn_delete = QtWidgets.QPushButton("Excluir Cliente")
            self.btn_delete.clicked.connect(self.delete_selected_client)
            btn_layout.addWidget(self.btn_delete)

            layout.addLayout(btn_layout)

        self.setLayout(layout)

    def edit_selected_client(self):
        selected_items = self.clientes_list.selectedItems()
        if selected_items:
            selected_client = selected_items[0].text()
            self.on_edit(selected_client)
            self.accept()  # Close the dialog

    def delete_selected_client(self):
        selected_items = self.clientes_list.selectedItems()
        if selected_items:
            selected_client = selected_items[0].text()
            reply = QtWidgets.QMessageBox.question(self, 'Confirmar Exclusão',
                                                   f"Tem certeza que deseja excluir o cliente '{selected_client}'?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.on_delete(selected_client)
                QtWidgets.QMessageBox.information(self, "Sucesso", f"Cliente '{selected_client}' excluído com sucesso!")
                self.accept()  # Close the dialog after deletion

class RelatorioDialog(QtWidgets.QDialog):
    def __init__(self, orcamento_produtos):
        super().__init__()
        self.setWindowTitle("Relatório de Vendas")
        self.setGeometry(200, 200, 1500, 600)

        layout = QtWidgets.QVBoxLayout(self)

        # Título do Relatório
        titulo = QtWidgets.QLabel("RELATÓRIO")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        # Configuração da Tabela
        self.tabela = QtWidgets.QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["PRODUTOS", "QUANTIDADE", "VALOR UNITÁRIO", "VALOR TOTAL", "CLIENTE"])
        self.tabela.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tabela.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Não permite edição

        if not orcamento_produtos:
            self.tabela.setRowCount(1)
            self.tabela.setItem(0, 0, QtWidgets.QTableWidgetItem("Nenhuma venda registrada."))
        else:
            self.orcamento_produtos = orcamento_produtos
            self.exibir_dados(orcamento_produtos)

        layout.addWidget(self.tabela)
        self.setLayout(layout)

    def exibir_dados(self, dados):
        self.tabela.setRowCount(len(dados))
        for row, produto in enumerate(dados):
            descricao = produto["descricao"]
            quantidade = produto["quantidade"]
            vlr_m = produto["vlr_m"]
            total = produto["total"]
            cliente = produto.get("cliente", "N/A")

            # Preenche os dados na tabela
            self.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(descricao))
            self.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem(str(quantidade)))
            self.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(f"R$ {vlr_m:.2f}"))
            self.tabela.setItem(row, 3, QtWidgets.QTableWidgetItem(f"R$ {total:.2f}"))
            self.tabela.setItem(row, 4, QtWidgets.QTableWidgetItem(cliente))

class SistemaOrcamentoMadeireira(QtWidgets.QMainWindow):
    # Define a signal to notify when a sale is added
    sale_added = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Orçamento - Madeireira")
        self.setGeometry(100, 100, 1400, 800)  # Increased window size

        # Central widget and layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Tab widget
        self.tabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabs)  # Add the tab widget to the layout

        # Create tabs
        self.tab_produtos = QtWidgets.QWidget()
        self.tab_clientes = QtWidgets.QWidget()
        self.tab_orcamento = QtWidgets.QWidget()

        self.tabs.addTab(self.tab_produtos, "Produtos")
        self.tabs.addTab(self.tab_clientes, "Clientes")
        self.tabs.addTab(self.tab_orcamento, "Orçamento")

        self.sub_tab_widget = QtWidgets.QTabWidget()
        self.tab_produtos_layout = QtWidgets.QVBoxLayout(self.tab_produtos)
        self.tab_produtos_layout.addWidget(self.sub_tab_widget)

        self.tab_produto = QtWidgets.QWidget()
        self.tab_subproduto = QtWidgets.QWidget()  # Initialize as a QWidget

        self.sub_tab_widget.addTab(self.tab_produto, "Produto Fonte")
        self.sub_tab_widget.addTab(self.tab_subproduto, "Sub Produto (m)")

        # Initialize data
        self.produtos = []
        self.subprodutos = []  # For sub-products in linear meters
        self.clientes = []
        self.orcamento_produtos = []  # List to hold products added to the budget
        self.vendas = []  # List to hold sales in cubic meters
        self.arquivo_dados = "dados.json"

        # Create interfaces
        self.criar_interface_produtos()
        self.criar_interface_subprodutos()  # Create interface for sub-products
        self.criar_interface_clientes()
        self.criar_interface_orcamento()

        # Load saved data
        self.carregar_dados()

        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                font-family: 'Garamond', serif;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px;
                font-weight: bold;
                min-width: 307px;  /* Minimum width for tabs */
            }
            QTabBar::tab:selected {
                background: #d0d0d0;
            }
            QWidget {
                background-color: #ffffff;  /* Light background for all tabs */
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #007BFF;  /* Blue border for better contrast */
                border-radius: 0;  /* Square corners */
                min-height: 40px;  /* Increased height */
                background-color: #ffffff;  /* White background for input fields */
                color: #000000;  /* Black text for input fields */
            }
            QLineEdit:focus {
                border: 2px solid #0056b3;  /* Change border color on focus */
            }
            QComboBox {
                padding: 10px;
                border: 2px solid #007BFF;  /* Blue border for better contrast */
                border-radius: 0;  /* Square corners */
                background-color: #ffffff;  /* White background for combo boxes */
                color: #000000;  /* Black text for combo boxes */
            }
            QComboBox:focus {
                border: 2px solid #0056b3;  /* Change border color on focus */
            }
            QLabel {
                font-size: 14px;
                color: #000000;  /* Black text for labels */
            }
        """)

    def criar_interface_produtos(self):
        layout = QtWidgets.QVBoxLayout(self.tab_produto)

        # Product input fields
        self.produto_desc = QtWidgets.QLineEdit()
        self.produto_desc.setPlaceholderText("Descrição do Produto Fonte")
        layout.addWidget(self.produto_desc)

        self.produto_madeira = QtWidgets.QLineEdit()
        self.produto_madeira.setPlaceholderText("Tipo de Madeira")  # New field for wood type
        layout.addWidget(self.produto_madeira)

        self.produto_largura = QtWidgets.QLineEdit()
        self.produto_largura.setPlaceholderText("Largura (em cm)")  # New field for width
        layout.addWidget(self.produto_largura)

        self.produto_espessura = QtWidgets.QLineEdit()
        self.produto_espessura.setPlaceholderText("Espessura (em cm)")  # New field for thickness
        layout.addWidget(self.produto_espessura)

        self.produto_vlr_m = QtWidgets.QLineEdit()
        self.produto_vlr_m.setPlaceholderText("Custo por Metro Cúbico")  # New field for Cost per Cubic Meter
        layout.addWidget(self.produto_vlr_m)

        # Button to register product
        self.btn_adicionar_produto = QtWidgets.QPushButton("Registrar Produto Fonte")
        self.btn_adicionar_produto.clicked.connect(self.adicionar_produto)
        layout.addWidget(self.btn_adicionar_produto)

        # Button to show registered products
        self.btn_mostrar_produtos = QtWidgets.QPushButton("Produtos Registrados")
        self.btn_mostrar_produtos.clicked.connect(self.mostrar_produtos_registrados)
        layout.addWidget(self.btn_mostrar_produtos)

        # Stretch to fill space
        layout.addStretch()

    def criar_interface_subprodutos(self):
        layout = QtWidgets.QVBoxLayout(self.tab_subproduto)

        # Label for selecting the source product
        self.label_produto_fonte = QtWidgets.QLabel("Escolha o Produto Fonte:")
        layout.addWidget(self.label_produto_fonte)

        # Combo box for selecting the source product
        self.produto_fonte_combobox = QtWidgets.QComboBox()
        self.produto_fonte_combobox.setPlaceholderText("Selecione o Produto Fonte")
        self.produto_fonte_combobox.currentIndexChanged.connect(self.preencher_dados_produto_fonte)  # Connect to fill data
        layout.addWidget(self.produto_fonte_combobox)

        # Sub-product input fields
        self.subproduto_desc = QtWidgets.QLineEdit()
        self.subproduto_desc.setPlaceholderText("Descrição do Sub Produto")
        layout.addWidget(self.subproduto_desc)

        self.subproduto_madeira = QtWidgets.QLineEdit()
        self.subproduto_madeira.setPlaceholderText("Tipo de Madeira")  # New field for wood type
        layout.addWidget(self.subproduto_madeira)

        self.subproduto_largura = QtWidgets.QLineEdit()
        self.subproduto_largura.setPlaceholderText("Largura (em cm)")  # New field for width
        layout.addWidget(self.subproduto_largura)

        self.subproduto_espessura = QtWidgets.QLineEdit()
        self.subproduto_espessura.setPlaceholderText("Espessura (em cm)")  # New field for thickness
        layout.addWidget(self.subproduto_espessura)

        self.subproduto_vlr_m = QtWidgets.QLineEdit()
        self.subproduto_vlr_m.setPlaceholderText("Valor Por Metro Linear")  # New field for Value per Linear Meter
        self.subproduto_vlr_m.textChanged.connect(self.calcular_lucro)  # Connect to calculate profit
        layout.addWidget(self.subproduto_vlr_m)

        # Label for profit display
        self.profit_label = QtWidgets.QLabel("Lucro: R$ 0.00 (0.00%)")
        layout.addWidget(self.profit_label)

        # Button to register sub-product
        self.btn_adicionar_subproduto = QtWidgets.QPushButton("Registrar Sub Produto")
        self.btn_adicionar_subproduto.clicked.connect(self.adicionar_subproduto)
        layout.addWidget(self.btn_adicionar_subproduto)

        # Button to show registered sub-products
        self.btn_mostrar_subprodutos = QtWidgets.QPushButton("Sub Produtos Registrados")
        self.btn_mostrar_subprodutos.clicked.connect(self.mostrar_subprodutos_registrados)
        layout.addWidget(self.btn_mostrar_subprodutos)

        # Stretch to fill space
        layout.addStretch()

    def preencher_dados_produto_fonte(self):
        """Preenche os dados do produto fonte selecionado."""
        produto_fonte = self.produto_fonte_combobox.currentText()
        source_product = next((p for p in self.produtos if p["descricao"] == produto_fonte), None)
        if source_product:
            self.subproduto_desc.setText(source_product["descricao"])
            self.subproduto_madeira.setText(source_product["madeira"])
            self.subproduto_largura.setText(str(source_product["largura"]))
            self.subproduto_espessura.setText(str(source_product["espessura"]))

    def calcular_lucro(self):
        """Calcula e exibe o lucro baseado no preço de venda e no produto fonte selecionado."""
        produto_fonte = self.produto_fonte_combobox.currentText()
        source_product = next((p for p in self.produtos if p["descricao"] == produto_fonte), None)
        if source_product:
            try:
                vlr_m = float(self.subproduto_vlr_m.text())  # Get the selling price per linear meter
                custo_por_metro_cubico = source_product["vlr_m"]
                largura = source_product["largura"] / 100  # Convert to meters
                espessura = source_product["espessura"] / 100  # Convert to meters

                # Calculate area of the cross-section
                area = largura * espessura  # Area in square meters

                # Calculate cost per linear meter
                custo_por_metro_linear = custo_por_metro_cubico * area  # Cost per linear meter

                # Calculate profit
                lucro = vlr_m - custo_por_metro_linear
                percentual_lucro = (lucro / custo_por_metro_linear) * 100 if custo_por_metro_linear > 0 else 0

                # Update profit label
                self.profit_label.setText(f"Lucro: R$ {lucro:.2f} ({percentual_lucro:.2f}%)")
            except ValueError:
                self.profit_label.setText("Lucro: R$ 0.00 (0.00%)")  # Reset if input is invalid
        else:
            self.profit_label.setText("Lucro: R$ 0.00 (0.00%)")  # Reset if no source product is selected

    def criar_interface_clientes(self):
        layout = QtWidgets.QVBoxLayout(self.tab_clientes)

        # Client input fields
        self.cliente_nome = QtWidgets.QLineEdit()
        self.cliente_nome.setPlaceholderText("Nome do Cliente (apenas letras e espaços)")
        self.cliente_nome.textChanged.connect(self.validate_name_input)  # Connect to validation method
        layout.addWidget(self.cliente_nome)

        # Group box for CPF/CNPJ selection
        self.cpf_cnpj_group = QtWidgets.QGroupBox("Tipo de Documento")
        self.cpf_cnpj_layout = QtWidgets.QHBoxLayout()
        self.radio_cpf = QtWidgets.QRadioButton("CPF")
        self.radio_cnpj = QtWidgets.QRadioButton("CNPJ")
        self.radio_cpf.setChecked(True)  # Default to CPF
        self.cpf_cnpj_layout.addWidget(self.radio_cpf)
        self.cpf_cnpj_layout.addWidget(self.radio_cnpj)
        self.cpf_cnpj_group.setLayout(self.cpf_cnpj_layout)
        layout.addWidget(self.cpf_cnpj_group)

        self.cliente_cpf = QtWidgets.QLineEdit()
        self.cliente_cpf.setPlaceholderText("CPF do Cliente (apenas números, 11 dígitos)")
        self.cliente_cpf.setMaxLength(14)  # Allow up to 14 characters for formatting
        self.cliente_cpf.textChanged.connect(self.validate_cpf_input)  # Connect to validation method
        layout.addWidget(self.cliente_cpf)

        self.cliente_endereco = QtWidgets.QLineEdit()
        self.cliente_endereco.setPlaceholderText("Endereço do Cliente")
        layout.addWidget(self.cliente_endereco)

        self.cliente_cidade = QtWidgets.QLineEdit()
        self.cliente_cidade.setPlaceholderText("Cidade do Cliente")
        layout.addWidget(self.cliente_cidade)

        self.cliente_telefone = QtWidgets.QLineEdit()
        self.cliente_telefone.setPlaceholderText("Telefone do Cliente (apenas números)")
        self.cliente_telefone.setMaxLength(15)  # Limitar a 15 caracteres
        self.cliente_telefone.textChanged.connect(self.validate_phone_input)  # Connect to validation method
        layout.addWidget(self.cliente_telefone)

        # Button to register client
        self.btn_adicionar_cliente = QtWidgets.QPushButton("Registrar Cliente")
        self.btn_adicionar_cliente.clicked.connect(self.adicionar_cliente)
        layout.addWidget(self.btn_adicionar_cliente)

        # Button to show registered clients
        self.btn_mostrar_clientes = QtWidgets.QPushButton("Clientes Registrados")
        self.btn_mostrar_clientes.clicked.connect(self.mostrar_clientes_registrados)
        layout.addWidget(self.btn_mostrar_clientes)

        # Stretch to fill space
        layout.addStretch()

        # Connect radio button toggled events
        self.radio_cpf.toggled.connect(self.update_document_placeholder)
        self.radio_cnpj.toggled.connect(self.update_document_placeholder)

        # Initialize cliente_combobox
        self.cliente_combobox = QtWidgets.QComboBox()
        layout.addWidget(self.cliente_combobox)

    def validate_name_input(self):
        """Allow spaces in the name input."""
        current_text = self.cliente_nome.text()
        self.cliente_nome.setText(current_text)  # No filtering, allow spaces

    def validate_cpf_input(self):
        """Remove any non-numeric characters from the CPF input."""
        current_text = self.cliente_cpf.text() 
        filtered_text = ''.join(filter(str.isdigit, current_text))  # Keep only digits
        self.cliente_cpf.setText(filtered_text)  # Update the line edit with filtered text

    def validate_phone_input(self):
        """Remove any non-numeric characters from the phone input."""
        current_text = self.cliente_telefone.text()
        filtered_text = ''.join(filter(str.isdigit, current_text))  # Keep only digits
        self.cliente_telefone.setText(filtered_text)  # Update the line edit with filtered text

    def update_document_placeholder(self):
        """Update the placeholder text based on the selected document type."""
        if self.radio_cpf.isChecked():
            self.cliente_cpf.setPlaceholderText("CPF do Cliente (apenas números, 11 dígitos)")
            self.cliente_cpf.setMaxLength(11)
        elif self.radio_cnpj.isChecked():
            self.cliente_cpf.setPlaceholderText("CNPJ do Cliente (apenas números, 14 dígitos)")
            self.cliente_cpf.setMaxLength(14)

    def criar_interface_orcamento(self):
        layout = QtWidgets.QVBoxLayout(self.tab_orcamento)

        # Set background color to white
        self.tab_orcamento.setStyleSheet("background-color: white;")

        # Label for product selection
        produto_label = QtWidgets.QLabel("Selecione o Sub Produto:")
        layout.addWidget(produto_label)

        # Product selection
        self.produto_combobox = QtWidgets.QComboBox()
        self.produto_combobox.setEditable(True)  # Make it editable
        self.produto_combobox.setPlaceholderText("Selecione um Produto")
        layout.addWidget(self.produto_combobox)

        # Size input
        self.produto_tamanho = QtWidgets.QLineEdit()
        self.produto_tamanho.setPlaceholderText("Tamanho (em metros)")
        self.produto_tamanho.textChanged.connect(self.validate_size_input)  # Connect to validation method
        layout.addWidget(self.produto_tamanho)

        self.quantidade_entry = QtWidgets.QLineEdit()
        self.quantidade_entry.setPlaceholderText("Quantidade")
        layout.addWidget(self.quantidade_entry)

        # Button to add product to budget
        self.btn_adicionar_orcamento = QtWidgets.QPushButton("Adicionar Sub Produto ao Orçamento")
        self.btn_adicionar_orcamento.setStyleSheet("background-color: #007BFF; color: white;")  # Blue button
        self.btn_adicionar_orcamento.clicked.connect(self.adicionar_produto_orcamento)
        layout.addWidget(self.btn_adicionar_orcamento)

        # List to display added products
        self.produtos_adicionados_list = QtWidgets.QTableWidget()
        self.produtos_adicionados_list.setColumnCount(5)
        self.produtos_adicionados_list.setHorizontalHeaderLabels(["PRODUTO", "QUANTIDADE", "VALOR UNITÁRIO", "VALOR TOTAL", "VOLUME TOTAL"])
        self.produtos_adicionados_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.produtos_adicionados_list)

        # Button to remove selected product from budget
        self.btn_remover_orcamento = QtWidgets.QPushButton("Remover Sub Produto do Orçamento")
        self.btn_remover_orcamento.setStyleSheet("background-color: #007BFF; color: white;")  # Blue button
        self.btn_remover_orcamento.clicked.connect(self.remover_produto_orcamento)
        layout.addWidget(self.btn_remover_orcamento)

        # Label for client selection
        cliente_label = QtWidgets.QLabel("Selecione o Cliente:")
        layout.addWidget(cliente_label)

        # Client selection using QComboBox
        self.cliente_combobox = QtWidgets.QComboBox()
        self.cliente_combobox.setEditable(True)  # Make it editable
        self.cliente_combobox.setPlaceholderText("Selecione um cliente")
        layout.addWidget(self.cliente_combobox)

        # Vendor entry (set to "EVERSON OLSEN" and disabled)
        self.vendedor_entry = QtWidgets.QLineEdit("EVERSON OLSEN")
        self.vendedor_entry.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.vendedor_entry)

        # Forma de Pagamento (set to always be "DINHEIRO" and disabled)
        self.forma_pagamento_entry = QtWidgets.QLineEdit("DINHEIRO")
        self.forma_pagamento_entry.setReadOnly(True)  # Make it read-only
        self.forma_pagamento_entry.setStyleSheet("background-color: lightgray;")  # Set background color to light gray
        layout.addWidget(self.forma_pagamento_entry)

        # Condição de Pagamento (set to allow only "A VISTA" or "A PRAZO")
        self.condicao_pagamento_entry = QtWidgets.QLineEdit()
        self.condicao_pagamento_entry.setPlaceholderText("Condição de Pagamento")
        layout.addWidget(self.condicao_pagamento_entry)

        # Generate PDF button
        self.btn_gerar_pdf = QtWidgets.QPushButton("Gerar Orçamento")
        self.btn_gerar_pdf.setStyleSheet("background-color: #007BFF; color: white;")  # Blue button
        self.btn_gerar_pdf.clicked.connect(self.gerar_pdf)
        layout.addWidget(self.btn_gerar_pdf)

        # Stretch to fill space
        layout.addStretch()

    def validate_size_input(self):
        """Allow decimal input for size."""
        current_text = self.produto_tamanho.text()
        filtered_text = ''.join(filter(lambda x: x.isdigit() or x == ',' or x == '.', current_text))  # Allow digits, comma, and dot
        self.produto_tamanho.setText(filtered_text)  # Update the line edit with filtered text

    def atualizar_combobox_clientes(self):
        """Populate the client selection box with registered clients."""
        self.cliente_combobox.clear()
        self.cliente_combobox.addItems([cliente["nome"] for cliente in self.clientes])

    def carregar_dados(self):
        """Carrega os dados de produtos e clientes do arquivo JSON."""
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'r') as arquivo:
                dados = json.load(arquivo)
                self.produtos = dados.get("produtos", [])
                self.subprodutos = dados.get("subprodutos", [])
                self.clientes = dados.get("clientes", [])
        
        # Atualizar as listas e comboboxes
        self.atualizar_combobox_orcamento()
        self.atualizar_combobox_clientes()

        # Populate the source product ComboBox
        self.produto_fonte_combobox.clear()
        self.produto_fonte_combobox.addItems([produto["descricao"] for produto in self.produtos])

    def atualizar_combobox_orcamento(self):
        self.produto_combobox.clear()
        # Add only sub-products to the combo box for budget
        for subproduto in self.subprodutos:
            if 'descricao' in subproduto and 'largura' in subproduto and 'espessura' in subproduto and 'madeira' in subproduto:
                produto_nome = f"{subproduto['descricao']} - {subproduto['largura']}X{subproduto['espessura']} - {subproduto['madeira']}"
                self.produto_combobox.addItem(produto_nome)

    def mostrar_produtos_registrados(self):
        """Show all registered products in a new window."""
        dialog = ProdutosDialog(self.produtos, self.edit_product, self.delete_product)
        dialog.exec_()  # Open the dialog

    def mostrar_subprodutos_registrados(self):
        """Show all registered sub-products in a new window."""
        dialog = ProdutosDialog(self.subprodutos, self.edit_subproduct, self.delete_subproduct)
        dialog.exec_()

    def mostrar_clientes_registrados(self):
        """Show all registered clients in a new window."""
        dialog = ClientesDialog(self.clientes, self.edit_client, self.delete_client)
        dialog.exec_()  # Open the dialog

    def edit_product(self, product_name):
        """Edit the selected product."""
        # Find the product and populate the fields for editing
        for produto in self.produtos:
            if produto["descricao"] == product_name:
                self.produto_desc.setText(produto["descricao"])
                self.produto_madeira.setText(produto.get("madeira", ""))  # Get the wood type
                self.produto_largura.setText(str(produto.get("largura", "")))  # Get the width
                self.produto_espessura.setText(str(produto.get("espessura", "")))  # Get the thickness
                self.produto_vlr_m.setText(str(produto.get("vlr_m", "")))  # Get the value per cubic meter
                break

    def edit_subproduct(self, subproduct_name):
        """Edit the selected sub-product."""
        # Find the sub-product and populate the fields for editing
        for subproduto in self.subprodutos:
            if subproduto["descricao"] == subproduct_name:
                self.subproduto_desc.setText(subproduto["descricao"])
                self.subproduto_madeira.setText(subproduto.get("madeira", ""))  # Get the wood type
                self.subproduto_largura.setText(str(subproduto.get("largura", "")))  # Get the width
                self.subproduto_espessura.setText(str(subproduto.get("espessura", "")))  # Get the thickness
                self.subproduto_vlr_m.setText(str(subproduto.get("vlr_m", "")))  # Get the value per linear meter
                break

    def delete_product(self, product_name):
        """Delete the selected product."""
        self.produtos = [produto for produto in self.produtos if produto["descricao"] != product_name]
        self.salvar_dados()

    def delete_subproduct(self, subproduct_name):
        """Delete the selected sub-product."""
        self.subprodutos = [subproduto for subproduto in self.subprodutos if subproduto["descricao"] != subproduct_name]
        self.salvar_dados()

    def edit_client(self, client_name):
        """Edit the selected client."""
        # Find the client and populate the fields for editing
        for cliente in self.clientes:
            if cliente["nome"] == client_name:
                self.cliente_nome.setText(cliente["nome"])
                self.cliente_cpf.setText(cliente["cpf_cnpj"])
                self.cliente_endereco.setText(cliente["endereco"])
                self.cliente_cidade.setText(cliente["cidade"])
                self.cliente_telefone.setText(cliente["telefone"])
                break

    def delete_client(self, client_name):
        """Delete the selected client."""
        self.clientes = [cliente for cliente in self.clientes if cliente["nome"] != client_name]
        self.salvar_dados()
        self.atualizar_combobox_clientes()  # Update the client combo box after deletion

    def adicionar_produto(self):
        descricao = self.produto_desc.text()
        madeira = self.produto_madeira.text()
        largura = self.produto_largura.text()
        espessura = self.produto_espessura.text()
        try:
            vlr_m = float(self.produto_vlr_m.text())  # Get the cost per cubic meter
            largura = float(largura)  # Convert to float
            espessura = float(espessura)  # Convert to float
            if not descricao or vlr_m <= 0 or largura <= 0 or espessura <= 0:
                raise ValueError("Preencha os campos corretamente!")

            self.produtos.append({"descricao": descricao, "madeira": madeira, "largura": largura, "espessura": espessura, "vlr_m": vlr_m})  # Store description, wood type, width, thickness, and cost per cubic meter
            self.atualizar_combobox_orcamento()
            self.produto_desc.clear()
            self.produto_madeira.clear()
            self.produto_largura.clear()
            self.produto_espessura.clear()
            self.produto_vlr_m.clear()  # Clear cost per cubic meter input

            self.salvar_dados()
            QtWidgets.QMessageBox.information(self, "Sucesso", "Produto Fonte adicionado com sucesso!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Erro", f"Entrada inválida: {e}")

    def adicionar_subproduto(self):
        descricao = self.subproduto_desc.text()
        madeira = self.subproduto_madeira.text()
        largura = self.subproduto_largura.text()
        espessura = self.subproduto_espessura.text()
        produto_fonte = self.produto_fonte_combobox.currentText()  # Get the selected source product

        try:
            largura = float(largura)  # Convert to float
            espessura = float(espessura)  # Convert to float
            vlr_m = float(self.subproduto_vlr_m.text())  # Get the selling price per linear meter
            if not descricao or not madeira or largura <= 0 or espessura <= 0 or vlr_m <= 0 or not produto_fonte:
                raise ValueError("Preencha os campos corretamente!")

            # Find the source product to calculate profit
            source_product = next((p for p in self.produtos if p["descricao"] == produto_fonte), None)
            if source_product is None:
                raise ValueError("Produto fonte não encontrado!")

            custo_por_metro_cubico = source_product["vlr_m"]
            
            # Calculate cost per linear meter
            largura_m = largura / 100  # Convert to meters
            espessura_m = espessura / 100  # Convert to meters
            area = largura_m * espessura_m  # Area in square meters
            custo_por_metro_linear = custo_por_metro_cubico * area  # Cost per linear meter

            # Calculate profit
            lucro = vlr_m - custo_por_metro_linear
            percentual_lucro = (lucro / custo_por_metro_linear) * 100 if custo_por_metro_linear > 0 else 0

            self.subprodutos.append({
                "descricao": descricao,
                "madeira": madeira,
                "largura": largura,
                "espessura": espessura,
                "vlr_m": vlr_m,
                "lucro": lucro,
                "percentual_lucro": percentual_lucro
            })  # Store description, wood type, width, thickness, and selling price per linear meter
            self.atualizar_combobox_orcamento()
            self.subproduto_desc.clear()
            self.subproduto_madeira.clear()
            self.subproduto_largura.clear()
            self.subproduto_espessura.clear()  # Clear inputs
            self.subproduto_vlr_m.clear()  # Clear selling price input

            self.salvar_dados()
            QtWidgets.QMessageBox.information(self, "Sucesso", f"Sub Produto adicionado com sucesso! Lucro: R$ {lucro:.2f} ({percentual_lucro:.2f}%)")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Erro", f"Entrada inválida: {e}")

    def adicionar_cliente(self):
        nome = self.cliente_nome.text()
        cpf = self.cliente_cpf.text()
        endereco = self.cliente_endereco.text()
        cidade = self.cliente_cidade.text()
        telefone = self.cliente_telefone.text()

        if not nome or not cpf or not endereco or not cidade or not telefone:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha todos os campos para adicionar um cliente!")
            return

        # Validate name (allow spaces)
        if not all(char.isalpha() or char.isspace() for char in nome):
            QtWidgets.QMessageBox.warning(self, "Erro", "O nome não pode conter números ou símbolos!")
            return

        # Validate CPF ou CNPJ
        if self.radio_cpf.isChecked():
            if not cpf.isdigit() or len(cpf) != 11:
                QtWidgets.QMessageBox.warning(self, "Erro", "CPF deve conter apenas números e ter 11 dígitos!")
                return
        elif self.radio_cnpj.isChecked():
            if not cpf.isdigit() or len(cpf) != 14:
                QtWidgets.QMessageBox.warning(self, "Erro", "CNPJ deve conter apenas números e ter 14 dígitos!")
                return

        # Validate phone (only digits)
        if not telefone.isdigit():
            QtWidgets.QMessageBox.warning(self, "Erro", "Telefone deve conter apenas números!")
            return

        self.clientes.append({
            "nome": nome,
            "cpf_cnpj": cpf,
            "endereco": endereco,
            "cidade": cidade,
            "telefone": telefone
        })
        
        self.atualizar_combobox_orcamento()
        self.cliente_nome.clear()
        self.cliente_cpf.clear()
        self.cliente_endereco.clear()
        self.cliente_cidade.clear()
        self.cliente_telefone.clear()

        self.salvar_dados()
        self.atualizar_combobox_clientes()  # Update the client combo box after adding
        QtWidgets.QMessageBox.information(self, "Sucesso", "Cliente adicionado com sucesso!")

    def adicionar_produto_orcamento(self):
        """Add selected product to the budget list."""
        produto_desc = self.produto_combobox.currentText()
        produto_tam = self.produto_tamanho.text().replace(',', '.')  # Replace comma with dot for float conversion
        quantidade = self.quantidade_entry.text()

        if not produto_desc or not produto_tam or not quantidade:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha todos os campos para adicionar um produto ao orçamento!")
            return

        # Validate size input
        try:
            produto_tam = float(produto_tam)  # Convert to float to allow decimal values
            quantidade = int(quantidade)  # Convert quantidade to int
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Erro", "O tamanho e a quantidade devem ser números válidos!")
            return

        # Get the value per meter for the selected product
        vlr_m = next((p.get("vlr_m") for p in self.subprodutos 
                       if 'largura' in p and 'espessura' in p and 'madeira' in p and 
                       f"{p['descricao']} - {p.get('largura', '0')}X{p.get('espessura', '0')} - {p.get('madeira', '')}" == produto_desc), None)
        if vlr_m is None:
            QtWidgets.QMessageBox.warning(self, "Erro", "Produto não encontrado ou valor inválido!")
            return

        # Calculate volume (m³)
        largura = next((p.get('largura') for p in self.subprodutos if f"{p['descricao']} - {p.get('largura', '0')}X{p.get('espessura', '0')} - {p.get('madeira', '')}" == produto_desc), None)
        espessura = next((p.get('espessura') for p in self.subprodutos if f"{p['descricao']} - {p.get('largura', '0')}X{p.get('espessura', '0')} - {p.get('madeira', '')}" == produto_desc), None)
        comprimento = produto_tam  # Using the size input as length

        if largura is not None and espessura is not None:
            volume = (largura / 100) * (espessura / 100) * float(comprimento)  # Convert cm to m for width and thickness
        else:
            volume = 0

        # Calcular o volume total
        volume_total = volume * quantidade  # Calculate total volume

        total = vlr_m * produto_tam * quantidade  # Calculate total based on quantity and unit price

        # Add product details to the list
        row_position = self.produtos_adicionados_list.rowCount()
        self.produtos_adicionados_list.insertRow(row_position)
        self.produtos_adicionados_list.setItem(row_position, 0, QtWidgets.QTableWidgetItem(produto_desc))
        self.produtos_adicionados_list.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(quantidade)))
        self.produtos_adicionados_list.setItem(row_position, 2, QtWidgets.QTableWidgetItem(f"R$ {vlr_m:.2f}"))
        self.produtos_adicionados_list.setItem(row_position, 3, QtWidgets.QTableWidgetItem(f"R$ {total:.2f}"))
        self.produtos_adicionados_list.setItem(row_position, 4, QtWidgets.QTableWidgetItem(f"{volume_total:.4f} m³"))

        self.orcamento_produtos.append({
            "descricao": produto_desc,
            "tamanho": produto_tam,
            "quantidade": quantidade,
            "vlr_m": vlr_m,
            "total": total,
            "volume": volume,
            "volume_total": volume_total    # Store volume
        })

        # Clear inputs
        self.produto_combobox.setCurrentIndex(-1)
        self.produto_tamanho.clear()
        self.quantidade_entry.clear()  # Clear quantity input

        self.salvar_dados()

        # Emit the signal after adding a product
        self.sale_added.emit()

    def remover_produto_orcamento(self):
        """Remove selected product from the budget list."""
        selected_items = self.produtos_adicionados_list.selectedItems()
        if selected_items:
            for item in selected_items:
                row = self.produtos_adicionados_list.row(item)
                self.produtos_adicionados_list.removeRow(row)  # Remove from list widget
                del self.orcamento_produtos[row]  # Remove from the budget list
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", "Selecione um produto para remover!")

    def gerar_pdf(self):
        try:
            # Coletar dados do cliente
            cliente_nome = self.cliente_combobox.currentText()  # Get selected client from combo box
            cliente = next((c for c in self.clientes if c["nome"] == cliente_nome), None)

            if cliente is None:
                QtWidgets.QMessageBox.warning(self, "Erro", "Selecione um cliente válido!")
                return

            cliente_endereco = cliente["endereco"]
            cliente_cidade = cliente["cidade"]
            cliente_cpf = cliente["cpf_cnpj"]
            cliente_telefone = cliente["telefone"]

            # Criar PDF
            pdf = FPDF(orientation='L', unit='mm', format=(500, 350))  # Landscape orientation
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Cabeçalho
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 5, "TICKET DE VENDA", ln=True, align="C")
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 5, "TIGELA MADEIRAS E ARTEFATOS LTDA", ln=True, align="C")
            pdf.cell(0, 5, "TIGELA MADEIREIRA E ARTEFATOS", ln=True, align="C")
            pdf.cell(0, 5, "Telefone: (44) 9754-8463 - Celular:", ln=True, align="C")
            pdf.cell(0, 5, "Endereco: AVENIDA BRASIL, No 1621, DISTRITO CASA BRANCA, XAMBRE - PR", ln=True, align="C")
            pdf.cell(0, 5, "CNPJ: 39.594.567/0001-79    IE: 9086731905", ln=True, align="C")
            pdf.ln(5)

            # Dados do cliente
            pdf.set_font("Arial", style="", size=10)
            pdf.cell(0, 5, f"Cliente: {cliente_nome}", ln=True)
            pdf.cell(0, 5, f"Endereco: {cliente_endereco}", ln=True)
            pdf.cell(0, 5, f"Cidade: {cliente_cidade}", ln=True)
            pdf.cell(0, 5, f"CPF/CNPJ: {cliente_cpf}", ln=True)
            pdf.cell(0, 5, f"Telefone: {cliente_telefone}", ln=True)
            pdf.ln(5)

            pdf.set_fill_color(200, 200, 200)
            pdf.cell(10, 7, txt="N\u00ba", border=1, align="C", fill=True)
            pdf.cell(80, 7, txt="Produto", border=1, align="C", fill=True)
            pdf.cell(30, 7, txt="Un. Com.", border=1, align="C", fill=True)  # Add "Un. Com." column
            pdf.cell(30, 7, txt="Vlr. Frete", border=1, align="C", fill=True)
            pdf.cell(30, 7, txt="Vlr. Outros", border=1, align="C", fill=True)
            pdf.cell(30, 7, txt="Vlr. Seguro", border=1, align="C", fill=True)
            pdf.cell(20, 7, txt="Qtd", border=1, align="C", fill=True)  # Quantity
            pdf.cell(20, 7, txt="Vlr. M.", border=1, align="C", fill=True)  # Add "Vlr. M." column
            pdf.cell(30, 7, txt="Vlr UN.", border=1, align="C", fill=True)  # Unit Price
            pdf.cell(30, 7, txt="Vlr Total", border=1, align="C", fill=True)  # Total
            pdf.ln()

            total_final = 0  # Initialize total

            # Loop through added products and add to PDF
            for index, produto in enumerate(self.orcamento_produtos):
                produto_desc = produto["descricao"]
                produto_tam = produto["tamanho"]
                quantidade = produto["quantidade"]
                vlr_m = next((p["vlr_m"] for p in self.produtos if p["descricao"] == produto_desc), 0)
                vlr_un = vlr_m * float(produto_tam)  # Calculate unit price
                total = int(quantidade) * vlr_un  # Calculate total based on quantity and unit price

                # Preenchendo produtos com o novo formato
                pdf.cell(10, 7, txt=str(index + 1), border=1, align="C")
                pdf.cell(80, 7, txt=f"{produto_desc} - {produto_tam}M", border=1, align="L")  # Concatenate description and size
                pdf.cell(30, 7, txt="UNID", border=1, align="C")  # Display "Un. Com."
                pdf.cell(30, 7, txt="R$ 00,00", border=1, align="C")
                pdf.cell(30, 7, txt="R$ 00,00", border=1, align="C")
                pdf.cell(30, 7, txt="R$ 00,00", border=1, align="C")
                pdf.cell(20, 7, txt=str(quantidade), border=1, align="C")  # Display quantity
                pdf.cell(20, 7, txt=f"R$ {vlr_m:.2f}", border=1, align="C")  # Display value per meter
                pdf.cell(30, 7, txt=f"R$ {vlr_un:.2f}", border=1, align="C")  # Display unit price
                pdf.cell(30, 7, txt=f"R$ {total:.2f}", border=1, align="C")  # Display total
                pdf.ln(10)

                total_final += total  # Add to final total

            # Totais e informações adicionais
            pdf.cell(17, 5, txt=f"Vendedor:", border=0, align="L")
            pdf.cell(29, 5, txt="", border=0)  # Espaço vazio
            pdf.cell(30, 5, txt=f"{self.vendedor_entry.text()}", border=0, align="L")
            pdf.cell(130, 5, txt="", border=0)  # Espaço vazio
            pdf.cell(30, 5, txt=f"Outros:", border=0, align="L")
            pdf.cell(30, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.cell(30, 5, txt=f"Total:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ {total_final:.2f}", border=0, align="L")  # Total after discount
            pdf.ln(6)

            pdf.cell(36, 5, txt=f"Forma de Pagamento:", border=0, align="L")
            pdf.cell(10, 5, txt="", border=0)  # Espaço vazio
            pdf.cell(30, 5, txt=f"{self.forma_pagamento_entry.text()}", border=0, align="L")
            pdf.cell(130, 5, txt="", border=0)  # Espaço vazio
            pdf.cell(30, 5, txt=f"Seguro:", border=0, align="L")
            pdf.cell(30, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.cell(30, 5, txt=f"Acréscimos:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.ln(6)

            pdf.cell(36, 5, txt=f"Condição de Pagamento:", border=0, align="L")
            pdf.cell(10, 5, txt="", border=0)  # Espaço vazio
            pdf.cell(30, 5, txt=f"{self.condicao_pagamento_entry.text()}", border=0, align="L")
            pdf.cell(130, 5, txt="", border=0)  # Espaço vazio
            pdf.cell(30, 5, txt=f"Frete:", border=0, align="L")
            pdf.cell(30, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.cell(30, 5, txt=f"Descontos:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.ln(6)

            pdf.cell(43, 5, txt=f"Limite de Crédito Utilizado:", border=0, align="L")
            pdf.cell(3, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.cell(190, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"Total Líquido:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.ln(6)

            pdf.set_font("Arial", style="B", size=10)
            pdf.cell(40, 5, "Composição Pgto", border=0, align="L")
            pdf.cell(30, 5, "Parcela", border=0, align="L")
            pdf.cell(50, 5, "Numerário", border=0, align="L")
            pdf.cell(30, 5, "Valor", border=0, align="L")
            pdf.cell(30, 5, "Data Pgto", border=0, align="L")
            pdf.ln()
            
            pdf.set_font("Arial", size=10)
            pdf.cell(40, 5, "", border=0, align="L")  # Empty space for "Composição Pgto"
            pdf.cell(30, 5, "1", border=0, align="L")  # Parcela
            pdf.cell(50, 5, "Dinheiro", border=0, align="L")  # Numerário
            pdf.cell(30, 5, f"R$ {total_final:.2f}", border=0, align="L")  # Valor
            pdf.cell(30, 5, datetime.now().strftime("%d/%m/%Y"), border=0, align="L")

            # Salvar PDF
            nome_pdf = "Ticket_Venda_Exemplo.pdf"
            pdf.output(nome_pdf)

            # Abrir PDF automaticamente
            os.startfile(nome_pdf)

            # Save the sales data to the JSON file
            self.salvar_dados_vendas()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o PDF: {str(e)}")

    def salvar_dados_vendas(self):
        """Append the sales data to the JSON file."""
        for produto in self.orcamento_produtos:
            dados_vendas = {
                "descricao": produto["descricao"],
                "tamanho": produto["tamanho"],
                "quantidade": produto["quantidade"],
                "total": produto["total"],
                "volume_total": produto["volume_total"],
                "cliente": self.cliente_combobox.currentText()
            }

            # Load existing sales data
            if os.path.exists(self.arquivo_dados):
                with open(self.arquivo_dados, 'r') as arquivo:
                    dados = json.load(arquivo)
                    if "vendas" not in dados:
                        dados["vendas"] = []
                    dados["vendas"].append(dados_vendas)
            else:
                dados = {"vendas": [dados_vendas]}

            # Save updated sales data
            with open(self.arquivo_dados, 'w') as arquivo:
                json.dump(dados, arquivo, indent=4)

    def salvar_dados(self):
        """Salva os dados de produtos e clientes no arquivo JSON."""
        dados = {
            "produtos": self.produtos,
            "clientes": self.clientes,
            "subprodutos": self.subprodutos,  # Save sub-products as well
            "orcamento_produtos": self.orcamento_produtos
        }
        with open(self.arquivo_dados, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

def carregar_dados_orcamento(arquivo_dados):
    """Carrega os dados de vendas do arquivo JSON."""
    if os.path.exists(arquivo_dados):
        try:
            with open(arquivo_dados, 'r') as arquivo:
                dados = json.load(arquivo)
                return dados.get("vendas", [])  # Change to "vendas" to get sales data
        except json.JSONDecodeError:
            return []
    return []

class WelcomeScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MADEREIRA CASA BRANCA")
        self.setGeometry(100, 100, 1000, 600)  # Increased window size

        # Layout principal
        layout = QtWidgets.QVBoxLayout(self)  # Layout vertical principal

        # Parte superior: Imagem do logo
        self.logo_label = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap("Imgs/logo.png")  # Substitua pelo caminho correto da imagem
        self.logo_label.setPixmap(logo_pixmap.scaledToHeight(200, QtCore.Qt.SmoothTransformation))  # Ajusta a altura
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.logo_label, stretch=1)  # Adiciona a imagem com prioridade de espaço

        # Parte inferior: Botões
        button_layout = QtWidgets.QVBoxLayout()  # Layout vertical para os botões

        # Criação dos botões com efeitos
        self.btn_clientes = self.create_button("Clientes", "Imgs/cliente.png", self.open_clientes)
        button_layout.addWidget(self.btn_clientes)

        self.btn_produtos = self.create_button("Produtos", "Imgs/Produtos.png", self.open_produtos)
        button_layout.addWidget(self.btn_produtos)

        self.btn_orcamento = self.create_button("Orçamento", "Imgs/Orçamento.png", self.open_orcamento)
        button_layout.addWidget(self.btn_orcamento)

        # Adiciona o layout dos botões na parte inferior
        button_widget = QtWidgets.QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setStyleSheet("background-color: white;")  # Fundo branco para os botões
        layout.addWidget(button_widget, stretch=2)  # Adiciona os botões com maior prioridade de espaço

        # Define o layout principal
        self.setLayout(layout)

    def create_button(self, text, icon_path, callback):
        """Cria um botão com ícone e efeito de hover."""
        button = QtWidgets.QPushButton(text)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(80, 80))  # Aumenta o tamanho do ícone
        button.setFont(QtGui.QFont("Arial", 28))  # Aumenta o tamanho da fonte
        button.setStyleSheet(self.button_hover_effect())
        button.clicked.connect(callback)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Expande horizontalmente
        return button

    def button_hover_effect(self):
        """Retorna o estilo CSS para o efeito de hover dos botões."""
        return """
            QPushButton {
                border: none;
                padding: 20px;  /* Aumenta o padding para botões maiores */
                font-size: 28px;  /* Tamanho da fonte */
                background-color: white;
            }
            QPushButton:hover {
                background-color: #e0e0e0;  /* Cor ao passar o mouse */
            }
        """

    def open_clientes(self):
        self.sistema_orcamento = SistemaOrcamentoMadeireira()
        self.sistema_orcamento.showMaximized()  # Open in maximized state
        self.sistema_orcamento.tabs.setCurrentIndex(1)  # Set to "Clientes" tab
        self.close()  # Close the welcome screen

    def open_produtos(self):
        self.sistema_orcamento = SistemaOrcamentoMadeireira()
        self.sistema_orcamento.showMaximized()  # Open in maximized state
        self.sistema_orcamento.tabs.setCurrentIndex(0)  # Set to "Produtos" tab
        self.close()  # Close the welcome screen

    def open_orcamento(self):
        self.sistema_orcamento = SistemaOrcamentoMadeireira()
        self.sistema_orcamento.showMaximized()  # Open in maximized state
        self.sistema_orcamento.tabs.setCurrentIndex(2)  # Set to "Orçamento" tab
        self.sistema_orcamento.sale_added.connect(self.update_relatorio)  # Connect the signal
        self.close()  # Close the welcome screen

    def update_relatorio(self):
        # Reload the report dialog with updated data
        arquivo_dados = "dados.json"
        orcamento_produtos = carregar_dados_orcamento(arquivo_dados)
        relatorio_dialog = RelatorioDialog(orcamento_produtos)
        relatorio_dialog.exec_()  # Show the updated report dialog

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_screen = WelcomeScreen()
    welcome_screen.show()  # Show the welcome screen
    sys.exit(app.exec_())