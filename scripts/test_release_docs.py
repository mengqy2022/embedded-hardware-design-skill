"""Regression checks for stale release docs, missing links, and invalid release tags."""
import json
import tempfile
import unittest
import hashlib
import subprocess
import sys
from zipfile import ZipFile
from pathlib import Path
from package_skill import EXPECTED
from update_release_docs import ROOT, check_readmes, latest_release, release_notes
from verify_repository import validate


class ReleaseDocumentationTests(unittest.TestCase):
    def fixture(self, root):
        (root / "provenance.json").write_text('{"version":"3.0.0"}', encoding="utf-8")
        (root / "release.json").write_text('{"version":"3.0.0"}', encoding="utf-8")
        (root / "CHANGELOG.md").write_text(
            "# Changes\n\n## 3.0.0 — 2026-11-03\n\n- 中文变化\n\n### English\n\n- English change\n"
            "\n## 2.0.0 — 2026-11-02\n\n- Earlier change\n", encoding="utf-8")
        for name in ("README.md", "README.en.md"):
            (root / name).write_text("# Header\n\n<!-- release:start -->\nstale\n<!-- release:end -->\n\nKeep this.\n", encoding="utf-8")
        self.assertEqual(check_readmes(root, write=True), [])

    def test_stale_summary_detected_and_repaired_without_changing_surroundings(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            before = (root / "README.md").read_text(encoding="utf-8")
            self.assertFalse(validate(root, "v3.0.0"))
            (root / "CHANGELOG.md").write_text((root / "CHANGELOG.md").read_text(encoding="utf-8").replace("中文变化", "新增变化"), encoding="utf-8")
            self.assertTrue(check_readmes(root))
            self.assertFalse(check_readmes(root, write=True))
            after = (root / "README.md").read_text(encoding="utf-8")
            self.assertEqual(before.split("<!-- release:start -->")[0], after.split("<!-- release:start -->")[0])
            self.assertEqual(before.split("<!-- release:end -->")[1], after.split("<!-- release:end -->")[1])
            self.assertFalse(validate(root, "v3.0.0"))

    def test_version_tag_and_bilingual_summary_mismatches_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            self.assertTrue(validate(root, "v2.0.0"))
            (root / "release.json").write_text('{"version":"2.0.0"}', encoding="utf-8")
            self.assertTrue(validate(root))
            path = root / "CHANGELOG.md"
            text = path.read_text(encoding="utf-8")
            for broken in (text.replace("## 3.0.0", "## 3.0.1"), text.replace("### English", "### Other")):
                path.write_text(broken, encoding="utf-8")
                with self.assertRaises(ValueError):
                    latest_release(root)

    def test_missing_and_unshipped_links_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            readme = root / "README.md"
            baseline = readme.read_text(encoding="utf-8")
            for link in ("missing.md", "../outside.md", "C:/private/file.md"):
                readme.write_text(baseline + f"\n[Broken]({link})\n", encoding="utf-8")
                self.assertTrue(validate(root))
            (root / "repo-only.md").write_text("# Extra", encoding="utf-8")
            readme.write_text(baseline + "\n[Not shipped](repo-only.md)\n", encoding="utf-8")
            self.assertTrue(validate(root))
            readme.write_text(baseline + "\n```text\n[Example](not-a-real-file.md)\n```\n", encoding="utf-8")
            self.assertFalse(validate(root))

    def test_release_notes_are_scoped_to_current_release(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            notes = release_notes(root)
            self.assertIn("English change", notes)
            self.assertIn("中文变化", notes)
            self.assertIn("/v3.0.0/embedded-hardware-design.zip", notes)
            self.assertIn("SHA256SUMS.txt", notes)
            self.assertNotIn("Earlier change", notes)

    def test_built_assets_and_checksums_match_the_reviewed_package(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            run = subprocess.run([sys.executable, str(ROOT / "scripts/build_release.py"),
                                  "--output", str(root)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
                expected, name = line.split("  ", 1)
                self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), expected)
            version = latest_release()[0]
            self.assertEqual((root / f"embedded-hardware-design-{version}.zip").read_bytes(),
                             (root / "embedded-hardware-design.zip").read_bytes())
            with ZipFile(root / "embedded-hardware-design.zip") as archive:
                self.assertEqual(set(archive.namelist()),
                                 {"embedded-hardware-design/" + p for p in EXPECTED | {"release.json"}})
                for path in EXPECTED | {"release.json"}:
                    self.assertEqual(archive.read("embedded-hardware-design/" + path), (ROOT / path).read_bytes())


if __name__ == "__main__":
    unittest.main()
