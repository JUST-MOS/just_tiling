
"""
Run hyperuniform tiling from the command line.
"""

import argparse
from pathlib import Path

from just_tiling.hyperuniform.hyperuniform_tiling import hyperuniform_tiling

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run hyperuniform tiling on an input catalog."
    )

    parser.add_argument(
        "-i",
        "--input-catalog",
        type = Path,
        default = Path("./lightcone_ra_0_90_dec_0_90_rmagcut20.5_cluster_mask.fits"),
        help = "Path to the input FITS catalog.",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type = Path,
        default = Path("./output/"),
        help="Output directory (default: ./).",
    )


    return parser.parse_args()


def main():
    args = parse_args()

    if not args.input_catalog.is_file():
        raise FileNotFoundError(
            f"Input catalog does not exist: {args.input_catalog}"
        )
    
    input_catalog = args.input_catalog
    output_dir = args.output_dir

    print(f"input file: {input_catalog}")
    print(f"output directory: {output_dir}")
    print("=="*20)

    hyperuniform_tiling(
        input_catalog,
        output_dir,
    )


if __name__ == "__main__":
    main()
