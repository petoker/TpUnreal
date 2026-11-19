# Paso 9: asigna los Anim Blueprints propios a BP_SurvivalCharacter y BP_Zombie
import unreal, traceback
LOG = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_log9.txt"
def log(*a):
    s = " ".join(str(x) for x in a)
    open(LOG, "a", encoding="utf-8").write(s + "\n"); unreal.log("[CLAUDE] " + s)
open(LOG, "w").close()
pairs = [("/Game/SurvivalHorror/Blueprints/Characters/BP_SurvivalCharacter", "/Game/SurvivalHorror/Animations/ABP_SurvivalCharacter"),
         ("/Game/SurvivalHorror/Blueprints/Enemies/BP_Zombie", "/Game/SurvivalHorror/Animations/ABP_Zombie")]
for bpp, abpp in pairs:
    try:
        bp = unreal.load_asset(bpp)
        abp = unreal.load_asset(abpp)
        cdo = unreal.get_default_object(bp.generated_class())
        mesh = cdo.get_editor_property("mesh")
        log(bpp, "before", mesh.get_editor_property("anim_class"))
        mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
        mesh.set_editor_property("anim_class", abp.generated_class())
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        unreal.EditorAssetLibrary.save_loaded_asset(bp, False)
        cdo2 = unreal.get_default_object(bp.generated_class())
        log(bpp, "after", cdo2.get_editor_property("mesh").get_editor_property("anim_class"))
    except Exception:
        log("ERR", bpp, traceback.format_exc())
