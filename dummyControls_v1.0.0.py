##  Dummy Controls By Virbhadra Gupta
##  give your feedback at viru.gupta8@gmail.com
##  write to me in case of any issue
##  Happy Animating :)

import maya.cmds as cmds

class dummy_control():
    def __init__(self):
        self.window_id = 'valueWindow'
        if cmds.window (self.window_id, ex=True):
            cmds.deleteUI (self.window_id)
        cmds.window (self.window_id, t='Dummy Controls', h=75, w=150, sizeable=False, mxb= False, mnb=False)
        cmds.columnLayout (adj=True)
        self.value_field = cmds.intFieldGrp (l='Number of controls', v1=2, cw=[50,50], cal =[1, "center"])
        cmds.button (l='Create', c='dummy_pros()')
    
    def show_win (self):
        cmds.showWindow (self.window_id)
        cmds.window (self.window_id, e=True, h=75, w=250)

def namespace_breaker(object):
    if ":" in object:
        place = object[::-1].index(":")
        obj_name, obj_namespace = object[len(object)-place::], object[0:len(object)-place-1]
    else:
        obj_name, obj_namespace = object, None
    return obj_namespace, obj_name

def dummy_pros():
    selection = cmds.ls (sl=True, tr=True)
    if not len (selection):
        cmds.warning ('Select any controls.')
        return
    number_copies = cmds.intFieldGrp(dummy_tool.value_field, q=True, v1=True)
    if not number_copies>1:
        cmds.warning("Minimum 2 controls required.")
        return
    for control in selection:
        test = connection_tester(control)
        if test:
            cmds.warning("unable to create Dummy Controls, '"+str(control),"' have incoming connections.")
            return
        grp_name = select_group(control)
        if grp_name[0]==control:
            cmds.warning("No group/parent found in hierarchy for '"+str(control)+"'.")
            cmds.select(selection)
            return
        control_shape = cmds.listRelatives(control, s=True)
        control_type = None
        for shape in control_shape:
            try:
                shape_type = cmds.nodeType(shape)
            except RuntimeError:
                shape_type, control_type = "error", "error"
            if shape_type=="nurbsCurve":
                control_type="nurbsCurve"
        dummy_conrtol = create_dummy(control, type=control_type)
        apply_override(dummy_conrtol)
        g_tran, g_rot = get_ws(control)
        dummy_conrtol_list = []
        dummy_grp = cmds.group(n="dummy_control_group_0#", em=True)
        scale_up = 0.93
        for count in range(0, number_copies):
            dummy_copy = cmds.duplicate(dummy_conrtol)
            cmds.scale(scale_up,scale_up,scale_up, dummy_copy)
            dummy_conrtol_list.append(dummy_copy[0])
            scale_up-=.08
        if len(dummy_conrtol_list)>1:
            end_range = len(dummy_conrtol_list)-1
            for num in range (0,end_range):
                cmds.parent(dummy_conrtol_list[num+1],dummy_conrtol_list[num])
            cmds.parent(dummy_conrtol_list[0], dummy_grp)
            cmds.makeIdentity(dummy_conrtol_list[0], apply=True, t=True, r=True, s=True)
        else:
            cmds.parent(dummy_conrtol_list[0], dummy_grp)
        cmds.move(g_tran[0],g_tran[1],g_tran[2],dummy_grp)
        cmds.rotate(g_rot[0],g_rot[1],g_rot[2],dummy_grp)
        cmds.parent(dummy_grp, grp_name)
        cmds.parentConstraint(dummy_conrtol_list[-1],control, mo=True)
        cmds.delete(dummy_conrtol)

def apply_override(object):
    cmds.makeIdentity(object, apply=True, t=True, r=True, s=True)
    dummy_object_shape = cmds.listRelatives(object, s=True)
    for shape in dummy_object_shape:
        if cmds.nodeType(shape) == "nurbsCurve":
            cmds.setAttr ((str(shape)+'.overrideEnabled'), 1)
            cmds.setAttr ((str(shape)+'.overrideColor'), 17)

def select_group(object):
    cmds.select(object)
    cmds.pickWalk(d="up")
    grp_name = cmds.ls(sl=True)
    cmds.select(cl=True)
    return grp_name

def get_ws(object):
    loc = cmds.spaceLocator(n="dummy_locator_0#")[0]
    cmds.parentConstraint(object, loc, mo=False)
    g_tran = cmds.xform(loc, q=True, t=True, ws=True)
    g_rot = cmds.xform(loc, q=True, ro=True, ws=True)
    cmds.delete(loc)
    return g_tran, g_rot

def create_dummy(object, type="mesh"):
    scale_multi = 1.5
    obj_namespace, obj_name = namespace_breaker(object)
    if not type=="nurbsCurve":
        dummy_conrtol = dummy_from_bb(object, obj_name, scale_multi)
    elif type == "error":
        temp_copy = cmds.duplicate(object, rc=True)
        if len(temp_copy)>1:
            cmds.delete(temp_copy[1::])
        loc = cmds.spaceLocator(n="dummy_locator_0#")[0]
        cmds.parentConstraint(loc, temp_copy[0], mo=False)
        cmds.delete(loc)
        refine_attrs(temp_copy[0])
        try:
            surface = cmds.Planar(temp_copy[0])
        except:
            surface = cmds.revolve(temp_copy[0])
        dummy_conrtol = dummy_from_bb(surface, obj_name, scale_multi)
        cmds.delete(surface)

    else:
        name = obj_name+"_dummy_control_00"
        copy_obj = cmds.duplicate(object, rc=True)
        if len(copy_obj)>1:
            cmds.delete(copy_obj[1::])
        loc = cmds.spaceLocator(n="dummy_locator_0#")[0]
        cmds.parentConstraint(loc, copy_obj[0], mo=False)
        cmds.delete(loc)
        refine_attrs(copy_obj[0])
        cmds.scale(scale_multi,scale_multi,scale_multi, copy_obj[0])
        cmds.makeIdentity(copy_obj[0], apply=True, t=True, r=True, s=True)
        name = cmds.rename(copy_obj[0], name)
        dummy_conrtol = name
        cmds.refresh()
    return dummy_conrtol

def connection_tester(object):
    main_attrs = ["translateX","translateY","translateZ","rotateX","rotateY","rotateZ"]
    for attr in main_attrs:
        connections = cmds.listConnections(str(object)+"."+attr)
        if connections:
            if len(connections)==1 and attr in connections:
                incoming_connection = False
            else:
                incoming_connection = True
                break
        else:
            incoming_connection = False
    return incoming_connection

def dummy_from_bb(object, obj_name, scale_multi):
    obj_bb = cmds.xform(object, q=True, bb=True)
    scaleX = abs(obj_bb[3]-obj_bb[0])
    scaleY = abs(obj_bb[4]-obj_bb[1])
    scaleZ = abs(obj_bb[5]-obj_bb[2])
    dummy_conrtol = dummy_curve(obj_name)
    cmds.scale(scaleX*scale_multi, scaleY*scale_multi, scaleZ*scale_multi, dummy_conrtol)
    cmds.refresh()
    return dummy_conrtol

def refine_attrs(object):
    attr_list = cmds.listAttr (object,ud=True)
    if attr_list:
        for attr in attr_list:
            cmds.setAttr (str(object)+'.'+str(attr), lock=False)
            cmds.deleteAttr (object,at=attr)
    scale_attrs = [".sx", ".sy", ".sz"]
    for attrs in scale_attrs:
        cmds.setAttr ((str(object)+attrs), cb=True)
        cmds.setAttr ((str(object)+attrs),lock=False)
        cmds.setAttr ((str(object)+attrs), k=True)
        cmds.delete((str(object)+attrs), icn=True)

def dummy_curve(name):
    name = name+"_dummy_control_00"
    dummy_obj = cmds.curve(n=name,d=1, p=[(-0.5,0.5,-0.5),(-0.5, 0.5, 0.5),(-0.5, -0.5, 0.5),(-0.5, -0.5, -0.5),
                    (-0.5, 0.5, -0.5 ),(0.5, 0.5, -0.5),(0.5, -0.5, -0.5),(-0.5, -0.5, -0.5 ),
                    (-0.5, -0.5, 0.5),(0.5, -0.5, 0.5),(0.5, 0.5, 0.5),(0.5, 0.5, -0.5),
                    (0.5, -0.5, -0.5),(0.5, -0.5, 0.5),(0.5, 0.5, 0.5),(-0.5, 0.5, 0.5)],
                     k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    return dummy_obj

dummy_tool = dummy_control()
dummy_tool.show_win()