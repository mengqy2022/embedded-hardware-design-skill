# 可选工作方式插件

这些插件帮助控制改动规模、调查问题和记录证据，不提供PCB电气正确性保证，也不替代EDA工具。本Skill无需它们也能工作；首次确有需要时提示安装一次即可，用户未安装时继续完成已能开展的工作。

下列命令来自安装时核读的上游说明：Ponytail 5.3.3的INSTALL.md、mattpocock-skills 1.3.2的README.md，核对日期2026-11-01。目标Codex须支持相应`plugin`命令；版本不支持时查上游适配说明，不反复试错安装。

## Codex：Ponytail

[上游仓库](https://github.com/DietrichGebert/ponytail) · [安装说明](https://github.com/DietrichGebert/ponytail/blob/main/INSTALL.md)

```powershell
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

按上游说明，在支持的Codex会话中查看`/hooks`、审阅并选择信任其生命周期Hooks；开始新会话，桌面端必要时重启。用户自行决定是否启用Hooks。PCB任务借用其“复用已有内容、最小完整改动、简短且有证据的反馈”方式。

## Codex：mattpocock-skills

[上游仓库及安装说明](https://github.com/mattpocock/skills)

```powershell
codex plugin marketplace add mattpocock/skills
codex plugin add mattpocock-skills@mattpocock
```

插件与`skills.sh`复制安装二选一，避免同一宿主重复安装。仓库初始配置可按上游的`/setup-matt-pocock-skills`处理；具体技能和命令以安装版本为准。

处理不确定的关键技术问题时使用`research`：限定问题，优先准确芯片数据手册/官方参考设计/板厂规范，将结论、版本、页码、未确定项记入项目。它的具体流程以安装的SKILL.md为准；不要因插件名字把所有PCB动作都改成研究任务。

## 普通 ChatGPT

上述命令属于支持插件的代理环境，不是在普通ChatGPT聊天输入框执行的安装命令。在普通聊天使用导出的规则Markdown和明确任务指令即可；不能据此宣称第三方插件已经安装或运行。
