"""Command-line interface."""
from __future__ import annotations
import argparse
import sys
from .converter import ConversionOptions, convert_file

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert an illustration into black-and-white line art.")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", default="output/coloring-page.png")
    parser.add_argument("--max-dimension", type=int, default=2400)
    parser.add_argument("--canny-low", type=int, default=45)
    parser.add_argument("--canny-high", type=int, default=125)
    parser.add_argument("--line-thickness", type=int, default=1)
    parser.add_argument("--min-component-area", type=int, default=3)
    parser.add_argument("--color-edges", action="store_true")
    parser.add_argument("--no-small-details", action="store_true")
    args = parser.parse_args(argv)
    try:
        options = ConversionOptions(max_dimension=args.max_dimension,canny_low=args.canny_low,canny_high=args.canny_high,line_thickness=args.line_thickness,min_component_area=args.min_component_area,use_color_edges=args.color_edges,preserve_small_dark_details=not args.no_small_details)
        output = convert_file(args.input,args.output,options)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"Saved coloring page: {output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
