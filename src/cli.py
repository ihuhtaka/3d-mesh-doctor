"""CLI tool for batch mesh processing."""

import argparse
import sys
from pathlib import Path

from src.core.mesh_exporter import export_mesh
from src.core.mesh_loader import SUPPORTED_EXTENSIONS, load_mesh
from src.core.mesh_metrics import compute_quality
from src.core.mesh_reducer import reduce_polygons
from src.core.mesh_repairer import RepairOptions, repair_mesh
from src.core.mesh_smoother import SmoothMethod, smooth_mesh


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mesh-doctor",
        description="3D Mesh Doctor — batch mesh repair, smoothing, and reduction tool.",
    )
    sub = parser.add_subparsers(dest="command")

    # --- batch ---
    batch = sub.add_parser("batch", help="Process all meshes in a directory")
    batch.add_argument("input", type=Path, help="Input directory with mesh files")
    batch.add_argument("-o", "--output", type=Path, required=True, help="Output directory")
    batch.add_argument(
        "--format", choices=["stl", "obj"], default="stl", help="Output format (default: stl)"
    )

    repair = batch.add_argument_group("Repair options")
    repair.add_argument("--fill-holes", action="store_true", help="Fill holes")
    repair.add_argument("--fix-normals", action="store_true", help="Fix inverted normals")
    repair.add_argument("--remove-degenerate", action="store_true", help="Remove degenerate faces")

    smooth = batch.add_argument_group("Smoothing options")
    smooth.add_argument(
        "--smooth", choices=["laplacian", "taubin", "humphrey"], help="Smoothing method"
    )
    smooth.add_argument(
        "-i", "--smooth-iterations", type=int, default=10, help="Smooth iterations (default: 10)"
    )
    smooth.add_argument(
        "-s", "--smooth-strength", type=float, default=0.5,
        help="Smooth strength 0.0-1.0 (default: 0.5)",
    )

    batch.add_argument("--reduce", type=float, help="Reduce to N%% of faces (e.g. 50)")
    batch.add_argument("--analyze-only", action="store_true", help="Analyze only, no repair/export")

    # --- analyze ---
    analyze = sub.add_parser("analyze", help="Analyze a single mesh file")
    analyze.add_argument("file", type=Path, help="Mesh file to analyze")

    return parser


def process_file(path: Path, output_dir: Path, fmt: str, options: RepairOptions,
                 smooth_method: SmoothMethod | None, smooth_iter: int, smooth_str: float,
                 reduce_pct: float | None, analyze_only: bool) -> bool:
    try:
        mesh = load_mesh(path)
        original = mesh.copy()

        if not analyze_only:
            repair_mesh(mesh, options)

            if smooth_method is not None:
                smooth_mesh(mesh, method=smooth_method, iterations=smooth_iter, lambd=smooth_str)

            if reduce_pct is not None:
                reduce_polygons(mesh, ratio=reduce_pct / 100.0)

            out_path = output_dir / f"{path.stem}.{fmt}"
            export_mesh(mesh, out_path)

        q = compute_quality(original, mesh)
        print(f"  {path.name}: {q.original_faces} -> {q.processed_faces} faces, "
              f"vol diff {q.volume_diff_pct:.2f}%, "
              f"area diff {q.area_diff_pct:.2f}%, "
              f"roughness {q.roughness:.3f}")
        return True

    except Exception as e:
        print(f"  {path.name}: ERROR - {e}", file=sys.stderr)
        return False


def main(argv: list[str] | None = None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    if args.command == "analyze":
        if not args.file.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            return 1
        mesh = load_mesh(args.file)
        report = compute_quality(mesh, mesh)
        print(f"File: {args.file.name}")
        print(f"  Faces: {report.original_faces:,}")
        print(f"  Vertices: {report.original_vertices:,}")
        print(f"  Volume: {report.original_volume:.4f}")
        print(f"  Area: {report.original_area:.4f}")
        print(f"  Roughness: {report.roughness:.3f}")
        return 0

    if args.command == "batch":
        input_dir = args.input
        if not input_dir.is_dir():
            print(f"Not a directory: {input_dir}", file=sys.stderr)
            return 1

        files = [f for f in sorted(input_dir.iterdir()) if f.suffix.lower() in SUPPORTED_EXTENSIONS]
        if not files:
            print(f"No mesh files found in {input_dir}")
            return 1

        output_dir = args.output
        output_dir.mkdir(parents=True, exist_ok=True)

        options = RepairOptions(
            fill_holes=args.fill_holes,
            fix_normals=args.fix_normals,
            remove_degenerate=args.remove_degenerate,
        )

        smooth_method = None
        if args.smooth:
            smooth_method = SmoothMethod(args.smooth)

        print(f"Processing {len(files)} file(s) from {input_dir}")
        if not args.analyze_only:
            print(f"Output: {output_dir} ({args.format})")

        ok = 0
        fail = 0
        for i, path in enumerate(files, 1):
            print(f"[{i}/{len(files)}] {path.name}")
            success = process_file(
                path, output_dir, args.format, options,
                smooth_method, args.smooth_iterations, args.smooth_strength,
                args.reduce, args.analyze_only,
            )
            if success:
                ok += 1
            else:
                fail += 1

        print(f"\nDone: {ok} succeeded, {fail} failed")
        return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
