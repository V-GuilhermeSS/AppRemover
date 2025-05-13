from PyQt5.QtWidgets import QApplication
from gui.interface import DesinstaladorApp

def main():
    app = QApplication([])
    janela = DesinstaladorApp()
    janela.show()
    app.exec_()

if __name__ == "__main__":
    main()
