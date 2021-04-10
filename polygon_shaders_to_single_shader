import maya.cmds as cmds
import operator
import re

def selection_list_function():
    # get a list of viewport selection
    # input: viewport selection
    return(cmds.ls( selection = True ))

def shape_list_function(list):
    # get a list of shapes
    # input: viewport selection
    return(cmds.listRelatives( list, type = 'shape' ))

def selection_function(node):
    # select any node/object on viewport
    # input: a variable or string of the node/object
    return(cmds.select(node))

def per_object_shader_list_function():
    # a list of shaders from selected object
    # input: selection of an object
    return(cmds.hyperShade(shaderNetworksSelectMaterialNodes = True))

def faces_per_shader_function(object_loop, shape_loop):
    # a selection of the shapes/faces from shader
    # input: shader
    select_faces_from_shader = cmds.hyperShade(objects='')
    faces_from_shader_list = cmds.ls(selection=True, flatten=True)
    per_shape_list = [per_shape_list for per_shape_list in faces_from_shader_list if str(object_loop) in per_shape_list]
    per_object_list = [per_object_list for per_object_list in faces_from_shader_list if str(shape_loop) in per_object_list]
    combine_list = per_shape_list + per_object_list
    return(combine_list)

def list_of_shader_connections_function(shader_loop):
    # get a list of all the connected nodes to the shader
    # input: shader
    shader_connections_list = []
    connections_list = cmds.listConnections(shader_loop, source=True, destination=False, connections=True)
    if connections_list != None:
        for per_connection in connections_list:
            shader_connections_list.append(per_connection)
    else:
        pass
    return(shader_connections_list)

def face_ID_function(per_face_loop):
    # extract face ID from selected faces
    # input: a list of faces
    if '[' in per_face_loop.encode() and ']' in per_face_loop.encode():
        start = per_face_loop.find("[") + len("[")
        end = per_face_loop.find("]")
        combine = per_face_loop[start:end]
        return(int(combine))
    else:
        pass

def get_attribute_function(node):
    # get information of the attribute
    # input: any attribute
    return(cmds.getAttr(node))

def add_attribute_function(parameter_loop, each_parameter_loop, shape_loop, float_parameter, color_parameter):
    # adds array attributes on the shape nodes from a list of shader parameters of changed values
    if cmds.attributeQuery('mtoa_uniform_'+each_parameter_loop, node=shape_loop, exists=True) == False and parameter_loop == float_parameter:
        cmds.addAttr( shape_loop, longName='mtoa_uniform_'+each_parameter_loop, dataType='doubleArray')
    elif cmds.attributeQuery('mtoa_uniform_'+each_parameter_loop, node=shape_loop, exists=True) == False and parameter_loop == color_parameter and each_parameter_loop!='normalCamera':
        cmds.addAttr( shape_loop, longName='mtoa_uniform_'+each_parameter_loop, dataType='vectorArray')
    else:
        pass

def add_bump_attribute_function(shader_loop, shape_loop):
    # adds array bump attribute on the shape nodes
    if cmds.connectionInfo(shader_loop+'.normalCamera', isDestination=True)==True and cmds.attributeQuery('mtoa_uniform_bumpDepth', node=shape_loop, exists=True) == False:
        cmds.addAttr( shape_loop, longName='mtoa_uniform_bumpDepth', dataType='doubleArray' )

def shader_connection_function(all_shader_connections_list):
    # generates a list of shader parameters which have values changed
    shader_connections_list = []
    for connection in all_shader_connections_list:
        if '.' in connection:
            dot_index = connection.rfind('.')
            strip = connection[dot_index+1:]
            if strip not in shader_connections_list:
                shader_connections_list.append(strip)
            else:
                pass
        else:
            pass
    return(shader_connections_list)

def add_texture_path_attribute_function(per_attribute, shape_loop, shader_loop_index):
    # adds a string compound attribute on shape nodes
    if cmds.attributeQuery('mtoa_constant_path_'+per_attribute, node=shape_loop, exists=True) == False:
        cmds.addAttr( shape_loop, longName='mtoa_constant_path_'+per_attribute, dataType='string', multi=True )
    else:
        pass
    cmds.setAttr( str(shape_loop) + '.mtoa_constant_path_'+per_attribute+'['+str(shader_loop_index)+']', '', type='string' )

def set_texture_path_attribute_function(shader_loop, shape_loop, shader_loop_index):
    # sets strings of texture paths on pre created string compound attribute
    if cmds.listConnections(shader_loop, source=True, destination=False) != None:
        connections_list = cmds.listConnections(shader_loop, source=True, destination=False, connections=True)
        for each_connection in connections_list:
            if '.' in each_connection:
                dot_index = each_connection.rfind('.')
                strip = each_connection[dot_index+1:]
                new_connection = cmds.listConnections(each_connection, source=True, destination=False, connections=True)
                history_list = cmds.listHistory(new_connection[1])
                for history in history_list:
                    if cmds.nodeType(history) == 'file':
                        file_texture_path = cmds.getAttr(history+'.fileTextureName')
                        cmds.setAttr( str(shape_loop) + '.mtoa_constant_path_'+strip+'['+str(shader_loop_index)+']', file_texture_path, type='string' )
                    elif cmds.nodeType(history) == 'aiImage':
                        aiImage_texture_path = cmds.getAttr(history+'.filename')
                        cmds.setAttr( str(shape_loop) + '.mtoa_constant_path_'+strip+'['+str(shader_loop_index)+']', aiImage_texture_path, type='string' )
                    else:
                        pass
            else:
                pass
    else:
        pass

def shader_ID_function(face_shader_ID_dictionary):
    # a list of shader index extracted from face_shader_ID_dictionary
    shader_ID_list = []
    for per_ID in face_shader_ID_dictionary:
        shader_ID_list.append(face_shader_ID_dictionary[per_ID])
    return(shader_ID_list)

def face_set_attribute_function(shader_list, shape_loop, shader_ID_list):
    # adds an array attribute of face sets/selection from shaders
    if len(shader_list) > 1:
        if cmds.attributeQuery('mtoa_uniform_face_set', node=shape_loop, exists=True) == False:
            cmds.addAttr(shape_loop, longName = 'mtoa_uniform_face_set', dataType = 'Int32Array')
        else:
            pass
        cmds.setAttr(str(shape_loop) + '.mtoa_uniform_face_set', shader_ID_list, type='Int32Array')

def changed_shader_parameter_dictionary_function(changed_shader_parameter_dictionary, all_changed_shader_parameter_dictionary):
    # generates a dictionary of the shader parameters which has change in values or has a texture connection
    for key, value in changed_shader_parameter_dictionary.items():
        changed_shader_parameter_dictionary = {}
        non_repeat_shader_parameter_list = []
        for parameter in value:
            if parameter not in non_repeat_shader_parameter_list:
                non_repeat_shader_parameter_list.append(parameter)
                if parameter not in all_changed_shader_parameter_dictionary[key]:
                    all_changed_shader_parameter_dictionary[key].append(parameter)
            else:
                pass
        changed_shader_parameter_dictionary[key] = non_repeat_shader_parameter_list
    return(changed_shader_parameter_dictionary)

def select_all_faces_function(shape_loop):
    # a list of all the faces of an object
    select_all_faces = cmds.select(shape_loop+'.f[*]')
    get_all_faces = cmds.ls(selection=True, flatten=True)
    return(get_all_faces)

def per_face_shader_function(per_face_loop):
    # a list of shaders assigned per face in a sequence
    per_face_shader_list = []
    select_each_face = cmds.select(per_face_loop)
    shader_per_face = cmds.hyperShade(shaderNetworksSelectMaterialNodes = True)
    select_shader_per_face = cmds.ls(selection=True)
    per_face_shader_list.append(select_shader_per_face[0])
    return(per_face_shader_list)

def set_shader_float_values_attribute_function(changed_value_dictionary_float, per_face_shader_list, shape_loop):
    # sets values inside pre created float shader attributes on shape node
    for each_float_value in changed_value_dictionary_float:
        float_value = []
        for per_face_shader in per_face_shader_list:
            get_float_value = round(get_attribute_function(per_face_shader+'.'+each_float_value), 3)
            float_value.append(get_float_value)
        cmds.setAttr(str(shape_loop) + '.mtoa_uniform_'+each_float_value, float_value, type='doubleArray')

def set_shader_color_values_attribute_function(changed_value_dictionary_color, per_face_shader_list, shape_loop):
    # sets values inside pre created color shader attributes on shape node
    for each_color_value in changed_value_dictionary_color:
        color_value = []
        if each_color_value!='normalCamera':
            for per_face_shader in per_face_shader_list:
                get_color_value = (round(get_attribute_function(per_face_shader+'.'+each_color_value)[0][0], 3), round(get_attribute_function(per_face_shader+'.'+each_color_value)[0][1], 3), round(cmds.getAttr(per_face_shader+'.'+each_color_value)[0][2], 3))
                color_value.append(get_color_value)
            cmds.setAttr(str(shape_loop) + '.mtoa_uniform_'+each_color_value, len(color_value), *color_value, type='vectorArray')

def set_shader_bump_values_attribute_function(per_face_shader_list, shape_loop):
    # sets values inside pre created bump shader attributes on shape node
    bump_value = []
    for per_face_shader in per_face_shader_list:
        if cmds.connectionInfo(per_face_shader+'.normalCamera', isDestination=True)==True and cmds.nodeType(cmds.listConnections(per_face_shader, type='bump2d'))=='bump2d':
            get_bump_node = cmds.listConnections(per_face_shader, type='bump2d')
            get_bump_value = round(get_attribute_function(get_bump_node[0]+'.'+'bumpDepth'), 3)
            bump_value.append(get_bump_value)
        elif cmds.connectionInfo(per_face_shader+'.normalCamera', isDestination=True)==True and cmds.nodeType(cmds.listConnections(per_face_shader, type='aiBump2d'))=='aiBump2d':
            get_aiBump_node = cmds.listConnections(per_face_shader, type='aiBump2d')
            get_aiBump_value = round(get_attribute_function(get_aiBump_node[0]+'.'+'bumpHeight'), 3)
            bump_value.append(get_aiBump_value)
        else:
            bump_value.append(0)
        cmds.setAttr(str(shape_loop) + '.mtoa_uniform_bumpDepth', bump_value, type='doubleArray')

def main_shader_function(all_texture_path_shader_parameter_dictionary_color, all_texture_path_shader_parameter_dictionary_float, all_changed_shader_parameter_dictionary_color, all_changed_shader_parameter_dictionary_float, test_shader, main_shader):
    # creates a shader only from the parameters which has changed values or texture conections
    
    # create and connect an aiImage node which contains tokens to access color texture path from shape attribute
    for each_color_path in all_texture_path_shader_parameter_dictionary_color:
        if each_color_path!='normalCamera':
            texture_color_file = cmds.createNode('aiImage', n=each_color_path+'_aiImage1')
            cmds.setAttr(texture_color_file+'.filename', '<attr:path_'+each_color_path+' index:face_set>', type='string')
            cmds.connectAttr(texture_color_file+'.outColor', main_shader+'.'+each_color_path)
    
    # create and connect an aiImage node which contains tokens to access scalar texture path from shape attribute
    for each_float_path in all_texture_path_shader_parameter_dictionary_float:
        texture_scalar_file = cmds.createNode('aiImage', n=each_float_path+'_aiImage1')
        cmds.setAttr(texture_scalar_file+'.filename', '<attr:path_'+each_float_path+' index:face_set>', type='string')
        cmds.connectAttr(texture_scalar_file+'.outColorR', main_shader+'.'+each_float_path)
    
    # create and connect a user data color node which contains all the changed values of color shader parameters
    for each_color_parameter in all_changed_shader_parameter_dictionary_color:
        if each_color_parameter!='normalCamera':
            user_data_color = cmds.createNode('aiUserDataColor', n=each_color_parameter+'_aiUserDataColor1')
            cmds.setAttr(user_data_color+'.attribute', each_color_parameter, type='string')
            cmds.setAttr(user_data_color+'.default', get_attribute_function(test_shader+'.'+each_color_parameter)[0][0], get_attribute_function(test_shader+'.'+each_color_parameter)[0][1], get_attribute_function(test_shader+'.'+each_color_parameter)[0][2])
            if cmds.connectionInfo(main_shader+'.'+each_color_parameter, sourceFromDestination=True)=="":
                cmds.connectAttr(user_data_color+'.outColor', main_shader+'.'+each_color_parameter)
            else:
                cmds.connectAttr(user_data_color+'.outColor', texture_color_file+'.missingTextureColor')
    
    # create and connect a user data float node which contains all the changed values of float shader parameters
    for each_float_parameter in all_changed_shader_parameter_dictionary_float:
        user_data_float = cmds.createNode('aiUserDataFloat', n=each_float_parameter+'_aiUserDataFloat1')
        cmds.setAttr(user_data_float+'.attribute', each_float_parameter, type='string')
        cmds.setAttr(user_data_float+'.default', get_attribute_function(test_shader+'.'+each_float_parameter))
        if cmds.connectionInfo(main_shader+'.'+each_float_parameter, sourceFromDestination=True)=="":
            cmds.connectAttr(user_data_float+'.outValue', main_shader+'.'+each_float_parameter)
        else:
            cmds.connectAttr(user_data_float+'.outValue', texture_scalar_file+'.missingTextureColorR')
            cmds.connectAttr(user_data_float+'.outValue', texture_scalar_file+'.missingTextureColorG')
            cmds.connectAttr(user_data_float+'.outValue', texture_scalar_file+'.missingTextureColorB')
    
    # create and connect bump nodes
    if 'normalCamera' in all_changed_shader_parameter_dictionary_color:
        cmds.createNode('aiImage', n='normalCamera_aiImage1')
        cmds.setAttr('normalCamera_aiImage1.filename', '<attr:path_normalCamera index:face_set>', type='string')
        cmds.createNode('aiBump2d', n='normalCamera_aiBump2d1')
        cmds.connectAttr('normalCamera_aiImage1.outColorR', 'normalCamera_aiBump2d1.bumpMap')
        cmds.connectAttr('normalCamera_aiBump2d1.outValue', main_shader+'.normalCamera')
        cmds.createNode('aiUserDataFloat', n='bumpDepth_aiUserDataFloat1')
        cmds.connectAttr('bumpDepth_aiUserDataFloat1.outValue', 'normalCamera_aiBump2d1.bumpHeight')
        cmds.setAttr('bumpDepth_aiUserDataFloat1.attribute', 'bumpDepth', type='string')
        cmds.setAttr('bumpDepth_aiUserDataFloat1.default', 0)

def shader_assignment_function(multiple_shader_object_list, main_shader, test_shader):
    # shader assignment only on objects which has multiple shaders per object
    cmds.select(multiple_shader_object_list)
    
    # a confirm dialog pop up to assign the shader
    confirm = cmds.confirmDialog( title='Confirm', message='Do you want to apply shader to selection?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if confirm == 'Yes':
        cmds.hyperShade(assign=main_shader)
        print("Shader is assigned.")
    else:
        print("Shader is created, you can assign it manually.")
    
    # delete test shader
    cmds.delete(test_shader)
    
    # select objects on viewport which has shader assignments
    cmds.select(multiple_shader_object_list)



def main_function():
    # main function
    viewport_selection = selection_list_function()
    
    # List of required shader attributes stored in dictionary
    float_parameters = ['base', 'diffuseRoughness', 'specular', 'specularRoughness', 'specularIOR', 'specularAnisotropy', 'specularRotation', 
                    'metalness', 'transmission', 'transmissionScatterAnisotropy', 'transmissionDispersion', 'transmissionExtraRoughness', 
                    'subsurface', 'subsurfaceScale', 'subsurfaceAnisotropy', 'sheen', 'sheenRoughness', 'coat', 'coatRoughness', 'coatIOR', 
                    'coatAnisotropy', 'coatRotation', 'thinFilmThickness', 'thinFilmIOR', 'emission', 'indirectDiffuse', 'indirectSpecular']
    
    color_parameters = ['normalCamera', 'aiMatteColor', 'baseColor', 'specularColor', 'transmissionColor', 'transmissionScatter', 'subsurfaceColor', 
                'subsurfaceRadius', 'sheenColor', 'tangent', 'coatColor', 'coatNormal', 'emissionColor', 'opacity']
    
    parameter_name = ['float_parameters', 'color_parameters']
    all_parameters = [float_parameters, color_parameters]
    all_parameters_dictionary = {name:parameter for name, parameter in zip(parameter_name, all_parameters)}
    
    # A test shader to get all default shader values
    if cmds.objExists( 'test_SHD' ) == 0:
        test_shader = cmds.createNode('aiStandardSurface', n='test_SHD')
    
    all_changed_shader_parameter_dictionary = {}
    all_changed_shader_parameter_dictionary['float_parameters'] = []
    all_changed_shader_parameter_dictionary['color_parameters'] = []
    
    all_texture_path_shader_parameter_dictionary = {}
    all_texture_path_shader_parameter_dictionary['float_parameters'] = []
    all_texture_path_shader_parameter_dictionary['color_parameters'] = []
    
    multiple_shader_object_list = []
    
    for shape in range(len(shape_list_function(viewport_selection))):
        print('object_name: '+viewport_selection[shape]+' | '+'object_number: '+str(shape+1)+'/'+str(len(viewport_selection))+' | '+'progress: '+str(float((shape+1))/len(viewport_selection)*100)+'%')
        all_shader_connections_list = []
        face_shader_ID_dictionary = {}
        shader_parameter_connections_list = []
        changed_shader_parameter_dictionary = {}
        texture_path_shader_parameter_dictionary = {}
        selection_function(shape_list_function(viewport_selection)[shape])
        per_object_shader_list_function()
        shader_list = selection_list_function()
        
        for shader in range(len(shader_list)):
            selection_function(shader_list[shader])
            faces_selection = faces_per_shader_function(viewport_selection[shape], shape_list_function(viewport_selection)[shape])
            all_shader_connections_list.extend(list_of_shader_connections_function(shader_list[shader]))
            for face in range(len(faces_selection)):
                face_shader_ID_dictionary[face_ID_function(faces_selection[face])] = shader
            if len(shader_list) > 1:
                for parameter in all_parameters_dictionary:
                    for each_parameter in all_parameters_dictionary[parameter]:
                        if get_attribute_function(str(test_shader)+'.'+each_parameter) != get_attribute_function(shader_list[shader]+'.'+each_parameter):
                            if cmds.connectionInfo(shader_list[shader]+'.'+each_parameter, isExactDestination=True) == False:
                                changed_shader_parameter_dictionary.setdefault(parameter,[]).append(each_parameter)
                                add_attribute_function(parameter, each_parameter, shape_list_function(viewport_selection)[shape], parameter_name[0], parameter_name[1])
                                
                        if cmds.connectionInfo(shader_list[shader]+'.'+each_parameter, isExactDestination=True) == True:
                            texture_path_shader_parameter_dictionary.setdefault(parameter,[]).append(each_parameter)
                            add_bump_attribute_function(shader_list[shader], shape_list_function(viewport_selection)[shape])
        
        shader_parameter_connections_list.extend(shader_connection_function(all_shader_connections_list))
        
        for shader in range(len(shader_list)):
            if len(shader_list) > 1:
                for per_attribute in shader_parameter_connections_list:
                    add_texture_path_attribute_function(per_attribute, shape_list_function(viewport_selection)[shape], shader)
                
                set_texture_path_attribute_function(shader_list[shader], shape_list_function(viewport_selection)[shape], shader)
    
        shader_ID_list = []
        shader_ID_list.extend(shader_ID_function(face_shader_ID_dictionary))
        
        face_set_attribute_function(shader_list, shape_list_function(viewport_selection)[shape], shader_ID_list)
        
        changed_shader_parameter_dictionary_function(changed_shader_parameter_dictionary, all_changed_shader_parameter_dictionary)
        
        changed_shader_parameter_dictionary_function(texture_path_shader_parameter_dictionary, all_texture_path_shader_parameter_dictionary)
    
        if len(shader_list) > 1:
            get_all_faces = select_all_faces_function(shape_list_function(viewport_selection)[shape])
            per_face_shader_list = []
            
            for each_face in get_all_faces:
                per_face_shader_list.extend(per_face_shader_function(each_face))
                
            try:
                set_shader_float_values_attribute_function(changed_shader_parameter_dictionary['float_parameters'], per_face_shader_list, shape_list_function(viewport_selection)[shape])
    
                set_shader_color_values_attribute_function(changed_shader_parameter_dictionary['color_parameters'], per_face_shader_list, shape_list_function(viewport_selection)[shape])
    
                set_shader_bump_values_attribute_function(per_face_shader_list, shape_list_function(viewport_selection)[shape])
            except:
                pass
            
            multiple_shader_object = cmds.listRelatives(shape_list_function(viewport_selection)[shape], parent=True)[0]
            multiple_shader_object_list.append(multiple_shader_object)
            
        else:
            pass
    
    main_shader = cmds.createNode('aiStandardSurface', n='shader_MAT')
    
    main_shader_function(all_texture_path_shader_parameter_dictionary['color_parameters'], all_texture_path_shader_parameter_dictionary['float_parameters'], all_changed_shader_parameter_dictionary['color_parameters'], all_changed_shader_parameter_dictionary['float_parameters'], test_shader, main_shader)
    
    shader_assignment_function(multiple_shader_object_list, main_shader, test_shader)

main_function()
