# VectorDeckPPT

VectorDeckPPT 是一个面向 AI Agent 的可编辑 PowerPoint 生成 Skill。宿主 Agent 负责理解资料、规划叙事、定义视觉系统并将每一页设计成结构化 SVG；仓库中的确定性脚本负责校验、渲染预览、编译 PPTX 和检查交付文件。

项目不调用任何 AI Provider SDK，也不把整页截图作为默认 PPT 内容。`SVG <text>`、基础图形和图片会尽可能编译为 PowerPoint 原生对象，以保留编辑能力；无法安全转换的可见元素必须回退为嵌入式 SVG 或明确报错，不能静默丢失。

## 核心流程

```text
source material -> Agent planning and design -> one SVG per slide
                -> validate -> render -> visual review -> revise
                -> compile editable PPTX -> validate -> deliver
```

## 目录

```text
.agents/skills/vectordeckppt/
  SKILL.md                 Agent 操作规程
  agents/openai.yaml       Skill 界面元数据
  references/              按需读取的设计与工具链规则
  scripts/                 确定性 SVG/PPTX 工具
  assets/                  少量可复用主题、图标和示例资产
tests/                     单元与集成测试
examples/basic-deck/       可编译的示例演示文稿
doc/PRD.md                 产品与实现规范
```

## 安装

需要 Python 3.12+ 与 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync
```

在支持仓库 Skill 自动发现的 Agent 中打开本仓库，或将 `.agents/skills/vectordeckppt` 复制/链接到 Agent 的 Skill 目录。随后可直接请求：

```text
使用 $vectordeckppt 根据这份 Markdown 制作一套 10 页的中文项目汇报 PPT。
```

## 命令行工具

```bash
# 校验单页 SVG
uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py slide.svg

# 渲染单页或整个目录
uv run python .agents/skills/vectordeckppt/scripts/render_svg.py slide.svg
uv run python .agents/skills/vectordeckppt/scripts/render_svg.py slides/ --output-dir preview/

# 编译多页 PPTX 并输出编译报告
uv run python .agents/skills/vectordeckppt/scripts/compile_pptx.py slides/ --output final.pptx

# 校验 PPTX 包结构和引用
uv run python .agents/skills/vectordeckppt/scripts/validate_pptx.py final.pptx
```

## 开发与验证

```bash
uv run ruff format .
uv run ruff check .
uv run pytest
```

提交使用 Conventional Commits，并在提交前运行 `git diff --check`、Ruff 和 Pytest。完整维护约束见 `AGENTS.md`。

## 当前范围

MVP 原生支持 `text`、`tspan`、`rect`、圆角矩形、`circle`、`ellipse`、`line`、`image` 和基础 `g` 样式/变换。复杂 path、filter、mask、动画、PowerPoint 动画与任意 SVG 规范完整兼容不在第一版范围内。

## Roadmap

- 扩展 polygon/polyline/freeform 支持
- 提升复杂路径与渐变的可编辑转换能力
- 扩展跨平台字体度量和文本基线校准
- 增加更多真实 presentation 类型的 Skill 前向测试
