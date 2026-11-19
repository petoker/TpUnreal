# Paso 5: reemplaza las AS_* (retarget manual roto) por las AUTO_* del retargeter automatico de UE
import unreal, os, traceback
LOG = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_log5.txt"
eal = unreal.EditorAssetLibrary
A = "/Game/SurvivalHorror/Animations"
def log(*a):
    s = " ".join(str(x) for x in a)
    open(LOG, "a", encoding="utf-8").write(s + "\n"); unreal.log("[CLAUDE] " + s)
try:
    open(LOG, "w").close()
    for p in eal.list_assets("/Game/SurvivalHorror", recursive=False):
        name = p.split("/")[-1].split(".")[0]
        if not name.startswith("AUTO_"):
            continue
        base = name[5:]
        if base == "Zombie_Walk_WithSkin_Anim":
            base = "Zombie_Walk"
        folder = A + ("/Zombie" if base.startswith("Zombie") else "/Player")
        dest = folder + "/AS_" + base
        if eal.does_asset_exist(dest):
            eal.delete_asset(dest)
        ok = eal.rename_asset("/Game/SurvivalHorror/" + name, dest)
        log("swap", name, "->", dest, ok)
    for old in (A + "/Retarget/RTG_Mixamo_To_Manny", A + "/Retarget/IK_Mixamo"):
        if eal.does_asset_exist(old):
            log("del", old, eal.delete_asset(old))
    eal.save_directory(A)
    log("== SWAP DONE ==")
except Exception:
    log("ERROR", traceback.format_exc())
