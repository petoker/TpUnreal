# Paso 3: importa Remy en T-pose sobre el skeleton Mixamo existente y rehace el retarget
import unreal, os, traceback
PROJ = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal"
LOG = os.path.join(PROJ, "Saved", "claude_log.txt")
MIX = "/Game/SurvivalHorror/Animations/Mixamo"
def log(*a):
    s = " ".join(str(x) for x in a)
    with open(LOG, "a", encoding="utf-8") as f: f.write(s + "\n")
    unreal.log("[CLAUDE] " + s)
def close_editors():
    s = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
    try:
        for a in s.get_all_edited_assets():
            s.close_all_editors_for_asset(a)
    except Exception as e:
        unreal.log("close err %s" % e)

try:
    close_editors()
    open(LOG, "w").close()
    skel = unreal.load_asset(MIX + "/Zombie_Walk_WithSkin_Skeleton")
    t = unreal.AssetImportTask()
    t.filename = os.path.join(PROJ, "SourceAssets", "Mixamo", "Remy_TPose.fbx")
    t.destination_path = MIX
    t.destination_name = "SK_Mixamo_TPose"
    t.automated = True; t.save = True; t.replace_existing = True
    o = unreal.FbxImportUI()
    o.import_mesh = True; o.import_as_skeletal = True; o.import_animations = False
    o.import_materials = False; o.import_textures = False
    o.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    o.skeleton = skel
    t.options = o
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
    log("tpose imported:", list(t.imported_object_paths))
except Exception:
    log("ERROR", traceback.format_exc())
