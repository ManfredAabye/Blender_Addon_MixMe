# Dateiname: mixme_props.py
# MixMe Addon für Blender - Property Group für MixMe Einstellungen
import bpy

class MixMeProperties(bpy.types.PropertyGroup):
    # 🔁 Bone-Mapping
    mapping_file: bpy.props.StringProperty(
        name="Mapping File",
        description="Pfad zur Bone-Mapping-Datei",
        subtype='FILE_PATH'
    )

    prefix: bpy.props.StringProperty(
        name="Bone Prefix",
        description="Präfix, das von Bone-Namen entfernt werden soll",
        default=""
    )

    # 📦 Export / Import
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Pfad für BVH-Export",
        subtype='DIR_PATH'
    )

    import_path: bpy.props.StringProperty(
        name="Import Path",
        description="Pfad für BVH-Import",
        subtype='FILE_PATH'
    )

    # 🧱 Rig-Vorlage
    rig_template_path: bpy.props.StringProperty(
        name="Rig Template Path",
        description="Pfad zu einer .blend-Datei mit Rig-Vorlage",
        subtype='FILE_PATH'
    )

    # 🎯 Ziel-Rig für Retargeting
    target_rig: bpy.props.PointerProperty(
        name="Target Rig",
        description="Armature-Objekt für Retargeting",
        type=bpy.types.Object
    )
