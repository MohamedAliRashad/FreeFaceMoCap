import shutil
from pathlib import Path
import argparse

default_dir = Path(__file__).parent

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

shutil.make_archive(args.path, "zip", default_dir)