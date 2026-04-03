"""
Maya Shelf Button Installer — YG_Rigging UI
Script Editor에서 한 번 실행하면 현재 셸프에 아이콘 버튼이 등록됩니다.
"""
import sys
import maya.cmds as cmds
import maya.mel as mel

_PATH = 'd:/YGJeong/MayaScripts'
if _PATH not in sys.path:
    sys.path.insert(0, _PATH)

_ICON = 'd:/YGJeong/MayaScripts/rigging/icon/YG_Tools.png'

_COMMAND = """
import sys
_PATH = 'd:/YGJeong/MayaScripts'
if _PATH not in sys.path:
    sys.path.insert(0, _PATH)

import rigging.ui.YG_rigging_ui as ui
import importlib
importlib.reload(ui)
ui.show()
"""

_current_shelf = cmds.tabLayout(
    mel.eval('$_tmp = $gShelfTopLevel'), q=True, selectTab=True
)

cmds.shelfButton(
    parent=_current_shelf,
    label='YG_Rigging',
    annotation='YG Rigging UI (Skin / Set / Joint / Utility / Naming)',
    image1=_ICON,
    command=_COMMAND,
    sourceType='python',
)

print('YG_Rigging shelf button added to: {}'.format(_current_shelf))
