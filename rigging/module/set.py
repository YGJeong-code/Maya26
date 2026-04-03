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
    cmds.select(myExportSel, r=True)
    cmds.sets(n='export_set_{}'.format(myExportName))
    cmds.select(cl=True)
