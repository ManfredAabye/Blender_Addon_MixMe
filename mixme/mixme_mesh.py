# Dateiname: mixme_mesh.py
# MixMe Addon für Blender - Mesh Funktionen
import bpy
from bpy.types import Operator

# Operator: Transforms anwenden
class MIXME_OT_apply_transforms(Operator):
    bl_idname = "mixme.apply_transforms"
    bl_label = "Apply Transforms"

    def execute(self, context):
        for obj in context.selected_objects:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        self.report({'INFO'}, "Transforms applied")
        return {'FINISHED'}

# Operator: Mesh bereinigen
class MIXME_OT_clean_mesh(Operator):
    bl_idname = "mixme.clean_mesh"
    bl_label = "Clean Mesh"

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.remove_doubles()
                bpy.ops.mesh.normals_make_consistent(inside=False)
                bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Mesh cleaned")
        return {'FINISHED'}

# Operator: Auto Weight
class MIXME_OT_auto_weight(Operator):
    bl_idname = "mixme.auto_weight"
    bl_label = "Auto Weight"

    def execute(self, context):
        rig = None
        mesh = None
        for obj in context.selected_objects:
            if obj.type == 'ARMATURE':
                rig = obj
            elif obj.type == 'MESH':
                mesh = obj

        if not rig or not mesh:
            self.report({'ERROR'}, "Select one rig and one mesh")
            return {'CANCELLED'}

        bpy.ops.object.select_all(action='DESELECT')
        rig.select_set(True)
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = rig

        bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        self.report({'INFO'}, "Mesh bound to rig with auto weights")
        return {'FINISHED'}

# Operator: Weight Paint Mode aktivieren
class MIXME_OT_weight_paint_mode(Operator):
    bl_idname = "mixme.weight_paint_mode"
    bl_label = "Weight Paint Mode"

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        self.report({'INFO'}, "Weight paint mode activated")
        return {'FINISHED'}

# Operator: Fehlende Vertex Groups prüfen
class MIXME_OT_check_weights(Operator):
    bl_idname = "mixme.check_weights"
    bl_label = "Check Missing Weights"

    def execute(self, context):
        mesh = context.active_object
        if not mesh or mesh.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        rig = mesh.parent
        if not rig or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Mesh must be parented to an armature")
            return {'CANCELLED'}

        missing = []
        for bone in rig.data.bones:
            if bone.name not in mesh.vertex_groups:
                missing.append(bone.name)

        if missing:
            self.report({'WARNING'}, f"Missing weights for: {', '.join(missing)}")
        else:
            self.report({'INFO'}, "All bones have weights")
        return {'FINISHED'}

# Operator: Bone-Hierarchie prüfen
class MIXME_OT_check_orphans(Operator):
    bl_idname = "mixme.check_orphans"
    bl_label = "Check Bone Hierarchy"

    def execute(self, context):
        rig = context.active_object
        if not rig or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        orphans = [bone.name for bone in rig.data.bones if bone.parent is None]
        self.report({'INFO'}, f"Orphan bones: {', '.join(orphans)}")
        return {'FINISHED'}

class MIXME_OT_adjust_weights(Operator):
    bl_idname = "mixme.adjust_weights"
    bl_label = "Adjust Weights"

    def execute(self, context):
        mesh = context.active_object
        if not mesh or mesh.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        bpy.ops.paint.weight_gradient(type='LINEAR')
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Weights adjusted with gradient")
        return {'FINISHED'}
