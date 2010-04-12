from PyQt4 import QtCore, QtGui, QtWebKit

from gui import MainWindow, Environment, Website, Timers

import os
import sys


class TabWidget(QtGui.QTabWidget):
    """
    Very basic class that handles the tabs.
    """
    def __init__(self, parent=None):
       super (TabWidget, self).__init__(parent)
       self.setTabsClosable(False)

if __name__ == '__main__':
    # Init environment.
    env = Environment(debug = True)
    # Init QApplication.
    qApp = QtGui.QApplication(sys.argv)
    env.qApp = qApp
    # Removes the frame around the widgets in the status bar. May apparently
    # cause some other problems:
    # http://www.qtcentre.org/archive/index.php/t-1904.html
    qApp.setStyleSheet("QStatusBar::item {border: 0px solid black}")

    # Init splash screen to show something is going on.
    pixmap = QtGui.QPixmap(os.path.join(env.res_dir, 'splash.png'))
    env.splash = QtGui.QSplashScreen(pixmap)
    env.splash.show()
    env.splash.showMessage('Init interface...', QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom,
                   QtCore.Qt.black) 
    # Force Qt to uodate outside of any event loop.
    qApp.processEvents()

    # Init the main window.
    window = QtGui.QMainWindow()

    # Init Tabbed Interface.
    tab = TabWidget()

    # Init the main window and add it to the tabs.
    main_window = MainWindow(env = env)
    tab.addTab(main_window, 'Main View')

    env.web = QtWebKit.QWebView()
    #web.load(QtCore.QUrl('http://www.google.com'))
    env.web.show()
    tab.addTab(env.web, 'Map')
    
    # Init Status bar.
    st = QtGui.QStatusBar()
    # Label to display the server status in the status bar. Need to init with
    # rich text if rich text should be used later on.
    env.server_status = QtGui.QLabel('<font color="#FF0000"></font>')
    st.addPermanentWidget(env.server_status)
    # Seperator Label.
    env.seperator = QtGui.QLabel()
    env.seperator.setFrameShape(5)
    env.seperator.setFrameShadow(QtGui.QFrame.Raised)
    st.addPermanentWidget(env.seperator)
    # Label to display the current UTC time.
    env.current_time = QtGui.QLabel('')
    st.addPermanentWidget(env.current_time)

    # Start the timers.
    timers = Timers(env = env)

    window.setCentralWidget(tab)
    window.setStatusBar(st)
    # Create status bar.
    window.resize(1150, 700)
    # Startup the rest.
    main_window.startup()
    qApp.processEvents()

    # After everything is loaded show the main window and close the splash
    # screen.
    window.show()
    env.splash.finish(window)
    qApp.exec_()
