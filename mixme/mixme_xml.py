# Dateiname: mixme_xml.py
# MixMe Addon für Blender - XML Parsing Funktionen
import bpy
import os
import xml.etree.ElementTree as ET
from mathutils import Euler

def get_template_xml_path():
    return os.path.join(os.path.dirname(__file__), "template", "avatar_skeleton.xml")

def get_bone_mapping_from_xml():
    try:
        tree = ET.parse(get_template_xml_path())
        root = tree.getroot()
        bone_map = {}

        for bone in root.findall(".//bone"):
            target = bone.get("name")
            aliases = bone.get("aliases", "").split()
            for alias in aliases:
                bone_map[alias] = target

        return "", bone_map
    except Exception as e:
        print(f"Fehler beim Laden der Mapping-XML: {e}")
        return "", {}

def get_tpose_from_xml():
    try:
        tree = ET.parse(get_template_xml_path())
        root = tree.getroot()
        pose_data = {}

        for bone in root.findall(".//bone"):
            name = bone.get("name")
            pos = tuple(map(float, bone.get("pos").split()))
            rot = tuple(map(float, bone.get("rot").split()))
            pose_data[name] = {"pos": pos, "rot": rot}

        return pose_data
    except Exception as e:
        print(f"Fehler beim Laden der T-Pose: {e}")
        return {}

def get_rig_structure_from_xml():
    try:
        tree = ET.parse(get_template_xml_path())
        root = tree.getroot()
        bones = []

        for bone in root.findall(".//bone"):
            name = bone.get("name")
            pos = tuple(map(float, bone.get("pos").split()))
            rot = tuple(map(float, bone.get("rot").split()))
            bones.append({
                "name": name,
                "parent": None,  # Optional: Hierarchie später ergänzen
                "head": pos,
                "tail": (pos[0], pos[1], pos[2] + 0.1),
                "rot": rot
            })

        return bones
    except Exception as e:
        print(f"Fehler beim Laden der Rig-Struktur: {e}")
        return []

def get_rig_structure_with_groups():
    try:
        tree = ET.parse(get_template_xml_path())
        root = tree.getroot()
        bones = []

        for bone in root.findall(".//bone"):
            name = bone.get("name")
            group = bone.get("group", "Ungrouped")
            pos = tuple(map(float, bone.get("pos").split()))
            bones.append({
                "name": name,
                "group": group,
                "head": pos,
                "tail": (pos[0], pos[1], pos[2] + 0.1)
            })

        return bones
    except Exception as e:
        print(f"Fehler beim Laden der Gruppenstruktur: {e}")
        return []
