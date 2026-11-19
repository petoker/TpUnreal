# Paso 6: Blend Spaces, Montajes (con notify de golpe) y copias de los Anim Blueprints en SurvivalHorror
import unreal, os, traceback

PROJ = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal"
LOG = os.path.join(PROJ, "Saved", "claude_log6.txt")
A = "/Game/SurvivalHorror/Animations"
P = A + "/Player"
Z = A + "/Zombie"
eal = unreal.EditorAssetLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
SKEL = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SK_Mannequin")


def log(*a):
    s = " ".join(str(x) for x in a)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")
    unreal.log("[CLAUDE] " + s)


def L(p):
    return unreal.load_asset(p)


def fresh(path):
    if eal.does_asset_exist(path):
        eal.delete_asset(path)


def make_bs(name, folder, one_d, params, samples):
    path = folder + "/" + name
    fresh(path)
    fac = unreal.BlendSpaceFactory1D() if one_d else unreal.BlendSpaceFactoryNew()
    fac.set_editor_property("target_skeleton", SKEL)
    cls = unreal.BlendSpace1D if one_d else unreal.BlendSpace
    bs = tools.create_asset(name, folder, cls, fac)
    try:
        bp = list(bs.get_editor_property("blend_parameters"))
        for i, (disp, mn, mx, grid) in enumerate(params):
            b = bp[i]
            b.set_editor_property("display_name", disp)
            b.set_editor_property("min", mn)
            b.set_editor_property("max", mx)
            b.set_editor_property("grid_num", grid)
            bp[i] = b
        bs.set_editor_property("blend_parameters", bp)
    except Exception as e:
        log("bs params err", name, e)
    try:
        arr = []
        for anim, x, y in samples:
            s = unreal.BlendSample()
            s.set_editor_property("animation", L(anim))
            s.set_editor_property("sample_value", unreal.Vector(x, y, 0))
            arr.append(s)
        bs.set_editor_property("sample_data", arr)
        log("bs ok", name, len(arr))
    except Exception as e:
        log("bs samples err", name, e)
    eal.save_loaded_asset(bs)
    return bs


def make_montage(name, folder, anim, slot="DefaultSlot", notifies=()):
    path = folder + "/" + name
    fresh(path)
    fac = unreal.AnimMontageFactory()
    fac.set_editor_property("source_animation", L(anim))
    m = tools.create_asset(name, folder, unreal.AnimMontage, fac)
    try:
        tracks = list(m.get_editor_property("slot_anim_tracks"))
        t = tracks[0]
        t.set_editor_property("slot_name", slot)
        tracks[0] = t
        m.set_editor_property("slot_anim_tracks", tracks)
    except Exception as e:
        log("slot err", name, e)
    for nname, frac in notifies:
        try:
            ln = m.get_play_length() if hasattr(m, "get_play_length") else unreal.AnimationLibrary.get_sequence_length(m)
            ev = unreal.AnimationLibrary.add_animation_notify_event(m, "1", ln * frac, unreal.AnimNotify_PlayMontageNotify)
            try:
                ev.set_editor_property("notify_name", nname)
            except Exception as e2:
                log("notify name err", e2)
            log("notify", name, nname, round(ln * frac, 2))
        except Exception as e:
            log("notify err", name, traceback.format_exc())
    for prop, val in (("blend_in", 0.15), ("blend_out", 0.2)):
        try:
            b = m.get_editor_property(prop)
            b.set_editor_property("blend_time", val)
            m.set_editor_property(prop, b)
        except Exception as e:
            log("blend err", e)
    eal.save_loaded_asset(m)
    log("montage ok", name, slot)
    return m


try:
    open(LOG, "w").close()
    log("== ASSETS START ==")
    # --- Blend Spaces
    make_bs("BS_Player_PistolAim", P, False,
            [("Direction", -180.0, 180.0, 4), ("Speed", 0.0, 200.0, 2)],
            [(P + "/AS_Player_Pistol_AimIdle", 0, 0), (P + "/AS_Player_Pistol_AimIdle", -180, 0), (P + "/AS_Player_Pistol_AimIdle", 180, 0),
             (P + "/AS_Player_Pistol_AimIdle", -90, 0), (P + "/AS_Player_Pistol_AimIdle", 90, 0),
             (P + "/AS_Player_Pistol_AimWalk_Fwd", 0, 200), (P + "/AS_Player_Pistol_AimWalk_Right", 90, 200),
             (P + "/AS_Player_Pistol_AimWalk_Left", -90, 200), (P + "/AS_Player_Pistol_AimWalk_Bwd", 180, 200),
             (P + "/AS_Player_Pistol_AimWalk_Bwd", -180, 200)])
    make_bs("BS_Player_Crouch", P, True, [("Speed", 0.0, 300.0, 2)],
            [(P + "/AS_Player_Crouch_Idle", 0, 0), (P + "/AS_Player_Crouch_Walk", 300, 0)])
    make_bs("BS_Zombie_Locomotion", Z, True, [("Speed", 0.0, 450.0, 3)],
            [(Z + "/AS_Zombie_Idle", 0, 0), (Z + "/AS_Zombie_Walk", 150, 0), (Z + "/AS_Zombie_Run", 450, 0)])
    # --- Montajes
    make_montage("AM_Player_Reload", P, P + "/AS_Player_Reload", "UpperBody")
    make_montage("AM_Player_Pickup", P, P + "/AS_Player_Pickup", "DefaultSlot")
    make_montage("AM_Zombie_Attack", Z, Z + "/AS_Zombie_Attack", "DefaultSlot", [("Hit", 0.45)])
    make_montage("AM_Zombie_Punch", Z, Z + "/AS_Zombie_Punch", "DefaultSlot", [("Hit", 0.4)])
    make_montage("AM_Zombie_HitReact", Z, Z + "/AS_Zombie_HitReact", "DefaultSlot")
    make_montage("AM_Zombie_Death", Z, Z + "/AS_Zombie_Death", "DefaultSlot")
    # --- Anim Blueprints propios (copias de ABP_Manny, la base del template)
    for name in ("ABP_SurvivalCharacter", "ABP_Zombie"):
        dst = A + "/" + name
        if not eal.does_asset_exist(dst):
            ok = eal.duplicate_asset("/Game/Characters/Mannequins/Animations/ABP_Manny", dst)
            log("dup", name, ok)
        else:
            log("exists", name)
    # variables nuevas en el ABP del player
    try:
        bel = unreal.BlueprintEditorLibrary
        abp = L(A + "/ABP_SurvivalCharacter")
        bt = bel.get_basic_type_by_name("bool")
        for v in ("bIsAiming", "bIsCrouching"):
            bel.add_member_variable(abp, v, bt)
        ft = bel.get_basic_type_by_name("real")
        bel.add_member_variable(abp, "Direction", ft)
        bel.compile_blueprint(abp)
        log("abp vars ok")
    except Exception:
        log("abp vars err", traceback.format_exc())
    eal.save_directory(A)
    log("== ASSETS DONE ==")
except Exception:
    log("ERROR", traceback.format_exc())
