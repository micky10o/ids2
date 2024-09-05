from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QHeaderView, QPushButton,QTableWidget, QTableWidgetItem,QTabWidget, QStackedWidget, QFrame, QListWidget, QMessageBox, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDate, QTime, pyqtSlot, QTimer 
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys 
#from NIDSpyqt import NIDS
#from generatesyslogpyqt import RealTimeLogViewer
#from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock


class NetTab(QWidget):
    add_packet_signal = pyqtSignal(str)
    add_prediction_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        #from NIDSpyqt import NIDS
        #self.nids_instance = NIDS()
       # self.nids_instance.pkt_summary_signal.connect(self.add_network_pkt_summary)
        #self.nids_instance.prediction_label_signal.connect(self.add_network_prediction_label)
 
        #self.pkt_summary = None
        #self.prediction_label = None
    
    def init_ui(self):
        
        
        netlayout = QVBoxLayout()
        
        self.networktable = QTableWidget()
        self.networktable.setColumnCount(5)
        self.networktable.setHorizontalHeaderLabels(["Id", "Packet", "Prediction", "Time", "Date"])
        
        self.networktable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.networktable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.refreshnet_button = QPushButton('Refresh Network Table')
        self.refreshnet_button.clicked.connect(self.load_networktable)
        
        self.net_button = QPushButton("delete",self)
        self.net_button.clicked.connect(self.delete_network)
        
        netlayout.addWidget(self.networktable)
        netlayout.addWidget(self.refreshnet_button)
        netlayout.addWidget(self.net_button)
        self.setLayout(netlayout)
        
        self.load_networktable()
        
        
    
        
    def load_networktable(self):
        self.networktable.setRowCount(0)
    
        query = QSqlQuery("SELECT * FROM NetworkTable")
        row = 0
        while query.next():
            Id = query.value(0)
            Packet = query.value(1)
            Prediction = query.value(2)
            Time = query.value(3)
            Date = query.value(4)
        
            self.networktable.insertRow(row)
            self.networktable.setItem(row,0,QTableWidgetItem(str(Id)))
            self.networktable.setItem(row,1,QTableWidgetItem(Packet))
            self.networktable.setItem(row,2,QTableWidgetItem(Prediction))
            self.networktable.setItem(row,3,QTableWidgetItem(Time))
            self.networktable.setItem(row,4,QTableWidgetItem(Date))
        
        
            row += 1   
            
    """
    def add_network_pkt_summary(self, pkt_summary):
        self.pkt_summary = pkt_summary
        self.add_network()
    
    def add_network_prediction_label(self, prediction_label):
        self.prediction_label = prediction_label
        self.add_network()
    """    
        
    @pyqtSlot(str,str)       
    def add_network(self, pkt_summary, prediction_label):
        
       # if self.pkt_summary and self.prediction_label:  
        
           #from NIDSpyqt import NIDS
 
           time = QTime.currentTime()
           date = QDate.currentDate() 
          # self.prediction = NIDS()
          #self.packet = NIDS()
      
   
           query = QSqlQuery()
           query.prepare("""
                         INSERT INTO NetworkTable(Packet, Prediction, Time, Date)
                         VALUES (?, ?, ?, ?)
                         """)
           query.addBindValue(pkt_summary)
           query.addBindValue(prediction_label)
           query.addBindValue(time.toString())
           query.addBindValue(date.toString())
           query.exec_()
   
   
           self.load_networktable()
       
           self.pkt_summary = None
           self.prediction_label = None
       
      
    def delete_network(self):
        selected_row = self.networktable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"No Packet Chosen","Please Choose Packet")
            return
        network_id = int(self.networktable.item(selected_row,0).text())
    
        query = QSqlQuery()
        query.prepare("DELETE FROM NetworkTable WHERE Id = ?")
        query.addBindValue(network_id)
        query.exec_()
    
        self.load_networktable()
        
    
    
        
        

class HostTab(QWidget):
    add_log_signal = pyqtSignal(str, int, str, str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        #from generatesyslogpyqt import RealTimeLogViewer
        #self.log_viewer = RealTimeLogViewer()
        #self.log_viewer.log_data_signal.connect(self.add_host)

        
    def init_ui(self):
        
        hostlayout = QVBoxLayout()
        
        self.hosttable = QTableWidget()
        self.hosttable.setColumnCount(7)
        self.hosttable.setHorizontalHeaderLabels(["Id", "Source","Event ID","General", "Prediction", "Time", "Date"])
        
        self.hosttable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.hosttable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.refreshhost_button = QPushButton('Refresh Host Table')
        self.refreshhost_button.clicked.connect(self.load_hosttable)
        
        self.hostt_button = QPushButton("delete",self)
        self.hostt_button.clicked.connect(self.delete_host)
        
        hostlayout.addWidget(self.hosttable)
        hostlayout.addWidget(self.refreshhost_button)
        hostlayout.addWidget(self.hostt_button)
        self.setLayout(hostlayout)
        
        self.load_hosttable()
    
        
    
    def load_hosttable(self):
        self.hosttable.setRowCount(0)
    
        query = QSqlQuery("SELECT * FROM HostTable")
        row = 0
        while query.next():
            Id = query.value(0)
            Source = query.value(1)
            Event_ID = query.value(2)
            General = query.value(3)
            Prediction = query.value(4)
            Time = query.value(5)
            Date = query.value(6)
        
            self.hosttable.insertRow(row)
            self.hosttable.setItem(row,0,QTableWidgetItem(str(Id)))
            self.hosttable.setItem(row,1,QTableWidgetItem(Source))
            self.hosttable.setItem(row,2,QTableWidgetItem(str(Event_ID)))
            self.hosttable.setItem(row,3,QTableWidgetItem(General))
            self.hosttable.setItem(row,4,QTableWidgetItem(Prediction))
            self.hosttable.setItem(row,5,QTableWidgetItem(Time))
            self.hosttable.setItem(row,6,QTableWidgetItem(Date))
        
        
            row += 1
            
    @pyqtSlot(str, int, str, str)        
    def add_host(self, source, event_id, message, prediction):
    
       
       #from generatesyslogpyqt import RealTimeLogViewer
       
       time = QTime.currentTime()
       date = QDate.currentDate()   
       #prediction = "Anomaly"
       #self.general =    RealTimeLogViewer()
       #self.event_ID =  RealTimeLogViewer()
      # self.source =  RealTimeLogViewer()
   
       query = QSqlQuery()
       query.prepare("""
                     INSERT INTO HostTable(Source, Event_ID, General, Prediction, Time, Date)
                     VALUES (?, ?, ?, ?, ?, ?)
                     """)
       query.addBindValue(source)
       query.addBindValue(event_id)
       query.addBindValue(message)
       query.addBindValue(prediction)
       query.addBindValue(time.toString())
       query.addBindValue(date.toString())
       query.exec_()
   
   
       self.load_hosttable()
       
       
    def delete_host(self):
        selected_row = self.hosttable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,"No Row Chosen","Please Choose Row")
            return
        host_id = int(self.hosttable.item(selected_row,0).text())
    
        query = QSqlQuery()
        query.prepare("DELETE FROM HostTable WHERE Id = ?")
        query.addBindValue(host_id)
        query.exec_()
    
        self.load_hosttable()
        
    
        
    

    
        
      

class Report(QWidget):
    
     # Define a signal for adding a device
    add_device_signal = pyqtSignal(str)
    del_device_signal = pyqtSignal(str)
    
    add_app_signal = pyqtSignal(str)
    del_app_signal = pyqtSignal(str)
    
    add_site_signal = pyqtSignal(str)
    del_site_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.add_device_signal.connect(self.add_device)
        #self.del_device_signal.connect(self.delete_device)
        
        
        
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.devicetab = QWidget()
        self.apptab = QWidget()
        self.sitetab = QWidget()
        
        self.tab_widget = QTabWidget()
        
        self.devicelayout =  QVBoxLayout(self.devicetab)
        self.applayout = QVBoxLayout(self.apptab)
        self.sitelayout = QVBoxLayout(self.sitetab)
        
        self.devicetable = QTableWidget()
        self.devicetable.setColumnCount(5)
        self.devicetable.setHorizontalHeaderLabels(["Id", "Device", "State", "Time", "Date"])
        
        self.devicetable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.devicetable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.refreshdevice_button = QPushButton('Refresh Device Table')
        self.refreshdevice_button.clicked.connect(self.load_devicetable)
        
        self.devicelayout.addWidget(self.devicetable)
        self.devicelayout.addWidget(self.refreshdevice_button)
        self.devicetab.setLayout(self.devicelayout)
        
        
        
        
        self.apptable = QTableWidget()
        self.apptable.setColumnCount(5)
        self.apptable.setHorizontalHeaderLabels(["Id", "App", "State", "Time", "Date"])
        
        self.devicetable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.devicetable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.refreshapp_button = QPushButton('Refresh App Table')
        self.refreshapp_button.clicked.connect(self.load_apptable)
        
        self.applayout.addWidget(self.apptable)
        self.applayout.addWidget(self.refreshapp_button)
        self.apptab.setLayout(self.applayout)
        
        
        
        self.sitetable = QTableWidget()
        self.sitetable.setColumnCount(5)
        self.sitetable.setHorizontalHeaderLabels(["Id", "Site", "State", "Time", "Date"])
        
        self.sitetable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.sitetable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.refreshsite_button = QPushButton('Refresh Site Table')
        self.refreshsite_button.clicked.connect(self.load_sitetable)
        
        self.sitelayout.addWidget(self.sitetable)
        self.sitelayout.addWidget(self.refreshsite_button)
        self.sitetab.setLayout(self.sitelayout)
        
        
        
       
        
        #self.blocked_devices = self.devicetable
        #self.blocked_apps  = self.apptable
        #self.blocked_site = self.sitetable
        self.NIDS = NetTab()
        self.HIDS = HostTab()
        
        self.tab_widget.addTab( self.devicetab, "Blocked devices")
        self.tab_widget.addTab( self.apptab, "Blocked apps")
        self.tab_widget.addTab(self.sitetab, "Blocked sites")
        self.tab_widget.addTab( self.NIDS, "NIDS")
        self.tab_widget.addTab(self.HIDS, "HIDS")

        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        
    
        self.load_devicetable()
        self.load_apptable()
        self.load_sitetable()
        
    
    def select_host_tab(self):
        # Select the "Host" tab
        self.tab_widget.setCurrentIndex(4)
        
    def select_net_tab(self):
        self.tab_widget.setCurrentIndex(3)
        
    def select_tab(self):
        self.tab_widget.setCurrentIndex(0)
        
        
    def load_devicetable(self):
        self.devicetable.setRowCount(0)
    
        query = QSqlQuery("SELECT * FROM DeviceTable")
        row = 0
        while query.next():
            Id = query.value(0)
            Device = query.value(1)
            State = query.value(2)
            Time = query.value(3)
            Date = query.value(4)
        
            self.devicetable.insertRow(row)
            self.devicetable.setItem(row,0,QTableWidgetItem(str(Id)))
            self.devicetable.setItem(row,1,QTableWidgetItem(Device))
            self.devicetable.setItem(row,2,QTableWidgetItem(State))
            self.devicetable.setItem(row,3,QTableWidgetItem(Time))
            self.devicetable.setItem(row,4,QTableWidgetItem(Date))
        
        
            row += 1
            
    
    @pyqtSlot(str)       
    def add_device(self, device_text):
        
       #from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock

    
       time = QTime.currentTime()
       date = QDate.currentDate() 
       state = "blocked" 
       #self.usb_page = USBDevicesPage() 
     
   
   
       query = QSqlQuery()
       query.prepare("""
                     INSERT INTO DeviceTable(Device, State, Time, Date)
                     VALUES (?, ?, ?, ?)
                      """)
       query.addBindValue(device_text)
       query.addBindValue(state)
       query.addBindValue(time.toString())
       query.addBindValue(date.toString())
       query.exec_()
   
   
       self.load_devicetable()
        
       
        
        
    def load_apptable(self):
        self.apptable.setRowCount(0)
    
        query = QSqlQuery("SELECT * FROM AppTable")
        row = 0
        while query.next():
            Id = query.value(0)
            App = query.value(1)
            State = query.value(2)
            Time = query.value(3)
            Date = query.value(4)
        
            self.apptable.insertRow(row)
            self.apptable.setItem(row,0,QTableWidgetItem(str(Id)))
            self.apptable.setItem(row,1,QTableWidgetItem(App))
            self.apptable.setItem(row,2,QTableWidgetItem(State))
            self.apptable.setItem(row,3,QTableWidgetItem(Time))
            self.apptable.setItem(row,4,QTableWidgetItem(Date))
        
        
            row += 1
            
    @pyqtSlot(str)        
    def add_app(self, application):
        
       #from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock

    
       time = QTime.currentTime()
       date = QDate.currentDate() 
       state = "blocked"  
      # self.app_page = BlockAppsPage()  
   
   
       query = QSqlQuery()
       query.prepare("""
                     INSERT INTO AppTable(App, State, Time, Date)
                     VALUES (?, ?, ?, ?)
                     """)
       query.addBindValue(application)
       query.addBindValue(state)
       query.addBindValue(time.toString())
       query.addBindValue(date.toString())
       query.exec_()
   
   
       #self.load_apptable()
        
        
        
        
    def load_sitetable(self):
        self.sitetable.setRowCount(0)
    
        query = QSqlQuery("SELECT * FROM SiteTable")
        row = 0
        while query.next():
            Id = query.value(0)
            Site = query.value(1)
            State = query.value(2)
            Time = query.value(3)
            Date = query.value(4)
        
            self.sitetable.insertRow(row)
            self.sitetable.setItem(row,0,QTableWidgetItem(str(Id)))
            self.sitetable.setItem(row,1,QTableWidgetItem(Site))
            self.sitetable.setItem(row,2,QTableWidgetItem(State))
            self.sitetable.setItem(row,3,QTableWidgetItem(Time))
            self.sitetable.setItem(row,4,QTableWidgetItem(Date))
        
        
            row += 1
            
            
    
    @pyqtSlot(str)       
    def add_site(self, website):
        
       #from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock

    
       time = QTime.currentTime()
       date = QDate.currentDate()
       state = "blocked" 
       #self.website_page =  WebsiteBlock()   
   
   
       query = QSqlQuery()
       query.prepare("""
                     INSERT INTO SiteTable(Site, State, Time, Date)
                     VALUES (?, ?, ?, ?)
                     """)
       query.addBindValue(website)
       query.addBindValue(state)
       query.addBindValue(time.toString())
       query.addBindValue(date.toString())
       query.exec_()
   
   
       self.load_sitetable()
       
       
    
    @pyqtSlot(str)  
    def delete_device(self, device_text):
        
        #from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock

       # self.device_name = USBDevicesPage()
    
        query = QSqlQuery()
        query.prepare("DELETE FROM DeviceTable WHERE Device =?")
        query.addBindValue(device_text)
        query.exec_() 
        self.load_devicetable()
        
    @pyqtSlot(str)    
    def delete_app(self, application):
        
       # from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock

        #self.app_name = BlockAppsPage()
    
        query = QSqlQuery()
        query.prepare("DELETE FROM AppTable WHERE App =?")
        query.addBindValue(application)
        query.exec_() 
        self.load_apptable()
    
    
    @pyqtSlot(str)
    def delete_site(self, website):
        
        #from login11 import USBDevicesPage, BlockAppsPage, WebsiteBlock
        
        
       # self.site_name = WebsiteBlock()
    
        query = QSqlQuery()
        query.prepare("DELETE FROM SiteTable WHERE Site =?")
        query.addBindValue(website)
        query.exec_() 
        self.load_sitetable()
   


        
       
class Dashboard(QWidget):
    switch_to_report = pyqtSignal()
    switch_to_reporthost = pyqtSignal()
    switch_to_reportnet = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self): 
        layout = QVBoxLayout()
        allbutlayout = QHBoxLayout()
        but1layout = QVBoxLayout()
        but2layout = QVBoxLayout()
        but3layout = QVBoxLayout()
        
         # Initialize counts
        self.net_count = 0
        self.row_count = 0
        self.device_count = 0
        self.app_count = 0
        self.web_count = 0
        
        self.update_counts()
        
        
        report_label = QLabel('Reports')
        self.report_button = QPushButton(str(self.net_count  + self.row_count + self.app_count + self.device_count + self.web_count),self)
        self.report_button.clicked.connect(self.on_report_button_clicked)
        
        but1layout.addWidget(report_label)
        but1layout.addWidget(self.report_button)
        
        
        
        
        host_label = QLabel('Host intrusions')
        self.host_button = QPushButton(str(self.row_count), self)
        self.host_button.clicked.connect(self.on_host_button_clicked)
        
        but2layout.addWidget(host_label)
        but2layout.addWidget(self.host_button)
        
        
        network_label = QLabel('Network intrusions')
        self.network_button = QPushButton(str(self.net_count),self)
        self.network_button.clicked.connect(self.on_network_button_clicked)
        
        but3layout.addWidget(network_label)
        but3layout.addWidget(self.network_button)
        
        
        allbutlayout.addLayout(but1layout)
        allbutlayout.addLayout(but2layout)
        allbutlayout.addLayout(but3layout)
        
        
        self.mixtable = QTableWidget()
        self.mixtable.setColumnCount(5)
        self.mixtable.setHorizontalHeaderLabels(["Id", "Description", "Prediction", "Time", "Date"])
        
        self.mixtable.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.mixtable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.refreshbutton = QPushButton("refresh")
        self.refreshbutton.clicked.connect(self.refresh)
        
        layout.addLayout(allbutlayout)
        layout.addWidget(self.mixtable)
        layout.addWidget(self.refreshbutton)
        
        self.setLayout(layout)
        
        self.load_mixtable()
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_row_count)
        self.timer.start(1000)
        
        self.update_row_count()
        
    def on_host_button_clicked(self):
        # Emit the signal to switch to the report page and select the Host tab
        self.switch_to_reporthost.emit()
        
    def on_report_button_clicked(self):
        # Emit the signal to switch to the report page and select the Host tab
        self.switch_to_report.emit()
        
    def on_network_button_clicked(self):
        # Emit the signal to switch to the report page and select the Host tab
        self.switch_to_reportnet.emit()
        
    def update_counts(self):
        
        query = QSqlQuery()
        query.exec_("SELECT COUNT(*) FROM NetworkTable")

        if query.next():
            self.net_count = query.value(0)
        
        
        query.exec_("SELECT COUNT(*) FROM HostTable")

        if query.next():
            self.row_count = query.value(0)
            
        
        query.exec_("SELECT COUNT(*) FROM DeviceTable")

        if query.next():
            self.device_count = query.value(0)
            
        
        query.exec_("SELECT COUNT(*) FROM AppTable")

        if query.next():
            self.app_count = query.value(0)
            
        
        query.exec_("SELECT COUNT(*) FROM SiteTable")

        if query.next():
            self.web_count = query.value(0)
    
    def update_row_count(self):
         
        self.update_counts()

        # Update the button text with the new row count
        self.host_button.setText(str(self.row_count))
        self.report_button.setText(str(self.net_count + self.row_count + self.app_count + self.device_count + self.web_count))
        self.network_button.setText(str(self.net_count))
            
    def load_mixtable(self):    
        query = QSqlQuery()
        query.exec_("DROP TABLE IF EXISTS CombinedTable")
        query.exec_("""CREATE TABLE CombinedTable AS
                    SELECT Id AS combined_column1, Packet AS combined_column2, Prediction AS combined_3, Time AS combined_4, Date AS combined_5
                       FROM NetworkTable
                       UNION ALL
                       SELECT Id AS combined_column1, General AS combined_column2, Prediction As combined_3, Time AS combined_4, Date AS combined_5 
                       FROM HostTable""")
        query.exec_("SELECT * FROM CombinedTable")
        row = 0
        while query.next():
            combined_column1 = query.value(0)
            combined_column2 = query.value(1)
            combined_column3 = query.value(2)
            combined_column4 = query.value(3)
            combined_column5 = query.value(4)
            
           # print(combined_column1, combined_column2)
           
            self.mixtable.insertRow(row)
            self.mixtable.setItem(row,0,QTableWidgetItem(str(combined_column1)))
            self.mixtable.setItem(row,1,QTableWidgetItem(combined_column2))
            self.mixtable.setItem(row,2,QTableWidgetItem(combined_column3))
            self.mixtable.setItem(row,3,QTableWidgetItem(combined_column4))
            self.mixtable.setItem(row,4,QTableWidgetItem(combined_column5))
        
        
            row += 1
            
    def delete_mixtable(self):
        query = QSqlQuery()
        query.prepare("DELETE FROM CombinedTable")
        if not query.exec_():
            print(f"Error deleting from CombinedTable: {query.lastError().text()}")

    # Optionally, you might want to clear the table widget before reloading
        self.mixtable.setRowCount(0)
    
        self.load_mixtable()
        
    

        
    def refresh(self):
        self.delete_mixtable()
        self.update_row_count()
        
        
       

    

#database

database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName ("Intrusion.db")
if not database.open():
    QMessageBox.critical(None, "Error","could not open Database")
    sys.exit(1)       
    
    
query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS NetworkTable(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Packet TEXT,
                Prediction TEXT,
                Time TEXT,
                Date TEXT
            )
            
            """)

query.exec_("""
            CREATE TABLE IF NOT EXISTS HostTable(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Source TEXT,
                Event_ID INTEGER,
                General TEXT,
                Prediction TEXT,
                Time TEXT,
                Date TEXT
            )
            
            """)

query.exec_("""
            CREATE TABLE IF NOT EXISTS DeviceTable(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Device TEXT,
                State TEXT,
                time TEXT,
                date TEXT
            )
            
            """)

query.exec_("""
            CREATE TABLE IF NOT EXISTS APPTable(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                App TEXT,
                State TEXT,
                time TEXT,
                date TEXT
            )
            
            """)


query.exec_("""
            CREATE TABLE IF NOT EXISTS SiteTable(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Site TEXT,
                State TEXT,
                time TEXT,
                date TEXT
            )
            
            """)



        
        

        
        
        
        

        

   


   
   
   

   
   

   
   
   

        
       

     


    



    
    