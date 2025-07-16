# Dateiname: mixme_rig.py
# MixMe Addon für Blender - Rig Management Funktionen
import bpy
import os
from mathutils import Euler
from bpy.types import Operator
from .mixme_xml import (
    get_rig_structure_from_xml,
    get_rig_structure_with_groups,
    get_tpose_from_xml
)

# Rig aus .blend-Datei laden
def append_rig_from_template(rig_name="Armature"):
    filepath = os.path.join(os.path.dirname(__file__), "template", "opensim_rig.blend")
    try:
        with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
            if rig_name in data_from.objects:
                data_to.objects = [rig_name]
        for obj in data_to.objects:
            if obj and obj.type == 'ARMATURE':
                bpy.context.collection.objects.link(obj)
                print(f"Rig '{rig_name}' importiert")
                return obj
    except Exception as e:
        print(f"Fehler beim Laden des Rig: {e}")
    return None

# Operator: Rig aus Vorlage laden
class MIXME_OT_load_template_rig(Operator):
    bl_idname = "mixme.load_template_rig"
    bl_label = "Load Template Rig"

    def execute(self, context):
        rig = append_rig_from_template()
        if rig:
            self.report({'INFO'}, f"Rig '{rig.name}' geladen")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Rig konnte nicht geladen werden")
            return {'CANCELLED'}

# Operator: Rig aus XML erzeugen
class MIXME_OT_create_rig_from_xml(Operator):
    bl_idname = "mixme.create_rig_from_xml"
    bl_label = "Create Rig from XML"

    def execute(self, context):
        bones_data = get_rig_structure_from_xml()

        bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
        armature = bpy.context.object
        armature.name = "XML_Rig"
        armature_data = armature.data
        armature_data.name = "XML_Rig_Data"

        edit_bones = armature_data.edit_bones
        bone_map = {}

        for bone_info in bones_data:
            bone = edit_bones.new(bone_info["name"])
            bone.head = bone_info["head"]
            bone.tail = bone_info["tail"]
            bone_map[bone_info["name"]] = bone

        # Eltern setzen
        for bone_info in bones_data:
            if bone_info.get("parent") and bone_info["parent"] in bone_map:
                bone_map[bone_info["name"]].parent = bone_map[bone_info["parent"]]

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, f"{len(bones_data)} Bones aus XML erzeugt")
        return {'FINISHED'}

# Operator: Rig mit Gruppen aus XML erzeugen
class MIXME_OT_create_rig_with_groups(Operator):
    bl_idname = "mixme.create_rig_with_groups"
    bl_label = "Create Rig with Groups from XML"

    def execute(self, context):
        bones_data = get_rig_structure_with_groups()

        bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
        rig = bpy.context.object
        rig.name = "XML_Rig"
        armature = rig.data
        armature.name = "XML_Rig_Data"

        edit_bones = armature.edit_bones
        bone_map = {}

        for bone_info in bones_data:
            bone = edit_bones.new(bone_info["name"])
            bone.head = bone_info["head"]
            bone.tail = bone_info["tail"]
            bone_map[bone_info["name"]] = bone

        bpy.ops.object.mode_set(mode='POSE')

        # Gruppen erstellen
        group_names = sorted(set(b["group"] for b in bones_data))
        group_map = {}
        for name in group_names:
            group = armature.pose.bone_groups.new(name=name)
            group.color_set = 'CUSTOM'
            group.colors.normal = (0.8, 0.8, 0.8)
            group.colors.select = (1.0, 1.0, 0.0)
            group.colors.active = (0.0, 1.0, 0.0)
            group_map[name] = group

        # Bones zu Gruppen zuweisen
        for bone_info in bones_data:
            pbone = rig.pose.bones.get(bone_info["name"])
            if pbone and bone_info["group"] in group_map:
                pbone.bone_group = group_map[bone_info["group"]]

        self.report({'INFO'}, f"{len(bones_data)} Bones mit Gruppen erstellt")
        return {'FINISHED'}

# Operator: T-Pose aus XML anwenden
class MIXME_OT_test_tpose(Operator):
    bl_idname = "mixme.test_tpose"
    bl_label = "Apply T-Pose from XML"

    def execute(self, context):
        rig = context.active_object
        if not rig or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an Armature object")
            return {'CANCELLED'}

        pose_data = get_tpose_from_xml()
        bpy.ops.object.mode_set(mode='POSE')

        for bone in rig.pose.bones:
            if bone.name in pose_data:
                data = pose_data[bone.name]
                bone.location = data["pos"]
                bone.rotation_euler = Euler(data["rot"], 'XYZ')

        self.report({'INFO'}, "T-Pose applied from XML")
        return {'FINISHED'}

class MIXME_OT_analyze_rig(Operator):
    bl_idname = "mixme.analyze_rig"
    bl_label = "Analyze Rig"

    def execute(self, context):
        rig = context.active_object
        if not rig or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        info = []
        for bone in rig.data.bones:
            info.append(f"{bone.name} → parent: {bone.parent.name if bone.parent else 'None'}")

        print("\n".join(info))
        self.report({'INFO'}, f"{len(info)} bones analyzed")
        return {'FINISHED'}


# class MIXME_OT_load_new_rig(Operator):
#     bl_idname = "mixme.load_new_rig"
#     bl_label = "Load New Rig"

#     def execute(self, context):
#         filepath = context.scene.mixme_props.rig_template_path
#         if not filepath or not os.path.exists(filepath):
#             self.report({'ERROR'}, "Rig template path is invalid")
#             return {'CANCELLED'}

#         try:
#             with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
#                 rigs = [name for name in data_from.objects if name.startswith("Armature")]
#                 if not rigs:
#                     self.report({'ERROR'}, "No armature found in file")
#                     return {'CANCELLED'}
#                 data_to.objects = [rigs[0]]

#             for obj in data_to.objects:
#                 if obj and obj.type == 'ARMATURE':
#                     bpy.context.collection.objects.link(obj)
#                     context.scene.mixme_props.target_rig = obj
#                     self.report({'INFO'}, f"Rig '{obj.name}' loaded and set as target")
#                     return {'FINISHED'}

#         except Exception as e:
#             self.report({'ERROR'}, f"Failed to load rig: {e}")
#             return {'CANCELLED'}

class MIXME_OT_analyze_rig(Operator):
    bl_idname = "mixme.analyze_rig"
    bl_label = "Analyze Rig"

    def execute(self, context):
        rig = context.active_object
        if not rig or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        info = []
        for bone in rig.data.bones:
            parent = bone.parent.name if bone.parent else "None"
            info.append(f"{bone.name} → parent: {parent}")

        print("\n".join(info))
        self.report({'INFO'}, f"{len(info)} bones analyzed")
        return {'FINISHED'}

class MIXME_OT_load_new_rig(Operator):
    bl_idname = "mixme.load_new_rig"
    bl_label = "Load New Rig"

    def execute(self, context):
        filepath = context.scene.mixme_props.rig_template_path
        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, "Rig template path is invalid")
            return {'CANCELLED'}

        try:
            with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                rigs = [name for name in data_from.objects if name.startswith("Armature")]
                if not rigs:
                    self.report({'ERROR'}, "No armature found in file")
                    return {'CANCELLED'}
                data_to.objects = [rigs[0]]

            for obj in data_to.objects:
                if obj and obj.type == 'ARMATURE':
                    bpy.context.collection.objects.link(obj)
                    context.scene.mixme_props.target_rig = obj
                    self.report({'INFO'}, f"Rig '{obj.name}' loaded and set as target")
                    return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Failed to load rig: {e}")
            return {'CANCELLED'}

class MIXME_OT_bind_mesh_to_rig(Operator):
    bl_idname = "mixme.bind_mesh_to_rig"
    bl_label = "Bind Mesh to Rig"

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

        bpy.ops.object.parent_set(type='ARMATURE')
        self.report({'INFO'}, f"Mesh '{mesh.name}' bound to rig '{rig.name}'")
        return {'FINISHED'}

class MIXME_OT_finetune_rig(Operator):
    bl_idname = "mixme.finetune_rig"
    bl_label = "Finetune Rig"

    def execute(self, context):
        rig = context.active_object
        if not rig or rig.type != 'ARMATURE':
            self.report({'ERROR'}, "Select an armature")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        for bone in rig.data.edit_bones:
            bone.use_connect = False
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Rig finetuned (disconnected bones)")
        return {'FINISHED'}
