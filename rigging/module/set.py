# Compatible: Maya 2022+
from maya import cmds


def skinJointSet():
    """선택 메시의 스킨 조인트로 Set 생성"""
    mySel = cmds.ls(sl=True)
    for mySource in mySel:
        mySourceShape = cmds.listRelatives(mySource, s=True, f=True)[0]
        temp = cmds.listHistory(mySourceShape, lv=True)
        mySkinJNT = []
        for i in temp:
            if 'skinCluster' in i:
                mySkinJNT = cmds.skinCluster(i, query=True, inf=True)
        cmds.select(mySkinJNT, r=True)
        cmds.sets(n='skin_set_{}'.format(mySource))
        cmds.select(cl=True)


def exportJointSet(myExportName):
    """선택 메시와 스킨 조인트로 Export Set 생성"""
    mySel = cmds.ls(sl=True)
    myExportSel = []
    for mySource in mySel:
        myExportSel.append(mySource)
        mySourceShape = cmds.listRelatives(mySource, s=True, f=True)[0]
        temp = cmds.listHistory(mySourceShape, lv=0)
        mySkinJNT = []
        for i in temp:
            if 'skinCluster' in i:
                mySkinJNT = cmds.skinCluster(i, query=True, inf=True)
        cmds.select(mySkinJNT, r=True)
        for j in mySkinJNT:
            myExportSel.append(j)
        mySel2 = cmds.ls(sl=True)
        for i in mySel2:
            myList = cmds.listRelatives(ap=True, ad=True)
            cmds.select(myList, add=True)
        for i in cmds.ls(sl=True):
            myExportSel.append(i)
    # Face: neck_01 이하 모든 조인트 추가
    if myExportName == 'Face' and cmds.objExists('neck_01'):
        faceJNT = ['neck_01'] + (cmds.listRelatives('neck_01', ad=True, type='joint', f=False) or [])
        for jnt in faceJNT:
            if jnt not in myExportSel:
                myExportSel.append(jnt)
    # Body / FullBody: neck, head, IK, weapon, attach 본 추가
    if myExportName in ('Body', 'FullBody'):
        extra = ['neck_01', 'neck_02', 'head',
                 'ik_foot_root', 'ik_foot_l', 'ik_foot_r',
                 'ik_hand_root', 'ik_hand_l', 'ik_hand_r',
                 'weapon_l', 'weapon_r', 'attach']
        for jnt in extra:
            if cmds.objExists(jnt) and jnt not in myExportSel:
                myExportSel.append(jnt)

    cmds.select(myExportSel, r=True)
    cmds.sets(n='export_set_{}'.format(myExportName))
    cmds.select(cl=True)


def exportAniSet():
    """UE5 표준 본 리스트로 애니메이션 Export Set(export_ani) 생성"""
    myList = [
        'root', 'pelvis',
        'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05',
        'neck_01', 'neck_02', 'head',
        'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l',
        'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
        'thigh_l', 'calf_l', 'foot_l', 'ball_l',
        'thigh_r', 'calf_r', 'foot_r', 'ball_r',
        'thumb_01_l', 'thumb_02_l', 'thumb_03_l',
        'index_metacarpal_l', 'index_01_l', 'index_02_l', 'index_03_l',
        'middle_metacarpal_l', 'middle_01_l', 'middle_02_l', 'middle_03_l',
        'ring_metacarpal_l', 'ring_01_l', 'ring_02_l', 'ring_03_l',
        'pinky_metacarpal_l', 'pinky_01_l', 'pinky_02_l', 'pinky_03_l',
        'thumb_01_r', 'thumb_02_r', 'thumb_03_r',
        'index_metacarpal_r', 'index_01_r', 'index_02_r', 'index_03_r',
        'middle_metacarpal_r', 'middle_01_r', 'middle_02_r', 'middle_03_r',
        'ring_metacarpal_r', 'ring_01_r', 'ring_02_r', 'ring_03_r',
        'pinky_metacarpal_r', 'pinky_01_r', 'pinky_02_r', 'pinky_03_r',
    ]
    exists = [j for j in myList if cmds.objExists(j)]
    if not exists:
        cmds.warning('export_ani: 씬에 해당 본이 존재하지 않습니다.')
        return
    cmds.select(exists, r=True)
    cmds.sets(n='export_ani')
    cmds.select(cl=True)
