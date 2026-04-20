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
│   │   ├── skin.py              # Skin Transfer (Multi↔One), Zero Weight 제거
│   │   ├── joint.py             # Root/IK/Weapon/위치 기반 조인트 생성
│   │   ├── set.py               # Skin Set, Export Set 생성 (FullBody: IK+Weapon 포함)
│   │   ├── naming.py            # Rename, Prefix/Suffix, Search/Replace
│   │   └── utility.py           # Locator, Midpoint, Outliner Color, Foot Contact Attr
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
| Set | Edit Set, Set - Skin, Set - Export (Body/Face/FullBody/Hair) |
| Joint | Make Root Joint, Make IK Joint, Make Weapon Joint, Make Joint To Sel |
| Utility | Make Locator, Get Midpoint, Delete Pasted, Add Foot Contact Attr, Outliner Color (10색) |
| Naming | Rename (A/B/C/D + Side), Add Prefix, Add Suffix, Search/Replace |

## GitHub

Repository: https://github.com/YGJeong-code/Maya26
