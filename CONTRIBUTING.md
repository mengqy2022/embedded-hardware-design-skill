# 贡献指南 / Contributing

欢迎提交可复现的问题、准确来源支持的规则建议和小范围修正。先搜索 [现有 Issues](https://github.com/mengqy2022/embedded-hardware-design-skill/issues)，使用对应模板说明问题。

## 规则建议需要什么

1. 说明涉及的 SCH/PCB 编号、适用器件/工艺和实际问题。
2. 提供原厂资料、官方参考设计或板厂规范，注明版本、页码及链接。经验和用户偏好明确标注范围。
3. 与现有规则冲突时，列出双方条件与证据。具体项目数值不直接提升为通用阈值。
4. 给出最小改动和核验方法。没有运行的检查、实测和性能评估保持未验证。

可复用去标识的最小例子；上传前移除订单、凭据、私人路径、原生项目、未授权截图/网表和第三方文档。公开规则只包含有权分发的原创总结，保留 [来源归属](references/sources.md)。

## 本地核验

辅助代码仅使用 Python 3.10+ 标准库：

```powershell
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/verify_repository.py
python scripts/update_release_docs.py --check
git diff --check
```

涉及分发文件时，人工审阅后运行 `python scripts/package_skill.py --refresh`，再运行 `--verify`。更新自动化逻辑时，增加能证明实际行为或失效检出的测试；单纯排版修改无需编写镜像测试。

## 提交与发布

PR 说明具体问题、最终变化、来源、核验和剩余限制。保持任务范围，保留已有规则编号；版本与摘要由维护者按 [发布流程](docs/RELEASING.md) 统一处理。贡献适用本仓库现有 [CC BY-SA 4.0](LICENSE) 及来源归属要求。

## English

Open a focused issue or pull request with the affected rule IDs, exact device/process scope, primary sources with revision and page numbers, and a verification method. Distinguish electrical requirements from preferences and project-specific values. Preserve attribution and do not upload private designs or documents you cannot redistribute.

Run the standard-library tests and documentation checks above. Changes to helper behavior need meaningful behavioral tests. Maintainers coordinate version changes and release generation using the documented procedure.
