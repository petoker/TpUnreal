# Paso 2: IK Rig de Mixamo + Retargeter Mixamo->Manny + retarget en lote
import unreal, os, traceback

PROJ = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal"
LOG = os.path.join(PROJ, "Saved", "claude_log.txt")
MIX = "/Game/SurvivalHorror/Animations/Mixamo"
RIGS = "/Game/SurvivalHorror/Animations/Retarget"
OUT_P = "/Game/SurvivalHorror/Animations/Player"
OUT_Z = "/Game/SurvivalHorror/Animations/Zombie"


def log(*a):
    s = " ".join(str(x) for x in a)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")
    unreal.log("[CLAUDE] " + s)


def methods(o):
    return [m for m in dir(o) if not m.startswith("_")]


ALIGN = globals().get("ALIGN_SIDE", unreal.RetargetSourceOrTarget.TARGET)
def close_editors():
    s = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
    try:
        for a in s.get_all_edited_assets():
            s.close_all_editors_for_asset(a)
    except Exception as e:
        unreal.log("close err %s" % e)

try:
    pass
    log("== RETARGET START ==")
    close_editors()
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    eal = unreal.EditorAssetLibrary
    src_mesh = unreal.load_asset(globals().get("SRC_MESH_PATH", MIX + "/SK_Mixamo_TPose"))
    tgt_mesh = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny")
    tgt_rig = unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin")
    log("src", src_mesh, "tgt", tgt_mesh, "tgt_rig", tgt_rig)

    # --- IK Rig Mixamo
    if eal.does_asset_exist(RIGS + "/IK_Mixamo"):
        eal.delete_asset(RIGS + "/IK_Mixamo")
    if True:
        rig = tools.create_asset("IK_Mixamo", RIGS, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
    rc = unreal.IKRigController.get_controller(rig)
    log("IKRigController methods:", methods(rc))
    rc.set_skeletal_mesh(src_mesh)
    ok = rc.apply_auto_generated_retarget_definition()
    log("auto retarget def:", ok)
    try:
        log("chains:", [str(c.chain_name) for c in rc.get_retarget_chains()])
    except Exception as e:
        log("chains err", e)
    eal.save_loaded_asset(rig)

    # --- Retargeter
    if eal.does_asset_exist(RIGS + "/RTG_Mixamo_To_Manny"):
        eal.delete_asset(RIGS + "/RTG_Mixamo_To_Manny")
    if True:
        rtg = tools.create_asset("RTG_Mixamo_To_Manny", RIGS, unreal.IKRetargeter, unreal.IKRetargetFactory())
    xc = unreal.IKRetargeterController.get_controller(rtg)
    log("IKRetargeterController methods:", methods(xc))
    S = unreal.RetargetSourceOrTarget.SOURCE
    T = unreal.RetargetSourceOrTarget.TARGET
    xc.set_ik_rig(S, rig)
    xc.set_ik_rig(T, tgt_rig)
    for fn, args in [("set_preview_mesh", (S, src_mesh)), ("set_preview_mesh", (T, tgt_mesh))]:
        try:
            getattr(xc, fn)(*args)
        except Exception as e:
            log(fn, "err", e)
    for fn, args in [("add_default_ops", ()), ("auto_map_chains", (unreal.AutoMapChainType.FUZZY, True))]:
        try:
            r = getattr(xc, fn)(*args)
            log(fn, "->", r)
        except Exception as e:
            log(fn, "err", e)
    # Mixamo en T-pose, Manny en A-pose: alinear la pose de retarget del source
    for side in (ALIGN,):
        try:
            xc.auto_align_all_bones(side)
            log("auto_align_all_bones ok", side)
        except Exception as e:
            log("auto_align err", e)
    eal.save_loaded_asset(rtg)

    # --- Retarget en lote
    anims = []
    for p in eal.list_assets(MIX, recursive=False):
        a = unreal.load_asset(p)
        if isinstance(a, unreal.AnimSequence):
            anims.append(unreal.AssetData(p) if False else unreal.EditorAssetLibrary.find_asset_data(p))
    log("anims to retarget:", len(anims))
    log("DOC:", unreal.IKRetargetBatchOperation.duplicate_and_retarget.__doc__)
    try:
        res = unreal.IKRetargetBatchOperation.duplicate_and_retarget(anims, src_mesh, tgt_mesh, rtg, "", "", "RT_", "", MIX, True)
    except Exception as e:
        log("try2 err", e)
        res = unreal.IKRetargetBatchOperation.duplicate_and_retarget(anims, src_mesh, tgt_mesh, rtg, "", "", "RT_", "", MIX, True, True)
    log("retargeted:", [str(r.package_name) for r in res])

    # --- mover y renombrar a carpetas finales (AS_*)
    for r in res:
        p = str(r.package_name)
        base = p.split("/")[-1][3:]  # sin RT_
        if base == "Zombie_Walk_WithSkin_Anim":
            base = "Zombie_Walk"
        dest = (OUT_Z if base.startswith("Zombie") else OUT_P) + "/AS_" + base
        if eal.does_asset_exist(dest):
            eal.delete_asset(dest)
        ok = eal.rename_asset(p, dest)
        log("move", p, "->", dest, ok)
    eal.save_directory("/Game/SurvivalHorror/Animations")
    log("== RETARGET DONE ==")
except Exception:
    log("ERROR", traceback.format_exc())
