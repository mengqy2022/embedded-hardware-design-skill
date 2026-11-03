"""Check release metadata and local Markdown targets without network requests."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from package_skill import EXPECTED
from update_release_docs import ROOT, check_readmes, latest_release


def markdown_links(text):
    # Current docs use inline links; ignore examples inside fenced code blocks.
    text = re.sub(r"^```[^\n]*\n.*?^```[^\n]*$", "", text, flags=re.M | re.S)
    return re.findall(r"\]\((<[^>]+>|[^\s)]+)(?:\s+\"[^\"]*\")?\)", text)


def validate(root=ROOT, tag=None):
    errors = check_readmes(root)
    try:
        version, _, _, _ = latest_release(root)
        manifest = json.loads((root / "release.json").read_text(encoding="utf-8"))
        if manifest.get("version") != version:
            errors.append("release.json version differs from provenance.json")
        if tag is not None and tag != f"v{version}":
            errors.append(f"Tag {tag!r} must match v{version}")
    except (OSError, ValueError, KeyError) as exc:
        errors.append(str(exc))
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.relative_to(root).parts:
            continue
        rel = path.relative_to(root).as_posix()
        for raw in markdown_links(path.read_text(encoding="utf-8")):
            link = raw.strip("<>")
            if re.match(r"^[A-Za-z]:[/\\]", link) or link.startswith(("file:", "\\\\")):
                errors.append(f"{rel}: non-portable local link {link}")
                continue
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root.resolve()) or not target.exists():
                errors.append(f"{rel}: missing or out-of-repository target {link}")
            elif rel in EXPECTED and target.is_file():
                target_rel = target.relative_to(root.resolve()).as_posix()
                if target_rel not in EXPECTED | {"release.json"}:
                    errors.append(f"{rel}: linked file excluded from installed package: {link}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", help="Require a release tag matching the package version")
    args = parser.parse_args()
    errors = validate(tag=args.tag)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Version, bilingual release summaries, and local documentation links verified.")


if __name__ == "__main__":
    main()
