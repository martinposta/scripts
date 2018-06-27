# 
#   -= ml_keyValueDragger.py =-
#                __   by Morgan Loomis
#     ____ ___  / /  http://morganloomis.com
#    / __ `__ \/ /  Licensed under Creative Commons BY-SA
#   / / / / / / /  http://creativecommons.org/licenses/by-sa/3.0/
#  /_/ /_/ /_/_/  _________                                   
#               /_________/  Revision 4, 2016-05-02
#      _______________________________
# - -/__ Installing Python Scripts __/- - - - - - - - - - - - - - - - - - - - 
# 
# Copy this file into your maya scripts directory, for example:
#     C:/Documents and Settings/user/My Documents/maya/scripts/ml_keyValueDragger.py
# 
# Run the tool by importing the module, and then calling the primary function.
# From python, this looks like:
#     import ml_keyValueDragger
#     ml_keyValueDragger.drag()
# From MEL, this looks like:
#     python("import ml_keyValueDragger;ml_keyValueDragger.drag()");
#      _________________
# - -/__ Description __/- - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Scale keyframes to their default value by dragging in the viewport.
#      ___________
# - -/__ Usage __/- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# Run the tool, and the cursor will turn into a hand. Left-click and hold in
# the viewport, and then drag either left or right to scale the key value up or down.
# If you have no keys selectd, the tool will act only on curves
# that are visibile in the graph editor. If there are no keys at the 
# current frame, keys will be set.
#      __________________
# - -/__ Requirements __/- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
# This script requires the ml_utilities module, which can be downloaded here:
# 	http://morganloomis.com/wiki/tools.html#ml_utilities
#                                                             __________
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - /_ Enjoy! _/- - -
__author__ = 'Morgan Loomis'
__license__ = 'Creative Commons Attribution-ShareAlike'
__category__ = 'animationScripts'
__revision__ = 4

import maya.cmds as mc
import maya.mel as mm
from maya import OpenMaya

try:
    import ml_utilities as utl
    utl.upToDateCheck(17)
except ImportError:
    result = mc.confirmDialog( title='Module Not Found', 
                message='This tool requires the ml_utilities module. Once downloaded you will need to restart Maya.', 
                button=['Download Module','Cancel'], 
                defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel' )
    
    if result == 'Download Module':
        mc.showHelp('http://morganloomis.com/download/animationScripts/ml_utilities.py',absolute=True)
    
def drag():
    '''The primary command to run the tool'''
    KeyValueDragger()


class KeyValueDragger(utl.Dragger):
    '''Creates the tool and manages the data'''

    def __init__(self, 
                 name='mlKeyValueDraggerContext',
                 minValue=0,
                 maxValue=None,
                 defaultValue=1,
                 title = 'Scale'):
        
        self.keySel = utl.KeySelection()
        selected = False
        if self.keySel.selectedKeys():
            selected = True
            pass
        elif self.keySel.visibleInGraphEditor():
            self.keySel.setKeyframe()
        elif self.keySel.keyedChannels():
            self.keySel.setKeyframe()
        elif self.keySel.selectedObjects():
            self.keySel.setKeyframe()
        
        if not self.keySel.initialized:
            return
        
        utl.Dragger.__init__(self, defaultValue=defaultValue, minValue=minValue, maxValue=maxValue, name=name, title=title)

        self.time = dict()
        self.default = dict()
        self.value = dict()
        self.curves = self.keySel.curves

        for curve in self.curves:
            if selected:
                self.time[curve] = mc.keyframe(curve, query=True, timeChange=True, sl=True)
                self.value[curve] = mc.keyframe(curve, query=True, valueChange=True, sl=True)
            else:
                self.time[curve] = self.keySel.time
                self.value[curve] = mc.keyframe(curve, time=self.keySel.time, query=True, valueChange=True)

            #get the attribute's default value
            node, attr = mc.listConnections('.'.join((curve,'output')), source=False, plugs=True)[0].split('.')
            self.default[curve] = mc.attributeQuery(attr, listDefault=True, node=node)[0]
            
        self.setTool()
        onscreenInstructions = 'Drag left to scale toward default, and right to go in the opposite direction.'
        self.drawString(onscreenInstructions)
        OpenMaya.MGlobal.displayWarning(onscreenInstructions)
        
        
    def dragLeft(self):
        '''
        Activated by the left mouse button, this scales keys toward or away from their default value.
        '''
        self.drawString('Scale '+str(int(self.x*100))+' %')
        for curve in self.curves:
            for i,v in zip(self.time[curve], self.value[curve]):
                mc.keyframe(curve, time=(i,), valueChange=self.default[curve]+((v-self.default[curve])*self.x))



#      ______________________
# - -/__ Revision History __/- - - - - - - - - - - - - - - - - - - - - - - -
#
# Revision 2: 2014-03-01 : Added revision notes, adding category
#
# Revision 3: 2016-05-01 : Bug fix
#
# Revision 4: 2016-05-02 : Actual bug fix
