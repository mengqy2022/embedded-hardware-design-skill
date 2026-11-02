# Embedded Hardware Design Skill

**嵌入式原理图与 PCB 设计规则，版本 2.2.1。** 由 `pcb-design-rules` 升级并改名为 `embedded-hardware-design`，原有 PCB 规则继续保留，完整加入原理图排版 SCH-01～27、嘉立创自动化补充 SCH-28～34 和检查模板。

适用于嘉立创EDA等工具中的常见低压嵌入式硬件设计。按任务读取规则，器件和制造参数由项目确定；本 Skill 不附带 EDA 控制工具或用户工程。

## 内容与入口

| 任务 | 文件 |
|---|---|
| 工作入口与范围 | [SKILL.md](SKILL.md) |
| 原理图功能分区、符号/引脚、连线、命名与排版 | [SCH-01～27](references/schematic-style.md) |
| 工程样本的方法、反例与规则冲突处理 | [样本学习与取舍](references/schematic-examples.md) |
| 原理图电气、视觉和数据一致性检查 | [检查模板](assets/SCHEMATIC_REVIEW.md) |
| 嘉立创自动化：查料、引脚扇出、对象修改与核验 | [API工作方式与取舍](references/easyeda-schematic.md) |
| PCB 布局、封装、机械与丝印 | [布局与制造](references/layout-manufacturing.md) |
| 电源、GND、去耦与输入/输出电容 | [电源与接地](references/power-ground.md) |
| 差分、等长与晶振 | [差分与晶振](references/differential-crystal.md) |
| 项目参数、验证与交付 | [项目配置](assets/PROJECT_RULES.md)、[核验证据](references/verification.md) |
| 来源、许可和适用边界 | [sources.md](references/sources.md) |

去耦电容通常并联；大到小的物理排列是有条件的用户偏好。直接平面供电不必然使去耦失效，芯片要求、低电感供地回路和稳定性优先。100 nF、线宽或固定蛇形容差不推广为所有器件的电气标准。

## 在 Codex 中安装或迁移

[GitHub 仓库](https://github.com/mengqy2022/embedded-hardware-design-skill) · [v2.2.0 发布与附件](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/tag/v2.2.0)

下载发布附件 `embedded-hardware-design-2.2.0.zip`。ZIP 内只有一个 `embedded-hardware-design/` 目录，不包含 `.git`。Windows PowerShell 首次安装示例：

```powershell
$skillZip = Join-Path $env:TEMP 'embedded-hardware-design-2.2.0.zip'
Invoke-WebRequest 'https://github.com/mengqy2022/embedded-hardware-design-skill/releases/download/v2.2.0/embedded-hardware-design-2.2.0.zip' -OutFile $skillZip
Expand-Archive -LiteralPath $skillZip -DestinationPath "$env:USERPROFILE/.codex/skills"
```

已有 `pcb-design-rules` 时，先备份并移出宿主扫描的 skills 目录，再安装新名；已有 `embedded-hardware-design` 时先比较/备份再替换，避免旧文件混入。历史旧名完成迁移后，通常只保留新 Skill。若宿主使用 `~/.agents/skills` 或自定义目录，安装到它实际识别的位置。

新建会话核对技能列表；未刷新时重启宿主。原调用 `$pcb-design-rules` 改为 `$embedded-hardware-design`。例如：

```text
使用 $embedded-hardware-design，整理当前原理图。
先读取 SCH-01～27，以我当前手绘布局为起点，保持网表不变，完成视觉检查和原理图检查。
```

```text
使用 $embedded-hardware-design，继续当前 PCB 布局布线。
读取项目 DESIGN_RULES.md 和实时工程，保留原理图网络、已完成敏感通道与锁定机械对象。
```

目标项目 `AGENTS.md` 可加入：

```text
原理图或 PCB 设计使用 embedded-hardware-design；按任务读取 SCH 规范或 PCB 细则，遵循项目规则和当前用户手绘基线，记录适用版本与核验证据。
```

嘉立创实时操作需另行连接 `easyeda-api` 等工具；KiCad 原生编辑使用其受支持的工具链。没有实时工具时可以审查资料，不能报告已编辑或已运行原生 ERC/DRC。

## 在普通 ChatGPT 中使用

下载并上传发布附件 `HARDWARE_DESIGN_RULES_CHATGPT.md`。若产品支持项目知识文件，可放入专用项目，并添加：

```text
原理图或 PCB 任务先读取 HARDWARE_DESIGN_RULES_CHATGPT.md 和本项目规则。
按任务应用 SCH/PCB 规则，器件参数以准确原厂资料为准；保持未检查项，没有工具证据不报告检查或实测通过。
```

另外提供工程、网表、当前项目说明，以及适用的机械、叠层和板厂条件。上传规则文件不等于永久训练模型，也不会自动获得 EDA 控制能力。

## Ponytail 与 mattpocock-skills

保留 [OPTIONAL_PLUGINS.md](OPTIONAL_PLUGINS.md) 中的可选安装提示。它们提供控制改动规模和定向研究的工作方式，不是本 Skill 的强制依赖；不自动安装、信任 Hooks 或更改全局配置。

## 维护与发布

本仓库是可携带规则的维护源，安装目录为部署副本。更新时同步相关工作区/项目规则，保留 SCH/PCB 编号、来源和适用边界，记录 [CHANGELOG](CHANGELOG.md) 与 [来源指纹](provenance.json)。新项目记录实际使用版本和提交；历史通过结论只对应历史修订。

Python 3.10+，仅使用标准库：

```powershell
python scripts/package_skill.py --refresh --output ../embedded-hardware-design-2.2.0.zip --chatgpt-output ../HARDWARE_DESIGN_RULES_CHATGPT.md
python scripts/package_skill.py --verify
```

`--refresh` 在人工审阅后记录文件哈希；`--verify` 只检查包完整性。规则更新不自动重验现有 PCB，也不能证明电气、SI/PI、EMC 或实物功能通过。打包采用显式文件清单，排除厂商 PDF、截图、原生工程、私有坐标/网表及对话记录。

## 来源与许可

规则按 [CC BY-SA 4.0](LICENSE) 提供；[来源表](references/sources.md)保留作者、链接、版本/页码和边界。厂商资料与第三方插件按各自许可，不随本包再分发或再授权。SCH 规范中的排版尺寸为工作习惯，不是制造或电气标准。
