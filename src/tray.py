import os
import sys
from PySide2 import QtWidgets, QtGui

opt = {
    True:False,
    False:True
}

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent, config):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

        self.Config = config
        self.config = self.Config.fetch_config()

        self.setToolTip('ValorantRPC V4.0')
        menu = QtWidgets.QMenu(parent)

        rpc_settings = menu.addMenu("Display Settings")

        self.show_rank:QtWidgets.QAction = rpc_settings.addAction("Show Rank")
        self.show_rank.triggered.connect(self.showrank)

        self.show_pcount = rpc_settings.addAction("Show Party Count")
        self.show_pcount.triggered.connect(self.showpcount)

        self.show_level = rpc_settings.addAction("Show Level")
        self.show_level.triggered.connect(self.showlevel)

        self.show_rank.setCheckable(True)
        self.show_level.setCheckable(True)
        self.show_pcount.setCheckable(True)

        self.show_rank.setChecked(self.config['presence']['show_rank'])
        self.show_pcount.setChecked(self.config['presence']['show_party_count'])
        self.show_level.setChecked(self.config['presence']['show_level'])

        menu.addSeparator()
        restart = menu.addAction("Restart")
        restart.triggered.connect(self.restart)
        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(sys.exit)

        self.setContextMenu(menu)

    def restart(self):
        os.startfile(os.path.abspath(sys.argv[0]))
        os._exit(1)

    def showrank(self):
        config = self.config
        config['presence']['show_rank'] = opt[self.config['presence']['show_rank']]
        self.Config.update(config)
        self.config = config
        self.show_rank.setChecked(self.config['presence']['show_rank'])
        

    def showpcount(self):
        config = self.config
        config['presence']['show_party_count'] = opt[self.config['presence']['show_party_count']]
        self.Config.update(config)
        self.config = config
        self.show_pcount.setChecked(self.config['presence']['show_party_count'])
    
    def showlevel(self):
        config = self.config
        config['presence']['show_level'] = opt[self.config['presence']['show_level']]
        self.Config.update(config)
        self.config = config
        self.show_level.setChecked(self.config['presence']['show_level'])

def sysrun(config):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(os.path.join(config.get_appdata_folder(),'favicon.ico')), w, config)
    tray_icon.show()
    sys.exit(app.exec_())
