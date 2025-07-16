# MixMe Addon für Blender
# MixMe Addon für Blender - UI Funktionen
import bpy
from bpy.types import Panel, Operator
from .mixme_props import MixMeProperties

# Übersetzungshilfe
def iface_(text):
    return bpy.app.translations.pgettext_iface(text)

# UI Panel
class MIXME_PT_main(Panel):
    bl_label = iface_("MixMe")
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MixMe"

    def draw(self, context):
        layout = self.layout

        layout.label(text=iface_("Templates:"))
        layout.operator("mixme.load_default_mapping", text=iface_("Load Default Mapping"))
        layout.operator("mixme.load_template_rig", text=iface_("Load Template Rig"))
        layout.operator("mixme.create_rig_from_xml", text=iface_("Create Rig from XML"))
        layout.operator("mixme.create_rig_with_groups", text=iface_("Create Rig with Groups"))
        layout.operator("mixme.test_tpose", text=iface_("Apply T-Pose"))

        layout.label(text="Retargeting:")
        layout.operator("mixme.retarget_animation", text="Retarget Animation")


        layout.separator()
        layout.label(text=iface_("Rig Conversion:"))
        layout.operator("mixme.convert_rig", text=iface_("Convert Rig"))
        layout.operator("mixme.map_bones", text=iface_("Map Bones"))

        layout.separator()
        layout.label(text=iface_("BVH Tools:"))
        layout.operator("mixme.import_bvh", text=iface_("Import BVH"))
        layout.operator("mixme.export_bvh", text=iface_("Export BVH"))

        layout.separator()
        layout.label(text=iface_("Mesh & Weight Tools:"))
        layout.operator("mixme.apply_transforms", text=iface_("Apply Transforms"))
        layout.operator("mixme.clean_mesh", text=iface_("Clean Mesh"))
        layout.operator("mixme.auto_weight", text=iface_("Auto Weight"))
        layout.operator("mixme.weight_paint_mode", text=iface_("Weight Paint Mode"))
        layout.operator("mixme.check_weights", text=iface_("Check Missing Weights"))
        layout.operator("mixme.check_orphans", text=iface_("Check Bone Hierarchy"))

        layout.separator()
        layout.label(text=iface_("Selection Tools:"))
        layout.operator("mixme.select_all_armatures", text=iface_("Select All Armatures"))
        layout.operator("mixme.select_all_meshes", text=iface_("Select All Meshes"))

# Operator: Alle Armatures auswählen
class MIXME_OT_select_all_armatures(Operator):
    bl_idname = "mixme.select_all_armatures"
    bl_label = iface_("Select All Armatures")

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            if obj.type == 'ARMATURE':
                obj.select_set(True)
        self.report({'INFO'}, "All armatures selected")
        return {'FINISHED'}

# Operator: Alle Meshes auswählen
class MIXME_OT_select_all_meshes(Operator):
    bl_idname = "mixme.select_all_meshes"
    bl_label = iface_("Select All Meshes")

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        self.report({'INFO'}, "All meshes selected")
        return {'FINISHED'}
