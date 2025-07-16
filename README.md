# MixMe Rig Converter – Dokumentation Alpha

## Übersicht

**MixMe** ist ein Blender-Add-on zur Konvertierung und Retargeting von Rigs und Animationen. Es unterstützt:

- ✅ Bone-Mapping (Mixamo → OpenSim oder eigene Zuordnung)
- ✅ Rig-Erstellung aus XML
- ✅ BVH-Import und Export
- ✅ Retargeting von Animationen
- ✅ Mesh-Bindung und Weighting
- ✅ Rig-Analyse und Tools zur Bereinigung

---

## 🔧 Installation

1. Lade den Ordner `mixme_addon` als ZIP-Datei.
2. Öffne Blender → Edit → Preferences → Add-ons → Install.
3. Wähle die ZIP-Datei → Aktiviere das Add-on „MixMe Rig Converter“.
4. Sidebar öffnen (`N`) → Tab „MixMe“.

---

## Funktionen im UI

### 🔹 Templates

- **Load Default Mapping**: Lädt Bone-Mapping aus `default_mapping.json`.
- **Load Template Rig**: Lädt Rig aus `opensim_rig.blend`.
- **Create Rig from XML**: Erzeugt Rig aus `avatar_skeleton.xml`.
- **Create Rig with Groups**: Erzeugt Rig mit Bone-Gruppen.
- **Apply T-Pose**: Setzt T-Pose aus XML auf aktives Rig.

### 🔹 Rig Conversion

- **Convert Rig**: Benennt Bones gemäß Mapping.
- **Map Bones**: Überträgt Pose-Daten von einem Rig auf ein anderes.

### 🔹 BVH Tools

- **Import BVH**: Lädt `.bvh` Datei und überträgt Animation.
- **Export BVH**: Exportiert aktuelle Animation als `.bvh`.

### 🔹 Mesh & Weight Tools

- **Apply Transforms**: Setzt Location, Rotation, Scale zurück.
- **Clean Mesh**: Entfernt doppelte Vertices, korrigiert Normalen.
- **Auto Weight**: Bindet Mesh an Rig mit automatischer Gewichtung.
- **Weight Paint Mode**: Aktiviert Weight Paint.
- **Check Missing Weights**: Prüft auf fehlende Vertex Groups.
- **Check Bone Hierarchy**: Zeigt Bones ohne Eltern.

### 🔹 Selection Tools

- **Select All Armatures**: Wählt alle Rigs aus.
- **Select All Meshes**: Wählt alle Meshes aus.

### 🔹 Retargeting

- **Retarget Animation**: Überträgt Animation vom Quell-Rig auf Ziel-Rig.

---

## Dateistruktur

```
mixme_addon/
├── __init__.py
├── mixme_ui.py
├── mixme_rig.py
├── mixme_mesh.py
├── mixme_bvh.py
├── mixme_convert.py
├── mixme_mapping.py
├── mixme_props.py
├── mixme_xml.py
└── template/
    ├── opensim_rig.blend
    ├── avatar_skeleton.xml
    └── default_mapping.json
```

---

## Hinweise

- Das Bone-Mapping kann aus XML oder JSON geladen werden.
- Ziel-Rig für Retargeting wird über `mixme_props.target_rig` gesetzt.
- Die XML-Datei muss `<bone>`-Elemente mit `name`, `pos`, `rot`, `group` enthalten.

---

## Beispielablauf

1. **Load Template Rig**
2. **Import Mesh**
3. **Auto Weight**
4. **Convert Rig**
5. **Import BVH**
6. **Retarget Animation**
7. **Export BVH**

---
