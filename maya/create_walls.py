#Jennifer Moorehead i7611989    MSc CAVE CGI Tools Script Submission

import maya.cmds as cmds


#Create Walls function

def CreateWalls(geo, num_of_duplicates, trans_x):
    '''Duplicate an object that has already been created and translate those duplicates relative to each other
       geo                   : name of geometry to be duplicated (string)
       num_of_duplicates     : the number of duplicates to be made (int)
       trans_x               : the amount the duplicate is to be translated in the X direction   
    '''
    
    for i in range(0,num_of_duplicates):
        clone = cmds.duplicate(geo)
        cmds.move(trans_x, geo, relative=True)

CreateWalls("pCube2",5,2)





