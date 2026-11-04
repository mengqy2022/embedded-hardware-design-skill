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

要在某工作区持续采用此方法，将下面一行加入该工作区的`AGENTS.md`（已有同义约定就合并）：

```text
原理图或PCB任务使用 embedded-hardware-design；新板、电气功能或接口变更先读其 references/design-workflow.md（HW-01～07），复用项目记录关联需求、依据与验收。纯排版/局部修复只复查受影响项，实测未完成时保持未验证。
```

保留默认自动发现配置；新会话确认Skill可见，必要时显式调用`$embedded-hardware-design`。工作区约定提供持续入口，阶段证据用于核验执行，二者都不保证工具或实物结果必然通过。

普通 ChatGPT 上传 `HARDWARE_DESIGN_RULES_CHATGPT.md`。若支持项目知识文件，可加入项目，并设置：

```text
原理图或 PCB 任务先读取 HARDWARE_DESIGN_RULES_CHATGPT.md 和本项目规则。
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
