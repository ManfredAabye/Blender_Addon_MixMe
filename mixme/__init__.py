# Datei __init__.py
# MixMe Addon für Blender

bl_info = {
    "name": "MixMe Rig Converter",
    "author": "Manfred Aabye",
    "version": (1, 0, 0),
    "blender": (4, 4, 3),
    "location": "View3D > Sidebar > MixMe",
    "description": "Konvertiert Rigs, BVH-Dateien und führt Retargeting durch",
    "category": "Animation",
}

import bpy
import importlib

# Module reload (für Entwicklung nützlich)
from . import (
    mixme_convert,
    mixme_rig,
    mixme_bvh,
    mixme_mesh,
    mixme_mapping,
    mixme_ui,
    mixme_props,
    mixme_xml,
)

importlib.reload(mixme_convert)
importlib.reload(mixme_rig)
importlib.reload(mixme_bvh)
importlib.reload(mixme_mesh)
importlib.reload(mixme_mapping)
importlib.reload(mixme_ui)
importlib.reload(mixme_props)
importlib.reload(mixme_xml)

# Alle Klassen sammeln
classes = (
    # Props
    mixme_props.MixMeProperties,

    # UI
    mixme_ui.MIXME_PT_main,
    mixme_ui.MIXME_OT_select_all_armatures,
    mixme_ui.MIXME_OT_select_all_meshes,

    # Mapping
    mixme_mapping.MIXME_OT_load_default_mapping,
    mixme_mapping.MIXME_OT_save_mapping,
    mixme_mapping.MIXME_OT_retarget_animation,

    # Convert
    mixme_convert.MIXME_OT_convert_rig,
    mixme_convert.MIXME_OT_map_bones,

    # Rig
    mixme_rig.MIXME_OT_load_template_rig,
    mixme_rig.MIXME_OT_analyze_rig,
    mixme_rig.MIXME_OT_load_new_rig,
    mixme_rig.MIXME_OT_bind_mesh_to_rig,
    mixme_rig.MIXME_OT_test_tpose,
    mixme_rig.MIXME_OT_finetune_rig,
    mixme_rig.MIXME_OT_create_rig_from_xml,
    mixme_rig.MIXME_OT_create_rig_with_groups,

    # BVH
    mixme_bvh.MIXME_OT_import_bvh,
    mixme_bvh.MIXME_OT_export_bvh,

    # Mesh
    mixme_mesh.MIXME_OT_auto_weight,
    mixme_mesh.MIXME_OT_adjust_weights,
    mixme_mesh.MIXME_OT_weight_paint_mode,
    mixme_mesh.MIXME_OT_check_weights,
    mixme_mesh.MIXME_OT_clean_mesh,
    mixme_mesh.MIXME_OT_apply_transforms,
    mixme_mesh.MIXME_OT_check_orphans,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.mixme_props = bpy.props.PointerProperty(type=mixme_props.MixMeProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.mixme_props
