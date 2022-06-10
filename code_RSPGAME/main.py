import sys

from PyQt5.QtWidgets import QApplication

from RSPgame_module import RSPgame
from GUI_module import MainWindow




if __name__=='__main__':
    model = RSPgame()
    
    
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    
    sys.exit(app.exec_())

# {0:'rock', 1:'12scissors', 2:'paper', 3:'23-scissors'}