# ----------------------------------------------------------------- #
#                                                                   #
#        Speed Facial Rig for Maya 2012/2013/2014/2015/2016         #
#                                                                   #
#               Author   : Faucillon Ludovic                        #
#               Contact  : ludovic.faucillon@gmail.com              #
#  Linkedin: https://fr.linkedin.com/in/faucillon-ludovic-72646133  #
#                                                                   #
#         This script has been downloaded on 'creativecrash'        #
#                                                                   #
#     If you have any request on this script, you can contact me    #
#        on 'Creativecrash' website or directly on my mail box      #
#                                                                   #
#                                                                   #
#                                                                   #
# ----------------------------------------------------------------- #


'''
1 - Select the folder corresponding of your maya version
2 - Place it where you want
3 - Copy paste the directory path of your installation in the variable instalPath
4 - Copy this code into Maya script editor and make a button on your shelf to launch the script
'''


# fichier d'installation du script facial rig version publique
import maya.cmds as mc
import os 
import sys
OS = sys.platform


# installation of facial rig path
instalPath = "put your path installation here"
paths = sys.path
newPath = ''
if OS.startswith('win'):
    pathElement = instalPath.split("/")
    print pathElement
    
    for elt in pathElement:
        if elt != pathElement[len(pathElement)-1]:
            newPath = newPath + str(elt) + '\\'
        else:
            newPath = newPath + str(elt)

    
else:
    newPath = instalPath


result = 'no'
for path in paths:
    if path == newPath:
        result = 'no'
        break
    else:
        result = 'yes'

if result == 'yes':
    sys.path.append(newPath)
    mc.warning('A new path was added into your python path for the facial rig script at : %s' % newPath)


print sys.path

from facial_rig_UI import * 
UI()
