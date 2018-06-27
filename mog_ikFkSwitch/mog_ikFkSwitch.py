import pymel.core as pm
import maya.OpenMaya as om
import logging

"""
// Universal IK FK
// version 1.6
// April 29, 2018
// Monika Gelbmann
// monikagelbmann@gmail.com
// www.monikagelbmann.com

	Universal IK FK Switch and Match Tool

	DESCRIPTION:
	This script lets you switch and match Poses between IK/FK controls in the animation scene.

	Works for Riggs that don't have IK/FK match built in and requires only Standard FK controls and IK Pole Vector Setup.
	The Controls are defined once and can be stored in Node for easy re use throughout the animation.

	1. Define Limb to work on
	This always needs to be defined bofore loading/storing/switching
	Sides are treated seperately to not be restriced by naming convention

	2. Define Ctrls necessary by selecting them and hit the << button
	<< FK1: Upper arm
	<< FK2: Lower arm
	<< FK3: Hand
	<< IK Ctrl: IK Hand
	<< IK Pole:
	<< Switch Ctrl: The ctrl that is used to switch between ik and fk mode
	<< Switch Attr: The attribute that is dialed to switch.
					It can be highlighted in the channel box and hit <<

	Rotation Offset:
	Some Riggs have different orientations in their IK and FK ctrls and joints.
	This becomes obvious when running 'Match' and seeing a 90 degree offset in the wrist
	Set the offset and run 'Match' again to align them

	Switch IK/FK: Simple switches between the modes (does not do any matching)

	Select all IK or FK ctrls

	Key all IK/FK controsl on current frame

	Bake IK/FK: Bake the entire frame range to ik or fk. Leaves source keys clean

	USAGE:
	import pymel.core as pm
	import mog_ikFkSwitch as mog_ikFkSwitch
	reload(mog_ikFkSwitch)
	mog_ikFkSwitch.FkIk_UI()

	LIMITATIONS:
	- Pole Vector Control is required and will not run if controlled with attribute
	- Works only on Referenced Riggs


	Future Improvements/Optimzations planned:
	 -   Make script work/not error if there is no polevector
	 -   create nodes in Rigg files and look for Referenced Nodes on Load
	 -	 function on non-referenced riggs

	VERSIONS:
	1.6 - August 27, 2017 - Offset Value Bug fix. Storing float values now.
	1.5 - August 27, 2017 - Blend Value 1 - 10 bug fix
							Pro version: Bake range and Set Keyframe for all IK/FK ctrls
							Free version: Select all ik/fk ctrls
	1.4 - April 24, 2017 - Beta release. New interface. Auto detect limbs by selecting
	1.1 - Jan 12, 2017 - Improvement to interface and bug fixes.
	1.0 - Jan 07, 2017 - Initial Release.

// Questions/comments/bugissues to
// monikagelbmann@gmail.com

"""

debug = False
_logger = logging.getLogger(__name__)

class FkIk_UI:
	COLOR_PRESETS = {
		"grey": (.5, .5, .5),
		"lightgrey": (.7, .7, .7),
		"darkgrey": (.25, .25, .25),
		"turquoise": (.3, .55, .55)}

	def __init__(self):
		global win
		win ='ikfkswitchUI_'

		# on off logging

		#logging.basicConfig(level=logging.INFO)
		_logger.disabled = not debug

		if pm.window("ikFkSwitch_UI", exists=True):
			pm.deleteUI("ikFkSwitch_UI")
		windowWidth = 320
		windowHeight = 250

		window = pm.window("ikFkSwitch_UI", width=windowWidth, height=windowHeight, title="Universal IK FK")
		topLevelColumn = pm.columnLayout(adjustableColumn=True, columnAlign="center")

		#Setup Tabs #every child creates new tab
		tabHeight = 250
		tabWidth = 300
		scrollWidth = tabWidth - 40

		riggTab = self.initializeTab(tabHeight, tabWidth)
		pm.setParent("..")

		#Display window
		pm.showWindow("ikFkSwitch_UI")

	def initializeTab(self, tabHeight, tabWidth):
		frameWidth = tabWidth - 20
		mainColumnLayout = pm.columnLayout(win+"mainColumnLayout", w=tabWidth,columnAttach=('left', 10))
		pm.setParent(win + "mainColumnLayout")
		##
		####################### SETUP FRAME ##############################
		##
		pm.frameLayout(win+"setupFrameLayout", w=tabWidth, label="Setup Store Node",collapsable=True, collapse=True )

		pm.separator(h=10)
		pm.text('1. Choose Limb ')
		pm.separator(h=10)

		pm.columnLayout(win + 'ctrlinputColumn', cal='left', columnWidth=20)
		pm.rowLayout(win+"switchLimb", numberOfColumns=5)
		self.collection2 = pm.radioCollection(win+'limbRadioCollt')
		self.rb1 = pm.radioButton(win+'R_arm', w=frameWidth/5, label='R Arm')
		self.rb2 = pm.radioButton(win+'L_arm', w=frameWidth/5, label='L Arm')
		self.rb3 = pm.radioButton(win+'R_leg', w=frameWidth/5, label='R Leg')
		self.rb4 = pm.radioButton(win+'L_leg', w=frameWidth/5, label='L Leg')
		pm.button(label='   From Sel   ', w=frameWidth/5, command=lambda a:self.autoDetectSideAndLimbWin())
		pm.setParent(win+"setupFrameLayout")

		pm.separator(h=10)
		pm.text('2. Define Controls')
		pm.separator(h=10)

		pm.textFieldButtonGrp(win+'fkshldrTfb', label='', text='', cw3=(0,200,100), ad3=3,  buttonLabel=' < FK Upper Limb', bc=lambda:self.inputSelTfb("fkshldrTfb"), columnAlign3=("right", "left", "left"))
		pm.textFieldButtonGrp(win+'fkellbowTfb', label='', text='', cw3=(0,200,100), ad3=3, buttonLabel='< FK Lower Limb', bc=lambda:self.inputSelTfb("fkellbowTfb"))
		pm.textFieldButtonGrp(win+'fkwristTfb', label='', text='', cw3=(0,200,100), ad3=3,  buttonLabel='< FK Wrist/Foot', bc=lambda:self.inputSelTfb("fkwristTfb"))
		pm.textFieldButtonGrp(win+'ikwristTfb', label='', text='',cw3=(0,200,100), ad3=3,   buttonLabel='< IK Wrist/Foot', bc=lambda:self.inputSelTfb("ikwristTfb"))
		pm.textFieldButtonGrp(win+'ikpvTfb', label='', text='', cw3=(0,200,100), ad3=3,  buttonLabel='< Pole Vector', bc=lambda:self.inputSelTfb("ikpvTfb"))



		pm.setParent(win+"setupFrameLayout")
		# pm.setParent(self.UIElements["mainColumnLayout"])
		#

		pm.textFieldButtonGrp(win+'switchCtrlTfb', label='', cw3=(0,200,100), ad3=3,  text='', buttonLabel='< Switch Ctrl', bc=lambda:self.inputSelTfb("switchCtrlTfb"))
		pm.textFieldButtonGrp(win+'switchAttrTfb', label='', cw3=(0,200,100), ad3=3,  text='', buttonLabel='< Switch Attr', bc=lambda:self.inputChannelboxSelectionTbf("switchAttrTfb"))

		pm.rowLayout(win+"ikIsValueRow", numberOfColumns=3)
		pm.text('Attribute on 0 is', w=frameWidth/3)
		collection2 = pm.radioCollection(win+'switch0isfkTfb')
		rb1 = pm.radioButton(win+'attr0IsIk', label='IK mode', w=frameWidth/3)
		rb2 = pm.radioButton(win+'attr0IsFk', label='FK mode', w=frameWidth/3)
		pm.radioCollection(win+"switch0isfkTfb", e=1, select=rb2)
		pm.setParent(win+"setupFrameLayout")

		pm.rowLayout(win+"ikIsRangeRow", numberOfColumns=3)
		pm.text('Attribute Range', w=frameWidth/3)
		collection2 = pm.radioCollection(win+'switchAttrRangeTfb')
		rb1 = pm.radioButton(win+'attr1', label='0 to 1', w=frameWidth/3)
		rb2 = pm.radioButton(win+'attr10', label='0 to 10', w=frameWidth/3)
		pm.radioCollection(win+"switchAttrRangeTfb", e=1, select=rb1)
		pm.setParent(win+"setupFrameLayout")


		pm.rowColumnLayout("rotOffsetRow", numberOfColumns=4, columnWidth=[(1,frameWidth/4), (2,frameWidth/4), (3,frameWidth/4)])
		pm.text(l='rotOffset')
		pm.textField(win+'rotOffsetX', tx=0)
		pm.textField(win+'rotOffsetY', tx=0)
		pm.textField(win+'rotOffsetZ', tx=0)
		pm.setParent(win + "setupFrameLayout")

		# store for clearing
		self.inputTxtFldBtnGrps = [win+"fkshldrTfb",win+"fkellbowTfb",win+"fkwristTfb",  win+"ikwristTfb",
							  win+"ikpvTfb",win+"switchCtrlTfb",win+"switchAttrTfb"]
		self.inputTxtFlds = [ win+"rotOffsetX", win+"rotOffsetY", win+"rotOffsetZ"]

		pm.button(label='   Save/Update  ', w=300, bgc=self.COLOR_PRESETS["turquoise"], command=lambda a:self.saveIkFkCtrlsWin())
		pm.button(label='Load',  bgc=self.COLOR_PRESETS["darkgrey"], w=300, h=20, command=lambda a: self.loadIkFkCtrlsWin())
		pm.button(label='clear Fields', bgc=self.COLOR_PRESETS["darkgrey"], w=300, h=20,command=lambda a: self.clearInputFields())

		pm.separator(h=10)
		##
		####################### HELP FRAME ##############################
		##
		pm.setParent(win + "mainColumnLayout")
		pm.frameLayout(win + "helpFrameLayout", w=300, label="Help", collapsable=True, collapse=True)
		pm.columnLayout(win + 'helpColumn', cal='left', columnWidth=300)
		pm.scrollField(w=300, wordWrap = True, editable=False, tx='Use <<< Button to Fill the Fields by what you have selected in the Viewport.\n\n' +
							  'Switch Ctrl: Choose the Ctrls that sets IK/FK mode\n\n' +
							  'Switch Attr: Highlight the "ikfk"  Attribute in the Channelbox and hit <<\n\n' +
					   		  'Switch Ctrl: Choose the Ctrls that sets IK/FK mode\n\n'	)
		pm.separator(h=10)


		#pm.button(label='   Load   ', w=300, command=lambda a:self.loadIkFkCtrlsWin())

		##
		####################### MATCH FRAME ##############################
		##
		pm.setParent(win+"mainColumnLayout")
		pm.frameLayout(win + "matchFrameLayout", w=300, label="Match and Switch", collapsable=True )
		pm.text('3. Match / Switch')
		pm.separator(h=10)
		pm.button(label='Load Store Node from Selection', w=300, command=lambda a: self.findStoreNodeFromSelectionWin())
		self.readyText = pm.text(win + 'readyText', label='Not Ready.', align='left', bgc=(.6,.4,.4))
		pm.separator(h=10)
		pm.rowColumnLayout(win+"matchIKRow", numberOfColumns=2, columnWidth=[(1,150), (2,150)])
		pm.button(label="Match IK >> FK", command=lambda a: self.matchIkFkWin(tofk=1))
		pm.button(label="Match FK >> IK", command=lambda a: self.matchIkFkWin(tofk=0))
		pm.setParent(win+"matchFrameLayout")

		pm.rowColumnLayout(win+"switchIKRow", numberOfColumns=2, columnWidth=[(1,150), (2,150)])
		pm.button(label="Switch IK", command=lambda a: self.switchIkFkWin())
		pm.button(label="Switch FK", command=lambda a: self.switchFkIkWin())
		pm.button(label="Select all IK", command=lambda a: self.selectAll(fk=0))
		pm.button(label="Select all FK", command=lambda a: self.selectAll(fk=1))
		pm.setParent(win+"matchFrameLayout")
		pm.setParent(win+"mainColumnLayout")

		pm.separator(h=5)
		pm.text('Release 1.0                  Monika Gelbmann                     01/2017')
		pm.separator(h=5)

	def inputSelTfb(self, name):
		if len(pm.selected()) == 0:
			pm.textFieldButtonGrp(win+name, e=1, tx='')
			return []
		pm.textFieldButtonGrp(win+name, e=1, tx=pm.selected()[0])


	def getAndCheckInputWin(self):

		inputValues = []
		errorFields = []

		# switch 0 is radio
		switch0isfkTfb= pm.radioCollection(win+"switch0isfkTfb", q=1, sl=1)

		if switch0isfkTfb == 'ikfkswitchUI_attr0IsFk':
			_logger.info( 'FK switch0isfk is %s'%switch0isfkTfb    )
			switch0isfk = 1
		else:
			_logger.info('IK switch0isfk is %s'%switch0isfkTfb        )
			switch0isfk = 0

		# switch range radio
		switchAttrRangeTfb = pm.radioCollection(win+"switchAttrRangeTfb", q=1, sl=1)
		if switchAttrRangeTfb == 'ikfkswitchUI_attr1':
			switchAttrRange = 1
		else:
			switchAttrRange = 10



		# check empty input text fields
		for inputTxtFldBtnGrp in self.inputTxtFldBtnGrps:
			input = pm.textFieldButtonGrp(inputTxtFldBtnGrp, q=1, tx=1)

			if len(input) == 0:
				errorFields.append(pm.textFieldButtonGrp(inputTxtFldBtnGrp, q=1, buttonLabel=1))

		if len(errorFields) > 0:
				message = 'Empty input field found. Please pick Ctrl to use.\n%s'%errorFields
				self.popupWarning(message)
				pm.error(message)
				return False


		# check ctrls are valid and do exist
		for inputTxtFldBtnGrp in self.inputTxtFldBtnGrps[:-1]:
			input = pm.textFieldButtonGrp(inputTxtFldBtnGrp, q=1, tx=1)
			if pm.objExists(input) == 0:
				errorFields.append(pm.textFieldButtonGrp(inputTxtFldBtnGrp, q=1, buttonLabel=1))
			else:
				inputValues.append(input)
		if len(errorFields) > 0:
				message = 'Non existing ctrls found. Check those names are correct:\n%s'%errorFields
				self.popupWarning(message)
				pm.error(message)
				return False

		# check switch attribute
		ctrlInput = pm.textFieldButtonGrp(self.inputTxtFldBtnGrps[-2], q=1, tx=1)
		attrInput = pm.textFieldButtonGrp(self.inputTxtFldBtnGrps[-1], q=1, tx=1)
		attr = '%s.%s'%(ctrlInput, attrInput)
		if pm.objExists(attr) == False:
				message = 'Switch Attribute does not exist. Check the naming:\n%s'%attr
				pm.warning(message)
				self.popupWarning(message)
				pm.error(message)
				return False
		else:
			inputValues.append(attrInput)


		# limb radio box
		limbRadio = pm.radioCollection(win+"limbRadioCollt", q=1, sl=1)
		_logger.info('raidobuttons: %s' % limbRadio)
		if limbRadio == 'NONE':
			message = 'Limb choice missing. Please choose R Arm / L Arm / R Leg / L Leg'
			self.popupWarning(message=message)
			pm.warning(message)
			return False

		###TODO IK PIV can stay empty...
		###TODO how to align with fk if there is no pv in ik
		# if pm.objExists(ikpv) == 0:
		#     pm.error('Input Piv %s does not exist. Aborting'%input)
		#     return False


		# validate offset numeric input fields
		rotOffsetX = pm.textField(win+'rotOffsetX', q=1, tx=1)
		logging.info('checking offsets')
		try:
			rotOffsetX = float(rotOffsetX)
		except:
			rotOffsetX = 0
			pass
		rotOffsetY = pm.textField(win+'rotOffsetY', q=1, tx=1)
		try:
			rotOffsetY = float(rotOffsetY)
		except:
			rotOffsetY = 0
			pass
		rotOffsetZ = pm.textField(win+'rotOffsetZ', q=1, tx=1)
		try:
			rotOffsetZ = float(rotOffsetZ)
		except:
			rotOffsetZ = 0
			pass
		rotOffset=[rotOffsetX, rotOffsetY, rotOffsetZ]


		inputValues.append(switch0isfk)
		inputValues.append(switchAttrRange)
		inputValues.append(rotOffset)

		_logger.info('returning %s'%inputValues)
		return inputValues


	def clearInputFields(self):
		# query text input fields
		for inputTxtFldBtnGrp in self.inputTxtFldBtnGrps:
			pm.textFieldButtonGrp(inputTxtFldBtnGrp, e=1, tx='')
		for inputTxtFld in self.inputTxtFlds:
			pm.textField(inputTxtFld, e=1, tx='')

	def popupWarning(self, message, title='Input Error'):

		result = pm.confirmDialog(
			title=title,
			message=message,
			button=['OK'],
			defaultButton='OK',)

		return result


	def autoDetectSideAndLimbWin(self):
		side, limb = autoDetectSideAndLimb(pm.selected()[0])
		if side and limb:
			pm.displayInfo( 'Matching Side and Limb found: %s %s'%(side, limb))
			if side == 'R' and limb == 'arm': pm.radioCollection(win+'limbRadioCollt' , edit=1, select=self.rb1)
			elif side == 'L' and limb == 'arm': pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb2)
			elif side == 'R' and limb == 'leg': pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb3)
			elif side == 'L' and limb == 'leg': pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb4)
			self.loadIkFkCtrlsWin()

	def inputChannelboxSelectionTbf(self, name):
		channelBox = pm.mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')	#fetch maya's main channelbox
		attrs = pm.channelBox(channelBox, q=True, sma=True)

		if not attrs:
			pm.textFieldButtonGrp(win+name, e=1, tx='')
			return []
		if len(attrs) is not 1:
			pm.warning('Highlight only the IK/FK Switch Attribute in the Channelbox')
			return []
		pm.textFieldButtonGrp(win+name, e=1, tx=attrs[0])
		return attrs

	def findStoreNodeFromSelectionWin(self):
		store_node = findStoreNodeFromSelection()
		_logger.debug( 'store node found is %s'%store_node)
		if store_node == []:
			message = 'No Storenode found for Selection. Fill out Setup section first and hit SAVE for future detection'
			pm.warning(message)
			#self.popupWarning(message)
			pm.text(self.readyText, e=1, label='No Storenode found. Use Setup. Not Ready.', align='left', bgc=(.6,.4,.4))


		else:
			ns = store_node.split('__')[0] if len(store_node.split('__'))>0 else ''
			side = store_node.split('_')[-3]
			limb = store_node.split('_')[-2]
			pm.displayInfo( 'Storenode found for %s %s. Loading %s'%(side, limb, store_node))
			if side and limb:
				_logger.info( 'Machting Side and Limb found')
				if side == 'R' and limb == 'arm':
					pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb1)
				elif side == 'L' and limb == 'arm':
					pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb2)
				elif side == 'R' and limb == 'leg':
					pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb3)
				elif side == 'L' and limb == 'leg':
					pm.radioCollection(win + 'limbRadioCollt', edit=1, select=self.rb4)
			self.loadIkFkCtrlsWin()
			pm.text(self.readyText, e=1, label='Storenode found >> %s %s. Ready.'%(side,limb), align='left', bgc=(.4,.6,.4))


	def saveIkFkCtrlsWin(self):
		fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset = self.getAndCheckInputWin()
		limbRadio = pm.radioCollection(win+"limbRadioCollt", q=1, sl=1)
		if limbRadio == 'NONE':
			pm.warning('Limb choice missing. Please choose form the UI options')
			return False
		limb = limbRadio.split('_')[-1]
		side = limbRadio.split('_')[1]

		storeNode =  saveIKFkCtrls(limb, side, fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset)
		if storeNode:
			self.popupWarning(message = 'Successfully saved.', title='Storenode saved')

	def loadIkFkCtrlsWin(self):
		limbRadio = pm.radioCollection(win+"limbRadioCollt", q=1, sl=1)

		if limbRadio == 'NONE':
			message = 'Limb choice missing. Please choose R Arm / L Arm / R Leg / L Leg'
			self.popupWarning(message=message)
			pm.warning(message)
			return False

		limb = limbRadio.split('_')[-1] # limbRadio  = ikfkswitchUI_R_arm
		side = limbRadio.split('_')[1]

		if len(pm.selected()) == 0:
			pm.warning('Select anything from the rigg')
			return False
		ns = pm.selected()[0].split(':')[0] if len(pm.selected()[0].split(':')) > 1 else ''

		storedic = loadIkFkCtrl(ns, limb, side)

		if len(storedic) == 0:
			pm.warning('No Store Node for %s. Define Limbs and Save Store Node'%limb)
		else:
			pm.displayInfo( 'Found Store Node for %s. Loading.'%limb  )

		for attrName, value in storedic.items():
			if attrName is 'switch0isfk':
				_logger.info('load switch0isfk is %s'%value )
				if value == '0':
					pm.radioCollection(win+"switch0isfkTfb", e=1, select=win+'attr0IsIk')
				else:
					pm.radioCollection(win+"switch0isfkTfb", e=1, select=win+'attr0IsFk')
			elif attrName is 'attrRange':
				_logger.info('load attrRange value is %s'%value )
				if value == '1':
					pm.radioCollection(win+"switchAttrRangeTfb", e=1, select=win+'attr1')
				else:
					pm.radioCollection(win+"switchAttrRangeTfb", e=1, select=win+'attr10')
			elif attrName is 'rotOffset':
				rotList = eval(value)
				_logger.debug( 'rotation list eval is %rotList'%rotList)
				pm.textField(win+"rotOffsetX", e=1, tx=rotList[0])
				pm.textField(win+"rotOffsetY", e=1, tx=rotList[1])
				pm.textField(win+"rotOffsetZ", e=1, tx=rotList[2])
			else:
				pm.textFieldButtonGrp(win+"%sTfb"%attrName, e=1, tx=value)



	def matchIkFkWin(self, tofk=1):
		try:
			fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset = self.getAndCheckInputWin()
		except:
			pm.warning( 'input error'    )
			return

		rotOffsetX = pm.textField(win+'rotOffsetX', q=1, tx=1)
		_logger.info('rotOffset X is %s'%rotOffsetX   )

		if rotOffsetX == '' : rotOffsetX = 0.0
		else: rotOffsetX = float(rotOffsetX)
		rotOffsetY = pm.textField(win+'rotOffsetY', q=1, tx=1)
		if rotOffsetY == '' : rotOffsetY = 0.0
		else: rotOffsetY = float(rotOffsetY)
		rotOffsetZ = pm.textField(win+'rotOffsetZ', q=1, tx=1)
		if rotOffsetZ == '' : rotOffsetZ = 0.0
		else: rotOffsetZ = float(rotOffsetZ)

		if tofk == 1:
			ikfkMatch(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=switch0isfk, switchAttrRange=switchAttrRange, rotOffset=[rotOffsetX, rotOffsetY, rotOffsetZ])
		elif tofk == 0:
			fkikMatch(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=switch0isfk,  switchAttrRange=switchAttrRange, rotOffset=[rotOffsetX, rotOffsetY, rotOffsetZ])

		pm.select(switchCtrl)

	def switchIkFkWin(self):
		fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset = self.getAndCheckInputWin()


		if switch0isfk == 1: setSwitchTo = switchAttrRange
		else: setSwitchTo = 0

		pm.setAttr('%s.%s'%(switchCtrl, switchAttr), setSwitchTo)
		pm.displayInfo( 'Done. Switched IK >> FK')

	def switchFkIkWin(self):
		fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset = self.getAndCheckInputWin()

		if switch0isfk == 1: setSwitchTo = 0
		else: setSwitchTo = switchAttrRange

		pm.setAttr('%s.%s'%(switchCtrl, switchAttr), setSwitchTo)
		pm.displayInfo( 'Done. Switched FK >> IK')

	def selectAll(self, fk=1):
		try:
			fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset = self.getAndCheckInputWin()
		except:
			pm.warning('Input error')
			return

		if fk == 1:
			pm.select(fkshldr, fkellbow, fkwrist)
			pm.displayInfo('Done.  Select 3 fk Ctrls.')

		elif fk == 0:
			pm.select(ikpv,ikwrist)
			pm.displayInfo('Done. Select 2 ik Ctrls.')
		return

	def keyAll(self, fk=1):
		try:
			fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset = self.getAndCheckInputWin()
		except:
			pm.warning('Input error')
			return

		if fk == 1:
			pm.setKeyframe(fkwrist,s=0, rk=1, mr=1)
			pm.setKeyframe(fkellbow,s=0, rk=1, mr=1)
			pm.setKeyframe(fkshldr,s=0, rk=1, mr=1)

			pm.displayInfo('Done. Set Keyframes on 3 fk Ctrls.')

		elif fk == 0:
			pm.setKeyframe(ikpv,s=0, rk=1, mr=1)
			pm.setKeyframe(ikwrist,s=0, rk=1, mr=1)

			pm.displayInfo('Done. Set Keyframes on 2 ik Ctrls.')
		return



def findStoreNodeFromSelection():
	storenode_found = []
	selection = pm.selected()[0]
	namespace = selection.split(':')[0] + ':' if len(selection.split(':')) > 1 else ''
	storenode_namespace = namespace.replace(':', '__')
	character_storenodes = pm.ls('%s*_IKFKSTORE'%storenode_namespace)

	if character_storenodes == []:
		return storenode

	for storenode in character_storenodes:
		storedic = {'fkwrist': '', 'fkellbow': '', 'fkshldr': '', 'ikwrist': '', 'ikpv': '', 'switchCtrl': '', 'switch0isfk':'', 'attrRange':'', 'rotOffset': ''}
		for attrName, value in storedic.items():
			_logger.debug(storenode.attr(attrName).get() + ' selection is ' + selection.name())
			storedic[attrName] = storenode.attr(attrName).get()

			if selection.name() == storedic[attrName]:
				_logger.debug( 'Found selection in store node %s'%storedic[attrName]    )
				return storenode

	return storenode_found

def autoDetectSideAndLimb(ctrl=None):
	'''
	Need to have one ctrl selecte. This ctrl will determine side, namespace and suffix
	From there we list all matching nodes and try to find Limb
	From there we filter FK IK
	Returns:

	'''
	if ctrl == None:
		ctrl = pm.selected()[0]
	ctrlname = pm.PyNode(ctrl).nodeName()
	namespace = ctrl.split(':')[0]+':' if len(ctrl.split(':')) > 1 else ''
	suffix = '_' + ctrlname.split('_')[-1] if 'ctrl' in ctrlname.split('_')[-1] else ''

	side = None
	limb = None

	# Detect Side
	for search_str in ['rt', 'Rt', 'R_', '_R', 'r_', '_r', 'right']:
		if search_str in ctrlname:
			side, side_str = 'R', search_str
			break
	if side == None:
		for search_str in ['lf', 'Lf', 'L_', '_L', 'l_', '_l', 'left']:
			if search_str in ctrlname:
				side, side_str = 'L', search_str
				break

	#_logger.debug('Side found: %s from %s'  % (side, side_str))

	# Detect Limb
	#side_ctrls = pm.ls('%s*%s*fk*%s' % (namespace, side_str, suffix),exactType='transform')
	#for side_ctrl in side_ctrls:
	#   side_ctrlname = side_ctrl.nodeName().split(namespace)[-1].split(suffix)[0]
	for search_str in ['hand', 'Hand', 'arm', 'Arm', 'elbow', 'ellbow', 'Elbow', 'wrist', 'Wrist']:
		if search_str in ctrlname:
			#_logger.debug(' Arm detected %s'%ctrlname)
			limb = 'arm'
			break
	if limb == None:
		for search_str in ['leg', 'Leg', 'knee', 'Knee', 'foot', 'Foot']:
			if search_str in ctrlname:
				#_logger.debug(' Leg detected %s' % ctrlname  )
				limb = 'leg'
				break
	return side, limb



def fkikMatch(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=1, switchAttrRange=1, rotOffset=[0,0,0]):
	'''
	Match fk to ik. Recreate the ik chain
	Args:
		fkwrist:
		fkellbow:
		fkshldr:
		ikwrist:
		ikpv:
		switchCtrl:
		switchAttr:
		switch0isfk:
		rotOffset:

	Returns:

	'''
	switch = '%s.%s'%(switchCtrl, switchAttr)

	# dup controls to constrain
	ikwristDup = pm.duplicate(ikwrist, parentOnly=1)[0]

	# go to fk mode to match correct position
	if switch0isfk == 0:      pm.setAttr(switch, switchAttrRange)  # 0 is fk
	else:   pm.setAttr(switch, 0)

	if pm.objExists('snapGrp'): pm.delete('snapGrp')
	snapGrp = pm.createNode('transform', name='snapGrp')

	# store if keyframe on attribute or not:
	fkwrist_key, fkellbow_key, fkshldr_key = pm.keyframe(fkwrist, q=1, t=pm.currentTime()),\
											 pm.keyframe(fkellbow, q=1, t=pm.currentTime()),\
											 pm.keyframe(fkshldr, q=1, t=pm.currentTime())




	# get positions from fk
	fkwRaw = pm.xform(fkwrist, ws=1, q=1, t=1)
	fkwPos = om.MVector(fkwRaw[0], fkwRaw[1], fkwRaw[2])
	fkeRaw = pm.xform(fkellbow, ws=1, q=1, t=1)
	fkePos = om.MVector(fkeRaw[0], fkeRaw[1], fkeRaw[2])
	fksRaw = pm.xform(fkshldr, ws=1, q=1, t=1)
	fksPos = om.MVector(fksRaw[0], fksRaw[1], fksRaw[2])

	# store rotation
	fkwRotRaw = pm.xform(fkwrist,  q=1, ro=1)
	fkeRotRaw = pm.xform(fkellbow, q=1, ro=1)
	fksRotRaw = pm.xform(fkshldr,  q=1, ro=1)

	# zero out fk
	pm.xform(fkshldr, ro=(0,0,0))
	pm.xform(fkellbow, ro=(0,0,0))
	pm.xform(fkwrist, ro=(0,0,0))

	pC = pm.pointConstraint(fkwrist, ikwristDup, mo=0)
	pm.xform(ikwristDup, ro=(0,0,0))
	oC = pm.orientConstraint(fkwrist, ikwristDup, mo=1)


	# restore fk
	pm.xform(fkshldr, ro=fksRotRaw)
	pm.xform(fkellbow, ro=fkeRotRaw)
	pm.xform(fkwrist, ro=fkwRotRaw)


	for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
		pm.setAttr('%s.%s'%(ikwrist, attr), pm.getAttr('%s.%s'%(ikwristDup, attr)))



	# set position of IK wrist ctrl lining up to fk wrist plus the user defined offset
	#fkRotLocWs = pm.spaceLocator(name='fkRot_loc')
	# snap to ik wrist
	#snap(fkwrist, fkRotLocWs, rot=1, pos=1 ) # 2016.5 and up
	#snap(fkRotLocWs, ikwrist, rot=1, pos=1)


	# considering rotation offset
	pm.setAttr('%s.rx'%ikwrist, pm.getAttr('%s.rx'%ikwrist)+rotOffset[0])
	pm.setAttr('%s.ry'%ikwrist, pm.getAttr('%s.ry'%ikwrist)+rotOffset[1])
	pm.setAttr('%s.rz'%ikwrist, pm.getAttr('%s.rz'%ikwrist)+rotOffset[2])


	# pole vector

	pvLoc = poleVectorPosition(fkshldr, fkellbow, fkwrist, length=12, createLoc =1)
	pm.parent(pvLoc, snapGrp)
	snap(pvLoc, ikpv, pos=1, rot=0)

	# print '2 creating locator for fk position'
	# # start figure out pole vector pos
	# # find avg (midpoint) of shoulder and wrist
	# midpoint = (fkwPos + fksPos) / 2
	# # find pv direction (origin)
	# pvOrig = fkePos - midpoint
	# # extend length
	# pvRaw = pvOrig * 2
	# # position, add it back to midpoint
	# pvPos = pvRaw + midpoint
	# # stick pole vector to pvPos
	# pm.move(pvPos.x, pvPos.y, pvPos.z, ikpv)

	# clean up
	pm.delete(ikwristDup)
	pm.delete(snapGrp)
	#pm.delete(pvLoc)
	#if not debug: pm.delete(fkRotLocWs)

	# clean up eventually created keyframe on fk ctrl on switch frame
	if len(fkwrist_key) == 0:
		try : pm.cutKey(fkwrist, t=pm.currentTime())
		except: pass
	if len(fkellbow_key) == 0:
		try : pm.cutKey(fkellbow, t=pm.currentTime())
		except: pass
	if len(fkshldr_key) == 0:
		try : pm.cutKey(fkshldr, t=pm.currentTime())
		except: pass


	# go to ik mode
	if switch0isfk == 0:      pm.setAttr(switch, 0)
	else:   pm.setAttr(switch, switchAttrRange)


	_logger.info( 'Done matching FK to IK.')



def keyframeAll(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=1, rotOffset=[0,0,0]):
	for ctrl in [fkwrist, fkellbow, fkshldr, ikwrist, ikpv]:
		for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
			try: pm.setKeyframe(ctrl, at=attr)
			except: pass

	pm.setKeyframe(switchCtrl, at=switchAttr)



def ikfkMatch(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=1, switchAttrRange=1, rotOffset=[0,0,0]):
	'''
	Snap fk to ik controls by building ik joint form fk control position and lining up to ik
	Args:
	Returns:

	'''
	ns = fkwrist.split(':')[0]
	switch = '%s.%s'%(switchCtrl, switchAttr)

	if pm.objExists('snapGrp'): pm.delete('snapGrp')
	snapGrp = pm.createNode('transform', name='snapGrp')

	# store if keyframe on ik attribute or not:
	ikwrist_key, ikpv_key = pm.keyframe(ikwrist, q=1, t=pm.currentTime()),\
											 pm.keyframe(ikpv, q=1, t=pm.currentTime())


	_logger.info( 'matching. switch attr range is %s'%switchAttrRange           )
	# go to fk mode to match correct position (some riggs use same foot ctrl for ik and fk)
	if switch0isfk == 0:      pm.setAttr(switch, switchAttrRange)  # 0 is fk
	else:   pm.setAttr(switch, 0)

	# zero out fk
	pm.xform(fkshldr, ro=(0,0,0))
	pm.xform(fkellbow, ro=(0,0,0))
	pm.xform(fkwrist, ro=(0,0,0))


	fkshldr_dup = pm.duplicate(fkshldr, parentOnly=1)[0]
	fkellbow_dup = pm.duplicate(fkellbow, parentOnly=1)[0]
	fkwrist_dup = pm.duplicate(fkwrist, parentOnly=1)[0]

	#unlock all of duplicate A's arrtibutes
	basicTransforms = ['translateX','translateY','translateZ','rotateX','  rotateY','rotateZ']
	for attr in basicTransforms:
		#unlock attr
		pm.setAttr((fkshldr_dup + '.' + attr), lock=False, k=True)
		pm.setAttr((fkellbow_dup + '.' + attr), lock=False, k=True)
		pm.setAttr((fkwrist_dup + '.' + attr), lock=False, k=True)

	# line up fk duplicates to fk controls
	pm.parent(fkshldr_dup, snapGrp)
	snap(fkshldr, fkshldr_dup, pos=1, rot=0)
	pm.parent(fkellbow_dup,fkshldr_dup)
	snap(fkellbow, fkellbow_dup, pos=1, rot=0)
	pm.parent(fkwrist_dup, fkellbow_dup)
	snap(fkwrist, fkwrist_dup, pos=1, rot=0)

	pm.select(snapGrp)
	root_ikSnap = pm.joint(n='root_ikSnap', p=pm.xform(fkshldr, t=1, q=1, ws=1))
	fkshldr_ikSnap = pm.joint(n='fkshldr_ikSnap', p=pm.xform(fkshldr, t=1, q=1, ws=1))
	fkellbow_ikSnap = pm.joint(n='fkellbow_ikSnap', p=pm.xform(fkellbow, t=1, q=1, ws=1))
	fkwrist_ikSnap = pm.joint(n='fkwrist_ikSnap', p=pm.xform(fkwrist, t=1, q=1, ws=1))

	#aimaxis = max(pm.getAttr('%s.tx'%fkellbow_ikSnap), pm.getAttr('%s.tx'%fkellbow_ikSnap), pm.getAttr('%s.tx'%fkellbow_ikSnap))

	pm.makeIdentity(fkshldr_ikSnap, apply=1)
	pm.makeIdentity(fkellbow_ikSnap, apply=1)
	pm.makeIdentity(fkwrist_ikSnap, apply=1)
	#pm.joint(n='fkshldr_ikSnap', e=1, oj='xyz', zso=1, ch=1,  zeroScaleOrient=True, secondaryAxisOrient='yup')
	pm.select(fkshldr_ikSnap)
	pm.joint(zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')

	# constrain fk
	clist = []

	clist.append(pm.parentConstraint(fkshldr_ikSnap, fkshldr_dup,  skipTranslate = ['x', 'y', 'z'], mo=1)   )
	clist.append(pm.parentConstraint(fkellbow_ikSnap, fkellbow_dup, skipTranslate = ['x', 'y', 'z'], mo=1)      )

	ikrot = pm.xform(ikwrist, q=1,  ro=1)
	pm.xform(ikwrist, ro=(0,0,0))
	clist.append(pm.parentConstraint(ikwrist, fkwrist_dup,  skipTranslate = ['x', 'y', 'z'], mo=1)    )
	pm.xform(ikwrist, ro=ikrot)

	if pm.getAttr('%s.jointOrientY'%fkellbow_ikSnap) < 1.0:
		pm.warning('Warning small joint orient. Setting to 1'  )
		pm.setAttr('%s.jointOrientY'%fkellbow_ikSnap, -1.0)


	# create ikDup setup for fk joint position
	ikHandle_ikSnap = pm.ikHandle(sj=fkshldr_ikSnap, ee=fkwrist_ikSnap, sol='ikRPsolver')
	pm.parent(ikHandle_ikSnap[0], snapGrp)

	# pole vector
	pole_ikSnap = pm.spaceLocator(n='pole_ikSnap')
	pm.parent(pole_ikSnap, snapGrp)


	# temp pole vector position. use the ellbow could use poleVectorPos as well
	snap(fkellbow_ikSnap, pole_ikSnap)

	pm.poleVectorConstraint(pole_ikSnap, ikHandle_ikSnap[0])
	#_logger.info( 'done polevector constraint' )
	# locator for each ikDup joint

	fkshldr_loc = pm.spaceLocator(n='fkshldr_loc')
	pm.parent(fkshldr_loc, fkshldr_ikSnap)
	snap(fkshldr_ikSnap, fkshldr_loc)

	fkellbow_loc = pm.spaceLocator(n='fkellbow_loc')
	pm.parent(fkellbow_loc, fkellbow_ikSnap)
	snap(fkellbow_ikSnap, fkellbow_loc)

	fkwrist_loc = pm.spaceLocator(n='fkwrist_loc')
	pm.parent(fkwrist_loc, fkwrist_ikSnap)
	snap(fkwrist_ikSnap, fkwrist_loc)

	# switch to ik mode (some riggs use same foot ctrl for ik and fk)
	if switch0isfk == 0:      pm.setAttr(switch, 0)  # 0 is fk
	else:   pm.setAttr(switch, switchAttrRange)

	# line up to ik wrist and pole
	pm.pointConstraint(ikwrist, ikHandle_ikSnap[0])
	#pc = pm.pointConstraint(ikpv, pole_ikSnap)
	#print 'snapping to ikhandle %s'%ikHandle_ikSnap[0]
	#snap(ikwrist, ikHandle_ikSnap[0], rot=0, pos=1)
	snap(ikpv, pole_ikSnap, rot=0, pos=1)

	# get wrist rotation
	snap(ikwrist, fkwrist_loc, rot=1, pos=0)

	#print 'delete constraints and snap to ikhandle'

	# snap(fkshldr_loc, fkshldr, rot=1, pos=0)
	# snap(fkellbow_loc, fkellbow, rot=1, pos=0)
	# snap(fkwrist_loc, fkwrist,  rot=1, pos=0)


	# snap back to original fk ctlrs
	snap(fkshldr_dup, fkshldr)
	snap(fkellbow_dup, fkellbow)
	snap(fkwrist_dup, fkwrist)

	pm.delete(clist)

	_logger.info('done snapping. setting offset' )
	# considering rotation offset
	pm.setAttr('%s.rx'%fkwrist, pm.getAttr('%s.rx'%fkwrist)+rotOffset[0])
	pm.setAttr('%s.ry'%fkwrist, pm.getAttr('%s.ry'%fkwrist)+rotOffset[1])
	pm.setAttr('%s.rz'%fkwrist, pm.getAttr('%s.rz'%fkwrist)+rotOffset[2])

	# clean up
	pm.delete(snapGrp)

	# clean up eventually created keyframe on ik ctrl on switch frame
	if len(ikwrist_key) == 0:
		try : pm.cutKey(ikwrist, t=pm.currentTime())
		except: pass
 	if len(ikpv_key) == 0:
		try : pm.cutKey(ikpv, t=pm.currentTime())
		except: pass

	# set to ik
	if switch0isfk == 0: pm.setAttr(switch, 1)
	else: pm.setAttr(switch, 0)


def saveIKFkCtrls(limb, side, fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, switchAttrRange, rotOffset):
	'''
	limb = 'arm'/'leg
	side = 'R'/'L'
	'''

	ns = fkwrist.split(':')[0] if len(fkwrist.split(':')) > 1 else ''
	storenode = ns + '__' + side + '_' + limb + '_IKFKSTORE'
	_logger.info('Storenode is %s'%storenode)
	if pm.objExists(storenode) == False:
		storenode = pm.createNode('transform', n=storenode)
	else:
		message =  'Do you want to replace existing store node?'
		confirm = pm.confirmDialog( title='Replace existing', message=message, button=['Yes','No'],
						  defaultButton='Yes', cancelButton='No', dismissString='No' )
		if confirm == 'Yes':
			_logger.info('deleting existing store node')
			pm.delete(storenode)
			storenode = pm.createNode('transform', n=storenode)
		else:
			return

	storenode = pm.PyNode(storenode)
	storedic = {'fkwrist': fkwrist, 'fkellbow': fkellbow, 'fkshldr':fkshldr, 'ikwrist':ikwrist, 'ikpv':ikpv, 'switchCtrl':switchCtrl, 'switchAttr':switchAttr, 'switch0isfk':switch0isfk, 'attrRange':switchAttrRange, 'rotOffset':rotOffset}
	for attrName, value in storedic.items():
		pm.addAttr(storenode, ln=attrName, dt='string', k=1)
		storenode.attr(attrName).set('%s'%value)

	return storenode



def loadIkFkCtrl(ns, limb, side):
	'''
	limb = 'arm'/'leg
	side = 'R'/'L'
	'''

	storenodeRegex = ns + '__' + side + '_' + limb + '_IKFKSTORE'
	_logger.info('loading %s '%storenodeRegex)
	storenode = pm.ls(storenodeRegex)
	if len(storenode) == 0:
		#_logger.info( 'No storenode found'           )
		return {}
	else:
		storenode = storenode[0]
	ns = storenode.split('__')[0]
	storenode = ns + '__' + side + '_' + limb + '_IKFKSTORE'

	if pm.objExists(storenode) == False:
		return {}
	storenode = pm.PyNode(storenode)

	storedic = {'fkwrist': '', 'fkellbow': '', 'fkshldr':'', 'ikwrist':'', 'ikpv':'', 'switchCtrl':'', 'switchAttr':'', 'switch0isfk':'', 'attrRange':'', 'rotOffset':''}
	for attrName, value in storedic.items():

		storedic[attrName] = storenode.attr(attrName).get()

	_logger.info('StoreNode found is %s'%storedic)
	return storedic


	'''
	# assign selection
	ns= 'JILLShirt_A02:'
	fkwrist = '%sjill_ac_rt_footFK'%ns
	fkellbow = '%sjill_ac_rt_kneeFK'%ns
	fkshldr = '%sjill_ac_rt_hipFK'%ns
	ikwrist = '%sjill_ac_rt_footIK'%ns
	ikpv = '%sjill_ac_rt_legPole'%ns

	import mo_Tools.mo_ikFkSwitch as mo_ikFkSwitch
	reload(mo_ikFkSwitch)
	mo_ikFkSwitch.saveIKFkCtrls(fkwrist, fkellbow, fkshldr, ikwrist, ikpv)
	'''


def get_variable_name(var_value, main_var):
	mvar = [key for key, val in main_var.items() if val==var_value][0]
	_logger.info( 'var: %s >> %s'%(mvar, var_value))  # 123 {'test_var': 123} test_var
	return [mvar, var_value]



def matchTransform(slave, master, rot=1, pos=1):
	'''
	Mimicking innate matchTransform of maya 2016.5 and up
	Args:
		slave: this object will be moved to master
		master: target position and rotation
	'''

	if rot == 0:
		skipRotAxis=["x","y","z"]
	else:
		skipRotAxis = []
	if pos == 0:
		skipTransAxis=["x","y","z"]
	else:
		skipTransAxis = []

	if rot == 1:
		target = pm.xform(master, q=1, ro=1, ws=1)
		pm.xform(slave, ro=target, ws=1)

	if pos == 1:

		target = pm.xform(master, q=1, t=1, ws=1)
		pm.xform(slave, t=target, ws=1)

# Align with Parent Constrain
def snap(master=None, slave=None, pos=1, rot=1):
	'''
	Snap slave to master. Check if attribute locked and skip
	'''
	lastSel = pm.selected()

	if master == None:
		master = pm.selected()[0]
	if slave == None:
		slave = pm.selected()[1:]
	slaves = pm.ls(slave)

	ptC, ptR = [], []

	# for each slave, parentconstrain for each position and rotation, skipping locked attributes
	for slave in slaves:

		slaveDup = pm.duplicate(slave, parentOnly=True)[0]
		_logger.debug('snapping slaveDup')

		#unlock all of duplicate A's arrtibutes
		basicTransforms = ['translateX','translateY','translateZ','rotateX','  rotateY','rotateZ']
		for attr in basicTransforms:
			#unlock attr
			pm.setAttr((slaveDup + '.' + attr), lock=False)

		ptC=pm.parentConstraint(master, slaveDup, mo=False)

		if pos == 1:
			for att in ['tx', 'ty', 'tz']:
				if pm.getAttr('%s.%s'%(slave,att), l=1) == False:
					pm.setAttr((slave + '.' + att), pm.getAttr((slaveDup + '.' + att)))

					_logger.info('Snap Constraining Traslation %s %s. Skiplist is '%(master, slave)  )


		if rot == 1:
			for att in ['rx', 'ry', 'rz']:
				if pm.getAttr('%s.%s'%(slave,att), l=1) == False:
					pm.setAttr((slave + '.' + att), pm.getAttr((slaveDup + '.' + att)))

					_logger.info('Snap Constraining Rotation %s %s. Skiplist is '%(master, slave))

		pm.delete(ptC)
		pm.delete(slaveDup)

	pm.select(lastSel)



def poleVectorPosition(startJnt, midJnt, endJnt, length=12, createLoc =0):

	import maya.api.OpenMaya as om

	start = pm.xform(startJnt ,q= 1 ,ws = 1,t =1 )
	mid = pm.xform(midJnt ,q= 1 ,ws = 1,t =1 )
	end = pm.xform(endJnt ,q= 1 ,ws = 1,t =1 )
	startV = om.MVector(start[0] ,start[1],start[2])
	midV = om.MVector(mid[0] ,mid[1],mid[2])
	endV = om.MVector(end[0] ,end[1],end[2])


	startEnd = endV - startV
	startMid = midV - startV

	# projection vector is vecA projected onto vecB
	# it is calculated by dot product if one vector normalized

	# proj= vecA * vecB.normalized (dot product result is scalar)
	proj = startMid * startEnd.normal()


	# multiply proj scalar with normalized startEndVector to project it onto vector
	startEndN = startEnd.normal()
	projV = startEndN * proj

	arrowV = startMid - projV
	arrowVN = arrowV.normal()

	# scale up to length and offset to midV
	finalV = arrowVN*length + midV


	if createLoc:
		loc = pm.spaceLocator(n='polePos')
		pm.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
		return loc

	return finalV
