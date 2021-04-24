import maya.cmds as cmds

def selection():
    sel = cmds.ls(selection=True)
    return(sel)

def shape():
    shp = cmds.listRelatives(selection(), type='shape', allDescendents=True, noIntermediate=True, fullPath=True)
    return(shp)

def transform():
    trans = cmds.listRelatives(shape(), type='transform', parent=True, fullPath=True)
    return(trans)

def maya_pref(sel, shp, trans):
    for obj in range(len(shp)):
        if cmds.attributeQuery('mtoa_varying_Pref', node=shp[obj], exists=True) == False:
            cmds.addAttr(shp[obj], longName='mtoa_varying_Pref', dataType='vectorArray')

            cmds.select(trans[obj]+'.vtx[*]')
            allvtx = cmds.ls(selection=True, flatten=True)
            vtxpos = []
            
            for vtx in allvtx:
                ppos = cmds.pointPosition(vtx)
                vtxpos.append(ppos)
                
            cmds.setAttr(shp[obj] + '.mtoa_varying_Pref', len(vtxpos), *vtxpos, type='vectorArray')
        
        else:
            pass
        
    cmds.select(sel)

def houdini_pref(sel, shp, trans):
    for obj in range(len(shp)):
        if cmds.attributeQuery('Pref', node=shp[obj], exists=True) == False:
            cmds.addAttr(shp[obj], longName='Pref', dataType='vectorArray')
            cmds.addAttr(shp[obj], longName="Pref_AbcGeomScope", dataType="string")
            
            cmds.select(trans[obj]+'.vtx[*]')
            allvtx = cmds.ls(selection=True, flatten=True)
            vtxpos = []
            
            for vtx in allvtx:
                ppos = cmds.pointPosition(vtx)
                vtxpos.append(ppos)
                
            cmds.setAttr(shp[obj] + '.Pref', len(vtxpos), *vtxpos, type='vectorArray')
            cmds.setAttr(shp[obj]+".Pref_AbcGeomScope", "var", type="string")
        
        else:
            pass
        
    cmds.select(sel)

def both_pref(sel, shp, trans):
    for obj in range(len(shp)):
        if cmds.attributeQuery('mtoa_varying_Pref', node=shp[obj], exists=True) == False and cmds.attributeQuery('Pref', node=shp[obj], exists=True) == False:
            cmds.addAttr(shp[obj], longName='mtoa_varying_Pref', dataType='vectorArray')
            cmds.addAttr(shp[obj], longName='Pref', dataType='vectorArray')
            
            cmds.addAttr(shp[obj], longName="Pref_AbcGeomScope", dataType="string")
            cmds.setAttr(shp[obj]+".Pref_AbcGeomScope", "var", type="string")
            
            cmds.select(trans[obj]+'.vtx[*]')
            allvtx = cmds.ls(selection=True, flatten=True)
            vtxpos = []
            
            for vtx in allvtx:
                ppos = cmds.pointPosition(vtx)
                vtxpos.append(ppos)
                
            cmds.setAttr(shp[obj] + '.mtoa_varying_Pref', len(vtxpos), *vtxpos, type='vectorArray')
            cmds.setAttr(shp[obj] + '.Pref', len(vtxpos), *vtxpos, type='vectorArray')
        
        else:
            pass
        
    cmds.select(sel)

def generate_pref():
    cmds.currentTime( cmds.intFieldGrp( "frame", query=True, value1=True) )
    if cmds.attributeQuery('mtoa_varying_Pref', node=shape()[0], exists=True) == True or cmds.attributeQuery('Pref', node=shape()[0], exists=True) == True or cmds.attributeQuery('Pref_AbcGeomScope', node=shape()[0], exists=True) == True:
        print("Pref already exist!")
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == True and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == False:
        maya_pref(selection(), shape(), transform())
        print("Pref generated on frame %s!" % int(cmds.currentTime(query=True)))
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == False and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == True:
        houdini_pref(selection(), shape(), transform())
        print("Pref generated on frame %s!" % int(cmds.currentTime(query=True)))
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == True and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == True:
        both_pref(selection(), shape(), transform())
        print("Pref generated on frame %s!" % int(cmds.currentTime(query=True)))
    elif cmds.checkBoxGrp( "dcc", query=True, value1=True ) == False and cmds.checkBoxGrp( "dcc", query=True, value2=True ) == False:
        print("Please select at least one DCC!")
    else:
        pass

def delete_pref(shp):
    for obj in shp:
        if cmds.attributeQuery('mtoa_varying_Pref', node=obj, exists=True) == False and cmds.attributeQuery('Pref', node=obj, exists=True) == False and cmds.attributeQuery('Pref_AbcGeomScope', node=obj, exists=True) == False:
            print("Pref doesn't exist!")
        else:
            pass
        if cmds.attributeQuery('mtoa_varying_Pref', node=obj, exists=True) == True:
            cmds.deleteAttr(obj+'.mtoa_varying_Pref')
            print("Pref deleted!")
        else:
            pass
        if cmds.attributeQuery('Pref', node=obj, exists=True) == True and cmds.attributeQuery('Pref_AbcGeomScope', node=obj, exists=True) == True:
            cmds.deleteAttr(obj+'.Pref')
            cmds.deleteAttr(obj+'.Pref_AbcGeomScope')
            print("Pref deleted!")
        else:
            pass

def pref_win():
    
    if cmds.window( "pref", exists=True ):
        cmds.deleteUI( "pref" )
    
    pref = cmds.window( "pref", title="Generate Pref v1.0", widthHeight=(170,170) )
    cmds.columnLayout( adjustableColumn=True )
    cmds.text( label='' )
    cmds.text( label='1. Drag and select mesh on viewport' )
    cmds.text( label='2. Select one or both DCCs' )
    cmds.text( label='3. Type frame number' )
    cmds.text( label='4. Generate Pref' )
    cmds.text( label='' )
    cmds.checkBoxGrp( "dcc", numberOfCheckBoxes=2, label='DCC:', labelArray2=['Maya', 'Houdini/Alembic'], columnAlign=(1, "center"), value1=True, columnWidth3=(50,70,130) )
    cmds.intFieldGrp( "frame", label="Frame:", value1=cmds.currentTime( query=True ), columnAlign=(1, "center"), columnWidth2=(50,180))
    cmds.text( label='' )
    cmds.button( label='Generate Pref', command="generate_pref()" )
    cmds.button( label='Delete Pref', command="delete_pref(shape())" )
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + "pref" + '\", window=True)') )
    cmds.showWindow( "pref" )

pref_win()
