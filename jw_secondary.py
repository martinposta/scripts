# https://vimeo.com/257551619
# auto generated secondary animation by Junjie Wang 

import maya.cmds as cmds
import random
 
 
def matchTransform(s,d,pos,rot):
    ##print d,s
    w_trans = cmds.xform(d,ws = True, rp = True, q = True)
    w_ros = cmds.xform(d,ws = True, ro = True, q = True)
    order = cmds.xform(d,rotateOrder = True, q = True)
    if pos:
        cmds.xform(s,ws = True, t = w_trans)
    if rot:
        cmds.xform(s,rotateOrder = order)
        cmds.xform(s,ws = True, ro = w_ros)
         
 
 
def particle_exist():
    partical =  cmds.ls(type = "particle")
    if len(partical) != 0:
        for i in partical:
            if i.__contains__("_temp_particle"):
                return True
 
 
def create_target(object):
    temp_null = cmds.spaceLocator(n = "{0}_temp_target".format(object))[0]
    #print temp_null
    matchTransform(temp_null,object,True,True)
    return temp_null
     
def create_front(object):
    temp_null = cmds.spaceLocator(n = "{0}_temp_front_indicator".format(object))[0]
    #print temp_null
    matchTransform(temp_null,object,True,True)
    return temp_null
     
 
def simulation(object,target,conserve,weight):
     
    start = cmds.playbackOptions(min=True,query= True)
    end = cmds.playbackOptions(max=True,query= True)
                 
    front = "{0}_temp_front_indicator".format(object)
     
    temp_cons = cmds.parentConstraint(object , target, n = "temp_cons",maintainOffset = True )
     
    #temp_cons2 = cmds.parentConstraint(object , front, n = "temp_cons2",maintainOffset = True )
                 
    cmds.bakeResults( target, sb=1,t=(start,end),simulation = True )
             
    cmds.delete(temp_cons)
     
    temp_particle = cmds.particle(n = "{0}_temp_particle".format(object), p = [0,0,0], c = conserve)[0]
         
    cmds.setAttr("{0}.particleRenderType".format(temp_particle), 4)
     
    #match position of particle to target
    matchTransform(temp_particle,target,True,True)
     
    #particle to move with target   
    cmds.goal( temp_particle, g = target, w= weight )
             
    #partical will not be baked, a null need to creatge to transfer the animation data from particle to null    
    target_control = cmds.spaceLocator(n = "{0}_temp_target_control".format(object))[0]
                 
    cmds.connectAttr( "{0}.cachedWorldCentroid".format(temp_particle), '{0}.translate'.format(target_control))
     
    object_parent = cmds.listRelatives(object, parent = True)       
     
    if object_parent:
         
        cmds.parent(front, object_parent )
     
    new_constraint = cmds.aimConstraint(target_control, object , n = "{0}_temp_aim".format(object),maintainOffset = True,worldUpType = "object",worldUpObject = front)
    #new_constraint = cmds.aimConstraint(target_control, object , n = "{0}_temp_aim".format(object),maintainOffset = True,worldUpType = "scene")
     
    cmds.hide(target)
    cmds.hide(target_control)
 
     
             
 
def simulation_translate(object,conserve,weight):
     
    start = cmds.playbackOptions(min=True,query= True)
    end = cmds.playbackOptions(max=True,query= True)
                 
    target = cmds.spaceLocator(n = "{0}_temp_target".format(object))[0]
     
    temp_cons = cmds.parentConstraint(object , target, n = "temp_cons",maintainOffset = False )
                 
    cmds.bakeResults( target, sb=1,t=(start,end),simulation = True )
             
    cmds.delete(temp_cons)
     
    temp_particle = cmds.particle(n = "{0}_temp_particle".format(object), p = [0,0,0], c = conserve)[0]
         
    cmds.setAttr("{0}.particleRenderType".format(temp_particle), 4)
     
    #match position of particle to target
    matchTransform(temp_particle,target,True,True)
     
    #particle to move with target   
    cmds.goal( temp_particle, g = target, w= weight )
             
    #partical will not be baked, a null need to creatge to transfer the animation data from particle to null    
    target_control = cmds.spaceLocator(n = "{0}_temp_target_control".format(object))[0]
                 
    cmds.connectAttr( "{0}.cachedWorldCentroid".format(temp_particle), '{0}.translate'.format(target_control) )
             
    new_constraint = cmds.pointConstraint(target_control, object , n = "{0}_temp_aim".format(object),maintainOffset = True)
     
    cmds.hide( target, target_control )
 
 
def change_btn_color(btn,f1,f2,f3):
    cmds.button(btn, bgc = (f1,f2,f3),e = True)
 
 
 
def create_target_btn(*arg):
    if particle_exist():
        cmds.confirmDialog(title='Oups', message='simulation is in process, must be applied before doing the next one', button=['Ok'])
    else:
        selection = cmds.ls(selection = True)
        if len(selection) == 1:
            global sel_object
             
            sel_object = selection[0]
             
            if cmds.getAttr("{0}.rotateX".format(sel_object), keyable = True,lock = True) or cmds.getAttr("{0}.rotateY".format(sel_object), keyable = True,lock = True) or cmds.getAttr("{0}.rotateZ".format(sel_object), keyable = True,lock = True):
                cmds.confirmDialog( title='Error', message='one or more rotate attributes are locked!!! unlock them first', button=['Cancel'])
            else:
                start = cmds.playbackOptions(min=True,query= True)
                cmds.currentTime( start, edit=True )
                global sel_target
                sel_target = create_target(sel_object)
                 
             
 
 
 
def create_front_btn(*arg):
    if particle_exist():
        cmds.confirmDialog(title='Oups', message='simulation is in process, must be applied before doing the next one', button=['Ok'])
    else:
        if cmds.objExists("{0}_temp_target".format(sel_object)):
            create_front(sel_object)
     
             
 
 
def simulation_btn(*arg):
    if particle_exist():
        cmds.confirmDialog(title='Oups', message='simulation is in process, must be applied before doing the next one', button=['Ok'])
    else:
        if cmds.objExists("{0}_temp_target".format(sel_object)) and cmds.objExists("{0}_temp_front_indicator".format(sel_object)):
            conserve = cmds.floatSlider( conserve_rotate , value=True, q = True )
            weight = cmds.floatSlider( weight_rotate , value=True, q = True )
            simulation(sel_object,sel_target,conserve,weight)
            pairBlend_list = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")
            #print "dfadfa",pairBlend_list
            if pairBlend_list:
                global pairBlend_
                pairBlend_= pairBlend_list[0]
                global node_x
                node_x = get_animation_node(pairBlend_, "_rotateX")
                global node_y
                node_y = get_animation_node(pairBlend_, "_rotateY")
                global node_z
                node_z = get_animation_node(pairBlend_, "_rotateZ")
            else:
                cmds.confirmDialog(title='Oups', message='there are no keys', button=['Ok'])
                 
             
            cmds.rowColumnLayout(hide_,visible = True,e= True)
            cmds.checkBox( r_X, v = True, e= True )
            cmds.checkBox( r_Y, v = True, e= True )
            cmds.checkBox( r_Z, v = True, e= True )
             
         
         
 
def simulation_translate_btn(*arg):
     
    if particle_exist():
        cmds.confirmDialog(title='Oups', message='simulation is in process, must be applied before doing the next one', button=['Ok'])
    else:
        global sel_trans_object
        sel_trans_object = cmds.ls(selection = True)[0]
        if cmds.getAttr("{0}.translateX".format(sel_trans_object), keyable = True,lock = True) or cmds.getAttr("{0}.translateY".format(sel_trans_object), keyable = True,lock = True) or cmds.getAttr("{0}.translateZ".format(sel_trans_object), keyable = True,lock = True):
            cmds.confirmDialog( title='Error', message='one or more translate attributes are locked!!! unlock them first', button=['Cancel'])
         
        else:
            conserve = cmds.floatSlider( conserve_translate , value=True, q = True )
            weight = cmds.floatSlider( weight_translate , value=True, q = True )
            simulation_translate(sel_trans_object,conserve,weight)
 
 
def conserve_onchange_rotate(*arg):
    #particle = "{0}_temp_particle".format(object)
    value = cmds.floatSlider(conserve_rotate,value = True, query = True)
    #print value
    if cmds.objExists("{0}_temp_particle".format(sel_object)):
        cmds.setAttr("{0}_temp_particle.conserve".format(sel_object), value)
        print "value change"
 
def weight_onchange_rotate(*arg):
    #particle = "{0}_temp_particle".format(object)
    value = cmds.floatSlider(weight_rotate,value = True, query = True)
    #print value
    if cmds.objExists("{0}_temp_particle".format(sel_object)): 
        #print "dfadfa"
        cmds.setAttr("{0}_temp_particle.goalWeight[0]".format(sel_object), value)
        print "value change"
 
 
def conserve_onchange_translate(*arg):
    #particle = "{0}_temp_particle".format(object)
    value = cmds.floatSlider(conserve_translate,value = True, query = True)
    #print value
    if cmds.objExists("{0}_temp_particle".format(sel_trans_object)):
        cmds.setAttr("{0}_temp_particle.conserve".format(sel_trans_object), value)
        print "value change"
 
def weight_onchange_translate(*arg):
    #particle = "{0}_temp_particle".format(object)
    value = cmds.floatSlider(weight_translate,value = True, query = True)
    #print value
    if cmds.objExists("{0}_temp_particle".format(sel_trans_object)):
        cmds.setAttr("{0}_temp_particle.goalWeight[0]".format(sel_trans_object), value)
        print "value change"
 
         
def apply_rotate(*arg):
    if cmds.objExists("{0}_temp_particle".format(sel_object)):
        cmds.rowColumnLayout(hide_,visible = False,e= True)
        start = cmds.playbackOptions(min=True,query= True)
        end = cmds.playbackOptions(max=True,query= True)
        cmds.select(sel_object)
        if cmds.checkBox(rot_sep_layer,v= True, q = True):
            layer_name = "{0}_secondary_rotation".format(sel_object)
            if not cmds.animLayer(layer_name, exists = True, q = True):
                anim_layer = cmds.animLayer(layer_name,override=True,passthrough = True)
             
        else:
            layer_name = "overlap_rotate_layer"
            if not cmds.animLayer(layer_name, exists = True, q = True):
                anim_layer = cmds.animLayer(layer_name,override=True,passthrough = True)
             
        cmds.bakeResults(sel_object, sb=1,t=(start,end), disableImplicitControl = True, preserveOutsideKeys = True,
            sparseAnimCurveBake = False, shape = True , simulation = True,bakeOnOverrideLayer = True,dl = layer_name)
                 
        cmds.delete("{0}_temp_target".format(sel_object))
        cmds.delete("{0}_temp_particle".format(sel_object))
        cmds.delete("{0}_temp_target_control".format(sel_object))
        cmds.delete("{0}_temp_front_indicator".format(sel_object))
     
     
    #cmds.delete("{0}_temp_aim".format(sel_object))
 
def apply_translate(*arg):
    if cmds.objExists("{0}_temp_particle".format(sel_trans_object)):
        start = cmds.playbackOptions(min=True,query= True)
        end = cmds.playbackOptions(max=True,query= True)
        cmds.select(sel_trans_object)
        if cmds.checkBox(trans_sep_layer,v= True, q = True):
            layer_name = "{0}_secondary_translate".format(sel_trans_object)
            if not cmds.animLayer(layer_name, exists = True, q = True):
                anim_layer = cmds.animLayer(layer_name,override=True,passthrough = True)
             
        else:
            layer_name = "overlap_trans_layer"
            if not cmds.animLayer(layer_name, exists = True, q = True):
                anim_layer = cmds.animLayer(layer_name,override=True,passthrough = True)
 
        cmds.bakeResults(sel_trans_object, sb=1,t=(start,end), disableImplicitControl = True, preserveOutsideKeys = True,
        sparseAnimCurveBake = False, shape = True , simulation = True,bakeOnOverrideLayer = True,dl = layer_name)
             
             
        cmds.delete("{0}_temp_target".format(sel_trans_object))
        cmds.delete("{0}_temp_particle".format(sel_trans_object))
        cmds.delete("{0}_temp_target_control".format(sel_trans_object))
         
     
     
def clean2(*arg):
    list = ["{0}_temp_target".format(sel_object),"{0}_temp_particle".format(sel_object),"{0}_temp_target_control".format(sel_object),
    "{0}_temp_aim".format(sel_object),"{0}_temp_front_indicator".format(sel_object)]
    for d in list:
        if cmds.objExists(d):
            cmds.delete(d)
    cmds.rowColumnLayout(hide_,visible = False,e= True)
     
 
def clean(*arg):
    list = ["_temp_target","_temp_particle","_temp_target_control","_temp_front_indicator",
    "_temp_aim"]
    for d in list:
        for i in cmds.ls():
            if i.__contains__(d):
                if cmds.objExists(i):
                    cmds.delete(i)
    cmds.rowColumnLayout(hide_,visible = False,e= True)
 
 
 
 
def get_animation_node(pairBlend_, attr):
    for a in cmds.listConnections(pairBlend_,source = True ):
        if a.__contains__(attr):
            return a
 
 
 
def X_off(*arg):
    print node_x
    print pairBlend_
    #pairBlend_ = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")[0]   
    if cmds.objExists(pairBlend_)and cmds.objExists("{0}.output".format(node_x)):
        cmds.disconnectAttr("{0}.output".format(node_x),"{0}.inRotate1.inRotateX1".format(pairBlend_))
        cmds.disconnectAttr("{0}.outRotate.outRotateX".format(pairBlend_),"{0}.rotate.rotateX".format(sel_object))
        cmds.connectAttr("{0}.output".format(node_x),"{0}.rotate.rotateX".format(sel_object))
 
def X_on(*arg):
    #pairBlend_ = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")[0]
    if cmds.objExists(pairBlend_) and cmds.objExists(" {0}.output".format(node_x)):
        cmds.disconnectAttr(" {0}.output".format(node_x),"{0}.rotate.rotateX".format(sel_object))
        cmds.connectAttr("{0}.output".format(node_x),"{0}.inRotate1.inRotateX1".format(pairBlend_))
        cmds.connectAttr("{0}.outRotate.outRotateX".format(pairBlend_),"{0}.rotate.rotateX".format(sel_object))
         
 
def Y_off(*arg):
    #pairBlend_ = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")[0]
    if cmds.objExists(pairBlend_)and cmds.objExists("{0}.output".format(node_y)):
        cmds.disconnectAttr("{0}.output".format(node_y),"{0}.inRotate1.inRotateY1".format(pairBlend_))
        cmds.disconnectAttr("{0}.outRotate.outRotateY".format(pairBlend_),"{0}.rotate.rotateY".format(sel_object))
        cmds.connectAttr("{0}.output".format(node_y),"{0}.rotate.rotateY".format(sel_object))
 
def Y_on(*arg):
    #pairBlend_ = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")[0]
    if cmds.objExists(pairBlend_) and cmds.objExists(" {0}.output".format(node_y)):
        cmds.disconnectAttr(" {0}.output".format(node_y),"{0}.rotate.rotateY".format(sel_object))
        cmds.connectAttr("{0}.output".format(node_y),"{0}.inRotate1.inRotateY1".format(pairBlend_))
        cmds.connectAttr("{0}.outRotate.outRotateY".format(pairBlend_),"{0}.rotate.rotateY".format(sel_object))
         
         
     
def Z_off(*arg):
    #pairBlend_ = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")[0]
    if cmds.objExists(pairBlend_)and cmds.objExists("{0}.output".format(node_z)):
        cmds.disconnectAttr("{0}.output".format(node_z),"{0}.inRotate1.inRotateZ1".format(pairBlend_))
        cmds.disconnectAttr("{0}.outRotate.outRotateZ".format(pairBlend_),"{0}.rotate.rotateZ".format(sel_object))
        cmds.connectAttr("{0}.output".format(node_z),"{0}.rotate.rotateZ".format(sel_object))
def Z_on(*arg):
    #pairBlend_ = cmds.listConnections("{0}_temp_aim".format(sel_object),type = "pairBlend")[0]
    if cmds.objExists(pairBlend_) and cmds.objExists(" {0}.output".format(node_z)):
        cmds.disconnectAttr(" {0}.output".format(node_z),"{0}.rotate.rotateZ".format(sel_object))
        cmds.connectAttr("{0}.output".format(node_z),"{0}.inRotate1.inRotateZ1".format(pairBlend_))
        cmds.connectAttr("{0}.outRotate.outRotateZ".format(pairBlend_),"{0}.rotate.rotateZ".format(sel_object))
         
def rot_sep_layer_on(*arg):
    cmds.checkBox(rot_one_layer, value = False, e = True)
     
def rot_sep_layer_off(*arg):
    cmds.checkBox(rot_one_layer, value = True, e = True)
 
 
def rot_one_layer_on(*arg):
    cmds.checkBox(rot_sep_layer, value = False, e = True)
     
def rot_one_layer_off(*arg):
    cmds.checkBox(rot_sep_layer, value = True, e = True)
 
 
def trans_sep_layer_on(*arg):
    cmds.checkBox(trans_one_layer, value = False, e = True)
     
def trans_sep_layer_off(*arg):
    cmds.checkBox(trans_one_layer, value = True, e = True)
 
 
def trans_one_layer_on(*arg):
    cmds.checkBox(trans_sep_layer, value = False, e = True)
     
def trans_one_layer_off(*arg):
    cmds.checkBox(trans_sep_layer, value = True, e = True)  
     
 
     
windowID = "mywindowID"
if cmds.window(windowID, exists = True):
    cmds.deleteUI(windowID)
 
window = cmds.window(windowID, title = "SecondaryAnimation_v7.1")
Headform = cmds.formLayout()
Headtabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
 
FK = cmds.formLayout(numberOfDivisions=100, p=Headtabs)
cmds.rowColumnLayout( numberOfColumns=1)
ta = cmds.button(l = 'Create Target', c = create_target_btn, w = 300)
cmds.separator( style='none',h = 5)
fr = cmds.button(l = 'Create up vector object', c = create_front_btn, w = 300)
cmds.separator( style='none',h = 5)
si = cmds.button(l = 'Simulate', c = simulation_btn)
cmds.separator( style='none',h = 5)
 
#hide_ = cmds.frameLayout("isolate individual axis", collapse = True, collapsable = True, visible = False)
 
hide_ = cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 100),(2,100),(3, 100)],visible = False )
r_X = cmds.checkBox( label='Isolate X', v = True, onc = X_on, ofc = X_off, al = 'center' )
r_Y = cmds.checkBox( label='Isolate Y', v = True, onc = Y_on, ofc = Y_off, al = 'center' )
r_Z = cmds.checkBox( label='Isolate Z', v = True, onc = Z_on, ofc = Z_off, al = 'center')
 
cmds.setParent("..")
 
 
#cmds.separator( style='none',h = 5)
cmds.text(l = 'Overlap')
conserve_rotate = cmds.floatSlider( min=0.5, max=1, value=0.8, step=0.05, dc = conserve_onchange_rotate )
cmds.separator( style='none',h = 5)
 
cmds.text(l = 'Weight')
weight_rotate = cmds.floatSlider( min=0.5, max=1, value=0.7, step=0.05, dc = weight_onchange_rotate )
cmds.separator( style='none',h = 5)
 
 
 
cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100),(2,60),(3, 110)] )
ap = cmds.button(l = 'Apply', c = apply_rotate)
cmds.separator( style='none')
rot_sep_layer = cmds.checkBox( label='To seperate layer', v = False, onc = rot_sep_layer_on, ofc = rot_sep_layer_off )
cmds.button(l = 'Cancel', c = clean)
cmds.separator( style='none')
rot_one_layer = cmds.checkBox( label='To one layer', v = True, onc = rot_one_layer_on, ofc = rot_one_layer_off )
 
#==============================================================
IK = cmds.formLayout(numberOfDivisions=100, p=Headtabs)
 
cmds.rowColumnLayout( numberOfColumns=1)
cmds.button(l = 'Simulate', c = simulation_translate_btn , w = 300)
cmds.separator( style='none',h = 5)
 
cmds.text(l = 'Overlap')
conserve_translate = cmds.floatSlider( min=0.5, max=1, value=0.8, step=0.05, dc = conserve_onchange_translate )
cmds.separator( style='none',h = 5)
 
 
cmds.text(l = 'Weight')
weight_translate = cmds.floatSlider( min=0.5, max=1, value=0.7, step=0.05, dc = weight_onchange_translate )
cmds.separator( style='none',h = 5)
 
 
cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100),(2,60),(3, 110)] )
cmds.button(l = 'Apply', c = apply_translate)
cmds.separator( style='none')
trans_sep_layer = cmds.checkBox( label='To separate layer', v = False, onc = trans_sep_layer_on, ofc = trans_sep_layer_off )
cmds.button(l = 'Cancel', c = clean)
cmds.separator( style='none')
trans_one_layer = cmds.checkBox( label='To one layer', v = True, onc = trans_one_layer_on, ofc = trans_one_layer_off )
 
 
cmds.tabLayout(Headtabs, edit=True, tabLabel=((FK, "Rotate"), (IK, "Translate")))
 
cmds.showWindow()
 
 
