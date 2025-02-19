# MOCAP FBX SETUP SCRIPT

##### USER DEFINED VARIBLES #####

set RANGELIST = 1_6 7_11 12_19 20_24 25_27
set TPOSE = tpose_fbx

# NOTES TO USER:
# Modify the RANGELIST variable to identify all beginning and end joint node chains of your FBX skeleton heirachy...
# Modify the TPOSE variable to the name of your T-POSE fbx subnetwork

##### END USER DEFINED VARIABLES #####

##### AUTOMATED VARIABLES #####

#locate and list all the FBX MOCAP subnets

opcf /obj

#create empty list for fbx objects
set FBXOBJECTLIST = " "

#examine each scene object in turn
foreach OBJECT ( `execute("opls -d *")` )

        #find the object type
        set OBJECT_TYPE = `execute("optype -t $OBJECT")`
        
        #determine if object is fbx subnet
        if(`strmatch("*_fbx",$OBJECT)` == 1 && $OBJECT_TYPE == subnet)
        
        message $OBJECT is MOCAP data
        
        #add fbx subnet to FBXOBJECTLIST variable
        set FBXOBJECTLIST = `strcat($FBXOBJECTLIST + " ", $OBJECT)`
        
        endif

end

set -u OBJECT

#print final fbx object list
message $FBXOBJECTLIST

# give a name for the MOCAP CHOP Network
set CNET = MOCAP_CONTROL

##### END AUTOMATED VARIABLES #####


##### BEGIN SCRIPT #####

#Remove previous MOCAP_CONTROL CHOP Network
oprm -f $CNET

#CREATE NEW CHOPNET
opadd -n chopnet $CNET

#BUILD CHOPNET CONTENTS
opcf /obj/$CNET
opadd -n switch MOCAP_CONTROL
opadd -n rename MOCAP_EXPORT
opparm MOCAP_EXPORT renamefrom ( * ) renameto ( /obj/$TPOSE/* )

opwire -n MOCAP_CONTROL -0 MOCAP_EXPORT
opset -d on -o on MOCAP_EXPORT

set INC = 0
set INC2 = 0

foreach OBJECT ( $FBXOBJECTLIST )

opadd -n merge $OBJECT
opwire -n $OBJECT -$INC MOCAP_CONTROL
set INC = `$INC + 1`

        foreach RANGE ( $RANGELIST )
        
                set FULLNAME = $OBJECT"_"$RANGE
                set TEMPLIST = `strreplace($RANGE, "_", " ")`
                set NUMSTART = `arg($TEMPLIST,0)`
                set NUMEND = `arg($TEMPLIST,1)`
                
                opadd -n objectchain $FULLNAME
                        if ( $OBJECT != $TPOSE ) then
                        opparm $FULLNAME startpath ( /obj/$OBJECT/reference/joint$NUMSTART )
                        opparm $FULLNAME endpath ( /obj/$OBJECT/reference/joint$NUMEND )
                        else
                        opparm $FULLNAME startpath ( /obj/$OBJECT/joint$NUMSTART )
                        opparm $FULLNAME endpath ( /obj/$OBJECT/joint$NUMEND )
                        endif
                opparm $FULLNAME fetchpretransform ( off )

                opwire -n $FULLNAME -$INC2 $OBJECT
                set INC2 = `$INC2 + 1`
        end

        
end





##### END SCRIPT #####

##### LOCK TPOSE MERGE #####

opset -l on $TPOSE

##### FINALLY TIDY UP THE NETWORK LAYOUT #####
oplayout -d 0




 