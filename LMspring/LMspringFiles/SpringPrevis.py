#######################################################################################
#                                                                                     #
#                            SPRING PREVIS 1.04.18                                    #
#                  by Luismi Herrera. Twitter: @luismiherrera                         #
#                                                                                     #
# 1. Select something (normaly an animation control, but it could be anything).       #
# 2. Execute SPRING PREVIS script (by clicking on the shelf icon).                    #
# 3. Change or animate 'Goal Weight[0]' value (under 'luismiParticleShape') until     #
#    you are happy with the result.                                                   #
# 4. Execute SPRING BAKE script (by clicking on the shelf icon).                      #
#                                                                                     #
#######################################################################################


import maya.cmds as cmds

minTime = cmds.playbackOptions(minTime=True, query=True)
maxTime = cmds.playbackOptions(maxTime=True, query=True)
sel = cmds.ls(selection=True)

if len(sel) == 0:
    cmds.warning( "Nothing Selected" ) 
elif cmds.objExists('luismiParticle'):
    cmds.warning( "luismiParticle already EXISTS!" )
else:
    cmds.currentTime( minTime, edit=True )
    selLoc = cmds.spaceLocator(name='OriginalPosition_Loc')
    cmds.particle(p=[(0, 0, 0)], name='luismiParticle')
    tempConst = cmds.parentConstraint(sel,selLoc,mo=False)
    cmds.bakeResults(selLoc, t=(minTime,maxTime))
    cmds.delete(tempConst)
    tempConst2 = cmds.parentConstraint(selLoc,'luismiParticle',mo=False)
    cmds.delete(tempConst2)
    cmds.goal( 'luismiParticle', g=selLoc, w=.45)
    cmds.spaceLocator(name='physicsLoc')
    cmds.connectAttr('luismiParticleShape.worldCentroid', 'physicsLoc.translate')
    tempConst3 = cmds.pointConstraint('physicsLoc', sel, mo=True)
    cmds.select('luismiParticle')