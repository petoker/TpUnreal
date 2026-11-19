import unreal
out = []
try:
    bp = unreal.load_asset('/Game/SurvivalHorror/Blueprints/Characters/BP_SurvivalCharacter')
    cdo = unreal.get_default_object(bp.generated_class())
    for n in ['bIsAiming', 'b_is_aiming']:
        try:
            out.append('before %s=%s' % (n, cdo.get_editor_property(n)))
            cdo.set_editor_property(n, False)
            out.append('set %s False' % n)
            break
        except Exception as e:
            out.append('err %s %s' % (n, e))
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp, False)
    out.append('saved BP')
except Exception as e:
    out.append('BP err %s' % e)

ar = unreal.AssetRegistryHelpers.get_asset_registry()
flt = unreal.ARFilter(class_paths=[unreal.TopLevelAssetPath('/Script/EnhancedInput', 'InputMappingContext')], recursive_paths=True, package_paths=['/Game'])
for ad in ar.get_assets(flt):
    imc = ad.get_asset()
    out.append('IMC %s' % imc.get_path_name())
    try:
        for m in imc.get_editor_property('default_key_mappings').get_editor_property('mappings'):
            a = m.get_editor_property('action')
            out.append('   %s -> %s' % (a.get_name() if a else None, m.get_editor_property('key').get_editor_property('key_name')))
    except Exception as e:
        try:
            for m in imc.get_editor_property('mappings'):
                a = m.get_editor_property('action')
                out.append('   %s -> %s' % (a.get_name() if a else None, m.get_editor_property('key').get_editor_property('key_name')))
        except Exception as e2:
            out.append('   err %s / %s' % (e, e2))

open(r'C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_aim_10.txt', 'w', encoding='utf-8').write('\n'.join(out))
