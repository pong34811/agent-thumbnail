"""Read-only audit of every timeline in an open DaVinci Resolve project.

Can be run inside Resolve's scripting context or imported by tools.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def audit_current_project(output_path: Optional[str] = None, resolve_project=None) -> Dict[str, Any]:
    """Scans all timelines in the current open Resolve project and dumps metadata to JSON."""
    project = resolve_project
    if project is None:
        try:
            # Check global scope (injected by Resolve MCP runner)
            project = globals().get("project")
        except Exception:
            pass

    if project is None:
        import DaVinciResolveScript as dvr
        project = dvr.scriptapp("Resolve").GetProjectManager().GetCurrentProject()

    data = {"project": project.GetName(), "timelines": []}

    for i in range(1, project.GetTimelineCount() + 1):
        t = project.GetTimelineByIndex(i)
        rec = {
            "index": i,
            "name": t.GetName(),
            "id": t.GetUniqueId(),
            "start": t.GetStartFrame(),
            "end": t.GetEndFrame(),
            "fps": t.GetSetting("timelineFrameRate"),
            "w": t.GetSetting("timelineResolutionWidth"),
            "h": t.GetSetting("timelineResolutionHeight"),
            "markers": {str(k): v for k, v in (t.GetMarkers() or {}).items()},
            "tracks": {},
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
                            d["media"] = None  # Text+ / generator
                        if kind == "video":
                            d["xf"] = {k: it.GetProperty(k) for k in ("ZoomX", "Pan", "Tilt")}
                            d["enabled"] = it.GetClipEnabled()
                    items.append(d)
                tracks.append({
                    "index": ti,
                    "name": t.GetTrackName(kind, ti),
                    "enabled": t.GetIsTrackEnabled(kind, ti),
                    "items": items,
                })
            rec["tracks"][kind] = tracks
        data["timelines"].append(rec)

    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    return data


if __name__ == "__main__":
    out_dir = os.environ.get("COVERS_WORK", ".")
    out_json = os.path.join(out_dir, "timeline-audit.json")
    result = audit_current_project(out_json)
    print(f"Audited {len(result['timelines'])} timelines -> {out_json}")
