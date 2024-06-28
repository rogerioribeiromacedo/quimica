# -*- coding: utf-8 -*-
"""
Generate and plot data about volumetry.

Author......: Rogério Ribeiro Macêdo
Github......: https://github.com/rogerioribeiromacedo/quimica/tree/main/quimica_analitica/volumetria
Last update.: 24/06/2024
"""
# pylint: disable=invalid-name
# pylint: disable=import-error
try:
    import sys
    import csv
    from pathlib import Path
    from PyQt5 import QtGui, QtWidgets, QtCore

    # Matplotlib
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

    # Classes use in this project
    import classMessageBox
    import classTitulacao
except ImportError as e:
    print('[!] The required Python libraries could not be imported:', file=sys.stderr)
    print(f'\t{e}')
    sys.exit(1)

# Constants
MSG_TITLE = "Volumetry"


class mplCustomizedToolbar(NavigationToolbar):
    """Modify the default matplotlib toolbar."""

    # Button that will appear in toolbar
    toolitems = [
        t for t in NavigationToolbar.toolitems
        if t[0] in ('Home', 'Pan', 'Zoom', 'Save')
    ]

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(mplCustomizedToolbar, self).__init__(*args, **kwargs)
        self.layout().takeAt(4)


class MplCanvas(FigureCanvas):
    """Class that create."""

    def __init__(self, parent=None, width=9.0, height=6.0, dpi=72):
        """Initialize the class."""
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QtWidgets.QMainWindow):
    """Class main window."""

    def __init__(self):
        """
        Class init.

        Returns
        -------
        None.

        """
        super().__init__()

        # Message box
        self.msgbox = classMessageBox.MessageBox()

        # Contruct the windows
        self.initUI()

    def initUI(self):
        """
        Widgets init.

        Returns
        -------
        None.

        """       
        # Properties of windows.
        self.setWindowTitle("Volumetry")
        self.setWindowIcon(QtGui.QIcon('images/logo_volumetry.png'))

        # Menu bar
        self.mainMenuBar()

        # Tool bar
        self.mainToolBar()

        # Status bar
        self.mainStatusBar()

        # window layout
        self.windowLayout()

    def windowLayout(self):
        """
        Windows Layout.

        Returns
        -------
        None.

        """
        # Principal
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setObjectName("mainLayout")

        # Frames Widgets
        self.setLeftFrame()
        self.setRightFrame()

        # Adding frames to mainLayout
        self.mainLayout.addWidget(self.leftFrame)
        self.mainLayout.addWidget(self.rightFrame)
        self.mainLayout.setStretchFactor(self.leftFrame, 1)
        self.mainLayout.setStretchFactor(self.rightFrame, 1)

        # Initiating window widget
        self.window = QtWidgets.QWidget()
        self.window.setObjectName("window")
        self.window.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Minimum)
        self.window.setLayout(self.mainLayout)

        # Central Widget
        self.setCentralWidget(self.window)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Minimum)

    def setLeftFrame(self):
        """Left Frame."""
        # Frame
        self.leftFrame = QtWidgets.QFrame()
        self.leftFrame.setObjectName("leftFrame")
        self.leftFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                     QtWidgets.QSizePolicy.Minimum)

        # Layout frame
        self.boxLeftLayout = QtWidgets.QVBoxLayout()
        self.boxLeftLayout.setObjectName("boxLeftLayout")

        #
        # Widgets
        #

        # Type of volumetry
        self.listTypeVolFrame = QtWidgets.QGroupBox("Volumetria de Neutralização")
        self.listTypeVolFrame.setObjectName("listTypeVolFrame")
        self.listTypeVolGrid = QtWidgets.QGridLayout()
        self.listTypeVolGrid.setRowStretch(2, 1)

        self.optAcForteBaForte = QtWidgets.QRadioButton("Ácido Forte com Base Forte")
        self.optAcForteBaForte.setStatusTip("O pH no P.E = 7,00")
        self.optAcForteBaForte.setObjectName("optAcForteBaForte")
        self.optAcForteBaForte.setAccessibleName("optAcForteBaForte")
        self.optAcForteBaForte.toggled.connect(self.onClicked)
        self.optAcForteBaForte.setChecked(True)
        self.getAcForteBaForte()  # list of strong acid and strong base
        self.listTypeVolGrid.addWidget(self.optAcForteBaForte, 0, 0, 1, 2)

        self.optAcFracoBaForte = QtWidgets.QRadioButton("Ácido Fraco com Base Forte")
        self.optAcFracoBaForte.setStatusTip("O pH no P.E > 7,00")
        self.optAcFracoBaForte.setObjectName("optAcFracoBaForte")
        self.optAcFracoBaForte.setAccessibleName("optAcFracoBaForte")
        self.optAcFracoBaForte.toggled.connect(self.onClicked)
        self.listTypeVolGrid.addWidget(self.optAcFracoBaForte, 1, 0, 1, 2)

        self.optAcForteBaFraca = QtWidgets.QRadioButton("Ácido Forte com Base Fraca")
        self.optAcForteBaFraca.setStatusTip("O pH no P.E < 7,00")
        self.optAcForteBaFraca.setObjectName("optAcForteBaFraca")
        self.optAcForteBaFraca.setAccessibleName("optAcForteBaFraca")
        self.optAcForteBaFraca.toggled.connect(self.onClicked)
        self.listTypeVolGrid.addWidget(self.optAcForteBaFraca, 2, 0, 1, 2)

        self.listTypeVolFrame.setLayout(self.listTypeVolGrid)

        # Acids and Bases (frame and layout)
        self.frameAcidsBases = QtWidgets.QFrame()
        self.frameAcidsBases.setObjectName("frameAcidsBases")
        self.layoutAcidosBases = QtWidgets.QHBoxLayout()
        self.layoutAcidosBases.setSpacing(4)  # Space between cells
        self.layoutAcidosBases.setContentsMargins(0, 0, 0, 0)  # Margins
        self.frameAcidsBases.setLayout(self.layoutAcidosBases)

        # Acids and Bases -> List of acids
        self.listAcidsGroupBox = QtWidgets.QGroupBox("Ácidos (titulado)")
        self.listAcidsGroupBox.setObjectName("listAcidsGroupBox")
        self.listAcidsLayout = QtWidgets.QGridLayout()
        self.listAcidsLayout.setAlignment(QtCore.Qt.AlignTop)

        self.combListAcids = QtWidgets.QComboBox()
        self.combListAcids.setObjectName("combListAcids")

        self.lblAcidConcentration = QtWidgets.QLabel("Concentração")
        self.lblAcidConcentration.setObjectName("lblAcidConcentration")
        self.edtAcidConcentration = QtWidgets.QLineEdit()
        self.edtAcidConcentration.setObjectName("edtAcidConcentration")
        self.edtAcidConcentration.setStatusTip("Concentração do ácido em mol/L")

        self.lblAcidVolume = QtWidgets.QLabel("Volume")
        self.lblAcidVolume.setObjectName("lblAcidVolume")
        self.edtAcidVolume = QtWidgets.QLineEdit()
        self.edtAcidVolume.setObjectName("edtAcidVolume")
        self.edtAcidVolume.setStatusTip("Volume do ácido em mL")

        self.listAcidsLayout.addWidget(self.combListAcids, 0, 0, 1, 3)
        self.listAcidsLayout.addWidget(self.lblAcidConcentration, 1, 0, 1, 2)
        self.listAcidsLayout.addWidget(self.edtAcidConcentration, 1, 1, 1, 2)
        self.listAcidsLayout.addWidget(self.lblAcidVolume, 2, 0, 1, 2)
        self.listAcidsLayout.addWidget(self.edtAcidVolume, 2, 1, 1, 2)

        self.listAcidsGroupBox.setLayout(self.listAcidsLayout)

        # Acids and Bases -> List of bases
        self.listBasesGroupBox = QtWidgets.QGroupBox("Bases (titulante)")
        self.listBasesGroupBox.setObjectName("listBasesGroupBox")
        self.listBasesLayout = QtWidgets.QGridLayout()
        self.listBasesLayout.setAlignment(QtCore.Qt.AlignTop)  # align widgets on top

        self.combListBases = QtWidgets.QComboBox()
        self.combListBases.setObjectName("combListBases")

        self.lblBaseConcentration = QtWidgets.QLabel("Concentração")
        self.lblBaseConcentration.setObjectName("lblBaseConcentration")
        self.edtBaseConcentration = QtWidgets.QLineEdit()
        self.edtBaseConcentration.setObjectName("edtBaseConcentration")
        self.edtBaseConcentration.setStatusTip("Concentração da base em mol/L")

        self.listBasesLayout.addWidget(self.combListBases, 0, 0, 1, 3)
        self.listBasesLayout.addWidget(self.lblBaseConcentration, 1, 0, 1, 2)
        self.listBasesLayout.addWidget(self.edtBaseConcentration, 1, 1, 1, 2)

        self.listBasesGroupBox.setLayout(self.listBasesLayout)

        # Adding widgets in Acids and Bases
        self.layoutAcidosBases.addWidget(self.listAcidsGroupBox)
        self.layoutAcidosBases.addWidget(self.listBasesGroupBox)

        #
        # Buttons
        #
        self.frameButtons = QtWidgets.QFrame()
        self.frameButtons.setObjectName("frameButtons")
        self.layoutButtons = QtWidgets.QHBoxLayout()
        self.layoutButtons.setSpacing(4)  # Space between cells
        self.layoutButtons.setContentsMargins(0, 0, 0, 0)  # Margins
        self.frameButtons.setLayout(self.layoutButtons)

        # Button -> Start
        self.btnCalculate = QtWidgets.QPushButton("Calcular")
        self.btnCalculate.setObjectName("btnCalculate")
        # self.btnCalculate.setEnabled(False)
        self.btnCalculate.setStatusTip('Calcular e gerar gráfico')
        self.btnCalculate.clicked.connect(self.on_click_calculate)

        # Button -> Results
        self.btnResults = QtWidgets.QPushButton("Resultados")
        self.btnResults.setObjectName("btnResults")
        # self.btnResults.setEnabled(False)
        self.btnResults.setStatusTip('Mostrar resultados')
        self.btnResults.clicked.connect(self.on_click_resultados)

        # Adding widgets in the frameButtons
        self.layoutButtons.addWidget(self.btnCalculate)
        self.layoutButtons.addWidget(self.btnResults)

        # Adding widgets in the boxLeftLayout
        self.boxLeftLayout.addWidget(self.listTypeVolFrame)
        self.boxLeftLayout.addWidget(self.frameAcidsBases)
        self.boxLeftLayout.addWidget(self.frameButtons)

        # Add a spacer
        self.boxLeftLayout.addStretch()

        # Adding layout to frame
        self.leftFrame.setLayout(self.boxLeftLayout)

        # Prepare list of acids and bases
        self.getAcForteBaForte()

    def on_click_calculate(self):
        self.objTitulacao = classTitulacao.Titulacao("A", 0.01, 0.01, "B", 0.01, 1.5*10**-2, 4.756)
        print(self.objTitulacao.getAcido())

    def on_click_resultados(self):
        pass

    def onClicked(self):
        """
        RadioButton clicked.

        Returns
        -------
        None.

        """
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.accessibleName() == "optAcForteBaForte":
                self.getAcForteBaForte()
            elif radioButton.accessibleName() == "optAcFracoBaForte":
                self.getAcFracoBaForte()
            elif radioButton.accessibleName() == "optAcForteBaFraca":
                self.getAcForteBaFraca()

    def getAcForteBaForte(self):
        """
        Get a list of strong acids and bases and add them to a combo box.

        Returns
        -------
        None.

        """
        # Get a list of strong acids
        list_of_acids = self.readAcids("S")
        # list_of_bases = readBases("S")

        # adding itens
        self.listAcidsGroupBox.clear()
        self.listAcidsGroupBox.addItems(list_of_acids)

    def getAcFracoBaForte(self):
        pass

    def getAcForteBaFraca(self):
        pass

    def readAcids(self, strength):
        """
        Read fron acids.csv a list of acids.

        Parameters
        ----------
        strength : str
            The acid strength.

        Returns
        -------
        list
            A list of all acids that have the type of specified acid strength.

        """
        list_of_acids = []
        with open("data/acids.csv", "r") as csv_file:
            # creating a csv reader object
            csv_reader = csv.reader(csv_file)

            # extracting each data row one by one
            for row in csv_reader:
                list_of_acids.append(row[0])

        return list_of_acids

    def setRightFrame(self):
        """Right Frame."""
        # Frame
        self.rightFrame = QtWidgets.QFrame()
        self.rightFrame.setObjectName("rightFrame")
        self.rightFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                      QtWidgets.QSizePolicy.Minimum)

        # Layout
        self.boxRightLayout = QtWidgets.QVBoxLayout()
        self.boxRightLayout.setObjectName("boxRightLayout")

        # Matplotlib graph
        self.mplGraphFrame = QtWidgets.QWidget()
        self.canvas = MplCanvas(self, width=5, height=4, dpi=72)
        self.cid = self.canvas.fig.canvas.mpl_connect('button_press_event',
                                                      self.clickIntegral)
        # self.mplToolbar = mplCustomizedToolbar(self.canvas, self.mplGraphFrame)
        self.mplToolbar = NavigationToolbar(self.canvas, self.mplGraphFrame)
        self.current_item_row = -1
        self.current_item = ""

        # self.mplToolbar = NavigationToolbar(self.canvas, self.mplGraphFrame)

        # Adding widgets
        self.boxRightLayout.addWidget(self.mplToolbar)
        self.boxRightLayout.addWidget(self.canvas)

        # Adding layout to frame
        self.rightFrame.setLayout(self.boxRightLayout)

    def clickIntegral(self, event):
        """When click on graph."""
        print("clickIntegral")

    def mainStatusBar(self):
        """
        Make de main status bar.

        Returns
        -------
        None.

        """
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("padding-top: 5px;padding-bottom: 5px;border-top:0.5px solid black;"
                                     "color:black;")
        self.statusBar.showMessage("Ready!?")

    def mainToolBar(self):
        """
        Make the main tool bar.

        Returns
        -------
        None.

        """
        # Toolbar
        toolbar = QtWidgets.QToolBar('Main toolbar')
        toolbar.setStyleSheet(".QToolBar {padding-top: 27px;padding-bottom: 27px;"
                              "border-bottom:1px solid black;"
                              "color:black;spacing:5px;}")
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.setIconSize(QtCore.QSize(32, 32))

        # Bottom exit
        exitAction = QtWidgets.QAction(QtGui.QIcon('images/exit.png'), 'Sair', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.setStatusTip('Sair.')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # Bottom open
        openAction = QtWidgets.QAction(QtGui.QIcon('images/open.png'), 'Abrir', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Abrir os dados de curva de titulação.')
        #openAction.triggered.connect(self.selectDataFile)

        # Bottom save
        saveAction = QtWidgets.QAction(QtGui.QIcon('images/save.png'), 'Salvar', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Salvar os dados da curva de titulação.')
        # saveAction.triggered.connect(self.saveFile)

        # Adding elements
        self.addToolBar(toolbar)
        toolbar.addAction(exitAction)
        toolbar.addSeparator()
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)

    def mainMenuBar(self):
        """
        Meke the main menu bar.

        Returns
        -------
        None.

        """
        # Menu bar
        upperMenuBar = self.menuBar()

        # Menu file
        menuFile = upperMenuBar.addMenu("&Arquivo")
        menuFile.setStyleSheet("QMenu {icon-size: 32px;}")

        # File -> Open
        openAction = QtWidgets.QAction(QtGui.QIcon("images/open.png"), "&Abrir", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Abrir os dados de curva de titulação.")
        #openAction.triggered.connect(self.selectDataFile)
        menuFile.addAction(openAction)

        # File -> Save
        saveAction = QtWidgets.QAction(QtGui.QIcon("images/save.png"), "&Salvar", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Salvar os dados da curva de titulação.")
        menuFile.addAction(saveAction)

        # File -> Save as
        # save_asAction = QtWidgets.QAction(QtGui.QIcon("images/save_as.png"), "&Save as", self)
        # save_asAction.setStatusTip("Save as file.")
        # menuFile.addAction(save_asAction)

        # Separator
        menuFile.addSeparator()

        # Exit option (File -> Exit)
        exitAction = QtWidgets.QAction(QtGui.QIcon('images/exit.png'), '&Sair', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.setStatusTip('Sair.')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        menuFile.addAction(exitAction)

        # Menu About
        menuAbout = upperMenuBar.addMenu("&Sobre")

        # About -> Info
        infoAction = QtWidgets.QAction(QtGui.QIcon("images/info.png"), "&Informações", self)
        infoAction.setShortcut("Ctrl+i")
        infoAction.setStatusTip("Informações sobre o programa.")
        infoAction.triggered.connect(self.aboutWindow)
        menuAbout.addAction(infoAction)

    def aboutWindow(self):
        """
        Create a pop-up window with information about the interface.

        Returns
        -------
        None.

        """
        infoMessage = QtWidgets.QMessageBox()
        infoMessage.setWindowTitle("Sobre")
        infoMessage.setText("<b>Volumetria de Neutralização<b><br/>\
                      Application written in Python<br/><br/>\
                      Author: Rogério Ribeiro Macêdo<br/>\
                      Institution: Chemistry and Physics Institute, University Federal of Itajubá<br/><br/>\
                      This program results from the author taking a discipline named Quantita-<br/>\
                      tive Analytical Chemistry and the necessity of creating a titration<br>\
                      graph with all data and not with some single point like in classes.<br/><br/>\
                      Year: 2024 and 2025<br/> \
                      Last Modified data: June 25, 2024")
        infoMessage.setIcon(1)
        infoMessage.exec_()


def main(exist_style=True):
    """
    Principal function.

    Parameters
    ----------
    exist_style : Bool, optional
        Existence or not about file "styles.css". The default is True.

    Returns
    -------
    None.

    """
    # Create the QtApplication
    application = QtWidgets.QApplication(sys.argv)

    # Create and show the principal window
    mainWindow = MainWindow()

    if exist_style:
        application.setStyleSheet(Path("styles.qss").read_text())
    else:
        print("Arquivo 'styles.qss' não encontrado. Usando estilo padrão.")
        mainWindow.msgbox.showError(MSG_TITLE, "Arquivo 'styles.qss' não encontrado. Usando estilo padrão.")

    # Maximize window
    mainWindow.showMaximized()

    # Run the main Qt loop
    sys.exit(application.exec())


if __name__ == "__main__":
    if (Path('data/acids.csv').exists()) and (Path('data/bases.csv').exists()):
        main(Path('styles.qss').exists())
    else:
        print("Arquivo 'acids.csv' e 'bases.csv' não encontrados na pasta 'data'.")
