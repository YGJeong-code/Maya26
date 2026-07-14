# Compatible: Maya 2022+
from maya import cmds


def makeRootJoint():
    """Root 조인트 생성 (X축 -90도)"""
    myJnt = cmds.joint(n='root')
    cmds.setAttr(myJnt + '.rx', -90)


def makeIKJoint():
    """발/손 IK 컨트롤 조인트 생성 및 계층 구성"""
    myList = ['ik_foot_root', 'ik_foot_l', 'ik_foot_r', 'ik_hand_root', 'ik_hand_l', 'ik_hand_r']

    # 이미 IK 조인트가 있으면 새로 만들지 않는다.
    existing = [i for i in myList if cmds.objExists(i)]
    if existing:
        cmds.warning('IK 조인트가 이미 존재합니다: {}'.format(', '.join(existing)))
        return

    cmds.select(cl=True)
    for i in myList:
        myJnt = cmds.joint(n=i)
        cmds.setAttr(myJnt + '.radius', 1)

    cmds.parent('ik_foot_root', 'root')
    cmds.parent('ik_foot_l', 'ik_foot_root')
    cmds.parent('ik_foot_r', 'ik_foot_root')
    cmds.parent('ik_hand_root', 'root')
    cmds.parent('ik_hand_l', 'ik_hand_root')
    cmds.parent('ik_hand_r', 'ik_hand_root')

    cmds.parentConstraint('foot_l', 'ik_foot_l', mo=False)
    cmds.parentConstraint('foot_r', 'ik_foot_r', mo=False)
    cmds.parentConstraint('hand_l', 'ik_hand_l', mo=False)
    cmds.parentConstraint('hand_r', 'ik_hand_r', mo=False)


def makeWeaponJoint():
    """hand_l, hand_r 자식으로 weapon 조인트 생성"""
    cmds.select(cl=True)
    weapon_map = [('hand_l', 'weapon_l'), ('hand_r', 'weapon_r')]
    for hand, weapon in weapon_map:
        if cmds.objExists(weapon):
            cmds.warning('{} 조인트가 이미 존재합니다.'.format(weapon))
            continue
        if not cmds.objExists(hand):
            cmds.warning('{} 조인트가 존재하지 않습니다.'.format(hand))
            continue
        myJnt = cmds.joint(n=weapon)
        cmds.matchTransform(myJnt, hand)
        cmds.parent(myJnt, hand)
        cmds.select(cl=True)


def makeAttachJoint():
    """root 자식으로 attach 조인트 생성 (root와 동일한 트랜스폼)"""
    if not cmds.objExists('root'):
        cmds.warning('root 조인트가 존재하지 않습니다.')
        return
    cmds.select(cl=True)
    myJnt = cmds.joint(n='attach')
    cmds.matchTransform(myJnt, 'root')
    cmds.parent(myJnt, 'root')
    cmds.select(cl=True)


def makeJointToSel():
    """선택한 오브젝트 또는 버텍스 위치에 조인트 생성"""
    mySel = cmds.ls(sl=True, flatten=True)
    cmds.select(cl=True)

    for i in mySel:
        if '.vtx[' in i:
            pos = cmds.xform(i, q=True, translation=True, worldSpace=True)
            myJnt = cmds.joint()
            cmds.xform(myJnt, translation=pos, worldSpace=True)
        else:
            myJnt = cmds.joint()
            cmds.matchTransform(myJnt, i)

        cmds.setAttr(myJnt + '.sx', 1)
        cmds.setAttr(myJnt + '.sy', 1)
        cmds.setAttr(myJnt + '.sz', 1)
        cmds.select(cl=True)
