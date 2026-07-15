"""Mesh quality metrics — comparing original vs processed meshes."""

from dataclasses import dataclass

import numpy as np
import trimesh


@dataclass
class MeshQualityReport:
    """Quality comparison between original and processed mesh."""

    original_faces: int
    processed_faces: int
    original_vertices: int
    processed_vertices: int
    original_volume: float
    processed_volume: float
    volume_diff_pct: float
    original_area: float
    processed_area: float
    area_diff_pct: float
    roughness: float
    max_hausdorff: float
    mean_chamfer: float


def compute_quality(original: trimesh.Trimesh, processed: trimesh.Trimesh) -> MeshQualityReport:
    """Compute quality metrics comparing original to processed mesh.

    Parameters
    ----------
    original : trimesh.Trimesh
        The original unmodified mesh.
    processed : trimesh.Trimesh
        The modified mesh (repaired, smoothed, reduced, etc.).

    Returns
    -------
    MeshQualityReport
        All comparison metrics.
    """
    orig_vol = original.volume if original.is_watertight else 0.0
    proc_vol = processed.volume if processed.is_watertight else 0.0
    vol_diff = abs(orig_vol - proc_vol) / orig_vol * 100 if orig_vol > 0 else 0.0

    orig_area = original.area
    proc_area = processed.area
    area_diff = abs(orig_area - proc_area) / orig_area * 100 if orig_area > 0 else 0.0

    try:
        hull = processed.convex_hull
        roughness = proc_area / hull.area if hull.area > 0 else 1.0
    except Exception:
        roughness = 1.0

    orig_query = trimesh.proximity.ProximityQuery(original)
    _, proc_dists, _ = orig_query.on_vertices(processed.vertices)
    proc_dists = np.asarray(proc_dists)
    max_hausdorff = float(np.max(proc_dists)) if len(proc_dists) > 0 else 0.0
    mean_chamfer = float(np.mean(proc_dists)) if len(proc_dists) > 0 else 0.0

    return MeshQualityReport(
        original_faces=len(original.faces),
        processed_faces=len(processed.faces),
        original_vertices=len(original.vertices),
        processed_vertices=len(processed.vertices),
        original_volume=orig_vol,
        processed_volume=proc_vol,
        volume_diff_pct=vol_diff,
        original_area=orig_area,
        processed_area=proc_area,
        area_diff_pct=area_diff,
        roughness=roughness,
        max_hausdorff=max_hausdorff,
        mean_chamfer=mean_chamfer,
    )
