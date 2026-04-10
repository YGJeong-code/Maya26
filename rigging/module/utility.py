# Compatible: Maya 2022+
from maya import cmds


def addFootContactAttr():
    """foot_l, foot_r 본에 contact_l, contact_r 어트리뷰트 추가"""
    foot_attr = [('foot_l', 'contact_l'), ('foot_r', 'contact_r')]
    for bone, attr in foot_attr:
        if not cmds.objExists(bone):
            cmds.warning('{} 본이 존재하지 않습니다.'.format(bone))
            continue
        if cmds.attributeQuery(attr, node=bone, exists=True):
            cmds.warning('{}.{} 어트리뷰트가 이미 존재합니다.'.format(bone, attr))
            continue
        cmds.addAttr(bone, longName=attr, attributeType='float', min=0, max=1, defaultValue=0, keyable=True)
        print('{}.{} 어트리뷰트 추가 완료'.format(bone, attr))


def makeLocator():
    """선택 오브젝트 위치에 로케이터 생성"""
    mySel = cmds.ls(sl=True)
    for i in mySel:
        cmds.spaceLocator()
        cmds.rename(i + '_loc')
        myLoc = i + '_loc'
        cmds.matchTransform(myLoc, i)


def getMidpoint():
    """선택 버텍스들의 중점에 로케이터 생성"""
    sel_verts = cmds.ls(selection=True, flatten=True)
    if not sel_verts:
        cmds.error('버텍스를 먼저 선택하세요.')
        return

    positions = [cmds.xform(v, q=True, translation=True, worldSpace=True) for v in sel_verts]
    center = [sum(axis) / len(positions) for axis in zip(*positions)]

    locator = cmds.spaceLocator()[0]
    cmds.xform(locator, translation=center, worldSpace=True)


def deletePasted():
    """선택 오브젝트 이름의 pasted__ 접두사 제거"""
    mySel = cmds.ls(sl=True)
    for i in mySel:
        cmds.rename(i, i.replace('pasted__', ''))


OUTLINER_COLORS = {
    'red':     (1.0, 0.0, 0.0),
    'green':   (0.0, 1.0, 0.0),
    'blue':    (0.0, 0.0, 1.0),
    'yellow':  (1.0, 1.0, 0.0),
    'cyan':    (0.0, 1.0, 1.0),
    'magenta': (1.0, 0.0, 1.0),
    'orange':  (1.0, 0.65, 0.0),
    'gray':    (0.5, 0.5, 0.5),
    'white':   (1.0, 1.0, 1.0),
    'default': (0.7, 0.7, 0.7),
}


def setOutlinerColor(color_name):
    """선택 오브젝트의 아웃라이너 색상 설정"""
    if color_name not in OUTLINER_COLORS:
        cmds.warning('알 수 없는 색 이름: %s' % color_name)
        return

    r, g, b = OUTLINER_COLORS[color_name]
    nodes = cmds.ls(sl=True, long=True) or []
    if not nodes:
        cmds.warning('오브젝트를 선택하세요.')
        return

    for n in nodes:
        if cmds.objExists(n + '.useOutlinerColor') and cmds.objExists(n + '.outlinerColor'):
            try:
                cmds.setAttr(n + '.useOutlinerColor', True)
                cmds.setAttr(n + '.outlinerColor', r, g, b, type='double3')
            except Exception as e:
                cmds.warning('%s 처리 중 오류: %s' % (n, e))
