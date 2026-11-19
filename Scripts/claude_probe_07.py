import unreal, traceback
LOG = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_probe7.txt"
o = []
try:
    for p in ["/Game/SurvivalHorror/Animations/Mixamo/SK_Mixamo_TPose", "/Game/SurvivalHorror/Animations/Mixamo/Zombie_Walk_WithSkin", "/Game/Characters/Mannequins/Meshes/SKM_Manny"]:
        m = unreal.load_asset(p)
        b = m.get_bounds()
        o.append("%s bounds origin %s extent %s" % (p, b.origin, b.box_extent))
        try:
            rig = unreal.IKRigController.get_controller(unreal.load_asset("/Game/SurvivalHorror/Animations/Retarget/IK_Mixamo"))
        except Exception:
            pass
    ctrl = unreal.IKRigController.get_controller(unreal.load_asset("/Game/SurvivalHorror/Animations/Retarget/IK_Mixamo"))
    for bn in ["mixamorig:Hips", "mixamorig:LeftUpLeg", "mixamorig:LeftArm", "mixamorig:Head", "mixamorig:LeftFoot"]:
        try:
            o.append("MIX %s %s" % (bn, ctrl.get_ref_pose_transform_of_bone(bn)))
        except Exception as e:
            o.append("MIX err %s %s" % (bn, e))
    c2 = unreal.IKRigController.get_controller(unreal.load_asset("/Game/Characters/Mannequins/Rigs/IK_Mannequin"))
    for bn in ["pelvis", "thigh_l", "upperarm_l", "head", "foot_l"]:
        o.append("MAN %s %s" % (bn, c2.get_ref_pose_transform_of_bone(bn)))
    o.append("retarget roots %s / %s" % (ctrl.get_retarget_root(), c2.get_retarget_root()))
except Exception:
    o.append(traceback.format_exc())
open(LOG, "w").write("\n".join(o))
