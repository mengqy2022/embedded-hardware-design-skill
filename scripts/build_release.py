"""Build checked release assets outside the checkout, without refreshing the manifest."""
import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path
from update_release_docs import ROOT, latest_release, release_notes
from verify_repository import validate


def build(output, tag=None):
    errors = validate(tag=tag)
    if errors:
        raise ValueError("\n".join(errors))
    version = latest_release()[0]
    output = output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError("Build outside the repository")
    output.mkdir(parents=True, exist_ok=True)
    versioned = output / f"embedded-hardware-design-{version}.zip"
    chat = output / "HARDWARE_DESIGN_RULES_CHATGPT.md"
    subprocess.run([sys.executable, str(ROOT / "scripts/package_skill.py"),
                    "--output", str(versioned), "--chatgpt-output", str(chat)], check=True)
    stable = output / "embedded-hardware-design.zip"
    shutil.copyfile(versioned, stable)
    notes = output / "RELEASE_NOTES.md"
    notes.write_text(release_notes(), encoding="utf-8", newline="\n")
    files = [versioned, stable, chat, notes]
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in files)
    (output / "SHA256SUMS.txt").write_text(checksums, encoding="utf-8", newline="\n")
    print(f"Release v{version} assets built at {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tag")
    args = parser.parse_args()
    try:
        build(args.output, args.tag)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
