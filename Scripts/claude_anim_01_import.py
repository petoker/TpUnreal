# Paso 1: importa las FBX de Mixamo (SourceAssets/Mixamo) a /Game/SurvivalHorror/Animations/Mixamo
import unreal, os, traceback

PROJ = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal"
LOG = os.path.join(PROJ, "Saved", "claude_log.txt")
SRC = os.path.join(PROJ, "SourceAssets", "Mixamo")
DST = "/Game/SurvivalHorror/Animations/Mixamo"


def log(*a):
    s = " ".join(str(x) for x in a)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")
    unreal.log("[CLAUDE] " + s)


def make_task(fn, skeleton=None):
    t = unreal.AssetImportTask()
    t.filename = fn
    t.destination_path = DST
    t.automated = True
    t.save = True
    t.replace_existing = True
    o = unreal.FbxImportUI()
    o.import_as_skeletal = True
    o.import_animations = True
    o.import_materials = False
    o.import_textures = False
    if skeleton is None:
        o.import_mesh = True
        o.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    else:
        o.import_mesh = False
        o.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
        o.skeleton = skeleton
    t.options = o
    return t


try:
    open(LOG, "w").close()
    log("== IMPORT START ==")
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    # 1) personaje con skin -> skeletal mesh + skeleton Mixamo
    skin = os.path.join(SRC, "Zombie_Walk_WithSkin.fbx")
    t = make_task(skin)
    tools.import_asset_tasks([t])
    log("skin imported:", list(t.imported_object_paths))
    skel = None
    mesh = None
    for p in unreal.EditorAssetLibrary.list_assets(DST, recursive=False):
        a = unreal.load_asset(p)
        if isinstance(a, unreal.Skeleton):
            skel = a
        if isinstance(a, unreal.SkeletalMesh):
            mesh = a
    log("mixamo skeleton:", skel.get_path_name() if skel else None, "mesh:", mesh.get_path_name() if mesh else None)
    # 2) resto como animaciones con ese skeleton
    tasks = []
    for f in sorted(os.listdir(SRC)):
        if f.lower().endswith(".fbx") and f != "Zombie_Walk_WithSkin.fbx":
            tasks.append(make_task(os.path.join(SRC, f), skel))
    tools.import_asset_tasks(tasks)
    for t in tasks:
        log("anim:", os.path.basename(t.filename), "->", list(t.imported_object_paths))
    log("== FOLDER CONTENT ==")
    for p in unreal.EditorAssetLibrary.list_assets(DST, recursive=True):
        log(p, type(unreal.load_asset(p)).__name__)
    log("== IMPORT DONE ==")
except Exception:
    log("ERROR", traceback.format_exc())
