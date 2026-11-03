"""Verify or package a reviewed schematic and PCB rules release, using only the standard library."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {
    "SKILL.md", "README.md", "OPTIONAL_PLUGINS.md", "CHANGELOG.md",
    "LICENSE", ".gitignore", ".gitattributes", "provenance.json",
}
RESOURCE_FILES = {
    "agents/openai.yaml", "assets/PROJECT_RULES.md", "assets/SCHEMATIC_REVIEW.md",
    "references/schematic-style.md", "references/schematic-examples.md", "references/easyeda-schematic.md",
    "references/layout-manufacturing.md", "references/power-ground.md",
    "references/differential-crystal.md", "references/verification.md",
    "references/sources.md", "references/pcb-stage-review.md", "assets/PCB_STAGE_REVIEW.json",
    "scripts/package_skill.py", "scripts/check_pcb_stage.py", "scripts/test_pcb_stage.py",
}
EXPECTED = ROOT_FILES | RESOURCE_FILES
MANIFEST = ROOT / "release.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="Record reviewed file hashes")
    mode.add_argument("--verify", action="store_true", help="Verify without changing files")
    parser.add_argument("--output", type=Path, help="ZIP destination outside the skill folder")
    parser.add_argument("--chatgpt-output", type=Path, help="Combined Markdown destination")
    args = parser.parse_args()
    if args.verify and (args.output or args.chatgpt_output):
        parser.error("--verify is read-only; omit it when exporting")
    for output in (args.output, args.chatgpt_output):
        if output and output.resolve().is_relative_to(ROOT):
            parser.error("Export outside the skill folder to keep source and release separate")
    if args.output and args.chatgpt_output and args.output.resolve() == args.chatgpt_output.resolve():
        parser.error("ZIP and Markdown need different output paths")
    actual = {}
    for rel in sorted(EXPECTED):
        path = ROOT / rel
        if not path.is_file() or path.is_symlink():
            parser.error(f"Missing or unsupported release file: {rel}")
        actual[rel] = digest(path)
    if args.refresh:
        version = json.loads((ROOT / "provenance.json").read_text(encoding="utf-8"))["version"]
        MANIFEST.write_text(json.dumps({"name": "embedded-hardware-design", "version": version,
                                      "sha256": actual}, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8", newline="\n")
    if not MANIFEST.is_file():
        parser.error("No release manifest; review files and run --refresh first")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("sha256") != actual:
        parser.error("Release differs from recorded hashes; review changes before --refresh")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(args.output, "w", ZIP_DEFLATED) as archive:
            for rel in sorted(EXPECTED | {"release.json"}):
                archive.write(ROOT / rel, "embedded-hardware-design/" + rel)
    if args.chatgpt_output:
        sections = ["SKILL.md", "references/schematic-style.md", "references/schematic-examples.md", "references/easyeda-schematic.md", "assets/SCHEMATIC_REVIEW.md", "references/layout-manufacturing.md", "references/power-ground.md",
                    "references/differential-crystal.md", "references/verification.md", "references/pcb-stage-review.md",
                    "references/sources.md", "assets/PROJECT_RULES.md"]
        parts = [f"# 嵌入式原理图与 PCB 可携带规则 {manifest['version']}\n\n"
                 "供上传聊天或项目知识文件。按当前项目任务读取适用部分；本文件不提供EDA控制能力。"
                 "相对链接在合并时改为文字；外部来源链接保留。\n"]
        for rel in sections:
            body = (ROOT / rel).read_text(encoding="utf-8")
            if rel == "SKILL.md":
                body = re.sub(r"\A---\n.*?\n---\n", "", body, count=1, flags=re.S)
            body = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                          lambda m: m[0] if re.match(r"https?://", m[2]) else m[1], body)
            parts.append(body.strip())
        args.chatgpt_output.parent.mkdir(parents=True, exist_ok=True)
        args.chatgpt_output.write_text("\n\n---\n\n".join(parts) + "\n", encoding="utf-8", newline="\n")
    print(f"Release {manifest['version']}: {len(actual)} file hashes verified. "
          "This checks package integrity, not circuit or PCB correctness.")


if __name__ == "__main__":
    main()
