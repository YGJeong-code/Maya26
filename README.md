# MayaScripts

Maya Python 스크립트 툴 모음. 리깅 중심으로 구성.

## 폴더 구조

| 폴더 | 설명 |
|------|------|
| `rigging/` | 리깅 관련 툴 (Skin / Set / Joint / Naming / Utility) |
| `pipeline/` | 임포트/익스포트, 파일/에셋 관리 툴 (추후 추가) |
| `utils/` | 공통 함수, 헬퍼 유틸리티 |

## rigging 모듈

| 모듈 | 기능 |
|------|------|
| `module/skin.py` | Skin Transfer (Multi↔One), Zero Weight 제거 |
| `module/joint.py` | Root/IK/위치 기반 조인트 생성 |
| `module/set.py` | Skin Set, Export Set 생성 |
| `module/naming.py` | Rename, Prefix/Suffix, Search/Replace |
| `module/utility.py` | Locator, Midpoint, Outliner Color, Foot Contact Attr |

## 실행 방법

1. `rigging/shelf_YG_rigging.py` 내용을 Maya Script Editor에서 실행하면 셸프 버튼이 등록된다.
2. 셸프 버튼 클릭으로 리깅 UI 실행.
3. Maya 재시작 시 `userSetup.py`가 경로를 자동 설정하여 UI가 복원된다.

## 환경

- Maya 2022+
- PySide6 / PySide2
- `userSetup.py` 위치: `maya/2025/scripts/userSetup.py`
