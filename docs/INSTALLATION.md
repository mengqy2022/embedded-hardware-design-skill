# 安装、升级与跨电脑使用 / Installation

[返回首页](../README.md) · [English overview](../README.en.md)

## 选择使用方式

| 环境 | 下载内容 | 安装后获得 |
| --- | --- | --- |
| Codex / 支持 Skill 的宿主 | `embedded-hardware-design.zip` | 可被宿主识别的 Skill、规则与检查模板 |
| 普通 ChatGPT | `HARDWARE_DESIGN_RULES_CHATGPT.md` | 可上传的合并规则文档 |
| 维护或贡献 | Git 仓库 | 完整文档、测试、CI 与发布工具 |

下载入口：[最新发布](https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest)。需要复现历史工程时，选择该工程记录的固定版本与提交。Python 3.10+ 仅为运行辅助脚本所需，阅读规则无需安装 Python。

## 首次安装

Windows PowerShell，Codex 默认目录示例：

```powershell
$skillArchive = Join-Path $env:TEMP 'embedded-hardware-design.zip'
Invoke-WebRequest 'https://github.com/mengqy2022/embedded-hardware-design-skill/releases/latest/download/embedded-hardware-design.zip' -OutFile $skillArchive
Expand-Archive -LiteralPath $skillArchive -DestinationPath "$env:USERPROFILE/.codex/skills"
```

ZIP 顶层只有 `embedded-hardware-design/`，解压后应能找到 `~/.codex/skills/embedded-hardware-design/SKILL.md`。若宿主实际使用 `~/.agents/skills` 或自定义路径，改用其识别目录。新建会话核对 Skill 列表；未刷新时重启宿主。

首次调用示例：

```text
使用 $embedded-hardware-design，先读取当前工程和项目约束，再按任务读取适用规则。
```

## 校验下载

Release 同时提供版本化 ZIP、同内容的稳定名称 ZIP、聊天规则文档和 `SHA256SUMS.txt`。从同一个固定版本发布页下载附件，比较 SHA-256：

```powershell
Get-FileHash -LiteralPath ./embedded-hardware-design.zip -Algorithm SHA256
```

结果应与 `SHA256SUMS.txt` 中同名文件一致。校验值检测文件损坏或内容差异，不是独立签名。运行包内检查器可再核对文件清单：

```powershell
python "$env:USERPROFILE/.codex/skills/embedded-hardware-design/scripts/package_skill.py" --verify
```

## 升级与迁移

1. 查看 [CHANGELOG](../CHANGELOG.md)，记录当前项目正在使用的版本与本地改动。
2. 将已安装的整个 `embedded-hardware-design` 目录备份并移到 **宿主不扫描** 的目录，例如 `~/.codex/skill-backups/embedded-hardware-design-旧版本/`。保留备份以便回退。
3. 将新版本 ZIP 解压到实际 Skill 目录。采用完整目录替换，避免残留旧文件；人工比较并迁移有意保留的本地规则。
4. 新建会话确认识别，核对 `release.json` 和 `provenance.json`，按需运行 `package_skill.py --verify`。

旧安装名 `pcb-design-rules` 已迁移为 `embedded-hardware-design`。同样先备份并移出扫描目录，再安装新名；调用改为 `$embedded-hardware-design`，避免重复规则被同时加载。

升级规则包不自动重验现有 PCB。历史验证结论仍绑定历史工程修订，只有实际复查后才能更新项目报告。

## 另一台电脑与普通 ChatGPT

另一台电脑安装相同 Release，并复制自己的项目说明、设计规则和必要工程资料；记录固定版本以便复现。仓库不会自动同步私人项目或 EDA 状态。

## 自动选用与可见提示

`agents/openai.yaml`显式设置`policy.allow_implicit_invocation: true`，允许支持此配置的宿主按任务选用；这是可选用策略，不是按时运行或无条件执行的Hook。安装后在新会话确认Skill可见。实时EDA编辑仍需已连接的工具。

要在某工作区持续采用此方法，将下面约定加入该工作区的`AGENTS.md`（已有同义约定就合并）：

```text
原理图、PCB、嵌入式硬件器件选型、电气/制造核验及硬件规则维护使用 embedded-hardware-design。任务开始先读取SKILL.md、provenance.json及适用参考，在首次回复说明“正在使用 embedded-hardware-design v<实际版本>；本次适用：<规则/阶段>”；交付时说明实际检查、未验证项和证据。新板、电气/接口变更执行HW-01～07，纯排版/局部修复只核验受影响项。Skill缺失或无法读取时先说明，不能只发使用声明。
```

若希望Codex在多个工作区默认采用这条硬件约定，可合并到宿主支持的用户级指令文件（Codex默认位置`~/.codex/AGENTS.md`，自定义CODEX_HOME时按实际位置）；保留其他已有指令，仅作用于上述硬件任务，普通固件或其他任务按实际关联选择。其他宿主使用其支持的项目/用户指令入口。

首次提示示例：“正在使用 embedded-hardware-design v2.4.1；本次适用：SCH-01～34、PCB-V07及项目规则。”示例版本和条目必须按当前安装及实际任务替换；问答不虚报板级DRC或实测。收尾示例：“本次使用v<实际版本>，已完成<检查>，<项目>待验证，证据见<路径>。”

此配置和约定让使用情况可见，未来会话是否正确选用仍以首次提示、适用规则及执行证据核对；无法从一次配置检查证明所有未来任务必然遵循。必要时显式调用`$embedded-hardware-design`。规则声明不保证工具或实物检查通过。

普通 ChatGPT 上传 `HARDWARE_DESIGN_RULES_CHATGPT.md`。若支持项目知识文件，可加入项目，并设置：

```text
原理图或 PCB 任务先读取 HARDWARE_DESIGN_RULES_CHATGPT.md 和本项目规则。
每项相关任务先说明正在依据规则文档的实际版本及适用范围工作，交付时列实际检查和待验证项。
器件参数以准确原厂资料为准，记录实际核验证据，未执行的检查保持未验证。
```

文件上传不等于永久训练模型。提供网表、器件资料和机械约束；没有实时工具时可审查和规划，不能宣称已修改工程或已运行原生 ERC/DRC。

## EDA 工具与可选插件

- **嘉立创 EDA 专业版：** 实时编辑需另行安装 [easyeda-api](https://github.com/easyeda/easyeda-api-skill) 及其当前要求的 Gateway/Bridge，连接成功后读取实际文档身份。
- **上游原理图增强 Skill：** 可单独安装 [easyeda-enhanced-schematic-skill](https://github.com/easyeda/easyeda-enhanced-schematic-skill)。本包已整合审阅过的方法与修正，见 [集成边界](../references/easyeda-schematic.md)；不包含上游完整运行环境，也不保证自动调用另一 Skill。
- **Ponytail / mattpocock-skills：** 见 [可选安装提示](../OPTIONAL_PLUGINS.md)。核心规则不依赖它们，不自动更改全局配置或信任 Hooks。
- **其他 EDA：** 使用各自支持的原生编辑、检查及生产文件导出工具。

## English installation notes

Download the ZIP and checksum list from the same release. Extract the single `embedded-hardware-design/` folder into the skill directory recognized by your host. The PowerShell example above is for a first installation in Codex's default directory.

For upgrades, back up and move the existing folder outside the host's scanned skill directories, then extract the replacement. Migrate intentional local changes after comparison. The former name `pcb-design-rules` should also be moved out of the scanned directory. Start a new session and verify discovery; `python scripts/package_skill.py --verify` checks installed package hashes.

For ordinary ChatGPT, upload `HARDWARE_DESIGN_RULES_CHATGPT.md` with your project constraints. Live EDA control requires separate tools. Optional workflow plugins are not installed by this package. Pin a release and commit when reproducing a project; updating these rules does not revalidate an existing PCB.

Implicit invocation is explicitly allowed in `agents/openai.yaml`. Add the hardware-task instruction to a supported workspace or user instruction file. At task start, read the installed entrypoint/version and relevant references, then announce the actual version and scope; at delivery, state completed checks, pending items and evidence. This is observable guidance, not a guarantee of future selection or engineering correctness.
