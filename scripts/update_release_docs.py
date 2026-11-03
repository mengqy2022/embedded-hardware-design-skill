"""Generate README release summaries from provenance and the latest changelog entry."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/mengqy2022/embedded-hardware-design-skill"
START = "<!-- release:start -->"
END = "<!-- release:end -->"


def latest_release(root=ROOT):
    version = json.loads((root / "provenance.json").read_text(encoding="utf-8"))["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Expected a stable semantic version in provenance.json")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    entry = re.search(r"^## (\d+\.\d+\.\d+) — (\d{4}-\d{2}-\d{2})\n(.*?)(?=^## |\Z)",
                      changelog, flags=re.M | re.S)
    if not entry or entry[1] != version:
        raise ValueError("Top CHANGELOG version must match provenance.json")
    chinese, separator, english = entry[3].partition("### English\n")
    if not separator or not chinese.strip() or not english.strip():
        raise ValueError("Latest changelog entry needs Chinese and English summaries")
    return version, entry[2], chinese.strip(), english.strip()


def summary(root=ROOT, english=False):
    version, date, zh, en = latest_release(root)
    heading = f"**[v{version}]({REPO}/releases/tag/v{version}) · {date}**"
    footer = (f"[All changes](CHANGELOG.md) · [Release assets and checksums]({REPO}/releases/tag/v{version})"
              if english else
              f"[完整变更记录](CHANGELOG.md) · [安装包与校验文件]({REPO}/releases/tag/v{version})")
    return f"{heading}\n\n{en if english else zh}\n\n{footer}"


def render_readme(text, root=ROOT, english=False):
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
        raise ValueError("README needs exactly one ordered release marker pair")
    before, rest = text.split(START)
    _, after = rest.split(END)
    return before + START + "\n" + summary(root, english) + "\n" + END + after


def check_readmes(root=ROOT, write=False):
    errors = []
    for filename, english in (("README.md", False), ("README.en.md", True)):
        path = root / filename
        try:
            current = path.read_text(encoding="utf-8")
            expected = render_readme(current, root, english)
            if current != expected:
                if write:
                    path.write_text(expected, encoding="utf-8", newline="\n")
                else:
                    errors.append(f"{filename}: stale release summary; run scripts/update_release_docs.py")
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f"{filename}: {exc}")
    return errors


def release_notes(root=ROOT):
    version, date, zh, en = latest_release(root)
    return (f"# Embedded Hardware Design v{version}\n\n{date}\n\n"
            f"## 更新内容\n\n{zh}\n\n## What's changed\n\n{en}\n\n"
            "## 安装 / Install\n\n"
            f"- [Skill ZIP]({REPO}/releases/download/v{version}/embedded-hardware-design.zip)"
            " — single `embedded-hardware-design/` directory; back up before upgrading.\n"
            f"- [ChatGPT rules]({REPO}/releases/download/v{version}/HARDWARE_DESIGN_RULES_CHATGPT.md)"
            " — upload with your project constraints.\n"
            f"- [SHA256SUMS.txt]({REPO}/releases/download/v{version}/SHA256SUMS.txt)"
            " — compare the matching filename's SHA-256.\n\n"
            f"[完整变更 / Changelog]({REPO}/blob/v{version}/CHANGELOG.md) · "
            f"[安装与升级 / Installation]({REPO}/blob/v{version}/docs/INSTALLATION.md)\n\n"
            "本次发布验证规则包与辅助工具；不代表任何板卡通过 ERC/DRC、SI/PI、EMC 或实测。\n"
            "Package checks do not certify a board or replace native EDA and hardware verification.\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Read-only check for stale summaries")
    args = parser.parse_args()
    errors = check_readmes(write=not args.check)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Bilingual README release summaries are current.")


if __name__ == "__main__":
    main()
