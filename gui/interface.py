from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton, QInputDialog, QMessageBox, \
    QLabel, QLineEdit
from PyQt5.QtGui import QIcon, QColor, QPalette
from core.apps import listar_aplicativos, localizar_arquivos_relacionados
from core.remover import remover_aplicativo
import os


class DesinstaladorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.titulo = None
        self.layout = None
        self.lista_apps = None
        self.caixa_log = None
        self.botao_remover = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AppRemover")
        self.setGeometry(100, 100, 500, 400)

        # Definindo ícone
        icon_path = os.path.abspath("assets/app_icon.icns")
        self.setWindowIcon(QIcon(icon_path))

        self.layout = QVBoxLayout()

        # Título
        self.titulo = QLabel("Apps encontrados:")
        self.titulo.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.titulo)

        # Lista de aplicativos
        self.lista_apps = QListWidget()
        self.lista_apps.addItems(listar_aplicativos())
        # noinspection PyUnresolvedReferences
        self.lista_apps.clicked.connect(self.exibir_arquivos)
        self.lista_apps.setStyleSheet("""
            background-color: white;
            color: black;
        """)
        self.layout.addWidget(self.lista_apps)

        # Caixa de log
        self.caixa_log = QTextEdit()
        self.caixa_log.setReadOnly(True)
        self.caixa_log.setStyleSheet("""
            background-color: white;
            color: black;
        """)
        self.layout.addWidget(self.caixa_log)

        # Botão remover
        self.botao_remover = QPushButton("Remover Aplicativo")
        self.botao_remover.setStyleSheet("color: black;")
        # noinspection PyUnresolvedReferences
        self.botao_remover.clicked.connect(self.remover_app)
        self.layout.addWidget(self.botao_remover)

        self.setLayout(self.layout)
        self.personalizar_estilo()

    def personalizar_estilo(self):
        # Fundo cinza claro com transparência
        self.setAutoFillBackground(True)
        palette = self.palette()
        cor_fundo = QColor(211, 211, 211, 230)  # RGBA
        palette.setColor(QPalette.ColorRole.Window, cor_fundo)
        self.setPalette(palette)

        # Barra de rolagem branca
        self.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: black;
            }
            QScrollBar:vertical {
                background: white;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                border-radius: 6px;
            }
        """)

    def exibir_arquivos(self):
        app_selecionado = self.lista_apps.currentItem().text()
        arquivos = localizar_arquivos_relacionados(app_selecionado)

        if arquivos:
            log_arquivos = "\n".join(arquivos)
        else:
            log_arquivos = "Nenhum arquivo relacionado encontrado."

        self.caixa_log.setText(log_arquivos)

    def remover_app(self):
        app_selecionado = self.lista_apps.currentItem().text()
        arquivos = localizar_arquivos_relacionados(app_selecionado)

        confirmacao = QMessageBox()
        confirmacao.setWindowTitle("Confirmação")
        confirmacao.setText(f"Deseja remover {app_selecionado} e os seguintes arquivos?\n" + "\n".join(arquivos))
        confirmacao.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Estilizando a caixa de confirmação para combinar com a janela principal
        confirmacao.setStyleSheet("""
            QMessageBox {
                background-color: rgba(211, 211, 211, 230);  /* Cor de fundo cinza claro */
                color: black;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: white;
                color: black;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

        resposta = confirmacao.exec_()

        if resposta == QMessageBox.Yes:
            senha, ok = QInputDialog.getText(self, "Senha de Administrador",
                                             "Digite sua senha de administrador para continuar:",
                                             QLineEdit.Password)
            if ok and senha:
                self.caixa_log.clear()
                self.caixa_log.append("Iniciando remoção...\n")
                remover_aplicativo(app_selecionado, senha, self.caixa_log)
                self.caixa_log.append("\nRemoção finalizada.")

                QMessageBox.information(self, "Sucesso", "Aplicativo removido com sucesso!",
                                        QMessageBox.Ok)
                self.lista_apps.clear()
                self.lista_apps.addItems(listar_aplicativos())
            else:
                QMessageBox.warning(self, "Erro", "A senha não foi fornecida ou está incorreta.")
