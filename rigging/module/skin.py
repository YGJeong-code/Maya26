# Compatible: Maya 2022+
"""
skin
Skin Transfer (Multi<->One), Zero Weight 조인트 제거,
Skin Weights 저장/불러오기 (조인트 목록 포함).
last updated 2026.07.13
by YeonGyun,Jeong
"""
import os
import json

from maya import cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


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


# =============================================================================
# Skin Weights 저장 / 불러오기 (조인트 목록 포함)
# -----------------------------------------------------------------------------
# 저장: 선택 메시의 스킨웨이트 + 인플루언스(조인트) 목록을 <현재 씬 폴더>/skinWeights/<메시>.json 으로 저장.
# 불러오기: 스킨 없는 메시를 선택하면 같은 이름의 .json 을 찾아, 저장된 조인트로 스킨클러스터를
#           바인드한 뒤 정점 인덱스 기준으로 웨이트를 복원한다. (같은 메시 = 정점 순서 동일 전제)
#           * 저장/불러오기 모두 "현재 열린 씬 파일 폴더" 기준이므로, 다른 파일에서 불러오려면
#             그 파일이 같은 폴더에 있거나 json 을 같은 폴더로 복사해야 한다.
# =============================================================================
FILE_VERSION = 1
_WEIGHT_EPS = 1.0e-6


def _skinDataDir():
    """스킨 데이터 폴더(<현재 씬 파일 폴더>/skinWeights). 없으면 생성.

    씬이 아직 저장되지 않아 폴더를 알 수 없으면
    프로젝트 data 폴더 -> 유저 앱 폴더 순으로 폴백하고 경고한다.
    """
    scene = cmds.file(query=True, sceneName=True) or ''
    if scene:
        base = os.path.dirname(scene)
    else:
        root = cmds.workspace(query=True, rootDirectory=True) or ''
        base = os.path.join(root, 'data') if root else cmds.internalVar(userAppDir=True)
        cmds.warning('[skin] 씬이 저장되지 않아 씬 폴더를 알 수 없음 → 폴백 경로 사용: %s' % base)

    path = os.path.join(base, 'skinWeights')
    if not os.path.isdir(path):
        os.makedirs(path)
    return path.replace('\\', '/')


def _shortName(node):
    """네임스페이스/경로를 제거한 짧은 이름 (파일명/조인트 매칭용)."""
    return node.split('|')[-1].split(':')[-1]


def _meshShape(mesh):
    """트랜스폼에서 비-인터미디어트 메시 셰이프 하나를 반환."""
    if cmds.nodeType(mesh) == 'mesh':
        return mesh
    shapes = cmds.listRelatives(mesh, s=True, f=True, ni=True) or []
    for s in shapes:
        if cmds.nodeType(s) == 'mesh':
            return s
    return None


def _findSkinCluster(shape):
    """셰이프 히스토리에서 skinCluster 노드를 찾아 반환."""
    for h in cmds.listHistory(shape) or []:
        if cmds.nodeType(h) == 'skinCluster':
            return h
    return None


def _mfnSkin(skinClusterName):
    sel = om.MSelectionList()
    sel.add(skinClusterName)
    return oma.MFnSkinCluster(sel.getDependNode(0))


def _shapeDagAndComponent(shape):
    """셰이프의 DagPath 와 '전체 정점' 컴포넌트, 정점 수를 반환."""
    sel = om.MSelectionList()
    sel.add(shape)
    dag = sel.getDagPath(0)
    numVerts = om.MFnMesh(dag).numVertices
    fnComp = om.MFnSingleIndexedComponent()
    comp = fnComp.create(om.MFn.kMeshVertComponent)
    fnComp.setCompleteData(numVerts)
    return dag, comp, numVerts


def saveSkinWeights(objs=None):
    """선택(또는 전달)한 메시들의 스킨웨이트 + 조인트 목록을 저장한다."""
    if objs is None:
        objs = cmds.ls(sl=True, l=True) or []
    if not objs:
        cmds.warning('[skin] 저장할 메시를 선택하세요.')
        return []

    out_dir = _skinDataDir()
    saved = []
    for obj in objs:
        shape = _meshShape(obj)
        if not shape:
            cmds.warning('[skin] 메시가 아님, 건너뜀: %s' % obj)
            continue

        sc = _findSkinCluster(shape)
        if not sc:
            cmds.warning('[skin] skinCluster 없음, 건너뜀: %s' % obj)
            continue

        fnSkin = _mfnSkin(sc)
        dag, comp, numVerts = _shapeDagAndComponent(shape)

        infPaths = fnSkin.influenceObjects()
        infNames = [_shortName(p.partialPathName()) for p in infPaths]
        numInf = len(infPaths)

        flatWeights, _cnt = fnSkin.getWeights(dag, comp)  # numVerts * numInf, influenceObjects 순서

        # 정점별 희소(0 아닌 것만) 저장: [[infIdx, w], ...]
        vtxWeights = []
        for v in range(numVerts):
            base = v * numInf
            pairs = []
            for ii in range(numInf):
                w = flatWeights[base + ii]
                if w > _WEIGHT_EPS:
                    pairs.append([ii, round(w, 6)])
            vtxWeights.append(pairs)

        data = {
            'version': FILE_VERSION,
            'object': _shortName(obj),
            'shape': _shortName(shape),
            'vertexCount': numVerts,
            'skinningMethod': cmds.getAttr(sc + '.skinningMethod'),
            'maxInfluences': cmds.skinCluster(sc, q=True, mi=True),
            'maintainMaxInfluences': cmds.getAttr(sc + '.maintainMaxInfluences'),
            'normalizeWeights': cmds.getAttr(sc + '.normalizeWeights'),
            'influences': infNames,
            'weights': vtxWeights,
        }

        file_path = os.path.join(out_dir, _shortName(obj) + '.json').replace('\\', '/')
        with open(file_path, 'w') as f:
            json.dump(data, f)
        saved.append(file_path)
        print('[skin] 저장: %s  (정점 %d, 조인트 %d) -> %s'
              % (_shortName(obj), numVerts, numInf, file_path))

    if saved:
        print('[skin] 스킨 저장 완료: %d개' % len(saved))
    return saved


def loadSkinWeights(objs=None):
    """선택(또는 전달)한 메시들에 대해 같은 이름의 .json 을 찾아 스킨을 복원한다.

    - 저장된 조인트로 skinCluster 바인드 후, 정점 인덱스 기준으로 웨이트 복원.
    - 조인트가 하나라도 씬에 없으면 경고 후 해당 메시는 건너뛴다.
    - 정점 수가 다르면 경고 후 건너뛴다.
    """
    if objs is None:
        objs = cmds.ls(sl=True, l=True) or []
    if not objs:
        cmds.warning('[skin] 불러올 메시를 선택하세요.')
        return []

    in_dir = _skinDataDir()
    loaded = []
    for obj in objs:
        shape = _meshShape(obj)
        if not shape:
            cmds.warning('[skin] 메시가 아님, 건너뜀: %s' % obj)
            continue

        file_path = os.path.join(in_dir, _shortName(obj) + '.json').replace('\\', '/')
        if not os.path.isfile(file_path):
            cmds.warning('[skin] 저장 파일 없음, 건너뜀: %s (%s)' % (_shortName(obj), file_path))
            continue

        with open(file_path, 'r') as f:
            data = json.load(f)

        savedInf = data['influences']
        numVerts = data['vertexCount']

        # 정점 수 확인
        curVerts = om.MFnMesh(_shapeDagAndComponent(shape)[0]).numVertices
        if curVerts != numVerts:
            cmds.warning('[skin] 정점 수 불일치(%d != %d), 건너뜀: %s'
                         % (curVerts, numVerts, _shortName(obj)))
            continue

        # 조인트 존재 확인 (짧은 이름 -> 실제 노드)
        resolved = {}
        missing = []
        for jn in savedInf:
            found = (cmds.ls(jn, type='joint', l=True)
                     or cmds.ls('*:' + jn, type='joint', l=True)  # 네임스페이스 폴백
                     or cmds.ls(jn, l=True)
                     or cmds.ls('*:' + jn, l=True))
            if found:
                resolved[jn] = found[0]
            else:
                missing.append(jn)
        if missing:
            cmds.warning('[skin] 조인트 %d개가 씬에 없어 중단: %s'
                         % (len(missing), ', '.join(missing[:20]) + (' ...' if len(missing) > 20 else '')))
            continue

        # 기존 skinCluster 있으면 제거 (스킨 없는 오브젝트 전제지만 방어)
        existing = _findSkinCluster(shape)
        if existing:
            cmds.warning('[skin] 이미 skinCluster 존재(%s), 건너뜀: %s' % (existing, _shortName(obj)))
            continue

        jointNodes = [resolved[jn] for jn in savedInf]

        sc = cmds.skinCluster(
            jointNodes, obj,
            toSelectedBones=True,
            bindMethod=0,
            skinMethod=data.get('skinningMethod', 0),
            normalizeWeights=1,
            maximumInfluences=data.get('maxInfluences', 8),
            obeyMaxInfluences=bool(data.get('maintainMaxInfluences', 0)),
            name=_shortName(obj) + '_skinCluster',
        )[0]

        fnSkin = _mfnSkin(sc)
        dag, comp, _n = _shapeDagAndComponent(shape)

        # 새 skinCluster 의 influence 순서/인덱스
        newPaths = fnSkin.influenceObjects()
        newNames = [_shortName(p.partialPathName()) for p in newPaths]
        numNewInf = len(newPaths)
        namePos = {nm: idx for idx, nm in enumerate(newNames)}

        infIndices = om.MIntArray()
        for p in newPaths:
            infIndices.append(int(fnSkin.indexForInfluenceObject(p)))

        # 저장 웨이트(희소, savedInf 순서)를 새 순서 flat 배열로 재구성
        newWeights = om.MDoubleArray(numVerts * numNewInf, 0.0)
        vtxWeights = data['weights']
        for v in range(numVerts):
            base = v * numNewInf
            for savedIdx, w in vtxWeights[v]:
                nm = savedInf[savedIdx]
                newWeights[base + namePos[nm]] = w

        # 저장된 값 그대로 적용 (normalize=False)
        cmds.setAttr(sc + '.normalizeWeights', 0)
        fnSkin.setWeights(dag, comp, infIndices, newWeights, False)
        cmds.setAttr(sc + '.normalizeWeights', data.get('normalizeWeights', 1))

        loaded.append(sc)
        print('[skin] 불러오기: %s  (정점 %d, 조인트 %d) <- %s'
              % (_shortName(obj), numVerts, numNewInf, file_path))

    if loaded:
        print('[skin] 스킨 불러오기 완료: %d개' % len(loaded))
    return loaded
