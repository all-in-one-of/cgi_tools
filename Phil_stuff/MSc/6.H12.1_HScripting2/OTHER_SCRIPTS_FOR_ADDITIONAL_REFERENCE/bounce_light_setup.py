#bounce light script

#BEGIN DEFINE OBJECT NAMES 

all  = 'all_objects'
b_light = 'bounce_light'
g_light = 'gi_light'
s_net = 'gi_light_shaders'
gi_shader = 'gi_light_shader'
obj_merge  = 'all_geometry'

#END DEFINE NAMES

#BEGIN DEFINE HOUDINI LEVELS

obj = hou.node('/obj')

#END DEFINE LEVELS

#BEGIN CHECK TO SEE IF OBJECTS TO BE CREATED ALREADY EXIST

scene_list = [all,b_light,g_light,s_net]

#delete any operators created by previous executions of this script
for item in scene_list:
    if obj.node(item):
        obj.node(item).destroy()

#END CHECK FOR OBJECTS

#BEGIN OBJECT CREATION

#1 - gi_geo
# create geometry object to store  all scene objects using an Object Merge SOP
temp = obj.createNode('geo',all)
temp.parm('lightmask').set(g_light)
temp.node('file1').destroy()
all_obj = obj.node(all).createNode('object_merge',obj_merge)
all_obj.parm('xformpath').set('.')

#2 - b_light
#create a distance light to control where the bounce light comes from
bounce_light = obj.createNode('hlight',b_light)
bounce_light.parm('light_type').set('distant')
bounce_light.parm('light_intensity').set(3)
#position it somewhere useful
bounce_light.parmTuple('t').set((10,10,10))
bounce_light.parm('l_lookatpath').set('../'+ all)

#3 - g_light
#create a light template for use as a gi light
obj.createNode('light',g_light).parm('shop_lightpath').set('../' + s_net + '/' + gi_shader)

#4 - s_net & gi_shader
#create a shop network for storing the gi light shader
gi =  obj.createNode('shopnet',s_net).createNode('v_gilight', gi_shader)
gi.parm('istyle').set('full')
gi.parm('samples').set('32')
gi.parm('doobjmask').set('1')
gi.parm('objmask').set('* ^' + all)
gi.parmTuple('background').set((0,0,0))

#END OBJECT CREATION

#BEGIN HOUSEKEEPING

#tidy up placement of new objects in network view
for item in scene_list:
    obj.node(item).moveToGoodPosition()

#END HOUSEKEEPING

#CREATE A COUNTER
i = 1

#LOOP THROUGH ALL OBJECTS
for obj_name in obj.children():

    #find out object type
    type = obj_name.type().name()

    #convert obj_name into a string
    name = str(obj_name)
    
    print 'object name is', name
    print 'object type is', type

    #print type(obj_name)
    #print type(all)
    
    if type == 'geo' and name != all:

        print 'ORIGINAL SCENE GEOMETRY OBJECT FOUND'

        obj_name.parm('lightmask').set(b_light)
        obj_name.parm('vm_phantom').set(1)
        all_obj.parm('numobj').set(i)
        all_obj.parm('objpath' + str(i)).set('../../' + name)

        #increase counter
        i += 1

    if (type == 'hlight' or type == 'light') and name != g_light and name != b_light:
        print 'THIS EXISTING SCENE LIGHT WILL BE SWITCHED OFF'
        
        if type == 'hlight':
            obj_name.parm('light_enable').set(0)
        elif type == 'light':
            obj_name.parm('dimmer').set(0)

#END BOUNCE LIGHT SETUP SCRIPT
