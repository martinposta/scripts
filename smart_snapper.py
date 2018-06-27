##  Smart Snapper By Virbhadra Gupta
##  give your feedback at viru.gupta8@gmail.com
## 	write to me in case of any issue
##  Happy Animating :)

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya

class Snapper_ui():
	def __init__(self):
		self.window_id = "SnapperWin"
		self.global_pos = None
		self.selection_job = None
		self.offset_state = None
		self.offset_loc = None
		self.child_status = None
		if cmds.window(self.window_id, ex=True):
		    cmds.deleteUI(self.window_id)
		cmds.window(self.window_id, t="Smart Snapper", w=175, h=50, sizeable=False, mnb=False, mxb=False)
		cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 15), (3, 150)] )
		self.check_box = cmds.checkBox(l="", v=False, en=True, w=15, cc="smart_Snapper.toggle_button()")
		self.smart_button = cmds.button(l="Copy", w=150, c="per_main()", bgc=(0.4,0.4,0.4))
		cmds.text(l="")
		cmds.text(l="By: Virbhadra Gupta",fn="smallPlainLabelFont")

	def toggle_button(self):
		if cmds.checkBox(self.check_box, q=True, v=True):
			cmds.button(self.smart_button, e=True, l="Lock All", c="per_main()", bgc=(0.6,0.6,0.6))
		else:
			cmds.button(self.smart_button, e=True, l="Copy", c="per_main()", bgc=(0.4,0.4,0.4))
		
	def show_win(self):
	    cmds.showWindow(self.window_id)
	    cmds.window(self.window_id, e=True, w=165, h=50)
		    
smart_Snapper = Snapper_ui()
smart_Snapper.show_win()

def get_range():
    time_slider = mel.eval('$tmpVal=$gPlayBackSlider')
    range = cmds.timeControl(time_slider, q=True, ra=True)
    frame_range = [int(range[0]), int(range[1])]
    return frame_range
    
def get_ws(objects):
    global_pos = []
    for obj in objects:
    	loc = create_loc(number=1)[0]
    	cmds.parentConstraint(obj, loc, mo=False)
        g_tras = cmds.xform(loc, q=True, ws=True, t=True)
        g_rot = cmds.xform(loc, q=True, ws=True, ro=True)
        global_pos.append([g_tras,g_rot])
        cmds.delete(loc)
    return global_pos
    
def do_parent(objects, traget_child, offset=True):
	if len(objects)>1 and len(traget_child)>1 and type(objects)==list and len(objects)==len(traget_child):
	    for obj, trg in zip(objects,traget_child):
	        cmds.parentConstraint(obj, trg, mo=offset)
	else:
		if type(traget_child)==list:
			for traget in traget_child:
			    cmds.parentConstraint(objects[0], traget, mo=offset)
		else:
			cmds.parentConstraint(objects, traget_child, mo=offset)
                
def create_loc(number=1):
    loc_list=[]
    if number >1:
        for num in range (0, number):
            loc = cmds.spaceLocator(n="dummy_smart_snap_locator_offset_#")[0]
            cmds.setAttr(str(loc)+(".v"),0)
            loc_list.append(loc)
    elif number ==0:
        pass
    else:
        loc = cmds.spaceLocator(n="dummy_smart_snap_locator_#")[0]
        cmds.setAttr(str(loc)+(".v"),0)
        loc_list.append(loc)
    return loc_list

def loc_snap(object, loc):
	do_parent(object, loc, offset=False)
	key_test(loc)
	cmds.select(loc)
	cmds.DeleteConstraints(loc)

def object_snap(object, ws_pos):
	loc = create_loc(number=1)
	cmds.move(ws_pos[0][0], ws_pos[0][1],ws_pos[0][2],loc[0])
	cmds.rotate(ws_pos[1][0], ws_pos[1][1],ws_pos[1][2],loc[0])
	loc_snap(loc, object)
	cmds.delete(loc)

def snap_for_offset(object, loc_list):
	loc_snap(object, loc_list)
	loc = loc_list.pop(0)
	loc_list.append(loc)
	cmds.parent(loc_list)

def key_test(object):
	if cmds.keyframe(object, q=True, kc=True):
		cmds.setKeyframe(object)

def create_hold(object):
    frame_range = get_range()
    loc=create_loc(number=1)
    cmds.currentTime(frame_range[0])
    do_parent(loc, object, offset=True)
    for frame in range(frame_range[0],frame_range[1]):
        cmds.currentTime(frame)
        cmds.setKeyframe(object)
    cmds.delete(loc)

def hold_with_offset(objects, loc_list, frame_range):
	cmds.currentTime(frame_range[0])
	cmds.parentConstraint(objects[0], loc_list[0], mo=False)
	for frame in range(frame_range[0], frame_range[1]):
		cmds.currentTime(frame)
		for  obj, loc in zip(objects[1:], loc_list[1:]):
			loc_snap(loc, obj)
		cmds.setKeyframe(objects[1:])
	cmds.delete(loc_list)

def child_test(objects):
	list = []
	for each in objects[1:]:
		child_list = cmds.listRelatives(each, ad=True, typ="transform")
		if child_list:
			for child in child_list:
				if not objects[0] in list:
					list.append(child)
	if objects[0] in list:
		return True
	else:
		return False

def child_snapper(objects, loc_list, frame_range):
	for frame in range(frame_range[0], frame_range[1]):
		cmds.currentTime(frame)
		cmds.parentConstraint(objects[0], loc_list[0], mo=False)
		cmds.setKeyframe(loc_list[0])
		cmds.setKeyframe(str(loc_list[0])+(".blendParent1"), v=1)
	cmds.parentConstraint(objects[0], loc_list[0], rm=True)
	for frame in range(frame_range[0], frame_range[1]):
		cmds.currentTime(frame)
		for  obj, loc in zip(objects[1:], loc_list[1:]):
			loc_snap(loc, obj)
			cmds.setKeyframe(loc_list)
		loc_snap(loc_list[0], objects[0])
		cmds.setKeyframe(objects)
	cmds.delete(loc_list)
    
def per_main():
	selection = cmds.ls(sl=True)
	frame_range = get_range()
	status = child_test(selection)
	if not selection:
		cmds.warning("Please select sometting.")
		return
	if len(selection) >15:
		message = "Too many objects, it might take time. Do you want to continue ?"
		confirm_input = cmds.confirmDialog(t='Confirm', m=message, b=['Yes','No'], cb='No', ds='No')
		if confirm_input == "Yes":
			pass
		else:
			return
	if len(selection)==1 or (len(selection)>1 and cmds.checkBox(smart_Snapper.check_box, q=True, v=True)==True):
		if frame_range[1]-frame_range[0]==1:
			global_val = get_ws(selection)
			smart_Snapper.global_pos = global_val
			smart_Snapper.offset_state = False
			cmds.button(smart_Snapper.smart_button, e=True, l="Paste", w=150, c="post_main()", bgc=(0.2,0.6,0.8))
			cmds.checkBox(smart_Snapper.check_box, e=True, v=False, en=False)
		else:
			create_hold(selection)
		cmds.select(selection)
	else:
		loc_list = create_loc(number=len(selection))
		tmp_list = loc_list[0:]
		cmds.currentTime(frame_range[0])
		snap_for_offset(selection, tmp_list)
		if frame_range[1]-frame_range[0]==1:
			cmds.select(selection)
			if status:
				smart_Snapper.child_status = True
			job = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", selection_tester)
			smart_Snapper.offset_loc = loc_list
			smart_Snapper.selection_job = job
			smart_Snapper.offset_state = True
			cmds.button(smart_Snapper.smart_button, e=True, l="Paste", w=150, c="post_main()", bgc=(0.2,0.6,0.8))
			cmds.checkBox(smart_Snapper.check_box, e=True, v=False, en=False)
		else:
			if status:
				child_snapper(selection, loc_list, frame_range)
				smart_Snapper.child_status = False
			else:
				hold_with_offset(selection, loc_list, frame_range)
			cmds.select(selection)
	        
def post_main():
	selection = cmds.ls(sl=True)
	frame_range = get_range()
	if smart_Snapper.offset_state:
		OpenMaya.MMessage.removeCallback(smart_Snapper.selection_job)
		if smart_Snapper.child_status:
			child_snapper(selection, smart_Snapper.offset_loc, frame_range)
		else:
			hold_with_offset(selection, smart_Snapper.offset_loc, frame_range)
		smart_Snapper.offset_loc=None
		smart_Snapper.child_status = None
	else:
		if len(selection) != len(smart_Snapper.global_pos):
			cmds.warning("You must select same number of objects.")
			return
		loc=create_loc(number=len(smart_Snapper.global_pos))
		for obj, pos in zip(loc, smart_Snapper.global_pos):
			object_snap([obj], pos)
		do_parent(loc, selection, offset=False)
		for frame in range(frame_range[0], frame_range[1]):
			cmds.currentTime(frame)
			cmds.setKeyframe(selection)
		cmds.delete(loc)
		smart_Snapper.global_pos=None
	cmds.select(selection)
	cmds.button(smart_Snapper.smart_button, e=True, l="Copy", w=150, c="per_main()", bgc=(0.4,0.4,0.4))
	cmds.checkBox(smart_Snapper.check_box, e=True, v=False, en=True)

def selection_tester(*args, **kwargs):
	loc_list = cmds.ls("dummy_smart_snap_locator*")
	cmds.delete(loc_list)
	cmds.warning("Selection Changed.")
	cmds.button(smart_Snapper.smart_button, e=True, l="Copy", w=150, c="per_main()", bgc=(0.4,0.4,0.4))
	cmds.checkBox(smart_Snapper.check_box, e=True, v=False, en=True)
	OpenMaya.MMessage.removeCallback(smart_Snapper.selection_job)
