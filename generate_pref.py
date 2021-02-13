# Generate Pref on selected objects on current frame
# on the last line write True or False to create or delete Pref attribute
# Just drag and select objects on viewport and run the script

import maya.cmds as cmds

sel = cmds.ls(selection=True)
shp = cmds.listRelatives(type='shape', fullPath=True)

def create_pref(sel, shp):
    for obj in range(len(shp)):
        if cmds.attributeQuery('mtoa_varying_Pref', node=shp[obj], exists=True) == False:
            cmds.addAttr(shp[obj], longName='mtoa_varying_Pref', dataType='vectorArray')
            
        cmds.select(sel[obj]+'.vtx[*]')
        allvtx = cmds.ls(selection=True, flatten=True)
        vtxpos = []
        
        for vtx in allvtx:
            ppos = cmds.pointPosition(vtx)
            vtxpos.append(ppos)
            
        cmds.setAttr(shp[obj] + '.mtoa_varying_Pref', len(vtxpos), *vtxpos, type='vectorArray')
        
    cmds.select(sel)
    
def del_pref(shp):
    for obj in shp:
        if cmds.attributeQuery('mtoa_varying_Pref', node=obj, exists=True) == True:
            cmds.deleteAttr(obj+'.mtoa_varying_Pref')
            
def pref(create):
    if create == True:
        create_pref(sel, shp)
        print
        print('Pref attribute is generated on frame %s' % cmds.currentTime( query=True ))
        
    else:
        del_pref(shp)
        print
        print('Pref attribute is deleted')
        
pref(create=True)    #<== use True or False to create or delete Pref attribute
