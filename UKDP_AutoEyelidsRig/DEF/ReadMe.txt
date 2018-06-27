How to install?
---------------

1/ Copy "UKDP_AER.py" in your maya scripts folder. Default is :

Windows:
<drive>:\Documents and Settings\<username>\My Documents\maya\<Version>\scripts

Mac OS X:
~/Library/Preferences/Autodesk/maya/<version>/scripts

Linux:
~/maya/<version>/scripts

------------------------------------------

2/ Copy "UKDP_AutoEyelidsRig_icon.png" in your maya icons folder. Default is :

Windows:
<drive>:\Documents and Settings\<username>\My Documents\maya\<Version>\prefs\icons

Mac OS X:
~/Library/Preferences/Autodesk/maya/<version>/prefs/icons

Linux:
~/maya/<version>/prefs/icons/

------------------------------------------

3/ Open Maya, create a new button (make sure its in python: "command" tab > language : python)
Copy and paste the following three lines in it.


import UKDP_AER
reload (UKDP_AER)
UKDP_AER.autoEyelidsRig.UI


--------------------------------------------------------------------


Credits & Contact
-----------------

ukdp.scripts@gmail.com