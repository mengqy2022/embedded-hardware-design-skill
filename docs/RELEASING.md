# 发布流程 / Releasing

[首页](../README.md) · [变更记录](../CHANGELOG.md)

## 版本信息的来源

- `provenance.json` 的 `version` 是规则包版本来源，`updated` 是实际维护日期。
- `CHANGELOG.md` 顶部版本必须一致，每版包含中文要点与 `### English` 下的英文要点；保留历史条目。
- `scripts/update_release_docs.py` 从以上内容生成两份 README 的 `release:start/end` 区块。
- `release.json` 保存人工审阅后的分发文件哈希，`--refresh` 不能替代审阅。

规则/模板/工具兼容变化采用语义版本。补充说明、维护与兼容修复用补丁版本；明显扩展能力用次版本；需要用户迁移的不兼容变化用主版本。标签形式为 `vX.Y.Z`。

## 发布节奏与保留策略（2026-11-05）

GitHub Releases仅保留有使用或迁移意义的里程碑和最新稳定版本。日常修正继续提交main，在CHANGELOG的待发布记录中累计；批量审阅后再决定版本与正式发布，不为每条小修改创建Release。严重正确性、兼容性或安全修复也可成为关键补丁发布，不能单凭版本尾号判断重要程度。

本轮保留5个发布页，后续按新增能力再选择，不自动逐版删除：

| 发布 | 保留原因 |
|---|---|
| v1.0.0 | 首次可携带PCB规则基线 |
| v2.0.0 | 原理图与PCB规则整合及改名 |
| v2.2.0 | 原理图增强工作方式、样本学习与通用排版 |
| v2.3.0 | PCB-V07逐器件/逐电源脚覆盖及当前证据门槛 |
| v2.4.1 | 当前推荐稳定版，包含HW-01～07和可见使用提示 |

清理的v1.1.0、v2.1.0、v2.3.1、v2.3.2、v2.4.0保留Git标签、提交与CHANGELOG；原发布说明和附件先在维护者本地归档并校验SHA-256。已清理Release的旧附件直链会失效：优先使用保留的稳定版；需要重现历史源码时按标签检出，确需原安装包时从本地归档恢复。未来再次删除发布页须有用户任务授权和具体清单。

本次属于发布维护，不升级Skill版本、不改写既有标签或发布包，不创建新的Release。

## 本地准备

1. 修改相关内容，保留规则编号、准确来源与许可。同步有授权的工作区/项目规则，分发包只包含允许公开的可复用方法。
2. 更新 `provenance.json`、顶部变更记录，生成首页摘要并审阅差异：

```powershell
python scripts/update_release_docs.py
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/verify_repository.py
```

3. 审阅后刷新文件指纹，再执行只读检查：

```powershell
python scripts/package_skill.py --refresh
python scripts/package_skill.py --verify
python scripts/update_release_docs.py --check
git diff --check
```

4. 构建到仓库之外，核对 ZIP 内容和校验文件：

```powershell
python scripts/build_release.py --output ../embedded-hardware-design-release
```

产物为版本化 ZIP、稳定名称 `embedded-hardware-design.zip`、`HARDWARE_DESIGN_RULES_CHATGPT.md`、`SHA256SUMS.txt` 和 `RELEASE_NOTES.md`。同版两份 ZIP 字节一致。发布说明来自本版变更记录，包含固定标签安装链接与校验说明。README/安装指南随包分发，贡献模板和 GitHub CI 保留在源码仓库。

## GitHub 发布

提交并推送经过检查的main后，可创建匹配版本的`vX.Y.Z`标签；main、PR和标签推送仅运行检查，不自动创建Release。需要发布里程碑时，在GitHub Actions的`CI`中选择main分支并手动运行：勾选`publish_release`，填写已有`release_tag`。未勾选时只运行检查。

手动发布流程会：

1. 在 Linux / Python 3.10、Windows / Python 3.13 上运行测试与一致性检查。
2. 检查与发布均检出指定标签，核对标签、来源版本、变更记录、双语README与分发指纹。
3. 构建 Release 附件，并使用 `RELEASE_NOTES.md` 创建正式发布。

普通PR/分支/标签检查仅有只读权限；写入Release的权限仅授予手动选择的发布job。仓库/组织的Actions设置可能限制发布，失败时查看日志并采用已构建、已核验的产物手动发布。

保留的已发布版本不改写标签或替换附件；修正累计后发适当新版本。经授权清理旧Release时先完成上述归档，保留源码历史。手动上传也必须执行以上检查，上传两份ZIP、聊天文档和校验文件，发布说明使用构建生成内容。

## 发布后核对

- 远端 main、版本标签与预期提交一致。
- GitHub 发布说明能看到本版具体变化，README 摘要与该版本一致。
- 附件可下载，远端内容或 API digest 与本地 SHA-256 一致，稳定名称下载链接存在。
- 本地安装副本先备份，再按完整发布清单同步；版本与逐文件哈希一致。
- 维护记录保存版本、提交、发布链接和校验结果；规则包发布不冒充板级 DRC/性能验收。

## English maintenance notes

The version is read from `provenance.json`. Add the matching top changelog entry with Chinese bullets and an English summary, then regenerate both README release blocks. Run tests and repository checks, review the changes, and refresh the package manifest. Build outside the repository with `scripts/build_release.py`.

Main/PR/tag pushes run checks only. For a reviewed milestone, manually dispatch `CI` from main with `publish_release` enabled and an existing `release_tag`; both check and publish jobs use that tag. Publish immutable versioned assets, the stable ZIP alias, the combined ChatGPT document, and checksums, then verify remote contents. Accumulate routine fixes instead of producing a release per edit. Retain the latest stable release and meaningful historical milestones; archive descriptions/assets and verify hashes before any user-authorized removal, preserving Git tags, commits and the full changelog. Removed asset URLs stop working; historical source remains available by tag.
