# Compatible: Maya 2022+
"""
YG_rigging_ui
Skin / Set / Joint / Utility / Naming UI
since 2026.04.02
last updated 2026.04.10
by YeonGyun,Jeong
"""

try:
    from PySide6 import QtWidgets, QtCore
except ImportError:
    from PySide2 import QtWidgets, QtCore

from maya import cmds, mel
import maya.OpenMayaUI as omui

try:
    from shiboken6 import wrapInstance
except ImportError:
    from shiboken2 import wrapInstance

from imp import reload
import rigging.module.skin    as skin
import rigging.module.joint   as joint
import rigging.module.set     as set_
import rigging.module.naming  as naming
import rigging.module.utility as utility
reload(skin); reload(joint); reload(set_); reload(naming); reload(utility)


class YG_RiggingWindow(QtWidgets.QWidget):
    TOOL_NAME = 'YG_Rigging'

    def __init__(self, parent=None):
        super(YG_RiggingWindow, self).__init__(parent=parent)
        self.setObjectName(self.__class__.TOOL_NAME)

        self.create_window_layout()
        self.create_skin_layout()
        self.create_set_layout()
        self.create_joint_layout()
        self.create_utility_layout()
        self.create_naming_layout()
        self.create_main_layout()
        self.create_connections()

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    def create_window_layout(self):
        self.dock_btn   = QtWidgets.QPushButton('Dock')
        self.undock_btn = QtWidgets.QPushButton('UnDock')

        self.window_group = QtWidgets.QGroupBox(title='Window')
        window_layout = QtWidgets.QHBoxLayout()
        window_layout.addWidget(self.dock_btn)
        window_layout.addWidget(self.undock_btn)
        self.window_group.setLayout(window_layout)

    def create_skin_layout(self):
        self.skinTransferMultiToOne_btn = QtWidgets.QPushButton('Multi → One')
        self.skinTransferOneToMulti_btn = QtWidgets.QPushButton('One → Multi')
        self.deleteZeroWeight_btn       = QtWidgets.QPushButton('Delete Zero Weight Joint')

        self.skin_group = QtWidgets.QGroupBox(title='Skin Transfer')
        skin_layout = QtWidgets.QVBoxLayout()
        skin_layout.addWidget(self.skinTransferMultiToOne_btn)
        skin_layout.addWidget(self.skinTransferOneToMulti_btn)
        skin_layout.addWidget(self.deleteZeroWeight_btn)
        self.skin_group.setLayout(skin_layout)

    def create_set_layout(self):
        self.editSet_btn   = QtWidgets.QPushButton('Edit Set')
        self.skinSet_btn   = QtWidgets.QPushButton('Set - Skin')
        self.exportSet_btn = QtWidgets.QPushButton('Set - Export')

        self.rbtn_body = QtWidgets.QRadioButton('Body')
        self.rbtn_face = QtWidgets.QRadioButton('Face')
        self.rbtn_hair = QtWidgets.QRadioButton('Hair')
        self.rbtn_body.setChecked(True)

        radio_layout = QtWidgets.QHBoxLayout()
        for btn in (self.rbtn_body, self.rbtn_face, self.rbtn_hair):
            radio_layout.addWidget(btn)

        self.set_group = QtWidgets.QGroupBox(title='Set')
        set_layout = QtWidgets.QVBoxLayout()
        set_layout.addWidget(self.editSet_btn)
        set_layout.addWidget(self.skinSet_btn)
        set_layout.addLayout(radio_layout)
        set_layout.addWidget(self.exportSet_btn)
        self.set_group.setLayout(set_layout)

    def create_joint_layout(self):
        self.makeRootJoint_btn  = QtWidgets.QPushButton('Make Root Joint')
        self.makeIKJoint_btn    = QtWidgets.QPushButton('Make IK Joint')
        self.makeJointToSel_btn = QtWidgets.QPushButton('Make Joint To Sel')

        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.makeRootJoint_btn)
        top_layout.addWidget(self.makeIKJoint_btn)

        self.joint_group = QtWidgets.QGroupBox(title='Joint')
        joint_layout = QtWidgets.QVBoxLayout()
        joint_layout.addLayout(top_layout)
        joint_layout.addWidget(self.makeJointToSel_btn)
        self.joint_group.setLayout(joint_layout)

    def create_utility_layout(self):
        self.makeLocator_btn      = QtWidgets.QPushButton('Make Locator')
        self.getMidpoint_btn      = QtWidgets.QPushButton('Get Midpoint')
        self.deletePasted_btn     = QtWidgets.QPushButton('Delete Pasted')
        self.footContactAttr_btn  = QtWidgets.QPushButton('Add Foot Contact Attr')

        self.outlinerColor_btns = {}
        color_items = list(utility.OUTLINER_COLORS.items())
        mid = len(color_items) // 2
        row1_layout = QtWidgets.QHBoxLayout()
        row2_layout = QtWidgets.QHBoxLayout()
        row1_layout.setSpacing(3)
        row2_layout.setSpacing(3)

        for i, (name, (r, g, b)) in enumerate(color_items):
            ri, gi, bi = int(r * 255), int(g * 255), int(b * 255)
            btn = QtWidgets.QPushButton(name)
            btn.setStyleSheet(
                'QPushButton {{ color: rgb({r},{g},{b}); background-color: #2b2b2b; border: 1px solid #555; }}'
                'QPushButton:hover {{ background-color: #3e3e3e; }}'
                'QPushButton:pressed {{ background-color: #1a1a1a; }}'.format(r=ri, g=gi, b=bi)
            )
            btn.clicked.connect(lambda checked=False, n=name: utility.setOutlinerColor(n))
            self.outlinerColor_btns[name] = btn
            if i < mid:
                row1_layout.addWidget(btn)
            else:
                row2_layout.addWidget(btn)

        color_btn_layout = QtWidgets.QVBoxLayout()
        color_btn_layout.setSpacing(3)
        color_btn_layout.addLayout(row1_layout)
        color_btn_layout.addLayout(row2_layout)

        locator_layout = QtWidgets.QHBoxLayout()
        locator_layout.addWidget(self.makeLocator_btn)
        locator_layout.addWidget(self.getMidpoint_btn)

        self.utility_group = QtWidgets.QGroupBox(title='Utility')
        utility_layout = QtWidgets.QVBoxLayout()
        utility_layout.addLayout(locator_layout)
        utility_layout.addWidget(self.deletePasted_btn)
        utility_layout.addWidget(self.footContactAttr_btn)
        utility_layout.addLayout(color_btn_layout)
        self.utility_group.setLayout(utility_layout)

    def create_naming_layout(self):
        self.nameA_le = QtWidgets.QLineEdit(); self.nameA_le.setPlaceholderText('A')
        self.nameB_le = QtWidgets.QLineEdit(); self.nameB_le.setPlaceholderText('B')
        self.nameC_le = QtWidgets.QLineEdit(); self.nameC_le.setPlaceholderText('C')
        self.nameD_le = QtWidgets.QLineEdit(); self.nameD_le.setPlaceholderText('D')

        self.sideL_btn    = QtWidgets.QRadioButton('L')
        self.sideR_btn    = QtWidgets.QRadioButton('R')
        self.sideC_btn    = QtWidgets.QRadioButton('C')
        self.sideNone_btn = QtWidgets.QRadioButton('None')
        self.sideNone_btn.setChecked(True)

        self.rename_btn = QtWidgets.QPushButton('Rename')

        self.prefix_le     = QtWidgets.QLineEdit(); self.prefix_le.setPlaceholderText('Prefix')
        self.addPrefix_btn = QtWidgets.QPushButton('Add Prefix')
        self.suffix_le     = QtWidgets.QLineEdit(); self.suffix_le.setPlaceholderText('Suffix')
        self.addSuffix_btn = QtWidgets.QPushButton('Add Suffix')

        self.search_le         = QtWidgets.QLineEdit(); self.search_le.setPlaceholderText('Search')
        self.replace_le        = QtWidgets.QLineEdit(); self.replace_le.setPlaceholderText('Replace')
        self.searchReplace_btn = QtWidgets.QPushButton('Replace')

        nameParts_layout = QtWidgets.QHBoxLayout()
        for w in (self.nameA_le, self.nameB_le, self.nameC_le, self.nameD_le):
            nameParts_layout.addWidget(w)

        side_layout = QtWidgets.QHBoxLayout()
        side_layout.addWidget(QtWidgets.QLabel('Side:'))
        for btn in (self.sideNone_btn, self.sideL_btn, self.sideR_btn, self.sideC_btn):
            side_layout.addWidget(btn)
        side_layout.addStretch()

        prefix_layout = QtWidgets.QHBoxLayout()
        prefix_layout.addWidget(self.prefix_le)
        prefix_layout.addWidget(self.addPrefix_btn)

        suffix_layout = QtWidgets.QHBoxLayout()
        suffix_layout.addWidget(self.suffix_le)
        suffix_layout.addWidget(self.addSuffix_btn)

        searchReplace_layout = QtWidgets.QHBoxLayout()
        searchReplace_layout.addWidget(self.search_le)
        searchReplace_layout.addWidget(self.replace_le)
        searchReplace_layout.addWidget(self.searchReplace_btn)

        self.naming_group = QtWidgets.QGroupBox(title='Naming')
        naming_layout = QtWidgets.QVBoxLayout()
        naming_layout.addLayout(nameParts_layout)
        naming_layout.addLayout(side_layout)
        naming_layout.addWidget(self.rename_btn)
        naming_layout.addLayout(prefix_layout)
        naming_layout.addLayout(suffix_layout)
        naming_layout.addLayout(searchReplace_layout)
        self.naming_group.setLayout(naming_layout)

    def create_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.window_group)
        self.main_layout.addWidget(self.skin_group)
        self.main_layout.addWidget(self.set_group)
        self.main_layout.addWidget(self.joint_group)
        self.main_layout.addWidget(self.utility_group)
        self.main_layout.addWidget(self.naming_group)
        self.main_layout.addStretch()

    # -------------------------------------------------------------------------
    # Connections
    # -------------------------------------------------------------------------
    def create_connections(self):
        # Window
        self.dock_btn.clicked.connect(dock)
        self.undock_btn.clicked.connect(undock)
        # Skin Transfer
        self.skinTransferMultiToOne_btn.clicked.connect(self.on_button_pressed)
        self.skinTransferOneToMulti_btn.clicked.connect(self.on_button_pressed)
        self.deleteZeroWeight_btn.clicked.connect(self.on_button_pressed)
        # Set
        self.editSet_btn.clicked.connect(self.on_button_pressed)
        self.skinSet_btn.clicked.connect(self.on_button_pressed)
        self.exportSet_btn.clicked.connect(self.on_button_pressed)
        # Joint
        self.makeRootJoint_btn.clicked.connect(self.on_button_pressed)
        self.makeIKJoint_btn.clicked.connect(self.on_button_pressed)
        self.makeJointToSel_btn.clicked.connect(self.on_button_pressed)
        # Utility
        self.makeLocator_btn.clicked.connect(self.on_button_pressed)
        self.getMidpoint_btn.clicked.connect(self.on_button_pressed)
        self.deletePasted_btn.clicked.connect(self.on_button_pressed)
        self.footContactAttr_btn.clicked.connect(self.on_button_pressed)
        # Naming
        self.rename_btn.clicked.connect(self.on_naming_pressed)
        self.addPrefix_btn.clicked.connect(self.on_naming_pressed)
        self.addSuffix_btn.clicked.connect(self.on_naming_pressed)
        self.searchReplace_btn.clicked.connect(self.on_naming_pressed)

    # -------------------------------------------------------------------------
    # Slots
    # -------------------------------------------------------------------------
    def on_button_pressed(self):
        sender = self.sender()

        # Skin Transfer
        if sender == self.skinTransferMultiToOne_btn:
            skin.skinTransferMultiToOne()
        elif sender == self.skinTransferOneToMulti_btn:
            skin.skinTransferOneToMulti()
        elif sender == self.deleteZeroWeight_btn:
            skin.deleteZeroWeightJoint()

        # Set
        elif sender == self.editSet_btn:
            mel.eval('SetEditor')
        elif sender == self.skinSet_btn:
            set_.skinJointSet()
        elif sender == self.exportSet_btn:
            part_map = {
                self.rbtn_body: ('Body', set_.exportJointSet),
                self.rbtn_face: ('Face', set_.exportJointSet),
                self.rbtn_hair: ('Hair', set_.exportJointSet),
            }
            for rbtn, (name, fn) in part_map.items():
                if rbtn.isChecked():
                    fn(name)
                    break

        # Joint
        elif sender == self.makeRootJoint_btn:
            joint.makeRootJoint()
        elif sender == self.makeIKJoint_btn:
            joint.makeIKJoint()
        elif sender == self.makeJointToSel_btn:
            joint.makeJointToSel()

        # Utility
        elif sender == self.makeLocator_btn:
            utility.makeLocator()
        elif sender == self.getMidpoint_btn:
            utility.getMidpoint()
        elif sender == self.deletePasted_btn:
            utility.deletePasted()
        elif sender == self.footContactAttr_btn:
            utility.addFootContactAttr()

    def on_naming_pressed(self):
        sender = self.sender()

        if sender == self.rename_btn:
            side = ''
            if self.sideL_btn.isChecked():   side = 'l'
            elif self.sideR_btn.isChecked(): side = 'r'
            elif self.sideC_btn.isChecked(): side = 'c'
            naming.renameObj(
                myA=self.nameA_le.text(), myB=self.nameB_le.text(),
                myC=self.nameC_le.text(), myD=self.nameD_le.text(),
                mySide=side
            )
        elif sender == self.addPrefix_btn:
            naming.renameObj(prefix=self.prefix_le.text())
        elif sender == self.addSuffix_btn:
            naming.renameObj(subfix=self.suffix_le.text())
        elif sender == self.searchReplace_btn:
            naming.renameObj(search=self.search_le.text(), replace=self.replace_le.text())


# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
WORKSPACE_CONTROL_NAME = 'YG_RiggingWorkspaceControl'


def show():
    if cmds.workspaceControl(WORKSPACE_CONTROL_NAME, q=True, exists=True):
        cmds.deleteUI(WORKSPACE_CONTROL_NAME)

    cmds.workspaceControl(
        WORKSPACE_CONTROL_NAME,
        label='YG_Rigging',
        floating=True,
        uiScript='import rigging.ui.YG_rigging_ui as ui; ui._fill_workspace()',
    )


def dock():
    if cmds.workspaceControl(WORKSPACE_CONTROL_NAME, q=True, exists=True):
        cmds.workspaceControl(
            WORKSPACE_CONTROL_NAME,
            e=True,
            floating=False,
            dockToMainWindow=('left', 1),
        )


def undock():
    if cmds.workspaceControl(WORKSPACE_CONTROL_NAME, q=True, exists=True):
        cmds.workspaceControl(
            WORKSPACE_CONTROL_NAME,
            e=True,
            floating=True,
        )


def _fill_workspace():
    ctrl_ptr = omui.MQtUtil.findControl(WORKSPACE_CONTROL_NAME)
    workspace_widget = wrapInstance(int(ctrl_ptr), QtWidgets.QWidget)

    global my_win
    my_win = YG_RiggingWindow(parent=workspace_widget)

    layout = workspace_widget.layout()
    if layout is None:
        layout = QtWidgets.QVBoxLayout(workspace_widget)
        layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(my_win)
