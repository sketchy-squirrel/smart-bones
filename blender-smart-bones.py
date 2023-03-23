bl_info = {
    "name": "Smart Bones",
    "description": "Automating adds action constraint to keyed bones within a selected action",
    "author": "Sketchy Squirrel",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Smart Bones",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "https://github.com/sketchy-squirrel/smart-bones",
    "category": "Rigging"
}

import bpy
import re

#---------------------------------------------------------------------
#    Properties
#---------------------------------------------------------------------

class SmartBoneProperties(bpy.types.PropertyGroup):
    
    armature_name : bpy.props.StringProperty(
        name = "Target",
        description = "Control Armature",
    )
    
    control_name : bpy.props.StringProperty(
        name = "Control",
        description = "Control Bone",
    )
    
    transform_channel : bpy.props.EnumProperty(
        name = "Channel",
        description = "Control Axis",
        items = [
                ('LOCATION_X', 'LOCATION_X',""),
                ('LOCATION_Y', 'LOCATION_Y',""),
                ('LOCATION_Z', 'LOCATION_Z',""),
                ('ROTATION_X', 'ROTATION_X',""),
                ('ROTATION_Y', 'ROTATION_Y',""),
                ('ROTATION_Z', 'ROTATION_Z',""),
                ('SCALE_X', 'SCALE_X',""),
                ('SCALE_Y', 'SCALE_Y',""),
                ('SCALE_Z', 'SCALE_Z',""),   
            ],
        default = 'LOCATION_X'
    )
    
    target_space : bpy.props.EnumProperty(
        name = "Space",
        description = "Transform Space",
        items =[
            ('WORLD', 'WORLD', ""),
            ('CUSTOM', 'CUSTOM', ""),
            ('LOCAL', 'LOCAL', "")
        ],
        default = 'LOCAL'
            
    )
    
    space_object_name : bpy.props.StringProperty(
        name = "Space Object",
        description = "Takes local space from another object, to apply to constraint",
        default = "",
    )
    
    space_subtarget : bpy.props.StringProperty(
        name = "Space Subtarget",
        description = "Custom space target, if 'Space Object' is of type ARMATURE",
        default = "",
    )
    
    transform_min : bpy.props.FloatProperty(
    name = "Min Transform Range",
    description = "Minimum Transform Value",
    default = 0.0,
    )
    
    transform_max : bpy.props.FloatProperty(
    name = "Max Transform Range",
    description = "Maximum Transform Value",
    default = 1.0,
    )
    
    #action
    
    action_name : bpy.props.StringProperty(
    name = "Action",
    description = "Name of affected action",
    )
    
    frame_min : bpy.props.IntProperty(
    name = "Min Frame",
    description = "Start Frame of Action",
    default = 0,
    )
    
    frame_max : bpy.props.IntProperty(
    name = "Max Frame",
    description = "End Frame of Action",
    default = 20,
    )

#---------------------------------------------------------------------
#    Operator
#---------------------------------------------------------------------
    
class OT_AddSmartBone(bpy.types.Operator):
    """Add action constraints to all bones in action"""
    bl_idname = "myops.add_smart_bone"
    bl_label = "Add Smart Bone"
    
    
    def execute(self, context):
        
        current_object = bpy.context.object
        
        smart_bone_tool = context.scene.smart_bone_tool
        
        #Find Action Bones
        action = bpy.data.actions[smart_bone_tool.action_name]
        action_bones = self.find_action_bones(action)
        
            
        #make all bone layers visible
        current_selection = []
        obj = context.scene.objects[smart_bone_tool.armature_name]
        if obj.type == "ARMATURE":
            armature_data = obj.data
            
            for i in range(0,32):
                current_selection.append(armature_data.layers[i])
                armature_data.layers[i] = True
        
        
        #Add final constraints
        self.add_action_constraint(
            current_object,
            smart_bone_tool.armature_name,
            action_bones,
            smart_bone_tool.control_name,
            smart_bone_tool.transform_channel,
            smart_bone_tool.target_space,
            smart_bone_tool.space_object_name,
            smart_bone_tool.space_subtarget,
            [smart_bone_tool.transform_min, smart_bone_tool.transform_max],
            smart_bone_tool.action_name,
            [smart_bone_tool.frame_min, smart_bone_tool.frame_max],
        )
        
        #revert to previous selection
        if obj.type == "ARMATURE":
            armature_data = obj.data
            
            armature_data.layers = current_selection


        return ({'FINISHED'})
    
    def find_action_bones(self, action):                                        # create a list of bones used in the action in armature
        
        bones = []
        
        for fcurve in action.fcurves:        
            action_bone = re.findall('"([^"]*)"', fcurve.data_path)[0]          # find bone for each key in action        
            if action_bone not in bones:                                        # add found bone to bones if not already present
                bones.append(action_bone)
        
        return(bones)
    
    
    def add_action_constraint(self, current_object, ctrl_armature_name, action_bones, control_name, transform_channel, target_space, space_obj, space_sub, transform_range, action_name, frame_range):
        
        
        if current_object.type == 'ARMATURE':
            
            #enter pose mode
            bpy.ops.object.mode_set(mode='POSE')
        
            #stores list of bones as string, to check if affected bone is in current object
            bones_in_current_obj = []
            for i in current_object.pose.bones:
              bones_in_current_obj.append(i.name)
            
            for action_bone in action_bones:
                
                    #bone = bpy.data.objects[ctrl_armature_name].pose.bones[control_name].bone
                    #current_object.data.bones.active = bone    
                    #bone.select = True 
                    
                    #Prevents trying to add constraint to bone in another armature
                    if action_bone in bones_in_current_obj:
                    
                        current_bone = current_object.pose.bones[action_bone]
                    
                        if bpy.data.objects[ctrl_armature_name].pose.bones[control_name] != current_bone: #prevents adding a constraint to a bone, targeting its self
                    
                            constraint_name = str("SB_"+control_name+"_"+action_name)
                            
                            constraint_exists = False
                            # Test if bone constraint already exists
                            for constraint in current_bone.constraints:
                                if constraint.name == constraint_name:
                                    constraint_exists = True
                            
                            if constraint_exists == False:
                                constraint = current_bone.constraints.new("ACTION")
                                constraint.name = constraint_name
                            
                            constraint.target = bpy.data.objects[ctrl_armature_name]
                            constraint.subtarget = control_name
                            constraint.transform_channel = transform_channel
                            constraint.target_space = target_space
                            
                            if target_space == "CUSTOM":
                                try:
                                    constraint.space_object = bpy.data.objects[space_obj]
                                    
                                    if space_obj != "" and bpy.context.objects[space_obj].type == "ARMATURE":
                                        constraint.space_subtarget = space_sub
                                        
                                except:
                                    constraint.target_space = "LOCAL"
                                    
                            constraint.min = transform_range[0]
                            constraint.max = transform_range[1]
                            constraint.action = bpy.data.actions[action_name]
                            constraint.frame_start = frame_range[0]
                            constraint.frame_end = frame_range[1]


class OT_DeleteSmartBone(bpy.types.Operator):
    """Delete relevant action constraints within selected armature"""
    
    bl_idname = "myops.delete_smart_bone"
    bl_label = "Delete Smart Bone"
    
    
    def execute(self, context):
        
        current_armature = bpy.context.object
        
        if current_armature.type == "ARMATURE":
            
            smart_bone_tool = context.scene.smart_bone_tool
            
            armature_name = smart_bone_tool.armature_name
            control_name = smart_bone_tool.control_name
            action_name = smart_bone_tool.action_name
            
            constraint_name = str("SB_"+control_name+"_"+action_name)
            
            bpy.ops.object.mode_set(mode='POSE')
        
            #select all the bones in armature
                
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.armature.select_all(action='DESELECT')
            
            #make all bone layers visible
            current_selection = []
            obj = context.scene.objects[smart_bone_tool.armature_name]
            if obj.type == "ARMATURE":
                armature_data = obj.data
                
                for i in range(0,32):
                    current_selection.append(armature_data.layers[i])
                    armature_data.layers[i] = True
                    
            
            for bone in current_armature.data.edit_bones:
                bone.select = True
            
            #remove_constraints
            for bone in current_armature.pose.bones:
                for constraint in bone.constraints:
                    if constraint_name in constraint.name:
                        bone.constraints.remove(constraint)
            
            #revert to previous selection
            if obj.type == "ARMATURE":
                armature_data = obj.data
                
                for i in range(0,32):
                    armature_data.layers[i] = current_selection[i]
            
            return {'FINISHED'}

#---------------------------------------------------------------------
#    Panel
#---------------------------------------------------------------------

class POSE_PT_SmartBonePanel(bpy.types.Panel):
    bl_label = "Smart Bone Panel"
    bl_idname = "SmartBonePanel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Smart Bones"
    #bl_context = "posemode"   

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        smart_bone_tool = scene.smart_bone_tool
        
        
        #properties
        
        row = layout.row()
        
        row = layout.row()
        row.prop_search(smart_bone_tool, "armature_name", bpy.context.scene, "objects")
        
        row = layout.row()
        if context.scene.smart_bone_tool.armature_name != "":
            tgt_object = context.scene.objects[smart_bone_tool.armature_name]
            if tgt_object.type == "ARMATURE":
                row.prop_search(smart_bone_tool, "control_name", tgt_object.data, "bones")
                tgt_bone = context.scene.smart_bone_tool.control_name
            else:
                row.label(text = "Object Type = " + tgt_object.type, icon = "ERROR")
        else:
            row.row().label(text="No selected Object", icon = "ERROR")
        
        row = layout.row()
        row.prop(smart_bone_tool, "transform_channel")
        row = layout.row()
        row.prop(smart_bone_tool, "target_space")
        
        row = layout.row()
        if smart_bone_tool.target_space == "CUSTOM":
            row.prop_search(smart_bone_tool, "space_object_name", context.scene, "objects")
            
            space_object = bpy.data.objects[smart_bone_tool.space_object_name]
            if space_object.type == "ARMATURE":
                row = layout.row()
                row.prop_search(smart_bone_tool, "space_subtarget", space_object.data, "bones")

        row = layout.row()
        row.label(text = 'Transform Range')
        row = layout.row()
        row.prop(smart_bone_tool, "transform_min", text="min")
        row.prop(smart_bone_tool, "transform_max", text="max")
        
        row = layout.row()
        layout.prop_search(smart_bone_tool, "action_name", bpy.data, "actions")
        row = layout.row()
        row.label(text = 'Frame Range')
        row = layout.row()
        row.prop(smart_bone_tool, "frame_min", text="min")
        row.prop(smart_bone_tool, "frame_max", text="max")
        
        #operator
        if (smart_bone_tool.armature_name != "" 
        and smart_bone_tool.control_name != "" 
        and smart_bone_tool.action_name != "") :
            
            layout.row()
            layout.row().label(text = 'Operators')
            layout.operator("myops.add_smart_bone")
            layout.row()
            layout.operator("myops.delete_smart_bone")
            
            layout.separator()
        else:
            layout.row()
            layout.row().label(text = 'Invalid Inputs', icon = "ERROR")




#---------------------------------------------------------------------
#    Register
#---------------------------------------------------------------------


blender_classes = [
    SmartBoneProperties,
    OT_AddSmartBone,
    OT_DeleteSmartBone,
    POSE_PT_SmartBonePanel
]

def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    
    bpy.types.Scene.smart_bone_tool = bpy.props.PointerProperty(type=SmartBoneProperties)
    
def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

    del bpy.types.Scene.smart_bone_tool


if __name__ == "__main__":
    register()



