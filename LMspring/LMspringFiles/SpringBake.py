###########################################################################
#                                                                		  #
#                      SPRING BAKE 1.04.18                       		  #
#            by Luismi Herrera. Twitter: @luismiherrera          		  #
#                                                                		  #
#  1. Your can adjust the Range Slider to chose the frames to be baked.   #
#  2. Execute SPRING BAKE by clicking on the shelf icon.         		  #
#                                                                		  #
###########################################################################

import maya.cmds as cmds

minTime = cmds.playbackOptions(minTime=True, query=True)
maxTime = cmds.playbackOptions(maxTime=True, query=True)

if cmds.objExists('luismiParticle'):
    cmds.bakeResults('physicsLoc', t=(minTime,maxTime), simulation=True)
    cmds.delete(selLoc, 'luismiParticle')
    cmds.bakeResults(sel, t=(minTime,maxTime))
    cmds.delete('physicsLoc')
else:
    cmds.warning( "Nothing to bake. Use SPRING PREVIS first." )