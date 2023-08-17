from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel
from DatabaseManager import DatabaseManager
from FileOrganizer import FileOrganizer

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DATABASE_PATH = r"C:\Users\perei\Desktop\projects\Python_AutomatedFileOrganizer\src\dbase\mydatabase.db"

class UserInterface:
    def __init__(self):
        """Initialize the main window and load user settings."""
        self.app = QtWidgets.QApplication([])
        self.window = QtWidgets.QMainWindow()
        self.loadSettings()
        self.fileSystemModel = QFileSystemModel()

    def launchGUI(self):
        """Launch the main GUI window."""
        self.setupMainWindow()
        self.setupButtons()
        self.setupLayouts()
        self.window.show()
        self.app.exec_()

    def setupMainWindow(self):
        """Set up the main window properties."""
        self.window.setWindowTitle("My App")
        self.window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def setupButtons(self):
        """Create and configure buttons."""
        self.buttons = {
            "organize": QtWidgets.QPushButton("Organize Files", clicked=self.onOrganizeButtonClicked),
            "zip": QtWidgets.QPushButton("Zip Files", clicked=self.onZipButtonClicked),
            "save": QtWidgets.QPushButton("Save Settings", clicked=self.onSaveSettingsButtonClicked),
            "back": QtWidgets.QPushButton("Back", clicked=self.onBackButtonClicked),
            "scan": QtWidgets.QPushButton("Scan", clicked=self.onScanButtonClicked),
        }

    def setupLayouts(self):
        """Set up layouts and widgets."""
        fileTreeView = self.setupFileTreeView()
        self.folderTextbox = QtWidgets.QLineEdit()

        topLayout = self.createHorizontalLayout([self.folderTextbox, self.buttons['back'], self.buttons['scan']])
        bottomLayout = self.createHorizontalLayout([fileTreeView])
        buttonLayout = self.createHorizontalLayout([self.buttons['organize'], self.buttons['zip']])
        mainlayout = QtWidgets.QVBoxLayout()
        mainlayout.addLayout(topLayout)
        mainlayout.addLayout(bottomLayout)
        mainlayout.addLayout(buttonLayout)
        mainlayout.addWidget(self.buttons['save'])

        widget = QtWidgets.QWidget()
        widget.setLayout(mainlayout)
        self.window.setCentralWidget(widget)

    def createHorizontalLayout(self, widgets):
        """Create a horizontal layout with the given widgets."""
        layout = QtWidgets.QHBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def setupFileTreeView(self):
        """Create and configure the file tree view."""
        self.fileTreeView = QtWidgets.QTreeView()
        self.fileSystemModel.setRootPath(QDir.rootPath())
        self.fileTreeView.setModel(self.fileSystemModel)
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(QDir.rootPath()))
        self.fileTreeView.clicked.connect(self.onTreeViewItemClicked)
        return self.fileTreeView

    def loadSettings(self):
        """Load user settings from the database."""
        self.database_path = r"C:\Users\perei\Desktop\projects\Python_AutomatedFileOrganizer\src\dbase\mydatabase.db"
        self.settings = DatabaseManager(self.database_path)
        self.settings.loadSettings()

    def onScanButtonClicked(self):
        """Handle the Scan button click."""
        folder_path = self.folderTextbox.text() # Get the text from the folderTextbox
        self.fileSystemModel.setRootPath(folder_path) # Set the new root path
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(folder_path)) # Set the new root index
    
    def onBackButtonClicked(self):
        """Handle the Back button click."""
        current_path = QDir(self.folderTextbox.text())
        current_path.cdUp() # Navigate up one directory
        parent_path = current_path.absolutePath() # Get the new path
        self.folderTextbox.setText(parent_path) # Update the folder text box
        self.fileSystemModel.setRootPath(parent_path) # Set the new root path
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(parent_path)) # Set the new root index

    def onTreeViewItemClicked(self, index):
        """Handle a tree view iten=m click"""
        selected_path = self.fileSystemModel.filePath(index)
        self.folderTextbox.setText(selected_path)

    def onOrganizeButtonClicked(self):
        """Handle the Organize Files button click."""
        folder_path = self.folderTextbox.text().replace("\\", "\\\\")
        FileOrganizer({}, self.database_path, folder_path).organizeFiles()
       
    def onZipButtonClicked(self):
        """Handle the Zip Files button click."""
        FileOrganizer().zipFiles()

    def onSaveSettingsButtonClicked(self):
        """Handle the Save Settings button click."""
        #Settings(self.settings).set()
        pass

    def closeApp(self):
        """Close the application and perform any necessary cleanup."""
        self.app.quit()

if __name__ == "__main__":
    ui = UserInterface()
    ui.launchGUI()
