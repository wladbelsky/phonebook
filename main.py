#entry point
import sys
from PyQt4 import QtGui, uic
from login_window import login_window


app = QtGui.QApplication(sys.argv)
window = login_window()
window.show()
app.exec_()
