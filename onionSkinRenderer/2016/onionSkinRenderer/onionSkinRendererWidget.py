# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Personal Work\2017\OnionSkinRenderer\onionSkinRenderer\onionSkinRendererWidget.ui'
#
# Created: Mon Feb 26 21:21:36 2018
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_onionSkinRenderer(object):
    def setupUi(self, onionSkinRenderer):
        onionSkinRenderer.setObjectName("onionSkinRenderer")
        onionSkinRenderer.resize(355, 474)
        self.onionSkinRenderer_mainLayout = QtGui.QWidget(onionSkinRenderer)
        self.onionSkinRenderer_mainLayout.setObjectName("onionSkinRenderer_mainLayout")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.onionSkinRenderer_mainLayout)
        self.verticalLayout_3.setContentsMargins(2, 0, 2, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.onionSkins_grp = QtGui.QGroupBox(self.onionSkinRenderer_mainLayout)
        self.onionSkins_grp.setTitle("")
        self.onionSkins_grp.setObjectName("onionSkins_grp")
        self.verticalLayout = QtGui.QVBoxLayout(self.onionSkins_grp)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.onionFrames_tab = QtGui.QTabWidget(self.onionSkins_grp)
        self.onionFrames_tab.setStyleSheet("")
        self.onionFrames_tab.setTabShape(QtGui.QTabWidget.Rounded)
        self.onionFrames_tab.setObjectName("onionFrames_tab")
        self.relative_tab = QtGui.QWidget()
        self.relative_tab.setObjectName("relative_tab")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.relative_tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.relative_frame = QtGui.QFrame(self.relative_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.relative_frame.sizePolicy().hasHeightForWidth())
        self.relative_frame.setSizePolicy(sizePolicy)
        self.relative_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.relative_frame.setMaximumSize(QtCore.QSize(100000, 16777215))
        self.relative_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.relative_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.relative_frame.setObjectName("relative_frame")
        self.relative_frame_layout = QtGui.QVBoxLayout(self.relative_frame)
        self.relative_frame_layout.setSpacing(3)
        self.relative_frame_layout.setContentsMargins(0, 4, 4, 4)
        self.relative_frame_layout.setObjectName("relative_frame_layout")
        self.horizontalLayout_3.addWidget(self.relative_frame)
        self.relative_settings_layout = QtGui.QVBoxLayout()
        self.relative_settings_layout.setObjectName("relative_settings_layout")
        self.relative_keyframes_chkbx = QtGui.QCheckBox(self.relative_tab)
        self.relative_keyframes_chkbx.setChecked(True)
        self.relative_keyframes_chkbx.setObjectName("relative_keyframes_chkbx")
        self.relative_settings_layout.addWidget(self.relative_keyframes_chkbx)
        self.relative_step_layout = QtGui.QHBoxLayout()
        self.relative_step_layout.setObjectName("relative_step_layout")
        self.relative_step_label = QtGui.QLabel(self.relative_tab)
        self.relative_step_label.setObjectName("relative_step_label")
        self.relative_step_layout.addWidget(self.relative_step_label)
        self.relative_step_spinBox = QtGui.QSpinBox(self.relative_tab)
        self.relative_step_spinBox.setMinimum(1)
        self.relative_step_spinBox.setObjectName("relative_step_spinBox")
        self.relative_step_layout.addWidget(self.relative_step_spinBox)
        self.relative_settings_layout.addLayout(self.relative_step_layout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.relative_settings_layout.addItem(spacerItem)
        self.relative_tint_strength_label = QtGui.QLabel(self.relative_tab)
        self.relative_tint_strength_label.setObjectName("relative_tint_strength_label")
        self.relative_settings_layout.addWidget(self.relative_tint_strength_label)
        self.relative_tint_strength_slider = QtGui.QSlider(self.relative_tab)
        self.relative_tint_strength_slider.setStyleSheet("QSlider{\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: 4px;\n"
"background: rgb(150, 150, 150);\n"
"}\n"
"QSlider::handle{\n"
"height: 8px;\n"
"background: rgb(50, 50, 50);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: -4px -4px;\n"
"}\n"
"QSlider::groove{\n"
"background: grey;\n"
"}\n"
"QSlider::sub-page{\n"
"background: rgb(75, 75, 75);\n"
"}\n"
"QSlider::add-page{\n"
"background: rgb(150, 150, 150);\n"
"}")
        self.relative_tint_strength_slider.setMaximum(100)
        self.relative_tint_strength_slider.setProperty("value", 100)
        self.relative_tint_strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.relative_tint_strength_slider.setObjectName("relative_tint_strength_slider")
        self.relative_settings_layout.addWidget(self.relative_tint_strength_slider)
        self.relative_tint_color_label = QtGui.QLabel(self.relative_tab)
        self.relative_tint_color_label.setObjectName("relative_tint_color_label")
        self.relative_settings_layout.addWidget(self.relative_tint_color_label)
        self.relative_futureTint_btn = QtGui.QPushButton(self.relative_tab)
        self.relative_futureTint_btn.setStyleSheet("background-color: rgb(20, 255, 114)")
        self.relative_futureTint_btn.setObjectName("relative_futureTint_btn")
        self.relative_settings_layout.addWidget(self.relative_futureTint_btn)
        self.relative_pastTint_btn = QtGui.QPushButton(self.relative_tab)
        self.relative_pastTint_btn.setStyleSheet("background-color:rgb(255, 26, 75)")
        self.relative_pastTint_btn.setObjectName("relative_pastTint_btn")
        self.relative_settings_layout.addWidget(self.relative_pastTint_btn)
        self.horizontalLayout_3.addLayout(self.relative_settings_layout)
        self.onionFrames_tab.addTab(self.relative_tab, "")
        self.absolute_tab = QtGui.QWidget()
        self.absolute_tab.setObjectName("absolute_tab")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.absolute_tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.absolute_frame = QtGui.QFrame(self.absolute_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.absolute_frame.sizePolicy().hasHeightForWidth())
        self.absolute_frame.setSizePolicy(sizePolicy)
        self.absolute_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.absolute_frame.setMaximumSize(QtCore.QSize(10000, 16777215))
        self.absolute_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.absolute_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.absolute_frame.setObjectName("absolute_frame")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.absolute_frame)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.absolute_list = QtGui.QListWidget(self.absolute_frame)
        self.absolute_list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.absolute_list.setObjectName("absolute_list")
        self.verticalLayout_2.addWidget(self.absolute_list)
        self.absolute_add_layout = QtGui.QHBoxLayout()
        self.absolute_add_layout.setObjectName("absolute_add_layout")
        self.absolute_add_spinBox = QtGui.QSpinBox(self.absolute_frame)
        self.absolute_add_spinBox.setMinimum(-100000)
        self.absolute_add_spinBox.setMaximum(100000)
        self.absolute_add_spinBox.setObjectName("absolute_add_spinBox")
        self.absolute_add_layout.addWidget(self.absolute_add_spinBox)
        self.absolute_add_btn = QtGui.QPushButton(self.absolute_frame)
        self.absolute_add_btn.setObjectName("absolute_add_btn")
        self.absolute_add_layout.addWidget(self.absolute_add_btn)
        self.absolute_addCrnt_btn = QtGui.QPushButton(self.absolute_frame)
        self.absolute_addCrnt_btn.setObjectName("absolute_addCrnt_btn")
        self.absolute_add_layout.addWidget(self.absolute_addCrnt_btn)
        self.absolute_clear_btn = QtGui.QPushButton(self.absolute_frame)
        self.absolute_clear_btn.setObjectName("absolute_clear_btn")
        self.absolute_add_layout.addWidget(self.absolute_clear_btn)
        self.verticalLayout_2.addLayout(self.absolute_add_layout)
        self.horizontalLayout_4.addWidget(self.absolute_frame)
        self.absolute_settings_layout = QtGui.QVBoxLayout()
        self.absolute_settings_layout.setObjectName("absolute_settings_layout")
        self.absolute_tint_strength_label = QtGui.QLabel(self.absolute_tab)
        self.absolute_tint_strength_label.setObjectName("absolute_tint_strength_label")
        self.absolute_settings_layout.addWidget(self.absolute_tint_strength_label)
        self.absolute_tint_strength_slider = QtGui.QSlider(self.absolute_tab)
        self.absolute_tint_strength_slider.setStyleSheet("QSlider{\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: 4px;\n"
"background: rgb(150, 150, 150);\n"
"}\n"
"QSlider::handle{\n"
"height: 8px;\n"
"background: rgb(50, 50, 50);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: -4px -4px;\n"
"}\n"
"QSlider::groove{\n"
"background: grey;\n"
"}\n"
"QSlider::sub-page{\n"
"background: rgb(75, 75, 75);\n"
"}\n"
"QSlider::add-page{\n"
"background: rgb(150, 150, 150);\n"
"}")
        self.absolute_tint_strength_slider.setMaximum(100)
        self.absolute_tint_strength_slider.setProperty("value", 100)
        self.absolute_tint_strength_slider.setOrientation(QtCore.Qt.Horizontal)
        self.absolute_tint_strength_slider.setObjectName("absolute_tint_strength_slider")
        self.absolute_settings_layout.addWidget(self.absolute_tint_strength_slider)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.absolute_settings_layout.addItem(spacerItem1)
        self.absolute_tint_label = QtGui.QLabel(self.absolute_tab)
        self.absolute_tint_label.setObjectName("absolute_tint_label")
        self.absolute_settings_layout.addWidget(self.absolute_tint_label)
        self.absolute_tint_btn = QtGui.QPushButton(self.absolute_tab)
        self.absolute_tint_btn.setStyleSheet("background:rgb(200, 200, 50)")
        self.absolute_tint_btn.setObjectName("absolute_tint_btn")
        self.absolute_settings_layout.addWidget(self.absolute_tint_btn)
        self.horizontalLayout_4.addLayout(self.absolute_settings_layout)
        self.onionFrames_tab.addTab(self.absolute_tab, "")
        self.verticalLayout.addWidget(self.onionFrames_tab)
        self.global_layout = QtGui.QHBoxLayout()
        self.global_layout.setSpacing(6)
        self.global_layout.setContentsMargins(10, -1, 10, 5)
        self.global_layout.setObjectName("global_layout")
        self.globalOpacity_label = QtGui.QLabel(self.onionSkins_grp)
        self.globalOpacity_label.setObjectName("globalOpacity_label")
        self.global_layout.addWidget(self.globalOpacity_label)
        self.globalOpacity_slider = QtGui.QSlider(self.onionSkins_grp)
        self.globalOpacity_slider.setStyleSheet("QSlider{\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: 4px;\n"
"background: rgb(150, 150, 150);\n"
"}\n"
"QSlider::handle{\n"
"height: 8px;\n"
"background: rgb(50, 50, 50);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"margin: -4px -4px;\n"
"}\n"
"QSlider::groove{\n"
"background: grey;\n"
"}\n"
"QSlider::sub-page{\n"
"background: rgb(75, 75, 75);\n"
"}\n"
"QSlider::add-page{\n"
"background: rgb(150, 150, 150);\n"
"}")
        self.globalOpacity_slider.setMaximum(100)
        self.globalOpacity_slider.setProperty("value", 99)
        self.globalOpacity_slider.setOrientation(QtCore.Qt.Horizontal)
        self.globalOpacity_slider.setObjectName("globalOpacity_slider")
        self.global_layout.addWidget(self.globalOpacity_slider)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.global_layout.addItem(spacerItem2)
        self.toggleRenderer_btn = QtGui.QPushButton(self.onionSkins_grp)
        self.toggleRenderer_btn.setObjectName("toggleRenderer_btn")
        self.global_layout.addWidget(self.toggleRenderer_btn)
        self.verticalLayout.addLayout(self.global_layout)
        self.verticalLayout_3.addWidget(self.onionSkins_grp)
        self.onionObjects_grp = QtGui.QGroupBox(self.onionSkinRenderer_mainLayout)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.onionObjects_grp.sizePolicy().hasHeightForWidth())
        self.onionObjects_grp.setSizePolicy(sizePolicy)
        self.onionObjects_grp.setObjectName("onionObjects_grp")
        self.horizontalLayout = QtGui.QHBoxLayout(self.onionObjects_grp)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.onionObjects_list = QtGui.QListWidget(self.onionObjects_grp)
        self.onionObjects_list.setBaseSize(QtCore.QSize(2, 1))
        self.onionObjects_list.setFrameShadow(QtGui.QFrame.Plain)
        self.onionObjects_list.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.onionObjects_list.setObjectName("onionObjects_list")
        self.horizontalLayout.addWidget(self.onionObjects_list)
        self.onionObjects_btn_layout = QtGui.QVBoxLayout()
        self.onionObjects_btn_layout.setObjectName("onionObjects_btn_layout")
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.onionObjects_btn_layout.addItem(spacerItem3)
        self.onionObjects_add_btn = QtGui.QPushButton(self.onionObjects_grp)
        self.onionObjects_add_btn.setObjectName("onionObjects_add_btn")
        self.onionObjects_btn_layout.addWidget(self.onionObjects_add_btn)
        self.onionObjects_remove_btn = QtGui.QPushButton(self.onionObjects_grp)
        self.onionObjects_remove_btn.setObjectName("onionObjects_remove_btn")
        self.onionObjects_btn_layout.addWidget(self.onionObjects_remove_btn)
        self.onionObjects_clear_btn = QtGui.QPushButton(self.onionObjects_grp)
        self.onionObjects_clear_btn.setObjectName("onionObjects_clear_btn")
        self.onionObjects_btn_layout.addWidget(self.onionObjects_clear_btn)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.onionObjects_btn_layout.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.onionObjects_btn_layout)
        self.verticalLayout_3.addWidget(self.onionObjects_grp)
        onionSkinRenderer.setCentralWidget(self.onionSkinRenderer_mainLayout)
        self.onionSkinRenderer_menubar = QtGui.QMenuBar(onionSkinRenderer)
        self.onionSkinRenderer_menubar.setGeometry(QtCore.QRect(0, 0, 355, 21))
        self.onionSkinRenderer_menubar.setObjectName("onionSkinRenderer_menubar")
        self.menubar_settings = QtGui.QMenu(self.onionSkinRenderer_menubar)
        self.menubar_settings.setObjectName("menubar_settings")
        onionSkinRenderer.setMenuBar(self.onionSkinRenderer_menubar)
        self.statusbar = QtGui.QStatusBar(onionSkinRenderer)
        self.statusbar.setObjectName("statusbar")
        onionSkinRenderer.setStatusBar(self.statusbar)
        self.settings_clearBuffer = QtGui.QAction(onionSkinRenderer)
        self.settings_clearBuffer.setCheckable(False)
        self.settings_clearBuffer.setObjectName("settings_clearBuffer")
        self.settings_autoClearBuffer = QtGui.QAction(onionSkinRenderer)
        self.settings_autoClearBuffer.setCheckable(True)
        self.settings_autoClearBuffer.setChecked(True)
        self.settings_autoClearBuffer.setObjectName("settings_autoClearBuffer")
        self.settings_preferences = QtGui.QAction(onionSkinRenderer)
        self.settings_preferences.setObjectName("settings_preferences")
        self.menubar_settings.addAction(self.settings_clearBuffer)
        self.menubar_settings.addAction(self.settings_autoClearBuffer)
        self.menubar_settings.addAction(self.settings_preferences)
        self.onionSkinRenderer_menubar.addAction(self.menubar_settings.menuAction())

        self.retranslateUi(onionSkinRenderer)
        self.onionFrames_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(onionSkinRenderer)

    def retranslateUi(self, onionSkinRenderer):
        onionSkinRenderer.setWindowTitle(QtGui.QApplication.translate("onionSkinRenderer", "OnionSkinRenderer", None, QtGui.QApplication.UnicodeUTF8))
        self.relative_keyframes_chkbx.setText(QtGui.QApplication.translate("onionSkinRenderer", "Keyframes", None, QtGui.QApplication.UnicodeUTF8))
        self.relative_step_label.setText(QtGui.QApplication.translate("onionSkinRenderer", "Relative Step", None, QtGui.QApplication.UnicodeUTF8))
        self.relative_tint_strength_label.setText(QtGui.QApplication.translate("onionSkinRenderer", "Tint Strength", None, QtGui.QApplication.UnicodeUTF8))
        self.relative_tint_color_label.setText(QtGui.QApplication.translate("onionSkinRenderer", "Tint Color", None, QtGui.QApplication.UnicodeUTF8))
        self.relative_futureTint_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Future", None, QtGui.QApplication.UnicodeUTF8))
        self.relative_pastTint_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Past", None, QtGui.QApplication.UnicodeUTF8))
        self.onionFrames_tab.setTabText(self.onionFrames_tab.indexOf(self.relative_tab), QtGui.QApplication.translate("onionSkinRenderer", "Relative", None, QtGui.QApplication.UnicodeUTF8))
        self.absolute_add_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.absolute_addCrnt_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Current", None, QtGui.QApplication.UnicodeUTF8))
        self.absolute_clear_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.absolute_tint_strength_label.setText(QtGui.QApplication.translate("onionSkinRenderer", "Tint Strength", None, QtGui.QApplication.UnicodeUTF8))
        self.absolute_tint_label.setText(QtGui.QApplication.translate("onionSkinRenderer", "Tint Color", None, QtGui.QApplication.UnicodeUTF8))
        self.absolute_tint_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Absolute", None, QtGui.QApplication.UnicodeUTF8))
        self.onionFrames_tab.setTabText(self.onionFrames_tab.indexOf(self.absolute_tab), QtGui.QApplication.translate("onionSkinRenderer", "Absolute", None, QtGui.QApplication.UnicodeUTF8))
        self.globalOpacity_label.setText(QtGui.QApplication.translate("onionSkinRenderer", "Global Opacity", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleRenderer_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Toggle Renderer", None, QtGui.QApplication.UnicodeUTF8))
        self.onionObjects_grp.setTitle(QtGui.QApplication.translate("onionSkinRenderer", "Onion Objects", None, QtGui.QApplication.UnicodeUTF8))
        self.onionObjects_add_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Add Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.onionObjects_remove_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Remove Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.onionObjects_clear_btn.setText(QtGui.QApplication.translate("onionSkinRenderer", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.menubar_settings.setTitle(QtGui.QApplication.translate("onionSkinRenderer", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_clearBuffer.setText(QtGui.QApplication.translate("onionSkinRenderer", "Clear Buffer", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_autoClearBuffer.setText(QtGui.QApplication.translate("onionSkinRenderer", "Auto Clear Buffer", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_preferences.setText(QtGui.QApplication.translate("onionSkinRenderer", "Preferences", None, QtGui.QApplication.UnicodeUTF8))

