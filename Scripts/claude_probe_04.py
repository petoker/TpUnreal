import unreal, os, traceback
LOG = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_probe.txt"
out = []
try:
    rtg = unreal.load_asset("/Game/SurvivalHorror/Animations/Retarget/RTG_Mixamo_To_Manny")
    xc = unreal.IKRetargeterController.get_controller(rtg)
    trc = unreal.IKRigController.get_controller(unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin"))
    src = unreal.IKRigController.get_controller(unreal.load_asset("/Game/SurvivalHorror/Animations/Retarget/IK_Mixamo"))
    out.append("DOC get_source_chain: " + str(xc.get_source_chain.__doc__))
    for c in trc.get_retarget_chains():
        n = c.chain_name
        try:
            s = xc.get_source_chain(n)
        except Exception as e:
            try:
                s = xc.get_source_chain(n, "FK Chains")
            except Exception as e2:
                s = "ERR %s | %s" % (e, e2)
        out.append("T %s [%s -> %s] <= S %s" % (n, c.start_bone.bone_name, c.end_bone.bone_name, s))
    for c in src.get_retarget_chains():
        out.append("S %s [%s -> %s]" % (c.chain_name, c.start_bone.bone_name, c.end_bone.bone_name))
    out.append("src root %s retarget_root %s" % (src.get_root_bone(), src.get_retarget_root()))
    out.append("tgt retarget_root %s" % trc.get_retarget_root())
except Exception:
    out.append(traceback.format_exc())
open(LOG, "w", encoding="utf-8").write("\n".join(map(str, out)))
