# Dateiname: mixme_mapping.py
# MixMe Addon für Blender - Bone Mapping Funktionen
import bpy
import json
import os
from bpy.types import Operator
from .mixme_xml import get_bone_mapping_from_xml

# Mapping aus XML laden
def get_bone_mapping():
    return get_bone_mapping_from_xml()

# Default-Mapping aus JSON laden
def get_template_path(filename):
    return os.path.join(os.path.dirname(__file__), "template", filename)

def load_default_mapping():
    filepath = get_template_path("default_mapping.json")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            bone_map = json.load(f)
        prefix = ""  # Optional: aus Datei extrahieren        
        return prefix, bone_map
    except Exception as e:
        print(f"Fehler beim Laden der Mapping-Datei: {e}")
        return "", {}

# Mapping speichern
def save_bone_mapping(filepath, prefix, bone_map):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(bone_map, f, indent=4)
        print(f"Mapping gespeichert unter: {filepath}")
    except Exception as e:
        print(f"Fehler beim Speichern des Mappings: {e}")

# Operator: Default-Mapping laden
class MIXME_OT_load_default_mapping(Operator):
    bl_idname = "mixme.load_default_mapping"
    bl_label = "Load Default Mapping"

    def execute(self, context):
        prefix, bone_map = load_default_mapping()
        context.scene.mixme_props.prefix = prefix
        self.report({'INFO'}, f"{len(bone_map)} Bones geladen")
        return {'FINISHED'}

# Operator: Mapping speichern
class MIXME_OT_save_mapping(Operator):
    bl_idname = "mixme.save_mapping"
    bl_label = "Save Bone Mapping"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an Armature object!")
            return {'CANCELLED'}

        bone_map = {bone.name: bone.name for bone in obj.data.bones}
        prefix = context.scene.mixme_props.prefix
        filepath = context.scene.mixme_props.mapping_file

        save_bone_mapping(filepath, prefix, bone_map)
        self.report({'INFO'}, "Bone mapping saved!")
        return {'FINISHED'}

class MIXME_OT_retarget_animation(Operator):
    bl_idname = "mixme.retarget_animation"
    bl_label = "Retarget Animation"

    def execute(self, context):
        src_rig = context.active_object
        tgt_rig = context.scene.mixme_props.target_rig

        if not src_rig or not tgt_rig:
            self.report({'ERROR'}, "Source and target rig must be set")
            return {'CANCELLED'}

        if not src_rig.animation_data or not src_rig.animation_data.action:
            self.report({'ERROR'}, "Source rig has no animation")
            return {'CANCELLED'}

        prefix, bone_map = get_bone_mapping()
        src_action = src_rig.animation_data.action
        new_action = bpy.data.actions.new(name=f"{tgt_rig.name}_Retargeted")
        tgt_rig.animation_data_create()
        tgt_rig.animation_data.action = new_action

        for fcurve in src_action.fcurves:
            path = fcurve.data_path
            if '"' not in path:
                continue

            src_bone = path.split('"')[1]
            if src_bone not in bone_map:
                continue

            tgt_bone = bone_map[src_bone]
            dst_path = path.replace(f'"{src_bone}"', f'"{tgt_bone}"')

            new_fcurve = new_action.fcurves.new(data_path=dst_path, index=fcurve.array_index)
            new_fcurve.keyframe_points.add(len(fcurve.keyframe_points))

            for i, kp in enumerate(fcurve.keyframe_points):
                new_fcurve.keyframe_points[i].co = kp.co
                new_fcurve.keyframe_points[i].interpolation = kp.interpolation

        self.report({'INFO'}, f"Animation retargeted to {tgt_rig.name}")
        return {'FINISHED'}
