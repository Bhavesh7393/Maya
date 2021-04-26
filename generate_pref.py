'''

Generate Pref for Arnold.

1. Drag and select mesh on viewport
2. Select one or both DCCs
3. Type frame number
4. Generate Pref

Bhavesh Budhkar
bhaveshbudhkar@yahoo.com

'''

import maya.cmds as cmds

# Selection list
def selection():
    sel = cmds.ls(selection=True)
    return(sel)

# Shape list from selection
def shape():
    shp = cmds.listRelatives(selection(), type='shape', allDescendents=True, noIntermediate=True, fullPath=True)
    return(shp)

# Iterate through selected geometries to get list of all vertices world position
def position(selection_loop):
    cmds.select(selection_loop+'.vtx[*]')
    allvtx = cmds.ls(selection=True, flatten=True)
    vtxpos = []
    for vtx in allvtx:
        ppos = cmds.pointPosition(vtx)
        vtxpos.append(ppos)
    return(vtxpos)

# Pref attribute generation for Maya/Arnold
def maya_pref(selection, shape):
    for obj in range(len(shape)):
        if cmds.attributeQuery('mtoa_varying_Pref', node=shape[obj], exists=True) == False:
            cmds.addAttr(shape[obj], longName='mtoa_varying_Pref', dataType='vectorArray')
            vtxpos = position(selection[obj])
            cmds.setAttr(shape[obj] + '.mtoa_varying_Pref', len(vtxpos), *vtxpos, type='vectorArray')
        else:
            pass
    cmds.select(selection)

# Pref attribute generation for Houdini/Arnold via Alembic
def houdini_pref(selection, shape):
    for obj in range(len(shape)):
        if cmds.attributeQuery('Pref', node=shape[obj], exists=True) == False:
            cmds.addAttr(shape[obj], longName='Pref', dataType='vectorArray')
            cmds.addAttr(shape[obj], longName="Pref_AbcGeomScope", dataType="string")
            vtxpos = position(selection[obj])
            cmds.setAttr(shape[obj] + '.Pref', len(vtxpos), *vtxpos, type='vectorArray')
            cmds.setAttr(shape[obj]+".Pref_AbcGeomScope", "var", type="string")
        else:
            pass
    cmds.select(selection)

# Pref attribute generation for both Maya/Arnold and Houdini/Arnold
def both_pref(selection, shape):
    for obj in range(len(shape)):
        if cmds.attributeQuery('mtoa_varying_Pref', node=shape[obj], exists=True) == False and cmds.attributeQuery('Pref', node=shape[obj], exists=True) == False:
            cmds.addAttr(shape[obj], longName='mtoa_varying_Pref', dataType='vectorArray')
            cmds.addAttr(shape[obj], longName='Pref', dataType='vectorArray')
            cmds.addAttr(shape[obj], longName="Pref_AbcGeomScope", dataType="string")
            vtxpos = position(selection[obj])
            cmds.setAttr(shape[obj] + '.mtoa_varying_Pref', len(vtxpos), *vtxpos, type='vectorArray')
            cmds.setAttr(shape[obj] + '.Pref', len(vtxpos), *vtxpos, type='vectorArray')
            cmds.setAttr(shape[obj]+".Pref_AbcGeomScope", "var", type="string")
        else:
            pass
    cmds.select(selection)

# Pref generation logic based on selection in UI
def generate_pref():
    cmds.currentTime( cmds.intFieldGrp( "frame", query=True, value1=True) )
    if cmds.attributeQuery('mtoa_varying_Pref', node=shape()[0], exists=True) == True or cmds.attributeQuery('Pref', node=shape()[0], exists=True) == True or cmds.attributeQuery('Pref_AbcGeomScope', node=shape()[0], exists=True) == True:
        print("Pref already exist!")
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == True and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == False:
        maya_pref(selection(), shape())
        print("Pref generated on frame %s!" % int(cmds.currentTime(query=True)))
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == False and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == True:
        houdini_pref(selection(), shape())
        print("Pref generated on frame %s!" % int(cmds.currentTime(query=True)))
        print('Please export Alembic with "Pref" attribute for Houdini.')
        confirm = cmds.confirmDialog( title='Note', message='Please export Alembic with "Pref" attribute for Houdini.', button=['Okay'], defaultButton='Okay' )
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == True and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == True:
        both_pref(selection(), shape())
        print("Pref generated on frame %s!" % int(cmds.currentTime(query=True)))
        print('Please export Alembic with "Pref" attribute for Houdini.')
        confirm = cmds.confirmDialog( title='Note', message='Please export Alembic with "Pref" attribute for Houdini.', button=['Okay'], defaultButton='Okay' )
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == False and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == False:
        print("Please select at least one DCC!")
    else:
        pass

# Delete Pref attribute.
def delete_pref(shape):
    for obj in shape:
        if cmds.attributeQuery('mtoa_varying_Pref', node=obj, exists=True) == False and cmds.attributeQuery('Pref', node=obj, exists=True) == False and cmds.attributeQuery('Pref_AbcGeomScope', node=obj, exists=True) == False:
            print("Pref doesn't exist!")
        elif cmds.attributeQuery('mtoa_varying_Pref', node=obj, exists=True) == True and cmds.attributeQuery('Pref', node=obj, exists=True) == True and cmds.attributeQuery('Pref_AbcGeomScope', node=obj, exists=True) == True:
            cmds.deleteAttr(obj+'.mtoa_varying_Pref')
            cmds.deleteAttr(obj+'.Pref')
            cmds.deleteAttr(obj+'.Pref_AbcGeomScope')
            print("Pref deleted!")
        elif cmds.attributeQuery('mtoa_varying_Pref', node=obj, exists=True) == True:
            cmds.deleteAttr(obj+'.mtoa_varying_Pref')
            print("Pref deleted!")
        elif cmds.attributeQuery('Pref', node=obj, exists=True) == True and cmds.attributeQuery('Pref_AbcGeomScope', node=obj, exists=True) == True:
            cmds.deleteAttr(obj+'.Pref')
            cmds.deleteAttr(obj+'.Pref_AbcGeomScope')
            print("Pref deleted!")
        else:
            pass

# Pref UI creation
def pref_ui():
    if cmds.window( "pref", exists=True ):
        cmds.deleteUI( "pref" )
    cmds.window( "pref", title="Generate Pref v1.0", width=200, height=250 )
    cmds.columnLayout( adjustableColumn=True )
    cmds.text( label='' )
    cmds.text( label='Bhavesh Budhkar    ', align='right' )
    cmds.text( label='bhaveshbudhkar@yahoo.com    ', align='right' )
    cmds.text( label='' )
    cmds.text( label='' )
    cmds.text( label='Generate Pref for Arnold' )
    cmds.text( label='' )
    cmds.text( label='    1. Drag and select mesh on viewport', align='left' )
    cmds.text( label='    2. Select one or both DCCs', align='left' )
    cmds.text( label='    3. Type frame number', align='left' )
    cmds.text( label='    4. Generate Pref', align='left' )
    cmds.text( label='' )
    cmds.checkBoxGrp( "dcc", numberOfCheckBoxes=2, label='DCC:', labelArray2=['MtoA', 'HtoA/Alembic'], columnAlign=(1, "center"), value1=True, columnWidth3=(50,70,130) )
    cmds.intFieldGrp( "frame", label="Frame:", value1=cmds.currentTime( query=True ), columnAlign=(1, "center"), columnWidth2=(50,180))
    cmds.text( label='' )
    cmds.button( label='Generate Pref', command="generate_pref()" )
    cmds.button( label='Delete Pref', command="delete_pref(shape())" )
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + "pref" + '\", window=True)') )
    cmds.showWindow( "pref" )

pref_ui()
