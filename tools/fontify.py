#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image


@dataclass(frozen=True)
class FontGrid:
    glyph_width: int
    glyph_height: int
    sep_x: int
    sep_y: int
    base_x: int
    base_y: int
    columns: int
    rows: int

    @property
    def cell_width(self) -> int:
        return self.glyph_width + self.sep_x

    @property
    def cell_height(self) -> int:
        return self.glyph_height + self.sep_y


def load_font_spec(spec_path: Path) -> Tuple[FontGrid, List[str]]:
    spec = json.loads(spec_path.read_text())

    glyph_width = int(spec["glyph-width"])  # 5
    glyph_height = int(spec["glyph-height"])  # 7
    sep_x = int(spec["glyph-sep-x"])  # 1
    sep_y = int(spec["glyph-sep-y"])  # 1
    base_x = int(spec.get("glyph-base-x", 0))
    base_y = int(spec.get("glyph-ofs-y", 0))

    in_glyphs_rows: List[str] = spec["in-glyphs"]
    rows = len(in_glyphs_rows)
    if rows == 0:
        raise ValueError("in-glyphs has no rows")
    columns = max(len(row) for row in in_glyphs_rows)

    grid = FontGrid(
        glyph_width=glyph_width,
        glyph_height=glyph_height,
        sep_x=sep_x,
        sep_y=sep_y,
        base_x=base_x,
        base_y=base_y,
        columns=columns,
        rows=rows,
    )

    # Flatten character list row-wise
    charset: List[str] = []
    for row in in_glyphs_rows:
        # Pad rows shorter than max with spaces to preserve indices
        padded = row + (" " * (columns - len(row)))
        charset.extend(list(padded))

    return grid, charset


def is_on_pixel(pixel: Tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    if a == 0:
        return False
    # Treat darker pixels as ink/on, lighter as background
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance < 128


def extract_glyph_runs(
    img: Image.Image,
    x0: int,
    y0: int,
    w: int,
    h: int,
) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int]]]:
    """
    Returns (lines, pixels) where
    - lines: list of (x1, y, x2) in glyph-local coordinates
    - pixels: list of (x, y) for isolated single pixels
    """
    lines: List[Tuple[int, int, int]] = []
    singles: List[Tuple[int, int]] = []

    for gy in range(h):
        run_start = None
        for gx in range(w):
            on = is_on_pixel(img.getpixel((x0 + gx, y0 + gy)))
            if on and run_start is None:
                run_start = gx
            elif (not on) and run_start is not None:
                run_end = gx - 1
                run_len = run_end - run_start + 1
                if run_len >= 2:
                    lines.append((run_start, gy, run_end))
                else:
                    singles.append((run_start, gy))
                run_start = None

        # Close run at end of row
        if run_start is not None:
            run_end = w - 1
            run_len = run_end - run_start + 1
            if run_len >= 2:
                lines.append((run_start, gy, run_end))
            else:
                singles.append((run_start, gy))

    return lines, singles


def build_ops(
    img_path: Path,
    spec_path: Path,
    out_path: Path,
) -> None:
    grid, charset = load_font_spec(spec_path)
    img = Image.open(img_path).convert("RGBA")

    # Infer 1px outer padding from total size if present
    # Expected width: columns * (w+sep) - sep + 2*pad
    # Expected height: rows * (h+sep) - sep + 2*pad
    expected_inner_w = grid.columns * grid.cell_width - grid.sep_x
    expected_inner_h = grid.rows * grid.cell_height - grid.sep_y
    pad_x = max((img.width - expected_inner_w) // 2, 0)
    pad_y = max((img.height - expected_inner_h) // 2, 0)

    ops: Dict[str, Dict[str, List]] = {}

    idx = 0
    for row in range(grid.rows):
        for col in range(grid.columns):
            ch = charset[idx]
            idx += 1

            # Skip characters outside provided rows (padded spaces) but keep space
            if ch == "":
                continue

            x0 = pad_x + col * grid.cell_width
            y0 = pad_y + row * grid.cell_height

            lines, singles = extract_glyph_runs(
                img, x0, y0, grid.glyph_width, grid.glyph_height
            )

            # Skip empty glyphs (but include space explicitly)
            if ch != " " and not lines and not singles:
                continue

            ops[ch] = {
                "lines": lines,  # [x1, y, x2] local coords
                "pixels": singles,  # [x, y] local coords
            }

    out = {
        "glyph_width": grid.glyph_width,
        "glyph_height": grid.glyph_height,
        "sep_x": grid.sep_x,
        "sep_y": grid.sep_y,
        "columns": grid.columns,
        "rows": grid.rows,
        "ops": ops,
    }

    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    img_path = root / "fonts/carrie-micro/carrie-micro-w.png"
    spec_path = root / "fonts/carrie-micro/carrie-micro.json"
    out_path = root / "fonts/carrie-micro/carrie-micro-w.ops.json"

    build_ops(img_path, spec_path, out_path)


if __name__ == "__main__":
    main()


