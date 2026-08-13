# Contributing to VectorDeckPPT

感谢参与 VectorDeckPPT。项目的核心目标不是扩大 SVG 规范覆盖面，而是在明确边界内稳定生成可编辑、可审阅、可复现的 PowerPoint。

## 开发环境

需要 Python 3.12+。推荐使用 uv：

```bash
uv sync
```

标准 pip 环境同样受支持：

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 架构边界

- VectorDeckPPT 是 Agent Skill，不是 AI Provider API 应用。
- `SKILL.md` 和 `references/` 定义 Agent 行为；`scripts/` 只做确定性处理。
- 一页一份 SVG，SVG 是视觉真源。
- 编译时优先 PowerPoint 原生对象，其次是显式 Office SVG 降级。
- 不支持的可见内容必须被转换、降级或明确失败，不能静默丢失。
- 坐标换算集中在 `scripts/lib/coordinates.py`，不要在各编译器模块复制比例逻辑。

完整规范见 [PRD](doc/PRD.md) 和 [仓库开发指南](AGENTS.md)。

## 目录职责

| 位置 | 职责 |
|---|---|
| `.agents/skills/vectordeckppt/SKILL.md` | 核心 Agent 工作流与不可违反的质量门 |
| `.agents/skills/vectordeckppt/references/` | 按需加载的规划、设计、SVG 和故障规则 |
| `.agents/skills/vectordeckppt/scripts/` | 校验、渲染、编译和包验证 CLI |
| `.agents/skills/vectordeckppt/scripts/lib/` | 可测试、可复用的确定性实现 |
| `.agents/skills/vectordeckppt/assets/` | 可复用资产和视觉方向参考 |
| `examples/` | 可复现 SVG、PPTX 与编译报告 |
| `tests/` | 行为、结构、依赖和端到端回归测试 |
| `doc/` | 用户指南、PRD、提示词与发布记录 |

## 修改时同步哪些内容

| 修改类型 | 必须同步 |
|---|---|
| Agent 工作流或审批门 | `SKILL.md`、相关 reference、README/使用指南、PRD、结构测试 |
| 视觉或内容质量规则 | 设计 references、提示词示例、模板或示例、视觉/结构测试 |
| SVG 支持范围或降级行为 | SVG 作者指南、映射文档、故障排查、编译测试、示例报告 |
| CLI 参数或输出格式 | CLI `--help`、README/使用指南命令、单元测试 |
| 依赖 | `pyproject.toml`、`uv.lock`、`requirements.txt`、依赖测试 |
| 发布版本 | `pyproject.toml`、`uv.lock`、CHANGELOG、PRD 状态、发布说明和发布测试 |

历史发布说明描述当时版本，不要为了匹配 `main` 的未发布能力而回写旧版本记录。

## 测试

提交前必须运行：

```bash
git diff --check
uv run ruff check .
uv run pytest
```

修改 Skill 结构或元数据后，额外运行 Skill 校验：

```bash
python <skill-creator-root>/scripts/quick_validate.py .agents/skills/vectordeckppt
```

确定性行为变化必须增加回归测试。优先使用可复现 fixture 和结构断言，不依赖脆弱的逐像素比较。端到端示例应完成 SVG 校验、渲染、编译、`python-pptx` 重开和 PPTX 包验证。

## 更新依赖

使用 uv 修改并锁定依赖，再导出标准 pip 文件：

```bash
uv lock
uv --no-managed-python export --format requirements.txt --all-groups --no-emit-project --no-hashes --frozen --output-file requirements.txt
```

不要手工编辑 `uv.lock` 或 `requirements.txt`。导出后运行依赖测试，确认文件不包含本地绝对路径或项目自身的 file URL。

## 文档约定

- README 负责定位、效果、快速开始和最重要的入口。
- [使用指南](doc/usage-guide.md) 面向生成、修改和验收 Deck 的使用者。
- [提示词示例](doc/prompt-examples.md) 提供可复制请求，不替代规范说明。
- `SKILL.md` 保持核心流程简洁；详细规则放在直接链接的 `references/` 中。
- 代码、命令、诊断码和文件路径必须与当前实现一致。
- 新增或修改本地 Markdown 链接后运行测试，确保目标存在。

## Git 约定

本仓库按项目约定直接维护 `main`，除非维护者明确要求，不创建其他分支。提交使用英文 Conventional Commits，例如：

```text
feat(compiler): support editable polyline freeforms
fix(text): preserve explicit whitespace only
docs(skill): clarify typography audit workflow
test(renderer): cover invalid output collisions
```

保持提交范围小而完整，不混入无关格式化或生成的 `output/`、`pptoutput/` 产物。不要 force-push 或重写无关历史。

## 发布检查

发布前确认：

1. 完整测试、Ruff、diff check 和 Skill 校验通过；
2. 示例 PPTX 使用当前编译器重新生成并通过包验证；
3. 示例编译报告与源 SVG 一致；
4. 当前版本、锁文件、CHANGELOG、PRD 状态和发布说明一致；
5. `requirements.txt` 可在标准 pip 环境安装；
6. 工作区没有被误提交的输出目录或临时文件。

只有在维护者明确要求发布时才创建标签和 GitHub Release。

## 发布流程

1. 选择符合语义化版本的版本号，并把 `CHANGELOG.md` 的已完成条目从 `Unreleased` 归档到带日期的版本段；
2. 同步 `pyproject.toml`、`uv.lock`、PRD 状态、README 版本入口、`doc/README.md` 和 `doc/releases/vX.Y.Z.md`；
3. 重新生成受版本信息影响的示例 PPTX、PNG 与编译报告，并逐项验证；
4. 运行 `git diff --check`、Ruff、Pytest、Skill 校验和发布元数据测试；
5. 在 `main` 创建并推送发布提交，再创建带注释的 `vX.Y.Z` 标签并推送；
6. 标签工作流使用同名 `doc/releases/vX.Y.Z.md` 创建 GitHub Release。确认 Release 已发布且标记为 latest。

不要在版本标签创建后继续修改对应发布说明；需要更正时发布补丁版本。
