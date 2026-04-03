# Compatible: Maya 2022+
from maya import cmds


def skinTransferMultiToOne():
    """선택한 여러 소스 메시의 스킨을 마지막 선택 타겟에 전송"""
    mySource = []
    selected = cmds.ls(sl=True, l=True)[0:-1]
    for obj in selected:
        shapes = cmds.listRelatives(obj, shapes=True)
        if shapes:
            if cmds.nodeType(shapes[0]) == 'mesh':
                mySource.append(obj)

    myTarget = cmds.ls(sl=True, l=True)[-1]

    mySourceShapeList = []
    for i in mySource:
        mySourceShape = cmds.listRelatives(i, s=True, f=True)[0]
        mySourceShapeList.append(mySourceShape)

    mySkinJointList = []
    for mySourceShape in mySourceShapeList:
        temp = cmds.listHistory(mySourceShape, lv=True)
        for i in temp:
            if 'skinCluster' in i:
                mySkinJoint = cmds.skinCluster(i, query=True, inf=True)
                for j in mySkinJoint:
                    if j not in mySkinJointList:
                        mySkinJointList.append(j)

    cmds.select(myTarget, mySkinJointList, r=True)
    cmds.optionVar(iv=[
        ('bindTo', 2), ('bindMethod', 1), ('skinMethod', 1),
        ('normalizeWeights', 2), ('multipleBindPosesOpt', 1), ('maxInfl', 1),
        ('obeyMaxInfl', 0), ('removeUnusedInfluences', 0), ('colorizeSkeleton', 0)
    ])
    cmds.SmoothBindSkin()

    cmds.select(mySource, myTarget, r=True)
    cmds.copySkinWeights(
        noMirror=True,
        surfaceAssociation='closestPoint',
        influenceAssociation='oneToOne'
    )


def skinTransferOneToMulti():
    """첫 번째 선택 소스 메시의 스킨을 나머지 여러 타겟에 전송"""
    mySource = cmds.ls(sl=True, l=True)[0]
    myCount = len(cmds.ls(sl=True))
    myTarget = cmds.ls(sl=True, l=True)[1:myCount]

    mySourceShape = cmds.listRelatives(mySource, s=True, f=True)[0]

    mySkinJointList = []
    temp = cmds.listHistory(mySourceShape, lv=0)
    for i in temp:
        if 'skinCluster' in i:
            mySkinJoint = cmds.skinCluster(i, query=True, inf=True)
            for j in mySkinJoint:
                if j not in mySkinJointList:
                    mySkinJointList.append(j)

    for target in myTarget:
        cmds.select(target, mySkinJointList, r=True)
        cmds.optionVar(iv=[
            ('bindTo', 2), ('bindMethod', 1), ('skinMethod', 1),
            ('normalizeWeights', 2), ('multipleBindPosesOpt', 1), ('maxInfl', 1),
            ('obeyMaxInfl', 0), ('removeUnusedInfluences', 0), ('colorizeSkeleton', 0)
        ])
        cmds.SmoothBindSkin()

        cmds.select(mySource, target, r=True)
        cmds.copySkinWeights(
            noMirror=True,
            surfaceAssociation='closestPoint',
            influenceAssociation='oneToOne'
        )


def deleteZeroWeightJoint():
    """선택 메시의 스킨 클러스터에서 웨이트 0인 조인트 제거"""
    mySource = cmds.ls(sl=True, l=True)[0]
    mySourceShape = cmds.listRelatives(mySource, s=True, f=True)[0]

    temp = cmds.listHistory(mySourceShape, lv=True)
    for i in temp:
        if 'skinCluster' in i:
            cmds.skinCluster(i, e=True, rui=True)
            print(i)
