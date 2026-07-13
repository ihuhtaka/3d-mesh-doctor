"""Mesh smoothing — Laplacian, Taubin, and Humphrey methods."""

from enum import Enum

import trimesh
from trimesh import smoothing


class SmoothMethod(Enum):
    """Available smoothing algorithms."""

    LAPLACIAN = "laplacian"
    TAUBIN = "taubin"
    HUMPHREY = "humphrey"


def smooth_mesh(
    mesh: trimesh.Trimesh,
    method: SmoothMethod = SmoothMethod.TAUBIN,
    iterations: int = 10,
    lambd: float = 0.5,
    mu: float = 0.5,
) -> trimesh.Trimesh:
    """Smooth a mesh using the specified algorithm.

    Parameters
    ----------
    mesh : trimesh.Trimesh
        The mesh to smooth (modified in-place).
    method : SmoothMethod
        Smoothing algorithm to use.
    iterations : int
        Number of smoothing iterations (1-100).
    lambd : float
        Smoothing strength (0.0-1.0). Higher = more smoothing.
    mu : float
        Taubin/Humphrey anti-shrinkage parameter (0.0-1.0).

    Returns
    -------
    trimesh.Trimesh
        The smoothed mesh (same object, modified in-place).
    """
    iterations = max(1, min(100, iterations))
    lambd = max(0.0, min(1.0, lambd))
    mu = max(0.0, min(1.0, mu))

    if method == SmoothMethod.LAPLACIAN:
        smoothing.filter_laplacian(mesh, lambd=lambd, iterations=iterations)
    elif method == SmoothMethod.TAUBIN:
        smoothing.filter_taubin(mesh, lambd=lambd, mu=mu, iterations=iterations)
    elif method == SmoothMethod.HUMPHREY:
        smoothing.filter_humphrey(mesh, lambd=lambd, mu=mu, iterations=iterations)

    return mesh
