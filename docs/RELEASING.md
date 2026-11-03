# 发布流程 / Releasing

[首页](../README.md) · [变更记录](../CHANGELOG.md)

## 版本信息的来源

- `provenance.json` 的 `version` 是规则包版本来源，`updated` 是实际维护日期。
- `CHANGELOG.md` 顶部版本必须一致，每版包含中文要点与 `### English` 下的英文要点；保留历史条目。
- `scripts/update_release_docs.py` 从以上内容生成两份 README 的 `release:start/end` 区块。
- `release.json` 保存人工审阅后的分发文件哈希，`--refresh` 不能替代审阅。

规则/模板/工具兼容变化采用语义版本。补充说明、维护与兼容修复用补丁版本；明显扩展能力用次版本；需要用户迁移的不兼容变化用主版本。标签形式为 `vX.Y.Z`。

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

提交并推送经过检查的 main 后，创建并推送匹配版本的 `vX.Y.Z` 标签。GitHub Actions 的 `CI` 工作流会：

1. 在 Linux / Python 3.10、Windows / Python 3.13 上运行测试与一致性检查。
2. 标签构建时核对标签、来源版本、变更记录、双语 README 与分发指纹。
3. 构建 Release 附件，并使用 `RELEASE_NOTES.md` 创建正式发布。

普通 PR/分支检查仅有只读权限；写入 Release 的权限仅授予标签发布 job。仓库/组织的 Actions 设置可能限制自动发布，失败时查看日志并采用已构建、已核验的产物手动发布。

已发布版本保留原标签和附件；修正后发新版本，避免用户无法复现旧包。使用手动发布时也必须执行以上检查，上传两份 ZIP、聊天文档和校验文件，发布说明使用构建生成内容。

## 发布后核对

- 远端 main、版本标签与预期提交一致。
- GitHub 发布说明能看到本版具体变化，README 摘要与该版本一致。
- 附件可下载，远端内容或 API digest 与本地 SHA-256 一致，稳定名称下载链接存在。
- 本地安装副本先备份，再按完整发布清单同步；版本与逐文件哈希一致。
- 维护记录保存版本、提交、发布链接和校验结果；规则包发布不冒充板级 DRC/性能验收。

## English maintenance notes

The version is read from `provenance.json`. Add the matching top changelog entry with Chinese bullets and an English summary, then regenerate both README release blocks. Run tests and repository checks, review the changes, and refresh the package manifest. Build outside the repository with `scripts/build_release.py`.

Pushing a matching version tag runs cross-platform CI and the tag-only release job. Publish immutable versioned assets, the stable ZIP alias, the combined ChatGPT document, and checksums. Verify the remote commit and asset hashes after publishing. An already published version should be corrected through a new release.
