# VectorDeckPPT Agent Skill — Codex Implementation Specification

**项目名称：** VectorDeckPPT  
**名称含义：** Vector + Presentation Deck + PowerPoint  
**项目类型：** Agent Skill / AI Presentation Generation / SVG-to-PPTX Toolchain  
**文档版本：** V0.3  
**项目状态：** Implementation Ready  

---

# 0. Codex 总指令

你需要实现的不是一个普通的“AI PPT Python 应用”。

你需要实现的是：

> **一个可被 AI Agent 调用的 PPT 生成 Skill。**

VectorDeckPPT 的核心产品是：

```text
SKILL.md
+
references/
+
scripts/
+
assets/
```

而不是：

```text
Python App
+
调用 OpenAI API
```

运行 VectorDeckPPT 的 ChatGPT、Codex 或其他兼容 Agent 本身已经具备：

- 内容理解能力；
- 内容规划能力；
- 推理能力；
- 文案能力；
- SVG 生成能力；
- 图片理解能力；
- 视觉审核能力。

因此不要在第一版重新实现：

```text
AIProvider
PresentationPlanner Python Service
SlidePlanner Python Service
ArtDirector Python Service
VisionModel Python Service
OpenAI API Wrapper
```

这些能力应该主要通过：

```text
SKILL.md
+
references/
```

指导宿主 AI 完成。

Python / CLI 脚本只负责需要**确定性执行**的部分：

```text
SVG 校验
SVG 渲染
SVG 分析
资源处理
SVG → PPTX
PPTX 校验
```

---

# 1. 最终产品定义

VectorDeckPPT 是一个：

> **面向 AI Agent 的高质量可编辑 PPT 生成 Skill。**

Skill 指导 AI 完成：

```text
用户需求理解
      ↓
资料阅读
      ↓
Presentation Planning
      ↓
Slide Planning
      ↓
Art Direction
      ↓
Design System
      ↓
逐页设计
      ↓
整页 SVG
      ↓
SVG 校验
      ↓
SVG → PNG Preview
      ↓
AI 视觉审核
      ↓
SVG 修改
      ↓
PPTX 编译
      ↓
PPTX 校验
      ↓
final.pptx
```

---

# 2. 核心架构原则

VectorDeckPPT 必须坚持以下架构：

```text
                    AI Agent
                       │
                       ↓
               VectorDeckPPT Skill
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
  Instructions     References        Assets
       │               │               │
       └───────────────┬───────────────┘
                       ↓
                  AI generates
                       ↓
                slide_xx.svg
                       │
                       ↓
              Deterministic Scripts
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Validate      Render       Compile
          ↓            ↓            ↓
         SVG          PNG          PPTX
                       │
                       ↓
                AI Visual Review
                       │
                       ↓
                   Revision
```

核心原则：

> **AI 负责设计，代码负责验证和执行。**

---

# 3. Skill 不应该自己调用 AI API

除非以后出现明确需求，否则第一版禁止实现：

```text
openai.OpenAI(...)
Anthropic(...)
Gemini(...)
AIProvider(...)
VisionProvider(...)
```

VectorDeckPPT 必须假设：

> 正在运行 Skill 的 Agent 本身就是 AI。

例如：

用户：

```text
帮我制作一个 15 页的 YOLO 焊缝缺陷检测答辩 PPT。
```

Agent 调用：

```text
VectorDeckPPT Skill
```

Skill 指导 Agent：

```text
分析资料
↓
规划内容
↓
设计页面
↓
生成 SVG
↓
调用脚本
↓
检查页面
↓
修改
↓
生成 PPTX
```

而不是：

```text
Agent
 ↓
Skill
 ↓
Python
 ↓
OpenAI API
 ↓
另一个 AI
```

避免这种重复架构。

---

# 4. Repository 结构

目标仓库：

```text
VectorDeckPPT/
│
├── .agents/
│   └── skills/
│       └── vectordeckppt/
│           │
│           ├── SKILL.md
│           │
│           ├── agents/
│           │   └── openai.yaml
│           │
│           ├── references/
│           │   ├── workflow.md
│           │   ├── presentation-planning.md
│           │   ├── design-system.md
│           │   ├── slide-design.md
│           │   ├── svg-authoring.md
│           │   ├── svg-to-pptx.md
│           │   ├── visual-review.md
│           │   └── troubleshooting.md
│           │
│           ├── scripts/
│           │   ├── validate_svg.py
│           │   ├── render_svg.py
│           │   ├── compile_pptx.py
│           │   ├── validate_pptx.py
│           │   └── lib/
│           │       ├── __init__.py
│           │       ├── svg_parser.py
│           │       ├── svg_models.py
│           │       ├── coordinates.py
│           │       ├── colors.py
│           │       ├── fonts.py
│           │       ├── pptx_text.py
│           │       ├── pptx_shapes.py
│           │       ├── pptx_images.py
│           │       └── pptx_utils.py
│           │
│           └── assets/
│               ├── examples/
│               ├── themes/
│               └── icons/
│
├── tests/
│   ├── fixtures/
│   │   ├── simple_text.svg
│   │   ├── simple_rect.svg
│   │   ├── simple_circle.svg
│   │   ├── simple_line.svg
│   │   ├── simple_image.svg
│   │   ├── mixed_slide.svg
│   │   ├── invalid_script.svg
│   │   └── invalid_foreign_object.svg
│   │
│   ├── test_svg_parser.py
│   ├── test_svg_validator.py
│   ├── test_svg_renderer.py
│   ├── test_coordinates.py
│   └── test_pptx_compiler.py
│
├── examples/
│   └── basic-deck/
│
├── docs/
│
├── output/
│
├── AGENTS.md
├── README.md
├── IMPLEMENTATION_SPEC.md
├── pyproject.toml
├── uv.lock
├── .gitignore
└── LICENSE
```

---

# 5. 如果仓库中存在参考 Skill

如果当前仓库中已经存在用户标注、指定或提供的参考 Skill：

> **必须先完整检查该 Skill。**

重点检查：

```text
目录结构
SKILL.md 写法
frontmatter
references 组织方式
scripts 接口
assets 组织方式
agents/openai.yaml
命名风格
脚本调用风格
```

VectorDeckPPT 应尽可能遵循参考 Skill 的成熟约定。

不要在没有查看参考 Skill 的情况下自行创造完全不同的 Skill 结构。

---

# 6. SKILL.md 是项目核心

以下文件：

```text
.agents/skills/vectordeckppt/SKILL.md
```

是整个项目最重要的文件。

它不是：

```text
README
```

也不是普通：

```text
prompt.txt
```

而应该是：

> AI 使用 VectorDeckPPT 制作 PPT 时必须遵守的操作规程。

---

# 7. SKILL.md Frontmatter

至少包含：

```yaml
---
name: vectordeckppt
description: >
  Create high-quality editable PowerPoint presentations using a
  vector-first workflow. Use this skill when the user asks to create,
  redesign, improve, generate, or export a presentation or PPT/PPTX.
  The skill plans the presentation, creates a shared design system,
  designs each slide as structured SVG, visually reviews rendered
  previews, and compiles supported SVG elements into editable
  PowerPoint objects.
---
```

Description 必须能够覆盖这些触发词：

```text
PPT
PPTX
PowerPoint
presentation
slides
slide deck
演示文稿
答辩 PPT
汇报 PPT
路演 PPT
生成幻灯片
重新设计 PPT
美化 PPT
```

---

# 8. Skill 的职责边界

VectorDeckPPT 应该在以下情况触发：

```text
制作新的 PPT
根据文档制作 PPT
根据 Markdown 制作 PPT
根据 PDF 制作 PPT
根据用户资料制作答辩 PPT
生成商业汇报
生成路演 Deck
重新设计已有 PPT
美化 PPT
制作可编辑 PPTX
```

以下任务不应作为主要触发场景：

```text
单纯解释 PowerPoint 功能
只询问 SVG 是什么
只要求生成普通图片
只要求写一段文案
只要求分析数据而不需要 presentation
```

---

# 9. SKILL.md 的核心工作流

SKILL.md 必须要求 Agent 遵循以下工作流。

---

## Phase 1 — Understand

分析：

```text
presentation purpose
audience
language
slide count
source materials
presentation type
visual preference
required assets
```

如果用户已经给出信息，不重复询问。

如果部分信息缺失，但能够合理推断：

> 直接采用合理默认值继续执行。

避免因为非关键缺失信息阻塞任务。

---

# 10. Phase 2 — Read Source Materials

如果用户提供：

```text
PDF
DOCX
Markdown
TXT
图片
截图
表格
其他资料
```

Agent 必须先阅读和理解资料。

不得：

```text
没看资料
 ↓
直接开始写 PPT
```

需要提取：

```text
核心主题
核心结论
重要数字
重要图表
关键证据
图片素材
叙事结构
```

---

# 11. Phase 3 — Presentation Plan

先规划整套 PPT。

生成逻辑上的：

```text
Presentation Plan
```

至少确定：

```text
Title
Audience
Purpose
Language
Slide Count
Storyline
Sections
Each Slide Purpose
```

例如：

```text
01 封面
02 项目背景
03 当前痛点
04 项目目标
05 系统架构
06 数据集
07 模型设计
08 训练过程
09 实验结果
10 系统实现
11 系统展示
12 创新点
13 总结
14 展望
15 致谢
```

---

# 12. Phase 4 — Art Direction

在制作任何页面之前，必须先定义整个 Deck 的视觉方向。

例如：

```text
Style:
Minimal Technology

Background:
White

Primary:
Blue

Secondary:
Purple

Mood:
Professional / Clean / Technical

Typography:
Modern Sans Serif

Composition:
Large whitespace

Shape language:
Rounded cards

Decorations:
Subtle geometric vector elements
```

---

# 13. Phase 5 — Design System

整套 PPT 必须共享一个 Design System。

默认结构：

```json
{
  "canvas": {
    "width": 1600,
    "height": 900
  },

  "colors": {
    "background": "#F8FAFC",
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "title": "#0F172A",
    "text": "#475569",
    "muted": "#94A3B8",
    "border": "#E2E8F0"
  },

  "typography": {
    "font_family": "Microsoft YaHei",
    "title": 54,
    "subtitle": 28,
    "heading": 32,
    "body": 21,
    "caption": 16
  },

  "spacing": {
    "grid": 8,
    "page_margin_x": 96,
    "page_margin_y": 72
  },

  "shape": {
    "card_radius": 24
  }
}
```

Agent 不要求每次真的创建 JSON 文件。

但必须在逻辑上维护同一套 Design System。

---

# 14. Design System 约束

同一套 PPT 禁止出现：

```text
Slide 1: 蓝色科技风
Slide 2: 绿色商务风
Slide 3: 黑金风
Slide 4: 卡通风
```

需要保持：

```text
字体一致
主色一致
辅助色一致
卡片语言一致
阴影语言一致
边距一致
视觉密度一致
标题层级一致
```

---

# 15. Phase 6 — Slide Planning

每页开始设计之前，要确定：

```text
slide purpose
key message
content hierarchy
visual structure
required assets
```

例如：

```json
{
  "slide": 5,
  "title": "系统整体架构",
  "purpose": "解释系统整体组成",
  "key_message": "系统由数据层、AI 模型层和应用层组成",
  "visual_type": "architecture"
}
```

---

# 16. 一页 SVG = 一页 PPT

VectorDeckPPT 的核心原则：

> **One SVG = One Slide**

例如：

```text
slide_01.svg
slide_02.svg
slide_03.svg
...
slide_15.svg
```

对应：

```text
PPT Slide 1
PPT Slide 2
PPT Slide 3
...
PPT Slide 15
```

---

# 17. SVG 画布

默认：

```text
1600 × 900
```

比例：

```text
16:9
```

必须使用：

```svg
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="1600"
    height="900"
    viewBox="0 0 1600 900">
```

除非用户明确要求其他比例。

---

# 18. SVG 是页面视觉 Source of Truth

一张 SVG 中应该包含完整页面：

```text
背景
标题
副标题
正文
卡片
流程图
图标
数据可视化
图片位置
装饰元素
页码
```

因此：

```text
SVG = 完整 Slide Design
```

而不是：

```text
SVG = PPT 中的一个小图标
```

---

# 19. SVG 推荐元素

AI 优先使用：

```text
<svg>
<g>
<text>
<tspan>
<rect>
<circle>
<ellipse>
<line>
<polyline>
<polygon>
<path>
<image>
```

---

# 20. SVG 禁止或限制元素

默认禁止：

```text
<script>
<foreignObject>
SVG animation
CSS animation
JavaScript
remote JavaScript
remote fonts
interactive elements
complex browser-only CSS
```

复杂 filter、mask、clipPath 等高级能力：

> 第一版谨慎使用。

如果存在无法可靠转换 PPTX 的效果，应：

```text
简化 SVG
```

而不是依赖无法转换的特性。

---

# 21. 中文文字要求

中文必须尽可能保持：

```svg
<text>
人工智能发展趋势
</text>
```

不要默认：

```text
Text → Path
```

因为最终要求：

```text
SVG <text>
 ↓
PowerPoint TextBox
```

从而保持：

```text
可编辑
可复制
可搜索
```

---

# 22. 字体策略

默认中文字体栈：

```text
Microsoft YaHei
PingFang SC
Noto Sans CJK SC
sans-serif
```

SVG 中应尽量提供 fallback。

例如：

```svg
font-family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif"
```

---

# 23. 图片策略

以下内容不要求矢量化：

```text
人物照片
产品照片
软件截图
实验截图
复杂 AI 插画
复杂背景照片
```

这些使用：

```text
PNG
JPEG
WebP
```

并通过：

```svg
<image>
```

插入 SVG。

---

# 24. 图片不得变形

插入图片时必须保持原始比例。

禁止：

```text
强行拉伸宽度
+
强行拉伸高度
```

导致画面变形。

需要使用：

```text
contain
cover
crop
```

等合理策略。

---

# 25. Phase 7 — SVG Validation

每生成一页 SVG：

> 必须进行校验。

调用：

```bash
uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py slide_01.svg
```

Validator 至少检查：

```text
XML 是否合法
root 是否为 svg
viewBox 是否存在
canvas 是否正确
是否包含 script
是否包含 foreignObject
是否使用远程资源
image 路径是否存在
非法元素
明显越界元素
明显异常尺寸
```

---

# 26. validate_svg.py CLI

目标接口：

```bash
uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py slide.svg
```

支持：

```bash
--json
```

例如：

```bash
uv run python .agents/skills/vectordeckppt/scripts/validate_svg.py slide.svg --json
```

输出：

```json
{
  "valid": true,
  "errors": [],
  "warnings": []
}
```

失败时返回非零 exit code。

---

# 27. Phase 8 — Render Preview

SVG 校验通过后：

```bash
uv run python .agents/skills/vectordeckppt/scripts/render_svg.py slide_01.svg
```

生成：

```text
slide_01.png
```

默认输出：

```text
1600 × 900
```

---

# 28. render_svg.py CLI

支持：

```bash
render_svg.py input.svg
```

和：

```bash
render_svg.py input.svg --output preview.png
```

支持批量：

```bash
render_svg.py slides/ --output-dir preview/
```

---

# 29. Phase 9 — AI Visual Review

这一阶段不要再次调用其他 AI API。

宿主 Agent 应直接查看：

```text
slide_01.png
```

然后检查视觉质量。

---

# 30. Visual Review Checklist

必须检查：

```text
□ 是否存在文字溢出

□ 是否存在元素重叠

□ 是否存在元素越界

□ 是否存在过小文字

□ 标题是否具有足够视觉层级

□ 正文是否过多

□ 是否存在大面积无意义空白

□ 是否缺少必要留白

□ 图片是否变形

□ 图片是否质量过低

□ 元素是否对齐

□ 卡片间距是否一致

□ 页面是否符合 Design System

□ 页面视觉重心是否平衡

□ 页面是否过度装饰

□ 页面是否过于模板化

□ 信息表达是否清楚
```

---

# 31. 不允许“只要不溢出就算成功”

Visual Review 不只是：

```text
没有 overflow
=
Pass
```

还需要判断：

```text
是否高级
是否清晰
是否舒服
是否符合叙事
是否有视觉层级
是否存在设计感
```

---

# 32. Revision Loop

如果视觉效果不够好：

```text
修改 SVG
 ↓
Validate
 ↓
Render
 ↓
Visual Review
```

重复。

推荐最大自动修改次数：

```text
3
```

但这是指导值，不需要硬编码进 Skill。

---

# 33. 不要保存无限版本

开发 Debug 时可以保存：

```text
slide_03.v1.svg
slide_03.v2.svg
```

最终输出应该保持整洁：

```text
slide_03.svg
```

---

# 34. Phase 10 — PPTX Compilation

所有 slides 完成后：

调用：

```bash
uv run python .agents/skills/vectordeckppt/scripts/compile_pptx.py slides/ --output final.pptx
```

---

# 35. PPTX Compiler 核心原则

禁止默认：

```text
SVG
 ↓
PNG
 ↓
整页图片
 ↓
PPT
```

目标是：

```text
SVG
 ↓
Parser
 ↓
PowerPoint Native Objects
```

---

# 36. SVG → PPTX 映射

## Level 1 — 必须首先支持

### text

```text
SVG <text>
 ↓
PowerPoint TextBox
```

### rect

```text
SVG <rect>
 ↓
PowerPoint Rectangle
```

### rounded rect

```text
SVG <rect rx="">
 ↓
PowerPoint Rounded Rectangle
```

### circle

```text
SVG <circle>
 ↓
PowerPoint Oval
```

### ellipse

```text
SVG <ellipse>
 ↓
PowerPoint Oval
```

### line

```text
SVG <line>
 ↓
PowerPoint Line
```

### image

```text
SVG <image>
 ↓
PowerPoint Picture
```

---

# 37. Level 2 — 后续支持

```text
polygon
polyline
simple path
```

尽可能转换成：

```text
PowerPoint Freeform
```

---

# 38. Level 3 — Fallback

遇到复杂：

```text
path
filter
compound vector graphic
```

如果无法可靠转为 PowerPoint 原生对象：

```text
保留为 SVG Asset
```

插入 PPT。

优先级：

```text
Native PowerPoint
      ↓
Freeform
      ↓
Embedded SVG
```

---

# 39. 不允许静默丢失元素

如果某个 SVG 元素无法转换：

禁止：

```text
直接忽略
```

必须：

```text
转换
或
Fallback
或
明确报错
```

最终 compilation report 应记录：

```json
{
  "native": 21,
  "freeform": 3,
  "embedded_svg": 1,
  "failed": 0
}
```

---

# 40. 坐标系统

SVG：

```text
1600 × 900
```

PPT：

```text
13.333 × 7.5 inch
```

转换：

```text
x_ppt = x_svg / 1600 × 13.333
y_ppt = y_svg / 900 × 7.5
```

所有坐标转换必须集中在：

```text
scripts/lib/coordinates.py
```

禁止多个文件重复实现换算公式。

---

# 41. SVG Group

Compiler 需要正确处理：

```svg
<g>
```

至少考虑：

```text
group translation
parent styles
opacity inheritance
```

第一版可以限制复杂 transform。

但不能完全忽略 `<g>`。

---

# 42. Text Compiler

SVG Text → PPT TextBox 是项目核心。

第一阶段至少处理：

```text
x
y
font-size
font-family
font-weight
fill
text-anchor
opacity
```

以及：

```text
<tspan>
```

基础支持。

---

# 43. Text Anchor

需要正确处理：

```text
start
middle
end
```

例如 SVG：

```svg
text-anchor="middle"
```

不能简单把：

```text
x
```

当成文本框左边界。

---

# 44. Text Position Difference

必须注意：

> SVG text 的 y 通常描述 baseline，而 PPT TextBox 的 y 通常描述文本框顶部。

因此：

```text
SVG text
→
PPT TextBox
```

不能只做简单坐标复制。

需要专门的文字位置转换策略。

---

# 45. Shape Style

至少支持：

```text
fill
stroke
stroke-width
opacity
```

以及：

```text
rx / ry
```

基础圆角。

---

# 46. Images

SVG：

```svg
<image href="assets/demo.png">
```

转换：

```text
PowerPoint Picture
```

必须：

```text
检查路径
保持比例
支持相对路径
```

---

# 47. SVG Renderer

选择可靠 SVG renderer。

推荐 Codex 调研后选择：

```text
CairoSVG
resvg
librsvg
```

第一阶段选择一种即可。

目标优先级：

```text
稳定
跨平台
中文支持
易安装
```

---

# 48. PPTX 库

第一阶段优先选择成熟的 PowerPoint Python 库。

核心需求：

```text
创建 slide
创建 textbox
创建 shape
添加 image
控制 fill
控制 stroke
控制 font
```

不要手写完整 PPTX Open XML，除非某些高级能力确实需要。

---

# 49. Phase 11 — PPTX Validation

生成：

```text
final.pptx
```

后必须运行：

```bash
uv run python .agents/skills/vectordeckppt/scripts/validate_pptx.py final.pptx
```

---

# 50. validate_pptx.py

至少检查：

```text
文件是否存在
ZIP/PPTX 是否完整
presentation.xml 是否存在
slide 数量
media 引用
关系文件
明显损坏
```

输出：

```json
{
  "valid": true,
  "slides": 15,
  "errors": [],
  "warnings": []
}
```

---

# 51. 最终 Skill Workflow

最终 SKILL.md 应让 AI 基本按照：

```text
1. Understand request

2. Read all relevant source material

3. Create presentation storyline

4. Create slide plan

5. Define art direction

6. Define shared design system

7. Design slide 1 as SVG

8. Validate SVG

9. Render SVG

10. Inspect rendered image

11. Revise if needed

12. Repeat for all slides

13. Compile all SVG slides to PPTX

14. Validate PPTX

15. Deliver final PPTX
```

---

# 52. references/workflow.md

详细说明：

```text
VectorDeckPPT 完整制作流程
每个阶段输入
每个阶段输出
什么时候调用脚本
失败以后如何恢复
```

---

# 53. references/presentation-planning.md

告诉 AI 如何规划不同 PPT：

```text
毕业答辩
商业汇报
产品发布
销售 Pitch
教学课件
技术分享
项目汇报
研究报告
```

强调：

```text
不是平均分配页面
而是围绕 narrative 构建 presentation
```

---

# 54. references/design-system.md

定义：

```text
颜色
字体
字号
留白
Grid
圆角
边框
阴影
图片风格
图标风格
```

默认：

```text
8px Grid
```

推荐间距：

```text
8
16
24
32
40
48
64
80
96
```

---

# 55. references/slide-design.md

告诉 AI：

```text
如何设计封面
如何做两栏布局
如何做架构图
如何做流程图
如何做时间线
如何做数据页
如何做总结页
```

这里提供：

```text
设计规则
```

而不是：

```text
大量固定模板
```

避免 VectorDeckPPT 退化成模板系统。

---

# 56. references/svg-authoring.md

详细定义允许的 SVG 子集。

包含：

```text
尺寸
字体
图片
Shape
Path
Group
坐标
颜色
Grid
禁止特性
```

这个文件必须足够明确，使 AI 生成 SVG 时天然适合 PPTX Compiler。

---

# 57. references/svg-to-pptx.md

记录：

```text
SVG Element
→
PowerPoint Element
```

映射规则。

同时记录：

```text
已支持
部分支持
不支持
Fallback
```

必须随着 compiler 开发持续更新。

---

# 58. references/visual-review.md

定义 AI 看 Preview 时的检查标准。

至少包括：

```text
Layout
Typography
Spacing
Alignment
Hierarchy
Contrast
Balance
Consistency
Density
Image Quality
Overflow
```

---

# 59. references/troubleshooting.md

记录常见问题：

```text
SVG 无法渲染
字体偏移
中文字体缺失
PPT 文字偏移
图片路径错误
PPTX 无法打开
复杂 Path 无法转换
```

以及解决策略。

---

# 60. assets/

assets 不应成为固定 PPT 模板仓库。

主要存放：

```text
Skill 图标
示例 SVG
通用图标
少量主题参考
测试素材
```

Skill 核心仍然是：

```text
AI 动态设计
```

而不是：

```text
从 30 个模板里选一个
```

---

# 61. agents/openai.yaml

创建：

```text
agents/openai.yaml
```

至少定义：

```yaml
interface:
  display_name: "VectorDeckPPT"
  short_description: "Create editable vector-first PowerPoint presentations"
```

可以增加：

```text
icon
brand color
default prompt
```

但第一版不是重点。

---

# 62. AGENTS.md

仓库根目录必须建立：

```text
AGENTS.md
```

该文件专门告诉 Codex：

```text
如何维护这个仓库
如何测试
如何提交 Git
有哪些架构原则不能破坏
```

不要把开发规范全部塞进：

```text
SKILL.md
```

因为：

```text
SKILL.md
```

是给使用 Skill 的 AI。

而：

```text
AGENTS.md
```

是给开发 VectorDeckPPT 的 Codex。

---

# 63. AGENTS.md 必须包含的核心原则

至少：

```text
- VectorDeckPPT is an Agent Skill, not an AI API application.

- Do not introduce AI provider SDKs unless explicitly required.

- SKILL.md and references define AI behavior.

- scripts/ contain deterministic utilities only.

- One SVG represents one slide.

- SVG is the visual source of truth.

- Preserve editability when compiling PPTX.

- Do not silently drop unsupported SVG elements.

- Keep the SVG subset intentionally constrained.

- Use uv for dependency management.

- Run lint and tests before every commit.

- Manage Git incrementally with Conventional Commits.

- Preserve unrelated user changes.
```

---

# 64. Python 项目管理

使用：

```text
uv
```

需要：

```text
pyproject.toml
uv.lock
```

基本流程：

```bash
uv sync
```

运行：

```bash
uv run python ...
```

测试：

```bash
uv run pytest
```

Lint：

```bash
uv run ruff check .
```

格式化：

```bash
uv run ruff format .
```

---

# 65. 推荐依赖

Codex 根据实际实现选择最终依赖。

预计需要：

```text
python-pptx
lxml
Pillow
CairoSVG 或其他 renderer
pytest
ruff
```

不要为了未来功能提前加入大量依赖。

---

# 66. 测试要求

使用：

```text
pytest
```

必须测试：

```text
SVG XML parsing
SVG validation
unsupported tags
coordinate conversion
text parsing
rect parsing
circle parsing
line parsing
image path resolution
SVG rendering
PPTX generation
multi-slide generation
```

---

# 67. Integration Test

至少准备一个：

```text
mixed_slide.svg
```

包含：

```text
背景
标题
正文
rect
circle
line
image
```

编译：

```text
mixed_slide.svg
 ↓
test.pptx
```

测试至少确认：

```text
PPTX 可以读取
slide count 正确
元素存在
```

---

# 68. Example Deck

建立：

```text
examples/basic-deck/
```

包含至少：

```text
slide_01.svg
slide_02.svg
slide_03.svg
```

展示：

```text
封面
内容页
流程页
```

并能够：

```text
compile
 ↓
example.pptx
```

---

# 69. Skill 验收测试

除了代码测试，还要验证 Skill 本身。

准备测试 Prompt：

### Case 1

```text
帮我做一个关于人工智能发展趋势的 8 页科技风 PPT。
```

### Case 2

```text
根据这个 Markdown 做一个毕业答辩 PPT。
```

### Case 3

```text
帮我把这个 PPT 重新设计得更高级。
```

### Case 4

```text
制作一个商业路演 Pitch Deck。
```

检查 Skill 是否能够：

```text
正确触发
正确读取资料
建立 Design System
生成整页 SVG
调用 scripts
执行视觉审核
输出 PPTX
```

---

# 70. MVP 定义

MVP 不要求实现全部高级能力。

第一版必须打通：

```text
AI / Agent
 ↓
SKILL.md
 ↓
Slide Planning
 ↓
Design System
 ↓
SVG
 ↓
validate_svg.py
 ↓
render_svg.py
 ↓
AI Visual Review
 ↓
compile_pptx.py
 ↓
validate_pptx.py
 ↓
Editable PPTX
```

---

# 71. MVP Compiler 支持范围

MVP 必须支持：

```text
text
rect
rounded rect
circle
ellipse
line
image
group basics
```

暂不要求完美：

```text
复杂 path
复杂 mask
复杂 clip
高级 gradient
SVG filter
PowerPoint chart
PowerPoint animation
PowerPoint transition
```

---

# 72. MVP 成功标准

至少实现：

```text
5 页 PPT
```

要求：

```text
□ 5 个完整 SVG

□ 所有 SVG 均为 1600×900

□ SVG 可以正常渲染

□ 中文正常显示

□ 页面视觉风格统一

□ PPTX 可以正常打开

□ PPT 页面为 16:9

□ SVG text 转为 PPT TextBox

□ 基础 Shape 可编辑

□ 图片正常显示

□ 没有静默元素丢失

□ tests pass

□ ruff pass

□ Git 历史规范
```

---

# 73. 开发阶段

## Milestone 1 — Skill Skeleton

完成：

```text
.agents/skills/vectordeckppt/
SKILL.md
references/
scripts/
assets/
agents/openai.yaml
AGENTS.md
README.md
pyproject.toml
tests/
```

提交：

```text
chore(skill): initialize VectorDeckPPT skill structure
```

---

# 74. Milestone 2 — SVG Validator

完成：

```text
SVG parser
SVG validator
CLI
tests
```

提交建议：

```text
feat(svg): add SVG parser and validation
test(svg): add SVG validation fixtures
```

---

# 75. Milestone 3 — SVG Renderer

完成：

```text
SVG → PNG
single render
batch render
tests
```

提交：

```text
feat(renderer): add SVG preview rendering
```

---

# 76. Milestone 4 — Coordinate System

完成：

```text
SVG → PPT coordinates
inch conversion
EMU conversion
tests
```

提交：

```text
feat(compiler): add SVG to PowerPoint coordinate mapping
```

---

# 77. Milestone 5 — Basic PPTX Compiler

实现：

```text
text
rect
circle
ellipse
line
image
```

不要一次一个巨大 commit。

例如：

```text
feat(compiler): add SVG text conversion
feat(compiler): add basic shape conversion
feat(compiler): add SVG image conversion
```

---

# 78. Milestone 6 — Multi-Slide Deck

实现：

```text
slides/
 ↓
final.pptx
```

提交：

```text
feat(pptx): compile multiple SVG slides into one deck
```

---

# 79. Milestone 7 — Skill Instructions

完善：

```text
SKILL.md
workflow.md
design-system.md
slide-design.md
svg-authoring.md
visual-review.md
svg-to-pptx.md
```

提交：

```text
docs(skill): define VectorDeckPPT generation workflow
```

注意：

> 虽然 SKILL.md 一开始就存在，但应随着确定性工具链实际能力同步修正。

不要让 Skill 指导 AI 使用尚不存在的功能。

---

# 80. Milestone 8 — End-to-End Example

完成：

```text
Prompt
 ↓
3–5 SVG
 ↓
Preview
 ↓
PPTX
```

提交：

```text
test(skill): add end-to-end VectorDeckPPT example
```

---

# 81. Git 由 Codex 自动管理

Codex 必须主动管理 Git。

在开发过程中：

```text
检查 Git 状态
 ↓
完成一个逻辑单元
 ↓
测试
 ↓
Lint
 ↓
检查 diff
 ↓
commit
 ↓
继续开发
```

不要等项目全部完成后只提交一次。

---

# 82. Git 初始化

如果仓库没有 Git：

```bash
git init
```

如果已经存在：

> 使用现有仓库。

不得重新初始化或破坏已有历史。

---

# 83. 每次工作前

执行：

```bash
git status
```

检查：

```text
用户是否有未提交改动
是否存在不相关文件
当前 branch
```

---

# 84. 禁止覆盖用户修改

如果发现已有修改：

```text
保留
```

不得随意：

```bash
git reset --hard
git checkout -- .
git clean -fd
```

不得把用户已有内容覆盖掉。

---

# 85. Commit Convention

所有提交采用：

> Conventional Commits

格式：

```text
<type>(<scope>): <summary>
```

尽量多的提交 提交内容要详细  使用中文

---

# 86. Commit Types

允许：

```text
feat
fix
refactor
test
docs
chore
build
ci
perf
style
```

---

# 87. 推荐 Scope

```text
skill
svg
renderer
compiler
pptx
text
shape
image
assets
tests
docs
project
```

---

# 88. Commit Examples

正确：

```text
chore(skill): initialize VectorDeckPPT structure
```

```text
feat(svg): add SVG validation
```

```text
feat(renderer): add SVG preview rendering
```

```text
feat(compiler): convert SVG text to PowerPoint textboxes
```

```text
feat(compiler): add editable shape conversion
```

```text
feat(pptx): support multi-slide deck compilation
```

```text
test(compiler): add SVG to PPTX integration tests
```

```text
docs(skill): document visual review workflow
```

---

# 89. 禁止的 Commit

不要：

```text
update
```

```text
fix
```

```text
final
```

```text
update files
```

```text
working
```

```text
完成
```

---

# 90. Commit 语言

Git commit message：

```text
使用英文
```

summary：

```text
简短
清晰
描述实际变化
```

不要以：

```text
.
```

结尾。

---

# 91. Commit 前必须运行

至少：

```bash
git diff --check
uv run ruff check .
uv run pytest
```

如果使用 formatter：

```bash
uv run ruff format .
```

然后重新检查：

```bash
git diff
git status
```

再提交。

---

# 92. Git 提交粒度

一个 commit 只完成一个逻辑目的。

例如不要：

```text
SVG validator
+
README rewrite
+
PPT compiler
+
rename project
```

全部放一个 commit。

---

# 93. Branch

如果当前已经在合适的开发 branch：

> 继续使用。

如果需要创建：

```text
feat/vectordeckppt-skill
```

不要随意创建大量 branch。

---

# 94. Push

Codex 可以自动：

```text
stage
commit
```

但没有用户明确要求时：

> 不主动 force push。

如果仓库 remote 已配置，也不要因为实现工作本身就假定必须推送远端。

---

# 95. .gitignore

至少：

```gitignore
.venv/
__pycache__/
*.pyc

.pytest_cache/
.ruff_cache/
.mypy_cache/

.env
.env.*

!.env.example

output/

dist/
build/

.DS_Store
Thumbs.db
```

示例资源和测试 fixture 不应被忽略。

---

# 96. README

README 面向人类开发者。

至少包含：

```text
VectorDeckPPT 是什么
为什么是 Agent Skill
核心架构
目录结构
安装
uv sync
如何安装/发现 Skill
如何调用 Skill
scripts 用法
测试
开发
Git 约定
Roadmap
```

---

# 97. SKILL.md 与 README 不要重复

README：

```text
给开发者
```

SKILL.md：

```text
给 AI Agent
```

AGENTS.md：

```text
给 Codex 开发代理
```

references：

```text
给使用 Skill 的 AI 提供深入规则
```

职责必须分清。

---

# 98. 项目最重要的三个文件

第一：

```text
SKILL.md
```

定义 AI 如何制作 PPT。

第二：

```text
svg-authoring.md
```

决定 AI 是否能生成适合编译的 SVG。

第三：

```text
compile_pptx.py
```

决定最终 PPT 是否真正可编辑。

---

# 99. 项目的真正技术难点

Codex 开发时重点关注：

```text
SVG Text → PPT TextBox
```

因为需要处理：

```text
baseline
font metrics
line height
text anchor
font fallback
Chinese text
```

其次是：

```text
SVG transforms
```

以及：

```text
Path → PowerPoint
```

不要把主要精力花在重新实现 AI planning API。

---

# 100. 核心非目标

第一版不要追求：

```text
完整实现 SVG Specification
复杂 SVG Filters
SVG animation
PowerPoint animation
PowerPoint transition
任意 HTML → PPT
所有图表完全原生化
完美跨字体像素一致
完整 PDF parser
完整 DOCX parser
AI API provider abstraction
Web UI
SaaS
数据库
用户系统
```

第一版目标：

> 把 Agent Skill + SVG → editable PPTX 这条路线证明可行。

---

# 101. Codex 自主权

Codex 被允许：

```text
创建文件
修改项目文件
初始化 uv
添加合理依赖
运行命令
运行测试
运行 lint
初始化 Git
创建合理 branch
stage 文件
创建 commits
调整内部实现
增加测试
增加 references
完善 SKILL.md
```

---

# 102. Codex 不需要逐步询问用户

对于正常工程决策，例如：

```text
模块怎么拆
函数怎么命名
测试文件怎么组织
使用 lxml 还是 ElementTree
使用哪一个 SVG renderer
```

应该：

> 自主做合理决定。

只有真正阻塞项目且无法安全推断的事项才需要用户参与。

---

# 103. 但是核心架构不得自行修改

不得把：

```text
Agent Skill
+
SVG
+
PPTX Compiler
```

改成：

```text
普通 AI API Web App
```

不得把：

```text
SVG
 ↓
PPT native objects
```

改成默认：

```text
SVG
 ↓
Screenshot
 ↓
PPT background
```

除非作为明确 fallback。

---

# 104. Definition of Done

VectorDeckPPT MVP 完成必须同时满足：

### Skill

```text
SKILL.md 可用
references 完整
Skill 能正确指导 PPT 工作流
```

### SVG

```text
完整 Slide SVG
1600×900
可校验
可渲染
```

### PPTX

```text
可编译
可打开
文字可编辑
基础 Shape 可编辑
图片正确
多页正确
```

### Quality

```text
pytest pass
ruff pass
example pass
```

### Git

```text
历史清晰
Conventional Commits
没有巨大 final commit
没有提交临时 output
```

---

# 105. Codex 开始执行时的顺序

收到本文档以后直接开始工作。

第一步：

```text
读取整个仓库
```

第二步：

```text
查找用户指定/标注的参考 Skill
```

第三步：

```text
读取现有 AGENTS.md
```

第四步：

```text
git status
```

第五步：

```text
建立 VectorDeckPPT Skill skeleton
```

然后按照：

```text
Skill Skeleton
 ↓
SVG Validator
 ↓
SVG Renderer
 ↓
Coordinate System
 ↓
Basic PPTX Compiler
 ↓
Multi-slide Compiler
 ↓
Skill Documentation
 ↓
End-to-End Test
```

执行。

---

# 106. 第一阶段建议 Git 历史

最终类似：

```text
chore(skill): initialize VectorDeckPPT skill structure

docs(skill): add initial VectorDeckPPT workflow

feat(svg): add SVG parser and validation

test(svg): add SVG validation fixtures

feat(renderer): add SVG preview renderer

feat(compiler): add coordinate conversion

feat(compiler): convert SVG text to PowerPoint textboxes

feat(compiler): convert basic SVG shapes

feat(compiler): convert SVG images

feat(pptx): support multi-slide deck compilation

test(compiler): add PPTX integration coverage

docs(skill): document SVG authoring and visual review

test(skill): add end-to-end example deck
```

具体 commits 根据实际开发内容调整。

不要为了匹配这个列表制造无意义提交。

---

# 107. 最终一句话定位

> **VectorDeckPPT is an Agent Skill for creating high-quality editable PowerPoint presentations through a vector-first workflow: AI plans and designs each slide as structured SVG, deterministic tools validate and render the SVG, the Agent visually reviews the result, and the SVG is compiled into editable PowerPoint objects.**

中文：

> **VectorDeckPPT 是一个面向 AI Agent 的可编辑 PPT 生成 Skill，通过标准化工作流指导 AI 完成内容规划、视觉设计、整页 SVG 生成与视觉审核，并利用确定性的 SVG → PPTX 工具链生成高质量、风格统一且可编辑的 PowerPoint 文件。**

---

# 108. 最终执行指令

Codex：

请完整阅读本规范，然后直接实现 VectorDeckPPT。

不要只生成项目骨架或概念代码。

按照 Milestone 持续实现真正可运行的功能。

每完成一个独立逻辑单元：

```text
实现
 ↓
测试
 ↓
Lint
 ↓
检查 Git Diff
 ↓
规范 Commit
```

持续推进，直到 MVP 的 Agent Skill、SVG 工具链、PPTX Compiler、测试和示例全部打通。

最重要的优先级依次是：

```text
Agent Skill correctness
      ↓
SVG authoring reliability
      ↓
SVG validation
      ↓
SVG rendering
      ↓
Editable PPTX compilation
      ↓
Visual consistency
      ↓
Advanced SVG support
```

**不要把 VectorDeckPPT 实现成一个需要自己调用 AI API 的普通应用。**

VectorDeckPPT 本身就是给 AI 使用的 Skill。