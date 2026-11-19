import unreal, traceback
LOG = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_probe10.txt"
o = []
for p in ["/Game/SurvivalHorror/Animations/Player/BS_Player_Crouch", "/Game/SurvivalHorror/Animations/Zombie/BS_Zombie_Locomotion", "/Game/SurvivalHorror/Animations/Player/BS_Player_PistolAim", "/Game/Characters/Mannequins/Animations/Manny/BS_MM_WalkRun"]:
    try:
        bs = unreal.load_asset(p)
        o.append("== %s skel=%s" % (p, bs.get_editor_property("skeleton")))
        for b in bs.get_editor_property("blend_parameters"):
            o.append("  param %s %s..%s grid %s" % (b.get_editor_property("display_name"), b.get_editor_property("min"), b.get_editor_property("max"), b.get_editor_property("grid_num")))
        for s in bs.get_editor_property("sample_data"):
            a = s.get_editor_property("animation")
            o.append("  sample %s %s skel=%s" % (a.get_name() if a else None, s.get_editor_property("sample_value"), a.get_editor_property("skeleton").get_name() if a else None))
        for prop in ("blend_space_data", "grid_samples"):
            try:
                v = bs.get_editor_property(prop)
                o.append("  %s len %s" % (prop, len(v) if hasattr(v, "__len__") else v))
            except Exception as e:
                o.append("  %s n/a" % prop)
    except Exception:
        o.append(traceback.format_exc())
open(LOG, "w").write("\n".join(o))
