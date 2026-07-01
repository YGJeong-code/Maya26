# Compatible: Maya 2022+
from maya import cmds


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


def _arm_moves(s):
    """팔 회전 이동 리스트 (s: 'L'/'R') — 어깨, 상박, 하박, 손목"""
    return [
        ('FKScapula_' + s,  'ry', -30),
        ('FKShoulder_' + s, 'ry', -80),
        ('FKShoulder_' + s, 'rz',  80),
        ('FKShoulder_' + s, 'rz', -80),
        ('FKElbow_' + s,    'rz',  70),
        ('FKWrist_' + s,    'ry',  60),
        ('FKWrist_' + s,    'ry', -60),
        ('FKWrist_' + s,    'rx', -80),
        ('FKWrist_' + s,    'rx',  80),
    ]


def _leg_moves(s):
    """다리 회전 이동 리스트 (s: 'L'/'R') — 허벅지, 종아리, 발목, 발가락"""
    return [
        ('FKHip_' + s,   'rz',  80),
        ('FKHip_' + s,   'rz', -80),
        ('FKHip_' + s,   'ry', -80),
        ('FKKnee_' + s,  'rz', -80),
        ('FKAnkle_' + s, 'rz', -65),
        ('FKAnkle_' + s, 'rz',  60),
        ('FKAnkle_' + s, 'rx',  60),
        ('FKAnkle_' + s, 'rx', -60),
        ('FKToes_' + s,  'rz',  50),
        ('FKToes_' + s,  'rz', -50),
    ]


def _skinAniMoves():
    """전체 (컨트롤러, 축, 값) 순서 리스트

    순서: 왼쪽 팔 -> 왼쪽 다리 -> 몸통(척추/목/머리) -> 오른쪽 팔 -> 오른쪽 다리.
    컨트롤러는 문자열 또는 (동시에 키할) 튜플. makeSkinAni/deleteSkinAni 공용.
    """
    SPINE = ('FKRoot_M', 'FKSpine1_M', 'FKChest_M')  # 척추 세 컨트롤러 동시 키
    body = [
        (SPINE,          'rz',  30),
        (SPINE,          'rz', -30),
        (SPINE,          'ry',  25),
        (SPINE,          'ry', -25),
        (SPINE,          'rx',  25),
        (SPINE,          'rx', -25),
        ('FKNeck_M',     'rz',  60),
        ('FKNeck_M',     'rz', -50),
        ('FKNeck_M',     'ry',  45),
        ('FKNeck_M',     'ry', -45),
        ('FKNeck_M',     'rx',  50),
        ('FKNeck_M',     'rx', -50),
        ('FKHead_M',     'rz',  35),
        ('FKHead_M',     'rz', -45),
        ('FKHead_M',     'ry',  40),
        ('FKHead_M',     'ry', -40),
        ('FKHead_M',     'rx',  50),
        ('FKHead_M',     'rx', -50),
    ]
    return (_arm_moves('L') + _leg_moves('L') + body
            + _arm_moves('R') + _leg_moves('R'))


def _skinAniControls():
    """makeSkinAni가 다루는 모든 컨트롤러 목록 (중복 제거, 순서 유지)"""
    ctrls = []
    for ctrl, axis, value in _skinAniMoves():
        for c in ((ctrl,) if isinstance(ctrl, str) else tuple(ctrl)):
            if c not in ctrls:
                ctrls.append(c)
    return ctrls


def makeSkinAni():
    """팔/다리/몸통/머리 FK 컨트롤러에 스킨 테스트용 회전 키 순차 생성

    순서: 왼쪽 팔 -> 왼쪽 다리 -> 몸통(척추/목/머리) -> 오른쪽 팔 -> 오른쪽 다리.
    각 회전은 0 -> 회전값(+2f) -> 0(+4f) 순으로 키를 찍고,
    다음 회전은 직전 회전이 끝난 프레임에서 이어진다.
    """
    # 다리는 FK로 구동되도록 FKIKBlend를 0으로
    for leg in ('FKIKLeg_L', 'FKIKLeg_R'):
        if cmds.objExists(leg):
            cmds.setAttr(leg + '.FKIKBlend', 0)
        else:
            cmds.warning('{} 컨트롤러가 존재하지 않습니다.'.format(leg))

    moves = _skinAniMoves()
    axes = ('rx', 'ry', 'rz')
    frame = 0
    for ctrl, axis, value in moves:
        ctrls = (ctrl,) if isinstance(ctrl, str) else tuple(ctrl)
        for c in ctrls:
            if not cmds.objExists(c):
                cmds.warning('{} 컨트롤러가 존재하지 않습니다.'.format(c))
                continue
            for a in axes:
                cmds.setKeyframe(c, attribute=a, value=0, time=frame)
                cmds.setKeyframe(c, attribute=a, value=(value if a == axis else 0), time=frame + 2)
                cmds.setKeyframe(c, attribute=a, value=0, time=frame + 4)
        frame += 4

    # 타임라인을 애니메이션 길이에 맞춤 (마지막 키 = frame)
    cmds.playbackOptions(min=0, max=frame, animationStartTime=0, animationEndTime=frame)
    cmds.currentTime(0)
    cmds.select(cl=True)


def deleteSkinAni():
    """makeSkinAni로 생성한 회전 키를 삭제하고 회전값을 0으로 초기화"""
    for c in _skinAniControls():
        if not cmds.objExists(c):
            continue
        for a in ('rx', 'ry', 'rz'):
            cmds.cutKey(c, attribute=a, clear=True)
            if cmds.getAttr(c + '.' + a, settable=True):
                cmds.setAttr(c + '.' + a, 0)

    # 타임라인을 0-30으로 초기화
    cmds.playbackOptions(min=0, max=30, animationStartTime=0, animationEndTime=30)
    cmds.currentTime(0)
    cmds.select(cl=True)


def makeMeshGroups():
    """mesh_grp(최상위) > face_mesh_grp / body_mesh_grp / fullbody_mesh_grp / outfit_mesh_grp 생성"""
    if not cmds.objExists('mesh_grp'):
        cmds.group(n='mesh_grp', em=True, world=True)
    for child in ('face_mesh_grp', 'body_mesh_grp', 'fullbody_mesh_grp', 'outfit_mesh_grp'):
        if not cmds.objExists(child):
            cmds.group(n=child, em=True, parent='mesh_grp')
    cmds.select(cl=True)


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
