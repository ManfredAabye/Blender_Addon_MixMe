# Dateiname: mixme_bvh.py
# MixMe Addon für Blender - BVH Import/Export Funktionen
import bpy
import os
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper, ExportHelper
from .mixme_mapping import get_bone_mapping

# Operator: BVH importieren und auf Ziel-Rig anwenden
class MIXME_OT_import_bvh(Operator, ImportHelper):
    bl_idname = "mixme.import_bvh"
    bl_label = "Import BVH"
    bl_description = "Import a BVH file and retarget to active rig"
    filename_ext = ".bvh"
    filter_glob: bpy.props.StringProperty(default="*.bvh", options={'HIDDEN'})

    def execute(self, context):
        target_rig = context.active_object
        if not target_rig or target_rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature before importing BVH")
            return {'CANCELLED'}

        filepath = self.filepath or context.scene.mixme_props.import_path
        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, "Valid BVH file not found")
            return {'CANCELLED'}

        # BVH importieren
        bpy.ops.import_anim.bvh(filepath=filepath)
        bvh_rig = context.selected_objects[-1]

        if not bvh_rig or bvh_rig.type != 'ARMATURE':
            self.report({'ERROR'}, "BVH import failed")
            return {'CANCELLED'}

        bvh_action = bvh_rig.animation_data.action if bvh_rig.animation_data else None
        if not bvh_action:
            self.report({'ERROR'}, "No animation found in BVH")
            return {'CANCELLED'}

        # Mapping laden
        prefix, bone_map = get_bone_mapping()

        # Neue Action für Ziel-Rig
        new_action = bpy.data.actions.new(name=f"{target_rig.name}_BVH_Action")
        target_rig.animation_data_create()
        target_rig.animation_data.action = new_action

        # Keyframes übertragen
        for fcurve in bvh_action.fcurves:
            src_path = fcurve.data_path
            src_bone = src_path.split('"')[1] if '"' in src_path else None

            if src_bone and src_bone in bone_map:
                dst_bone = bone_map[src_bone]
                dst_path = src_path.replace(f'"{src_bone}"', f'"{dst_bone}"')

                new_fcurve = new_action.fcurves.new(data_path=dst_path, index=fcurve.array_index)
                new_fcurve.keyframe_points.add(count=len(fcurve.keyframe_points))

                for i, kp in enumerate(fcurve.keyframe_points):
                    new_fcurve.keyframe_points[i].co = kp.co
                    new_fcurve.keyframe_points[i].interpolation = kp.interpolation

        # BVH-Rig entfernen
        bpy.data.objects.remove(bvh_rig, do_unlink=True)

        self.report({'INFO'}, "BVH animation applied to rig")
        return {'FINISHED'}

# Operator: Animation als BVH exportieren
class MIXME_OT_export_bvh(Operator, ExportHelper):
    bl_idname = "mixme.export_bvh"
    bl_label = "Export BVH"
    bl_description = "Export animation as BVH file"
    filename_ext = ".bvh"
    filter_glob: bpy.props.StringProperty(default="*.bvh", options={'HIDDEN'})

    def execute(self, context):
        bpy.ops.export_anim.bvh(
            filepath=self.filepath,
            global_scale=1.0,
            frame_start=bpy.context.scene.frame_start,
            frame_end=bpy.context.scene.frame_end,
            rotate_mode='XYZ'
        )
        self.report({'INFO'}, "BVH exported successfully!")
        return {'FINISHED'}
