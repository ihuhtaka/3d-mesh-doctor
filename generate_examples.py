"""Generate example mesh files with known issues for demonstration."""

import numpy as np
import trimesh

OUT = "scans"


def sphere_with_holes():
    """Sphere with several circular holes cut out."""
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    # Cut holes by removing faces whose center is near certain directions
    centers = sphere.triangles_center
    directions = np.array([
        [1, 0, 0],   # +X
        [0, 1, 0],   # +Y
        [0, 0, 1],   # +Z
    ])
    keep = np.ones(len(sphere.faces), dtype=bool)
    for d in directions:
        dots = np.dot(centers, d)
        keep &= dots < 0.7
    sphere.update_faces(keep)
    sphere.export(f"{OUT}/sphere_with_holes.stl")
    print(f"  sphere_with_holes.stl  ({len(sphere.faces)} faces, watertight={sphere.is_watertight})")


def torus_high_poly():
    """High-polygon torus — good for reduction demo."""
    torus = trimesh.creation.torus(major_radius=1.0, minor_radius=0.3, count=[128, 64])
    torus.export(f"{OUT}/torus_high_poly.stl")
    print(f"  torus_high_poly.stl    ({len(torus.faces)} faces)")


def cube_with_inverted_normals():
    """Cube with some faces having inverted normals."""
    cube = trimesh.creation.box(extents=[1, 1, 1])
    # Invert normals on the top face (faces pointing in +Z)
    normals = cube.face_normals
    top_mask = normals[:, 2] > 0.9
    cube.faces[top_mask] = cube.faces[top_mask][:, ::-1]  # flip winding
    cube.export(f"{OUT}/cube_inverted_normals.stl")
    print(f"  cube_inverted_normals.stl  ({len(cube.faces)} faces, normals fixed needed)")


def ear_canal():
    """Tapered tube resembling an ear canal — non-watertight at both ends."""
    # Create a tapered tube using revolution
    t = np.linspace(0, 1, 60)
    theta = np.linspace(0, 2 * np.pi, 48, endpoint=False)
    T, THETA = np.meshgrid(t, theta, indexing="ij")

    # Radius tapers from 3mm to 1.5mm (in cm scale)
    radius = 0.3 - 0.15 * T
    # Length is 2.5cm
    length = 2.5
    x = radius * np.cos(THETA)
    y = radius * np.sin(THETA)
    z = T * length

    # Build vertices
    verts = np.stack([x.ravel(), y.ravel(), z.ravel()], axis=-1)

    # Build faces (quads split into triangles)
    nt, ntheta = len(t), len(theta)
    faces = []
    for i in range(nt - 1):
        for j in range(ntheta):
            j_next = (j + 1) % ntheta
            v00 = i * ntheta + j
            v01 = i * ntheta + j_next
            v10 = (i + 1) * ntheta + j
            v11 = (i + 1) * ntheta + j_next
            faces.append([v00, v10, v11])
            faces.append([v00, v11, v01])

    canal = trimesh.Trimesh(vertices=verts, faces=np.array(faces))
    canal.fix_normals()
    # Not watertight — open ends at z=0 and z=length
    canal.export(f"{OUT}/ear_canal.stl")
    print(f"  ear_canal.stl          ({len(canal.faces)} faces, watertight={canal.is_watertight})")


def bumpy_sphere():
    """Sphere with added surface noise — good for smoothing demo."""
    sphere = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    # Add displacement noise to vertices
    verts = sphere.vertices.copy()
    noise = np.random.RandomState(42).randn(*verts.shape) * 0.03
    # Scale noise by distance from center for more natural look
    norms = np.linalg.norm(verts, axis=1, keepdims=True)
    noise *= norms
    verts += noise
    sphere.vertices = verts
    sphere.export(f"{OUT}/bumpy_sphere.stl")
    print(f"  bumpy_sphere.stl       ({len(sphere.faces)} faces, for smoothing demo)")


def overlapping_cubes():
    """Two overlapping cubes — non-manifold edges at intersection."""
    c1 = trimesh.creation.box(extents=[1, 1, 1], offset=[-0.3, 0, 0])
    c2 = trimesh.creation.box(extents=[1, 1, 1], offset=[0.3, 0, 0])
    merged = trimesh.util.concatenate([c1, c2])
    merged.export(f"{OUT}/overlapping_cubes.stl")
    print(f"  overlapping_cubes.stl  ({len(merged.faces)} faces, non-manifold edges)")


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    print("Generating example meshes:")
    sphere_with_holes()
    torus_high_poly()
    cube_with_inverted_normals()
    ear_canal()
    bumpy_sphere()
    overlapping_cubes()
    print("Done.")
