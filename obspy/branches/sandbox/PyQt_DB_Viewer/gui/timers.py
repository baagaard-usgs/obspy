from PyQt4 import QtCore
from obspy.core import UTCDateTime

class Timers(QtCore.QThread):
    def __init__(self, env, parent = None, *args, **kwargs):
        super(Timers, self).__init__(parent)
        self.env = env
        # Set to lowest priority.
        #self.setPriority(1)
        self.start()

    def updateServerStatus(self):
        msg = 'SeisHub server %s: ' % self.env.seishub_server
        connection = self.env.seishub.ping()
        if connection:
            self.env.seishub.online = True
            msg += '<font color="#339966">connected</font>'
        else:  
            self.env.seishub.online = False
            msg += '<font color="#FF0000">no connection</font>'
        self.env.server_status.setText(msg)

    def updateCurrentTime(self):
        msg = 'Current UTC time: '
        cur = UTCDateTime()
        msg += str(cur)[:19]
        self.env.current_time.setText(msg)

    def run(self):
        # Run once.
        self.updateCurrentTime()
        self.updateServerStatus()
        # Setup server timer.
        self.server_timer = QtCore.QTimer()
        self.server_timer.timeout.connect(self.updateServerStatus)
        # Call every ten second.
        self.server_timer.start(10000)
        # Setup time timer.
        self.time_timer = QtCore.QTimer()
        self.time_timer.timeout.connect(self.updateCurrentTime)
        # Call every  second.
        self.time_timer.start(1000)
        # Start main loop of the thread. Needed for the timers.
        self.exec_()
