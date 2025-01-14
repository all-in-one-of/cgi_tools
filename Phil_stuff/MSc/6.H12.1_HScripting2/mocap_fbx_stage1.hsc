# DEFINE MOCAP SKELETON HIERARCHY NUMBERING
# DEFINE MOCAP REST POSE FBX NAME

##### USER DEFINED VARIBLES #####

# NOTES TO USER:
# Modify the RANGELIST variable to identify all beginning
# and end joint node chains of your FBX skeleton heirachy...
# Modify the TPOSE variable to the name of your
# T-POSE / REST POSE fbx subnetwork

set RANGELIST = 1_6 7_11 12_19 20_24 25_27
set TPOSE = rest_pose_fbx

##### END USER DEFINED VARIABLES #####



# AT OBJ LEVEL CYCLE THROUGH EACH SCENE OBJECT TO DETERMINE IF IT IS A FBX MOCAP CLIP

opcf /obj

# create empty list for fbx objects
set FBXOBJECTLIST = " "

# examine each scene object in turn

foreach OBJECT ( `execute("opls")` )

    # DETERMINE THE OBJECT TYPE
    set OBJECT_TYPE = `execute("optype -t $OBJECT")`

    message $OBJECT $OBJECT_TYPE

    # DETERMINE IF THE OBJECT NAME MATCHES *_fbx, AND THE OBJECT TYPE IS A SUBNET
    # IF YES, ADD THE FOUND FBX CLIP TO A CLIP LIST

end




# ASK THE USER TO VERIFY THE FOUND FBX MOCAP CLIPS AND INDICATE IF THEY WISH TO PROCEED WITH THE REST OF THE SCRIPT

# IF YES, REMOVE ANY PREVIOUS ITERATIONS OF THIS SCRIPT - IF NO EXIT SCRIPT

# DEFINE NAMES FOR KEY CHOP OPERATORS BEING CREATED

# CREATE A CUSTOM CHOP NETWORK FOR MOCAP DATA AND GO INSIDE IT

        # CREATE A SWITCH CHOP
        # CREATE A RENAME CHOP
        # WIRE THE SWITCH CHOP INTO THE RENAME CHOP
        # ACTIVATE THE DISPLAY FLAG ON THE RENAME CHOP

# IF A FBX MOCAP CLIP IS FOUND, IMPORT IT INTO THE CUSTOM CHOP NETWORK USING OBJECT CHAIN CHOPS

# LOCK THE OBJECT CHAIN CHOPS FOR THE REST POSE TO PREVENT RECURSION ERRORS

# WHEN ALL OBJECT CHAIN CHOPS FOR A MOCAP CLIP HAVE BEEN CREATED, MERGE THEM TOGETHER

# FEED THE MERGED OBJECT CHAIN CHOPS INTO THE SWITCH CHOP

# ACTIVATE THE ORANGE EXPORT FLAG ON THE RENAME CHOP

# TIDY UP THE AUTOMATICALLY GENERATED NODES

# DELETE SCRIPT VARIABLES