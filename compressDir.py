import argparse
import shutil
from pathlib import Path

default_dir = Path(__file__).parent
addon_output = default_dir / "FreeFaceMoCapV1.0.2"

# Create the parser
parser = argparse.ArgumentParser(description="Build the archive for FreeFaceMoCap Addon")

# Add the arguments
parser.add_argument("-p", "--path", type=Path, default=default_dir / "Addon", help="directory path for compression")

# Execute the parse_args() method
args = parser.parse_args()

if not args.path.is_dir():
    raise ValueError("Path provided is not a folder")

if not args.path.exists():
    raise ValueError("Path provided does not exist")

shutil.make_archive(addon_output, 'zip', args.path.parent, args.path.stem)
