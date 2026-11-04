<div align="center">

![Embedded Hardware Design — Schematic. Layout. Routing. Evidence.](assets/cover.svg)

# Embedded Hardware Design

**让原理图清楚易读，让 PCB 设计有据可查。**

面向 AI 辅助嵌入式硬件设计的可携带规则、检查模板与证据门槛。

[![Release](https://img.shields.io/github/v/release/mengqy2022/embedded-hardware-design-skill?style=flat-square&color=0f766e)](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest)
[![CI](https://github.com/mengqy2022/embedded-hardware-design-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/mengqy2022/embedded-hardware-design-skill/actions/workflows/ci.yml)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-334155?style=flat-square)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-334155?style=flat-square)](https://www.python.org/downloads/)

**简体中文** · [English](README.en.md) · [快速安装](docs/INSTALLATION.md) · [版本记录](CHANGELOG.md) · [提出建议](https://github.com/mengqy2022/embedded-hardware-design-skill/issues/new/choose)

</div>

## 最新进展

<!-- release:start -->
**[v2.4.0](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v2.4.0) · 2026-11-04**

- 新增HW-01～07工程闭环：量化需求/验收、共享接口、计算与边界条件、按风险研究/仿真、装配/测试接入、样机测试及经验反馈。
- 新增精简设计依据模板，复用已有记录并关联需求、器件/网络、计算、模型与实测证据；新板/电气/接口变更读取，纯排版和局部修复只核验受影响项。
- 区分设计检查、制造输出、样机和合规结论；仿真记录模型边界，未测项保持未验证。延续PCB-V07及全部既有规则，更新双语首页、安装包和聊天合并规则；未修改EDA或追溯认证旧板。

[完整变更记录](CHANGELOG.md) · [安装包与校验文件](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v2.4.0)
<!-- release:end -->

## 能解决什么

把原理图排版、PCB 布局布线和交付检查串成可复用的工作方式。规则按任务读取，复用现有工程与已验证记录，减少重复解释和无关修改。

| 设计环节 | 关注内容 | 入口 |
| --- | --- | --- |
| 新板与电气变更 | 量化需求、共享接口、计算与风险验证、样机反馈 | [HW-01～07](references/design-workflow.md) · [记录模板](assets/DESIGN_EVIDENCE.md) |
| 原理图 | 功能分区、引脚与符号一致、连线清晰、标签与字体不重叠 | [SCH 规范](references/schematic-style.md) |
| PCB 布局 | 锁定机械条件、器件装配间距、接口位置、丝印可读性 | [布局与制造](references/layout-manufacturing.md) |
| 供电与回流 | 逐电源脚去耦、输入/输出电容、低电感回路、真实 GND 铜路 | [电源与接地](references/power-ground.md) |
| 敏感网络 | 差分耦合、连续参考、必要等长、晶振敏感区域 | [差分与晶振](references/differential-crystal.md) |
| 阶段验收 | 器件/电源脚覆盖、当前修订证据、原生 DRC、制造输出 | [PCB-V07](references/pcb-stage-review.md) |

**适用范围：** 常见低压嵌入式硬件。器件参数、叠层、阻抗、电流和制造工艺按项目确定；高压、隔离、DDR、RF 等专用设计另查准确指南。规则包提供设计方法，实时操作由独立的 EDA 工具完成。

## 三步开始

### 1. 安装规则

在 [最新 Release](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest) 下载 `embedded-hardware-design.zip`；Windows PowerShell **首次安装**：

```powershell
$skillArchive = Join-Path $env:TEMP 'embedded-hardware-design.zip'
Invoke-WebRequest 'https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest/download/embedded-hardware-design.zip' -OutFile $skillArchive
Expand-Archive -LiteralPath $skillArchive -DestinationPath "$env:USERPROFILE/.codex/skills"
```

新建会话核对 Skill 列表。已有安装或旧名 `pcb-design-rules` 时，按 [升级与迁移](docs/INSTALLATION.md#升级与迁移) 先备份再替换。发布附件附带 `SHA256SUMS.txt`。

普通 ChatGPT 可上传 Release 中的 `HARDWARE_DESIGN_RULES_CHATGPT.md`；工具连接和可选插件见 [完整安装说明](docs/INSTALLATION.md)。

### 2. 带上工程与约束

提供当前工程、项目规则、准确器件资料，以及板框、锁定器件、叠层和板厂条件。示例：

```text
使用 $embedded-hardware-design 优化当前原理图与 PCB。
先读取项目说明、规则和现有核验报告；保持未授权的网络与锁定机械对象不变。
新板或电气/接口变更按 HW-01～07 关联需求、计算与验收；仿真按风险选择，实测状态单独记录。
先完成布局和逐电源脚供电/回地审查，再布线；按 PCB-V07 留下当前修订证据。
```

项目 `AGENTS.md` 可加入：

```text
原理图或 PCB 任务使用 embedded-hardware-design；按任务读取 SCH/PCB 细则，
遵循项目约束，记录适用规则版本和核验证据。
```

### 3. 以证据完成验收

```mermaid
flowchart LR
  A[读取工程与约束] --> B[布局与关键回路]
  B --> C[布局阶段门槛]
  C --> D[关键及普通布线]
  D --> E[铺铜与 GND 收尾]
  E --> F[DRC · 适用泪滴 · 重铺铜 · DRC]
  F --> G[最终门槛与生产文件检查]
```

```powershell
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage layout
python scripts/check_pcb_stage.py review.json --pcb current.epcb --stage final
```

记录格式见 [阶段模板](assets/PCB_STAGE_REVIEW.json)。检查器验证覆盖、阶段和证据文件哈希；几何、电气、原生 DRC 与人工判断仍须真实执行。历史结论只对应其原有修订。

## 规则与模板导航

| 我现在需要…… | 阅读或复用 |
| --- | --- |
| 建立需求、计算和样机验证闭环 | [HW-01～07](references/design-workflow.md) · [精简模板](assets/DESIGN_EVIDENCE.md) |
| 了解 Skill 的执行入口 | [SKILL.md](SKILL.md) |
| 绘制/整理原理图 | [排版规则](references/schematic-style.md) · [检查清单](assets/SCHEMATIC_REVIEW.md) |
| 借鉴工程版式、处理规则冲突 | [样本方法与取舍](references/schematic-examples.md) |
| 使用嘉立创原理图自动化 | [SCH-28～34 与 API 工作方式](references/easyeda-schematic.md) |
| 配置新项目并记录例外 | [项目规则模板](assets/PROJECT_RULES.md) |
| 完成核验与交付 | [核验与证据](references/verification.md) · [阶段审查](references/pcb-stage-review.md) |
| 查明来源与适用边界 | [来源表](references/sources.md) · [来源指纹](provenance.json) |
| 安装 Ponytail / mattpocock-skills | [可选插件](OPTIONAL_PLUGINS.md) |

规则区分电气原则、用户偏好、项目参数和待验证建议。例如，去耦电容通常并联，物理上的“大到小”排列须服从准确器件要求、低电感回路与稳定性；100 nF 或 20 mil 不是所有设计的通用答案。

## 工具兼容与边界

| 环境 | 用法 |
| --- | --- |
| Codex / 支持 Skill 的宿主 | 安装完整目录，显式调用或由宿主按任务选用 |
| 普通 ChatGPT / 项目知识文件 | 上传合并规则与项目资料；读取规则不等于模型永久训练 |
| 嘉立创 EDA 专业版 | 配合另行安装、连接的 `easyeda-api` 等工具 |
| 其他 EDA | 复用设计原则，使用该工具支持的原生编辑与核验方式 |

Ponytail 与 mattpocock-skills 是可选工作方式插件。上游原理图增强 Skill 的已审阅方法及修正见 [集成说明](references/easyeda-schematic.md)；安装本规则包不自动安装其他插件，也不附带用户工程。

## 参与与维护

- **报告问题 / 提议规则：** 使用 [Issue 模板](https://github.com/mengqy2022/embedded-hardware-design-skill/issues/new/choose)，附准确来源、适用范围与最小证据。
- **贡献内容：** 见 [贡献指南](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/CONTRIBUTING.md)，保留 SCH/PCB 编号及来源归属。
- **发布维护：** [发布流程](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/docs/RELEASING.md) 使用变更记录生成双语首页摘要，并在 CI 核对版本、链接、测试和包哈希。
- **敏感信息：** 按 [安全说明](https://github.com/mengqy2022/embedded-hardware-design-skill/blob/main/SECURITY.md) 处理；公开内容只保留可复用方法。

## 许可与致谢

文档与原创辅助代码采用 [CC BY-SA 4.0](LICENSE)。[来源表](references/sources.md) 保留作者、链接及适用边界；SparkFun Electronics / jimblom 等来源的归属继续保留。厂商文档、第三方插件和原始工程遵循各自许可，不随本包重新授权。
