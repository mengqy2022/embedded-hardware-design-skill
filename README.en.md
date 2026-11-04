<div align="center">

![Embedded Hardware Design — Schematic. Layout. Routing. Evidence.](assets/cover.svg)

# Embedded Hardware Design

**Readable schematics. PCB decisions backed by evidence.**

Portable rules, review templates, and evidence gates for AI-assisted embedded hardware design.

[![Release](https://img.shields.io/github/v/release/mengqy2022/embedded-hardware-design-skill?style=flat-square&color=0f766e)](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest)
[![CI](https://github.com/mengqy2022/embedded-hardware-design-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/mengqy2022/embedded-hardware-design-skill/actions/workflows/ci.yml)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-334155?style=flat-square)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-334155?style=flat-square)](https://www.python.org/downloads/)

[简体中文](README.md) · **English** · [Installation](docs/INSTALLATION.md) · [Changelog](CHANGELOG.md) · [Open an issue](https://github.com/mengqy2022/embedded-hardware-design-skill/issues/new/choose)

</div>

## Latest release

<!-- release:start -->
**[v2.4.0](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v2.4.0) · 2026-11-04**

- Added HW-01–07 for measurable requirements, shared interfaces, bounded calculations, risk-based research/simulation, assembly/test access, prototype tests, and feedback.
- Added a compact evidence template linking requirements, design objects, calculations, models, and measurements; reuse existing records and limit cosmetic/local changes to affected checks.
- Report design, manufacturing, prototype, and compliance states separately; state model limits and keep unmeasured items unverified. Preserve PCB-V07 and existing rules, refresh bilingual release docs and portable packages; no EDA edits or retroactive board certification.

[All changes](CHANGELOG.md) · [Release assets and checksums](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v2.4.0)
<!-- release:end -->

## What this provides

A reusable workflow for schematic presentation, PCB layout and routing, and delivery review. Load only the references relevant to the task and reuse the existing design and verified records.

| Area | Design focus | Reference |
| --- | --- | --- |
| New designs and electrical changes | Measurable acceptance, shared interfaces, calculations, risk-based analysis, prototype feedback | [HW-01–07](references/design-workflow.md) · [Evidence template](assets/DESIGN_EVIDENCE.md) |
| Schematics | Functional blocks, symbol/pin consistency, clear wiring and labels | [Schematic style](references/schematic-style.md) |
| Layout | Protected mechanics, assembly access, connector placement, readable silkscreen | [Layout and manufacturing](references/layout-manufacturing.md) |
| Power and return | Per-pin decoupling, regulator capacitors, low-inductance loops, actual ground copper | [Power and ground](references/power-ground.md) |
| Sensitive nets | Differential coupling and reference continuity, necessary matching, crystal loops | [Differential and crystal](references/differential-crystal.md) |
| Verification | Component/power-pin coverage, current evidence, native DRC, fabrication files | [PCB-V07 gates](references/pcb-stage-review.md) |

Designed for common low-voltage embedded hardware. Device values, stackup, impedance, current capacity, and fabrication requirements are project-specific. High-voltage, isolation, DDR, and RF designs need their dedicated guidance. Most detailed design references are currently in Chinese.

## Quick start

### 1. Install

Download `embedded-hardware-design.zip` from the [latest release](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest). For a **first installation** on Windows:

```powershell
$skillArchive = Join-Path $env:TEMP 'embedded-hardware-design.zip'
Invoke-WebRequest 'https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest/download/embedded-hardware-design.zip' -OutFile $skillArchive
Expand-Archive -LiteralPath $skillArchive -DestinationPath "$env:USERPROFILE/.codex/skills"
```

Open a new session and check the skill list. Back up an existing installation before replacing it; see [installation and migration](docs/INSTALLATION.md). Release assets include `SHA256SUMS.txt`. For ordinary ChatGPT, upload `HARDWARE_DESIGN_RULES_CHATGPT.md` together with project context.

### 2. Supply the project context

```text
Use $embedded-hardware-design to improve this schematic and PCB.
Read the current design, project rules, and verification report first.
For new designs or electrical/interface changes, use HW-01–07 to link requirements, calculations and acceptance; select simulations by risk and report measurement states separately.
Keep electrical connectivity unchanged unless explicitly authorized; preserve locked mechanics.
Complete layout and per-power-pin supply/return review before routing.
Record evidence for the current revision using PCB-V07.
```

Provide the current engineering files, device documentation, mechanical constraints, stackup, and fabrication limits. A project `AGENTS.md` can require this skill for schematic and PCB tasks.

### 3. Review against current evidence

The workflow proceeds from constraints to placement, the layout gate, critical/ordinary routing, ground pours and stitching, native DRC, applicable teardrops, repour, repeat DRC, and final fabrication review.

```powershell
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage layout
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage final
```

Start with the [review template](assets/PCB_STAGE_REVIEW.json). The checker validates coverage, stage, and evidence hashes. It does not evaluate geometry, prove reviewer conclusions, run native DRC, or certify hardware performance. Historical results apply to their original revision.

## Documentation

| Task | Start here |
| --- | --- |
| Agent workflow | [SKILL.md](SKILL.md) |
| Schematic checks | [Review template](assets/SCHEMATIC_REVIEW.md) |
| Learn from schematic examples | [Methods and tradeoffs](references/schematic-examples.md) |
| EasyEDA schematic automation | [Integration and corrections](references/easyeda-schematic.md) |
| Define project constraints | [Project rules template](assets/PROJECT_RULES.md) |
| Verify and deliver | [Verification](references/verification.md) · [Stage review](references/pcb-stage-review.md) |
| Trace sources | [Source attribution](references/sources.md) · [Provenance](provenance.json) |
| Optional workflow plugins | [Ponytail and mattpocock-skills](OPTIONAL_PLUGINS.md) |

Electrical principles, user preferences, project parameters, and unverified suggestions remain distinct. Decoupling capacitors are normally parallel; a preferred physical capacitor order is subordinate to the exact device guidance, low-inductance loops, and regulator stability.

## Tools and compatibility

The skill supplies design guidance. Live EasyEDA Pro editing requires a separately installed and connected tool such as `easyeda-api`. Other EDA tools require their own supported native editing and verification workflow. Uploading rules does not permanently train a model or grant EDA control.

Ponytail and mattpocock-skills are optional. Reviewed methods from the upstream enhanced schematic skill are documented with corrections and scope; this package does not automatically install third-party plugins or include user designs.

## Contributing and maintenance

Use the [issue templates](https://github.com/mengqy2022/embedded-hardware-design-skill/issues/new/choose) for bugs or source-backed rule proposals. Read the [contribution guide](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/CONTRIBUTING.md), [release procedure](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/docs/RELEASING.md), and [security notes](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/SECURITY.md).

Release summaries in both READMEs are generated from the version metadata and changelog. CI checks documentation consistency, local links, helper tests, and package hashes before tagged releases are built.

## License and attribution

Documentation and original helper code are licensed under [CC BY-SA 4.0](LICENSE). Preserve attribution, including SparkFun Electronics / jimblom, as recorded in the [sources](references/sources.md). Vendor documents, plugins, and original engineering projects retain their respective rights and are not relicensed by this repository.
