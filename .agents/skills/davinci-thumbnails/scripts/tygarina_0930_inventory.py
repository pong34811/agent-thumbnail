"""Read-only inventory of every Resolve project in Tygarina folder 2026-09-30 (each project holds N landscape + N _9x16 timelines).
Writes reports/tygarina/2026-09-30/timeline-inventory.json. Saves + restores the originally open project.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting/Modules")
import DaVinciResolveScript as dvr  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "reports/tygarina/2026-09-30/timeline-inventory.json"

resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
orig = pm.GetCurrentProject().GetName()
names = pm.GetProjectListInCurrentFolder()
pm.SaveProject()
time.sleep(1.2)
rows = []
for pname in names:
    pm.CloseProject(pm.GetCurrentProject()); time.sleep(1.2)
    proj = pm.LoadProject(pname); time.sleep(1.5)
    for i in range(1, proj.GetTimelineCount() + 1):
        tl = proj.GetTimelineByIndex(i)
        start, end = tl.GetStartFrame(), tl.GetEndFrame()
        src = srcstart = None
        for ti in range(1, tl.GetTrackCount("video") + 1):
            items = tl.GetItemListInTrack("video", ti) or []
            if items:
                mp = items[0].GetMediaPoolItem()
                src = mp.GetClipProperty("File Path") if mp else None
                srcstart = items[0].GetLeftOffset()
                break
        subs = [[it.GetStart() - start, it.GetName()] for ti in range(1, tl.GetTrackCount("subtitle") + 1)
                for it in (tl.GetItemListInTrack("subtitle", ti) or [])]
        rows.append(dict(project=pname, i=i, name=tl.GetName(), frames=end - start, fps=float(tl.GetSetting("timelineFrameRate") or 60),
                         res=[tl.GetSetting("timelineResolutionWidth"), tl.GetSetting("timelineResolutionHeight")],
                         src=src, srcstart=srcstart, subs=subs))
    print(pname, proj.GetTimelineCount())
pm.CloseProject(pm.GetCurrentProject()); time.sleep(1.2)
pm.LoadProject(orig)
OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
print("wrote", len(rows), "restored", orig)
