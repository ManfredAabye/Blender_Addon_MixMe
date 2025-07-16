# Dateiname: mixme_convert.py
# MixMe Addon für Blender - Rig Konvertierungsfunktionen
import bpy
from bpy.types import Operator
from .mixme_mapping import get_bone_mapping

# Übersetzungshilfe
def iface_(text):
    return bpy.app.translations.pgettext_iface(text)

# 🔁 Operator: Rig konvertieren mit Mapping
class MIXME_OT_convert_rig(Operator):
    bl_idname = "mixme.convert_rig"
    bl_label = iface_("Convert Rig")
    bl_description = iface_("Renames bones to target format using mapping")
    bl_translation_context = 'Operator'

    def execute(self, context):
        prefix, bone_map = get_bone_mapping()
        obj = context.active_object

        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, iface_("Select an Armature object!"))
            return {'CANCELLED'}

        renamed = 0
        for bone in obj.data.bones:
            name_clean = bone.name[len(prefix):] if prefix and bone.name.startswith(prefix) else bone.name
            if name_clean in bone_map:
                bone.name = bone_map[name_clean]
                renamed += 1

        self.report({'INFO'}, iface_(f"{renamed} Bones renamed"))
        return {'FINISHED'}

# 🔗 Operator: Bone-Mapping anwenden (Pose-Mode)
class MIXME_OT_map_bones(Operator):
    bl_idname = "mixme.map_bones"
    bl_label = iface_("Map Bones")
    bl_description = iface_("Applies bone mapping to pose bones")
    bl_translation_context = 'Operator'

    def execute(self, context):
        prefix, bone_map = get_bone_mapping()
        src_rig = context.active_object
        tgt_rig = context.scene.mixme_props.target_rig

        if not src_rig or not tgt_rig or src_rig.type != 'ARMATURE' or tgt_rig.type != 'ARMATURE':
            self.report({'ERROR'}, iface_("Select source and target armatures"))
            return {'CANCELLED'}

        for bone in src_rig.pose.bones:
            if bone.name in bone_map:
                target_name = bone_map[bone.name]
                if target_name in tgt_rig.pose.bones:
                    tgt_bone = tgt_rig.pose.bones[target_name]
                    tgt_bone.location = bone.location
                    tgt_bone.rotation_quaternion = bone.rotation_quaternion

        self.report({'INFO'}, iface_("Bone mapping applied"))
        return {'FINISHED'}
