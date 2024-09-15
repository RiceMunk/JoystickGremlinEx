# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_gremlin.ui'
#
# Created by: PySide6 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Gremlin(object):
    def setupUi(self, main_window):
        main_window.setObjectName("Gremlin")
        main_window.resize(800, 600)
        self.main = QtWidgets.QWidget(main_window)
        self.main.setObjectName("main")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.devices = QtWidgets.QTabWidget(self.main)
        self.devices.setObjectName("devices")

       
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.devices.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.devices.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.devices)
        
        main_window.setCentralWidget(self.main)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuRecent = QtWidgets.QMenu(self.menuFile)
        self.menuRecent.setObjectName("menuRecent")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(main_window)
        self.toolBar.setObjectName("toolBar")
        main_window.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionSave = QtGui.QAction(main_window)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setToolTip("Save a profile")
        self.actionOpen = QtGui.QAction(main_window)
        self.actionOpen.setToolTip("Open a profile")
        self.actionOpen.setObjectName("actionOpen")
        self.actionLoadProfile = QtGui.QAction(main_window)
        self.actionLoadProfile.setObjectName("actionLoadProfile")
        self.actionImportProfile = QtGui.QAction(main_window)
        self.actionImportProfile.setObjectName("actionImportProfile")
        self.actionActivate = QtGui.QAction(main_window)
        self.actionActivate.setCheckable(True)
        self.actionActivate.setObjectName("actionActivate")
        self.actionActivate.setToolTip("Activate Gremlin Ex")
        self.actionNewProfile = QtGui.QAction(main_window)
        self.actionNewProfile.setObjectName("actionNewProfile")
        self.actionSaveProfile = QtGui.QAction(main_window)
        self.actionSaveProfile.setObjectName("actionSaveProfile")
        self.actionSaveProfileAs = QtGui.QAction(main_window)
        self.actionSaveProfileAs.setObjectName("actionSaveProfileAs")
        self.actionRevealProfile = QtGui.QAction(main_window)
        self.actionRevealProfile.setObjectName("actionRevealProfile")
        self.actionOpenXmlProfile = QtGui.QAction(main_window)
        self.actionOpenXmlProfile.setObjectName("actionOpenXmlProfile")
        self.actionGenerate = QtGui.QAction(main_window)
        self.actionGenerate.setObjectName("actionGenerate")
        self.actionDeviceInformation = QtGui.QAction(main_window)
        self.actionDeviceInformation.setObjectName("actionDeviceInformation")
        self.actionAbout = QtGui.QAction(main_window)
        self.actionAbout.setObjectName("actionAbout")
        self.actionManageCustomModules = QtGui.QAction(main_window)
        self.actionManageCustomModules.setObjectName("actionManageCustomModules")
        self.actionInputRepeater = QtGui.QAction(main_window)
        self.actionInputRepeater.setCheckable(True)
        self.actionInputRepeater.setObjectName("actionInputRepeater")
        self.actionCalibration = QtGui.QAction(main_window)
        self.actionCalibration.setObjectName("actionCalibration")
        self.actionManageModes = QtGui.QAction(main_window)
        self.actionManageModes.setObjectName("actionManageModes")
        self.actionHTMLCheatsheet = QtGui.QAction(main_window)
        self.actionHTMLCheatsheet.setObjectName("actionHTMLCheatsheet")
        self.actionPDFCheatsheet = QtGui.QAction(main_window)
        self.actionPDFCheatsheet.setObjectName("actionPDFCheatsheet")
        self.actionViewInput = QtGui.QAction(main_window)
        self.actionViewInput.setObjectName("actionViewInput")
        self.actionExit = QtGui.QAction(main_window)
        self.actionExit.setObjectName("actionExit")
        self.actionOptions = QtGui.QAction(main_window)
        self.actionOptions.setObjectName("actionOptions")
        self.actionCreate1to1Mapping = QtGui.QAction(main_window)
        self.actionCreate1to1Mapping.setObjectName("actionCreate1to1Mapping")
        self.actionLogDisplay = QtGui.QAction(main_window)
        self.actionLogDisplay.setObjectName("actionLogDisplay")
        self.actionMergeAxis = QtGui.QAction(main_window)
        self.actionMergeAxis.setObjectName("actionMergeAxis")
        self.actionModifyProfile = QtGui.QAction(main_window)
        self.actionModifyProfile.setObjectName("actionModifyProfile")
        self.actionRecent = QtGui.QAction(main_window)
        self.actionRecent.setObjectName("actionRecent")
        self.actionEmpty = QtGui.QAction(main_window)
        self.actionEmpty.setObjectName("actionEmpty")
        self.actionSwapDevices = QtGui.QAction(main_window)
        self.actionSwapDevices.setObjectName("actionSwapDevices")
        self.actionInputViewer = QtGui.QAction(main_window)
        self.actionInputViewer.setObjectName("actionInputViewer")
        self.menuRecent.addAction(self.actionEmpty)
        self.menuFile.addAction(self.actionNewProfile)
        self.menuFile.addAction(self.actionLoadProfile)
        self.menuFile.addAction(self.menuRecent.menuAction())
        self.menuFile.addAction(self.actionSaveProfile)
        self.menuFile.addAction(self.actionSaveProfileAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImportProfile)
        self.menuFile.addAction(self.actionRevealProfile)
        self.menuFile.addAction(self.actionOpenXmlProfile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionModifyProfile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionManageModes)
        self.menuTools.addAction(self.actionInputRepeater)
        self.menuTools.addAction(self.actionDeviceInformation)
        self.menuTools.addAction(self.actionCalibration)
        self.menuTools.addAction(self.actionInputViewer)
        main_window.add_custom_tools_menu(self.menuTools)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionViewInput)
        self.menuTools.addAction(self.actionPDFCheatsheet)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionOptions)
        self.menuTools.addAction(self.actionLogDisplay)
        self.menu_Help.addAction(self.actionAbout)
        self.menuActions.addAction(self.actionCreate1to1Mapping)
        self.menuActions.addAction(self.actionMergeAxis)
        self.menuActions.addAction(self.actionSwapDevices)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionActivate)

        self.retranslateUi(main_window)
        self.devices.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, Gremlin):
        _translate = QtCore.QCoreApplication.translate
        Gremlin.setWindowTitle(_translate("GremlinEx", "Joystick Gremlin Ex"))
        self.devices.setTabText(self.devices.indexOf(self.tab), _translate("GremlinEx", "Tab 1"))
        self.devices.setTabText(self.devices.indexOf(self.tab_2), _translate("GremlinEx", "Tab 2"))
        self.menuFile.setTitle(_translate("GremlinEx", "&File"))
        self.menuRecent.setTitle(_translate("GremlinEx", "Recent"))
        self.menuTools.setTitle(_translate("GremlinEx", "&Tools"))
        self.menu_Help.setTitle(_translate("GremlinEx", "&Help"))
        self.menuActions.setTitle(_translate("GremlinEx", "&Actions"))
        self.toolBar.setWindowTitle(_translate("GremlinEx", "toolBar"))
        self.actionSave.setText(_translate("GremlinEx", "Save"))
        self.actionOpen.setText(_translate("GremlinEx", "Load"))
        self.actionLoadProfile.setText(_translate("GremlinEx", "&Open Profile..."))
        self.actionImportProfile.setText(_translate("GremlinEx", "&Import Profile..."))
        self.actionActivate.setText(_translate("GremlinEx", "Activate"))
        self.actionNewProfile.setText(_translate("GremlinEx", "&New Profile"))
        self.actionSaveProfile.setText(_translate("GremlinEx", "&Save Profile"))
        self.actionSaveProfileAs.setText(_translate("GremlinEx", "&Save Profile As"))
        self.actionRevealProfile.setText(_translate("GremlinEx", "&Reveal Profile in Explorer..."))
        self.actionOpenXmlProfile.setText(_translate("GremlinEx","&View Profile XML..."))
        self.actionGenerate.setText(_translate("GremlinEx", "Generate"))
        self.actionDeviceInformation.setText(_translate("GremlinEx", "Device Information"))
        self.actionAbout.setText(_translate("GremlinEx", "&About"))
        self.actionManageCustomModules.setText(_translate("GremlinEx", "&Manage Custom Modules"))
        self.actionInputRepeater.setText(_translate("GremlinEx", "Input Repeater"))
        self.actionCalibration.setText(_translate("GremlinEx", "&Calibration"))
        self.actionManageModes.setText(_translate("GremlinEx", "Manage Modes"))
        self.actionHTMLCheatsheet.setText(_translate("GremlinEx", "HTML Cheatsheet"))
        self.actionPDFCheatsheet.setText(_translate("GremlinEx", "PDF Cheatsheet"))
        self.actionViewInput.setText(_translate("GremlinEx","View Input Map"))
        self.actionExit.setText(_translate("GremlinEx", "E&xit"))
        self.actionOptions.setText(_translate("GremlinEx", "&Options"))
        self.actionCreate1to1Mapping.setText(_translate("GremlinEx", "Create 1:1 mapping"))
        self.actionLogDisplay.setText(_translate("GremlinEx", "&Log display"))
        self.actionMergeAxis.setText(_translate("GremlinEx", "&Merge Axis"))
        self.actionModifyProfile.setText(_translate("GremlinEx", "Modify Profile"))
        self.actionRecent.setText(_translate("GremlinEx", "&Recent"))
        self.actionEmpty.setText(_translate("GremlinEx", "Empty"))
        self.actionSwapDevices.setText(_translate("GremlinEx", "Swap Devices"))
        self.actionInputViewer.setText(_translate("GremlinEx", "Input Viewer"))

