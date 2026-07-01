# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Maya Python 스크립트 툴 모음. 리깅 중심으로 구성되며 추후 파이프라인 툴이 추가될 예정이다.

## Maya 스크립트 실행

Maya 내부 Script Editor 또는 셸프 버튼에서 실행한다.

```python
# UI 실행 (셸프 버튼)
import sys
_PATH = 'd:/YGJeong/MayaScripts'
if _PATH not in sys.path:
    sys.path.insert(0, _PATH)

import rigging.ui.YG_rigging_ui as ui
import importlib
importlib.reload(ui)
ui.show()
```

## Maya 환경 설정

`userSetup.py`가 Maya 시작 시 자동으로 스크립트 경로를 추가한다.
위치: `C:/Users/yg_jeong/Documents/maya/2025/scripts/userSetup.py`

## 폴더 구조

```
MayaScripts/
├── rigging/
│   ├── ui/
│   │   └── YG_rigging_ui.py     # 메인 UI (workspaceControl 기반, 도킹 지원)
│   ├── module/
│   │   ├── skin.py              # Skin Transfer (Multi↔One), Zero Weight 조인트 제거
│   │   ├── joint.py             # Root/IK/Weapon/Attach/위치 기반 조인트 생성
│   │   ├── set.py               # Skin Set, Export Set(Body/Face/FullBody/Hair), Ani Set(export_ani)
│   │   ├── naming.py            # Rename, Prefix/Suffix, Search/Replace
│   │   └── utility.py           # Locator, Midpoint, Delete Pasted, Mesh Groups, Skin Ani(검수 모션), Outliner Color
│   ├── icon/
│   │   └── YG_Tools.png
│   └── shelf_YG_rigging.py      # 셸프 버튼 설치 스크립트
│
├── pipeline/                    # 추후 추가 예정
└── utils/                       # rigging/pipeline 공통 함수
```

## 코드 작성 규칙

- Python 스크립트: `.py`
- Maya API: `maya.cmds` (일반) / `OpenMaya 2.0` (고성능)
- UI: PySide6 (우선) / PySide2 (fallback), `workspaceControl` 기반으로 도킹 지원
- 스크립트 최상단에 Maya 버전 호환 범위 명시
- 파일 수정 시 docstring의 `last updated` 날짜를 당일로 갱신

```python
# Compatible: Maya 2022+
import maya.cmds as cmds
```

## rigging 모듈 구조

각 기능은 `rigging/module/` 하위의 독립 파일로 분리되어 있다.
UI(`YG_rigging_ui.py`)에서 각 모듈을 개별 import하여 사용한다.

```python
import rigging.module.skin    as skin
import rigging.module.joint   as joint
import rigging.module.set     as set_
import rigging.module.naming  as naming
import rigging.module.utility as utility
```

## UI 카테고리

| 카테고리 | 기능 |
|----------|------|
| Window | Dock / UnDock (Maya 좌측 도킹) |
| Skin Transfer | Multi → One, One → Multi, Delete Zero Weight Joint |
| Skin Ani | Make Skin Ani (FK 컨트롤러 검수용 회전 키), Delete Skin Ani |
| Set | Edit Set, Set - Skin, Set - Export (Body/Face/FullBody/Hair), Set - Ani (export_ani, UE5 표준 본) |
| Joint | Make Root Joint, Make IK Joint, Make Weapon Joint, Make Attach Joint, Make Joint To Sel |
| Utility | Make Locator, Get Midpoint, Delete Pasted, Make Mesh Groups, Outliner Color (10색) |
| Naming | Rename (A/B/C/D + Side), Add Prefix, Add Suffix, Search/Replace |

## 스켈레톤 규약 (UE5 파이프라인)

여러 기능이 **UE5 표준 본 이름을 코드에 직접 참조**한다 — 이 프로젝트는 UE5 캐릭터 익스포트를 겨냥한다.

- Joint: `root`, `ik_foot_root`/`ik_foot_l`/`ik_foot_r`, `ik_hand_root`/`ik_hand_l`/`ik_hand_r`, `weapon_l`/`weapon_r`, `attach`. IK Bone 은 `foot_l`/`foot_r`/`hand_l`/`hand_r` 에 parentConstraint.
- `set.py` `exportAniSet()` 의 `export_ani` 본 리스트: `root`, `pelvis`, `spine_01~05`, `neck_01~02`, `head`, `clavicle/upperarm/lowerarm/hand`, `thigh/calf/foot/ball`, 손가락 `*_metacarpal`/`*_01~03` (l/r). 씬에 존재하는 본만 셋에 포함.
- Export Set: Face=`neck_01` 이하 전체, Body/FullBody=neck·head·IK·weapon·attach 추가.
- Skin Ani: FK 컨트롤러 이름 규약 사용 (`FKRoot_M`/`FKSpine1_M`/`FKChest_M`, `FKShoulder_L` 등, `FKIKLeg_L/R.FKIKBlend`).

## GitHub

Repository: https://github.com/YGJeong-code/Maya26
