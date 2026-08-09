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
使用 $vectordeckppt 根据这份 Markdown 制作一套 10 页中文项目汇报 PPT。
受众是管理层，目标是获得下一阶段预算批准。先提炼决策叙事，再定义一种
克制、精确、编辑感强的视觉方向；不要使用通用蓝紫渐变、三卡片模板或无意义图标。
所有页面逐页渲染复审，最终交付可编辑 PPTX、源 SVG 和编译报告。
```

## 如何写出更好的请求

VectorDeckPPT 会主动补全非关键缺失信息，但下面这些内容能显著提高结果质量：

- **沟通任务**：观众听完后应该理解、相信、批准或采取什么行动；
- **受众与场景**：专业背景、决策权、演讲时长、会议或投影环境；
- **证据边界**：必须使用的数据、不可改写的结论、需要标注的不确定性；
- **视觉性格**：用具体气质描述，例如“编辑感、理性、克制”，而不是只说“高级”；
- **视觉禁区**：不希望出现的模板、配色、图像风格或行业陈词滥调；
- **交付要求**：页数、语言、比例、可编辑程度以及是否保留源 SVG。

### 商业汇报

```text
使用 $vectordeckppt 将附件整理成 12 页季度经营汇报。受众是 CEO 和业务负责人，
核心任务是解释利润率下降的三个驱动因素并获得两项资源决策。叙事采用“信号—原因—
风险—建议—负责人”的路径。视觉上采用数据优先的编辑风格：暖白底、深色正文、
少量朱红用于风险和关键偏差，使用大数字、直接标注和有节奏的疏密变化；避免仪表盘、
渐变和大量圆角卡片。所有结论必须能追溯到附件数据。
```

### 技术方案

```text
使用 $vectordeckppt 根据 PRD 和架构说明制作 15 页技术评审 PPT。受众是架构师和研发负责人，
重点讲清系统边界、关键数据流、故障隔离和迁移风险。视觉方向要像一份严谨的工程图册：
严格网格、清晰拓扑、低饱和中性色、钴蓝只表示主链路，禁止发光节点、赛博背景和装饰性
电路线。架构页优先保证连接关系可读和对象可编辑，复杂路径降级时在报告中说明。
```

### 路演与产品发布

```text
使用 $vectordeckppt 把这份产品资料重构为 10 页路演 Deck。受众是产业投资人，目标是让他们
相信需求真实、产品差异明确且商业路径可执行。视觉方向采用“高端克制 + 人文纪实”：
大尺度标题、真实场景照片、深海军蓝背景与一处明亮酸橙色强调，页面保持强烈留白和电影式
节奏；不要使用握手照片、火箭图标、虚假 3D 图表或统一三列布局。结尾明确融资用途和下一步。
```

### 重新设计已有 PPT

```text
使用 $vectordeckppt 重新设计现有 PPT，保留事实、页序和品牌色，但重写冗长标题并优化视觉
叙事。先识别每页真正的结论，再为全套定义统一的字体、网格、图片裁剪和图表强调规则。
减少边框、阴影、图标和卡片数量，让每页只有一个主要视觉焦点。交付前对 SVG 预览和最终
PPTX 逐页比较，特别检查中文换行、图片裁剪和 PowerPoint 字体偏移。
```

## 美学与设计原则

项目不把“好看”理解为增加装饰，而是要求视觉形式服务于叙事：从受众结果和证据出发，先确定视觉命题，再建立字体、空间、颜色、图像与几何规则。每页根据内容关系选择构图，并通过层级、比例、留白、节奏和克制形成辨识度。

详细指导见 [art-direction.md](.agents/skills/vectordeckppt/references/art-direction.md)、[design-system.md](.agents/skills/vectordeckppt/references/design-system.md)、[slide-design.md](.agents/skills/vectordeckppt/references/slide-design.md) 和 [visual-review.md](.agents/skills/vectordeckppt/references/visual-review.md)。

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

## V1.0 范围

V1.0 原生支持 `text`、`tspan`、`rect`、圆角矩形、`circle`、`ellipse`、`line`、`image` 和基础 `g` 样式/变换。复杂 `path`、渐变、裁剪或旋转元素通过 Office SVG 关系降级并记录在编译报告中；`filter`、`mask`、动画、PowerPoint 动画与任意 SVG 规范完整兼容不在 V1.0 范围内。

## Roadmap

- 扩展 polygon/polyline/freeform 支持
- 提升复杂路径与渐变的可编辑转换能力
- 扩展跨平台字体度量和文本基线校准
- 增加更多真实 presentation 类型的 Skill 前向测试
