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
examples/project-intro-deck/  10 页项目介绍（可编辑 PPTX、源 SVG 与编译报告）
doc/PRD.md                 产品与实现规范
```

## 安装

需要 Python 3.12+。可以使用 [uv](https://docs.astral.sh/uv/)：

```bash
uv sync
```

也可以使用标准 `pip`：

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

如果创建了虚拟环境，请先激活它，或将上面的 `python` 替换为 `.venv` 中的 Python 可执行文件。`requirements.txt` 从 `uv.lock` 导出，包含运行、测试与 lint 所需的锁定依赖，因此不安装 `uv` 也能使用项目。

## 使用 Skill

### 1. 让 Agent 发现 VectorDeckPPT

在 Codex 中打开本仓库时，仓库级 Skill 位于：

```text
.agents/skills/vectordeckppt/
```

Codex 可以在当前仓库中发现它。若希望在其他项目中也能使用，可以将整个 `vectordeckppt` 目录复制或链接到个人 Skill 目录：

```text
$CODEX_HOME/skills/vectordeckppt/
```

未设置 `CODEX_HOME` 时，通常使用：

```text
~/.codex/skills/vectordeckppt/
```

不要只复制 `SKILL.md`；`references/`、`scripts/` 和 `assets/` 都是完整工作流的一部分。

### 2. 在请求中调用 Skill

最稳定的调用方式是在请求开头显式写出 `$vectordeckppt`：

```text
使用 $vectordeckppt 根据这份 Markdown 制作一套 10 页中文项目汇报 PPT。
```

也可以直接提出“制作 PPT、重新设计 PowerPoint、生成答辩演示文稿”等请求，让 Agent 根据 Skill 描述自动触发；如果需要确保使用本项目的向量工作流，建议始终显式写 `$vectordeckppt`。

### 3. 提供输入资料与准确需求

可以在请求中附加文件，或给出 Agent 能访问的本地路径。支持作为内容来源的资料包括：

- Markdown、TXT 和已有文案；
- PDF、DOCX 和现有 PPTX；
- CSV、Excel、表格与数据摘要；
- 图片、截图、Logo 和品牌素材；
- PRD、研究报告、技术文档及多份混合资料。

同时说明哪些内容属于不可改写的事实、哪些数字必须保留、哪些图片可以使用，以及是否有品牌字体、颜色或保密限制。Agent 会先读取资料，再规划演示文稿，不应在未理解来源时直接绘制页面。

如果描述存在残缺、矛盾或会产生明显不同的理解，Skill 会先提出少量具体问题并等待回答。例如，“受众是开发者和潜在用户”仍可能需要明确谁是主要受众、双方的身份与知识水平，以及这套 PPT 最终要推动谁做什么。非关键缺省会使用合理默认值，不会把所有偏好都变成问卷。

### 4. 推荐请求模板

```text
使用 $vectordeckppt 根据【资料或文件路径】制作一套【页数】页的【语言】PPT。

主要受众身份/角色：
受众知识水平与决策权：
次要受众：
演示场景：
沟通目标或期望行动：
必须保留的事实或数据：
希望采用的视觉性格：
不要出现的视觉风格：
品牌与素材约束：
可编辑性要求：
最终交付目录：默认使用当前目录下的 pptoutput/

请先提交完整的文字版逐页内容供我确认；文字内容批准后，只生成 3 页有代表性的
SVG/PNG 视觉样稿供我确认；两次批准后再生成全套页面、编译并验证 PPTX，同时保留
源 SVG、PNG 预览和 compilation-report.json。
```

其中只有资料和核心目标是必需的；页数、视觉方向等非关键信息缺失时，Skill 会采用合理默认值继续工作。

### 5. Skill 会执行什么

一次完整任务包含两个明确的用户确认节点：

1. 检查需求是否准确；关键描述不清时先提问并等待回答；
2. 阅读资料并提取结论、证据、数据和可用素材；
3. 生成完整的文字版逐页内容并保存为 `pptoutput/slide-content.md`；
4. **等待用户明确批准文字内容**，批准前不生成 SVG、PNG 或 PPTX；
5. 建立统一的艺术方向和设计系统，只生成 3 页代表性 SVG/PNG 样稿；
6. **等待用户明确批准视觉样稿**，根据意见反复修改这 3 页；
7. 两次批准后生成所有最终 SVG，并逐页校验、渲染和视觉复审；
8. 将文本、基础图形和图片尽可能编译为 PowerPoint 原生对象；
9. 验证最终 PPTX，并报告影响编辑能力的 SVG 降级元素。

文字批准和视觉批准相互独立，沉默或“继续”不会被自动当作两个阶段都已批准。用户对文字内容做实质修改后，受影响的视觉样稿需要重新确认。

### 6. 典型交付内容

未指定其他位置时，Skill 使用当前工作目录下的 `pptoutput/`：

```text
pptoutput/
  slide-content.md
  sample/
    slides/
      slide_01.svg
      slide_05.svg
      slide_08.svg
    preview/
      slide_01.png
      slide_05.png
      slide_08.png
  slides/
    slide_01.svg
    slide_02.svg
  assets/
  preview/
    slide_01.png
    slide_02.png
  compilation-report.json
  final.pptx
```

- `final.pptx`：最终演示文稿；
- `slide-content.md`：经用户确认的完整文字版逐页内容；
- `sample/`：用于第二次确认的 3 页视觉样稿；
- `slides/`：每页的视觉源文件，也是后续修改入口；
- `preview/`：用于逐页视觉复审的 PNG；
- `compilation-report.json`：原生对象、SVG 降级和失败元素统计。

当报告中的 `embedded_svg` 大于 `0` 时，相关对象只能进行整体编辑，内部路径不一定是 PowerPoint 原生对象；`failed` 必须为 `0` 才能交付。

### 7. 快速开始示例

```text
使用 $vectordeckppt 根据这份 Markdown 制作一套 10 页中文项目汇报 PPT。
受众是管理层，目标是获得下一阶段预算批准。先提炼决策叙事，再定义一种
克制、精确、编辑感强的视觉方向；不要使用通用蓝紫渐变、三卡片模板或无意义图标。
先给我完整文字版逐页内容；我批准后制作封面、核心证据页和最复杂图解页这 3 页样稿；
视觉批准后再完成全套。所有页面逐页渲染复审，最终交付到当前目录的 pptoutput/。
```

如果只需要重新编译已经完成的 SVG，可以直接使用后文的命令行工具；命令行工具不会替代 Agent 的内容规划、艺术指导和视觉复审。

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

使用 uv：

```bash
uv run ruff format .
uv run ruff check .
uv run pytest
```

使用 pip 环境：

```bash
python -m ruff format .
python -m ruff check .
python -m pytest
```

依赖发生变化时，先更新 `uv.lock`，再重新导出 pip 依赖：

```bash
uv export --format requirements.txt --all-groups --no-emit-project --no-hashes --frozen --no-header --output-file requirements.txt
```

保留 `requirements.txt` 顶部的说明注释，不要提交包含本机绝对路径的导出命令。

提交使用 Conventional Commits，并在提交前运行 `git diff --check`、Ruff 和 Pytest。完整维护约束见 `AGENTS.md`。

## V1.0 范围

V1.0 原生支持 `text`、`tspan`、`rect`、圆角矩形、`circle`、`ellipse`、`line`、`image` 和基础 `g` 样式/变换。复杂 `path`、渐变、裁剪或旋转元素通过 Office SVG 关系降级并记录在编译报告中；`filter`、`mask`、动画、PowerPoint 动画与任意 SVG 规范完整兼容不在 V1.0 范围内。

## Roadmap

- 扩展 polygon/polyline/freeform 支持
- 提升复杂路径与渐变的可编辑转换能力
- 扩展跨平台字体度量和文本基线校准
- 增加更多真实 presentation 类型的 Skill 前向测试
