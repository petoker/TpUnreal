import unreal, traceback
LOG = r"C:\Users\Usuario\Desktop\LevelKit\TpUnreal\Saved\claude_probe8.txt"
o = []
try:
    names = [n for n in dir(unreal) if "Retarget" in n or "IKRig" in n]
    o.append("NAMES: " + ", ".join(names))
    o.append("RUN DOC: " + str(unreal.IKRetargetBatchOperation.run_batch_retarget.__doc__))
    for n in names:
        if "Input" in n or "Settings" in n:
            c = getattr(unreal, n)
            o.append("== %s\n%s" % (n, c.__doc__))
    o.append("ALIGN DOC: " + str(unreal.IKRetargeterController.auto_align_all_bones.__doc__))
    o.append("MAP DOC: " + str(unreal.IKRetargeterController.auto_map_chains.__doc__))
except Exception:
    o.append(traceback.format_exc())
open(LOG, "w").write("\n".join(o))
