# Compatible: Maya 2022+
from maya import cmds


def renameObj(*, myA='', myB='', myC='', myD='', mySide='', prefix='', subfix='', search='', replace=''):
    """선택 오브젝트 이름 변경 (번호/사이드/prefix/suffix/search-replace)"""
    selected_objects = cmds.ls(selection=True)
    for i, obj in enumerate(selected_objects):
        padded_number = '{:02d}'.format(i + 1)
        new_name = ''
        if myA:
            new_name = '{}_{}'.format(myA, padded_number)
            if myB:
                new_name = '{}_{}_{}'.format(myA, myB, padded_number)
                if myC:
                    new_name = '{}_{}_{}_{}'.format(myA, myB, myC, padded_number)
                    if myD:
                        new_name = '{}_{}_{}_{}_{}'.format(myA, myB, myC, myD, padded_number)
        if len(selected_objects) == 1:
            new_name = '{}_root'.format(myA)
            if myB:
                new_name = '{}_{}_root'.format(myA, myB)
        if mySide:
            new_name = '{}_{}'.format(new_name, mySide)
        if prefix:
            new_name = '{}_{}'.format(prefix, obj)
        if subfix:
            new_name = '{}_{}'.format(obj, subfix)
        if search:
            new_name = obj.replace(search, replace)
        if new_name:
            cmds.rename(obj, new_name)
