###########   Mocap FBX Setup code Python version   #############
#################################################################

# User Defined Variables

RANGELIST = ['1_6','7_11','12_19','20_24','25_27']
TPOSE = 'tpose_fbx'


# NOTES TO USER:
# Modify the RANGELIST variable to identify all beginning and end joint node chains of your FBX skeleton heirachy...
# Modify the TPOSE variable to the name of your T-POSE fbx subnetwork


##### END USER DEFINED VARIABLES #####

##### AUTOMATED VARIABLES #####

#locate and list all the FBX MOCAP subnets

obj = hou.node('/obj')

#create empty list for fbx objects

FBXOBJECTLIST = []

#examine each scene object in turn

for obj_name in obj.children() :
        #find the object type
        OBJECT_TYPE = obj_name.type().name()
        
        #convert obj_name into a string
        name = str(obj_name)    

        #determine if object is fbx subnet
        if 'fbx' in name and OBJECT_TYPE == 'subnet' :
                hou.ui.displayMessage(name+' is a mocap')
#               print name, 'is a mocap'
        #add fbx subnet to FBXOBJECTLIST variable
                FBXOBJECTLIST.append(name)

# set -u OBJECT ----- unset the variable

#print final fbx object list
#hou.ui.displayMessage(FBXOBJECTLIST)

# give a name for the MOCAP CHOP Network
CNET = 'MOCAP_CONTROL'

##### END AUTOMATED VARIABLES #####


##### BEGIN SCRIPT #####

#Remove previous MOCAP_CONTROL CHOP Network
for obj_name in obj.children() :
        if str(obj_name) == CNET :
                obj_name.destroy()

#CREATE NEW CHOPNET
cnet = obj.createNode("chopnet", CNET)

#BUILD CHOPNET CONTENTS
sw = cnet.createNode("switch", "MOCAP_CONTROL")
rn = cnet.createNode("rename", "MOCAP_EXPORT")

rn.setParms({"renamefrom" : '*', "renameto" : '/obj/tpose_fbx/*'})
rn.setInput(0, sw, 0)
rn.setDisplayFlag(1)            # -d --- display ; -o --- export
rn.setExportFlag(1)

INC = 0
INC2 = 0

for OBJECT in FBXOBJECTLIST :
        OBJFBX = cnet.createNode("merge",OBJECT)
        sw.setInput(INC, OBJFBX, 0)
        INC = INC + 1

        for RANGE in RANGELIST :
                FULLNAME = str(OBJECT + RANGE)
                #hou.ui.displayMessage(FULLNAME)
                
                TEMP = RANGE.replace("_", " ")
                NUMLIST = TEMP.split()
                                
                NUMSTART = NUMLIST[0]
                NUMEND   = NUMLIST[1]
                
                #hou.ui.displayMessage(NUMSTART)
                #hou.ui.displayMessage(NUMEND)

                mocapdata = cnet.createNode("objectchain", FULLNAME)

                if OBJECT != TPOSE :
                        mocapdata.setParms({"startpath": '/obj/'+OBJECT+'/reference/joint'+NUMSTART, "endpath": '/obj/'+OBJECT+'/reference/joint'+NUMEND})
                        
                else :
                        mocapdata.setParms({"startpath": '/obj/'+OBJECT+'/joint'+NUMSTART, "endpath": '/obj/'+OBJECT+'/joint'+NUMEND})
                        ##### LOCK TPOSE MERGE #####
                #        mocapdata.setHardLocked(1)

                OBJFBX.setInput(INC2, mocapdata, 0)
                INC2 = INC2 + 1

##### END SCRIPT #####

##### FINALLY TIDY UP THE NETWORK LAYOUT #####
obj.layoutChildren()
