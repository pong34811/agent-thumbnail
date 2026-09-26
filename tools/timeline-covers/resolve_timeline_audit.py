"""Read-only dump of every timeline in the open DaVinci Resolve project.

Run inside Resolve's scripting environment (e.g. the DaVinci Resolve MCP
`run_script_unsafe`, where `project` is pre-injected). Writes
timeline-audit.json next to this file's working folder (WORK below).

Deliberately does NOT open Fusion comps of Text+ items: doing that item by item
hung Resolve 21.1. Read Text+ captions from a .drp backup with
extract_textplus.py instead.
"""
import json
import os

WORK = os.environ.get("COVERS_WORK", r"D:\agent-thumbnail\.work\aomi-debut")

try:
    project  # noqa: B018  (injected by the MCP runner)
except NameError:
    import DaVinciResolveScript as dvr  # type: ignore

    project = dvr.scriptapp("Resolve").GetProjectManager().GetCurrentProject()

data = {"project": project.GetName(), "timelines": []}
for i in range(1, project.GetTimelineCount() + 1):
    t = project.GetTimelineByIndex(i)
    rec = {
        "index": i, "name": t.GetName(), "id": t.GetUniqueId(), "start": t.GetStartFrame(), "end": t.GetEndFrame(),
        "fps": t.GetSetting("timelineFrameRate"), "w": t.GetSetting("timelineResolutionWidth"),
        "h": t.GetSetting("timelineResolutionHeight"),
        "markers": {str(k): v for k, v in (t.GetMarkers() or {}).items()}, "tracks": {},
    }
    for kind in ("video", "audio", "subtitle"):
        tracks = []
        for ti in range(1, t.GetTrackCount(kind) + 1):
            items = []
            for it in t.GetItemListInTrack(kind, ti) or []:
                d = {"name": it.GetName(), "start": it.GetStart(), "end": it.GetEnd()}
                if kind != "subtitle":
                    mpi = it.GetMediaPoolItem()
                    if mpi is not None:
                        d["path"] = mpi.GetClipProperty("File Path")
                        d["type"] = mpi.GetClipProperty("Type")
                        d["src_start"] = it.GetSourceStartFrame()
                        d["src_end"] = it.GetSourceEndFrame()
                    else:
                        d["media"] = None  # Text+ / generator: text comes from the .drp
                    if kind == "video":
                        d["xf"] = {k: it.GetProperty(k) for k in ("ZoomX", "Pan", "Tilt")}
                        d["enabled"] = it.GetClipEnabled()
                items.append(d)
            tracks.append({"index": ti, "name": t.GetTrackName(kind, ti), "enabled": t.GetIsTrackEnabled(kind, ti),
                           "items": items})
        rec["tracks"][kind] = tracks
    data["timelines"].append(rec)

os.makedirs(WORK, exist_ok=True)
with open(os.path.join(WORK, "timeline-audit.json"), "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)
result = {"timelines": len(data["timelines"]), "out": os.path.join(WORK, "timeline-audit.json")}
