# PCB Design Rules Skill

面向常见低压嵌入式 PCB 的可携带设计规则：布局、差分/等长、晶振、电源/GND、去耦、机械、丝印及交付核验。版本 **1.0.0**。规则按需读取，项目参数单独填写；已有原理图为电气依据。

## 在另一台电脑的 Codex 中使用

从仓库克隆源码，或解压发布包。Windows PowerShell首次安装示例：

```powershell
git clone https://github.com/mengqy2022/pcb-design-rules-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE/.codex/skills" | Out-Null
Copy-Item -Recurse ./pcb-design-rules-skill "$env:USERPROFILE/.codex/skills/pcb-design-rules"
```

复制时可只复制本仓库受Git管理的文件，跳过`.git`。已有同名Skill时先比较/备份，再替换完整文件夹，避免旧文件混入。若宿主使用`~/.agents/skills`或自定义全局目录，则安装到它实际识别的位置；同一宿主只保留一份。

新建会话并在技能列表核对`pcb-design-rules`；若没有刷新，重启宿主。在对话中明确调用：

```text
使用 $pcb-design-rules，先读取本项目 DESIGN_RULES.md 和当前 PCB 状态。
只进行 PCB 布局布线，保留原理图电气功能和所有锁定机械对象。
```

可在目标项目`AGENTS.md`加入一句：

```text
涉及PCB布局、布线或审查时使用pcb-design-rules；先读取项目DESIGN_RULES.md，按其锁定规则版本和约束执行。
```

本仓库是规则Skill，不包含嘉立创Bridge、EDA控制插件或KiCad工具。嘉立创需单独安装/连接easyeda-api等工具；KiCad使用其受支持的工具链。缺少工具时可以审查资料，不能声称已修改或验证实时PCB。

## 在普通 ChatGPT 网页或其他聊天助手中使用

普通聊天不会因本机安装Codex Skill而自动读取这些文件。将`PCB_RULES_CHATGPT.md`上传到新对话；如果当前产品支持项目文件，也可放入专用项目，并添加指令：

```text
涉及PCB任务时先读取PCB_RULES_CHATGPT.md和本项目规则。
使用文件中的通用方法和用户默认，按实际器件、接口、叠层确定项目参数。
保留未检查项；没有工具输出时不报告DRC、仿真或实测通过。
```

同时提供待设计工程、网表、层叠/板厂条件、锁定对象和当前项目说明。跨电脑同步的是文件与版本，不是给模型永久训练，也不会自动赋予EDA控制能力。项目文件/上传能力随产品和账号不同；上述说明不承诺具体套餐功能。

## Ponytail 与 mattpocock-skills

可选安装方法见[OPTIONAL_PLUGINS.md](OPTIONAL_PLUGINS.md)。本Skill独立可用，不自动安装插件、执行其Hooks或改变全局配置。

## 更新与发布

以Git仓库为可携带规则的维护入口，安装目录视为部署副本；在原嵌入式工作区使用时仍以其当前用户指令和工作区规则为准。更新时对照来源记录，修改相关条款，在[CHANGELOG.md](CHANGELOG.md)说明影响，调整版本并生成校验清单。原工作区发生变化不会自动修改本仓库，需要人工复核后合入。

新项目记录Skill版本和Git提交；规则更新后先审查变更，再更新项目锁定版本。不覆盖历史项目的通过结论，不把历史V9参数移植为通用值。

Python 3.10+打包和完整性检查（不需要安装第三方Python包）：

```powershell
python scripts/package_skill.py --verify
python scripts/package_skill.py --refresh --output ../pcb-design-rules-1.0.0.zip --chatgpt-output ../PCB_RULES_CHATGPT.md
```

`--refresh`明确更新本次发布的文件哈希；先人工审核规则，哈希一致只证明文件完整。`--verify`不写文件，可在另一台电脑复核。Git仓库和ZIP均不带厂商PDF、原生PCB、私有工程或对话日志。

## 来源与许可

[sources.md](references/sources.md)记录原厂文档、版本、页码和适用边界。[LICENSE](LICENSE)使用CC BY-SA 4.0；厂商资料和第三方插件分别遵守其自己的许可，不随本仓库再授权。规则不代替准确器件指南、板厂确认或最终工程检查。

Codex机制参考[官方Skills文档](https://developers.openai.com/codex/skills/)。本次该页面返回403，未据此承诺所有宿主版本均使用相同安装目录；安装请以目标工具实际识别目录为准。
