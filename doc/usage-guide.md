# VectorDeckPPT 使用指南

本指南面向使用 Skill 生成、修改和验收演示文稿的人。首次体验可以先看根目录 [60 秒快速开始](../README.md#quick-start)；需要编写完整请求时配合 [提示词示例](prompt-examples.md) 使用。

## 1. 选择使用方式

### 在仓库中直接使用

克隆并在 Codex 中打开本仓库。项目内的 `.agents/skills/vectordeckppt/` 会提供 Skill、脚本、参考规则和视觉方向素材。

推荐使用 uv 安装环境：

```bash
uv sync
```

也可以使用标准 pip：

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 在其他项目中全局使用

把整个 `.agents/skills/vectordeckppt/` 目录复制或链接到 `$CODEX_HOME/skills/vectordeckppt/`；未设置 `CODEX_HOME` 时通常是 `~/.codex/skills/vectordeckppt/`。不要只复制 `SKILL.md`，因为 `references/`、`scripts/` 和 `assets/` 都参与工作流。

全局 Skill 不会自动创建 Python 环境。请在运行脚本的环境中安装本仓库 `requirements.txt` 的依赖，或使用已完成 `uv sync` 的仓库环境。

## 2. 写清请求合同

正式开始前，Skill 会补齐并汇总完整请求合同。不会改变方向的缺省项可以由 Skill 提议，但也必须列入合同并由用户明确确认，不能静默采用。

| 输入 | 建议写法 | 为什么重要 |
|---|---|---|
| 资料 | 附件、Markdown、PDF、DOCX、表格或本地路径 | 决定事实和证据边界 |
| 主要受众 | 身份、知识水平、决策权 | 决定解释深度和措辞 |
| 目标 | 演示结束后希望受众理解、相信或批准什么 | 决定叙事路径 |
| 场景 | 汇报、答辩、路演、发布、培训或评审 | 决定节奏与正式程度 |
| 页数、语言与时长 | 例如“10 页中文，15 分钟” | 约束内容取舍与密度 |
| 视觉方向 | 性格、品牌约束、禁止项或内置方向名称 | 约束设计系统 |
| 必须保留内容 | 数字、结论、引用、品牌资产 | 防止错误删减 |
| 事实边界 | 哪些内容不能改、哪些未知必须标注 | 防止推断变成事实 |
| 编辑与交付 | 可编辑程度、PPTX/SVG/PNG/报告 | 明确验收范围 |
| 输出位置 | 默认当前目录的 `pptoutput/` | 保持交付物集中 |

Skill 会用少量分组问题补齐缺失信息，再提交一份简明合同摘要。只有用户明确确认受众、目标、场景、资料、事实边界、页数、语言、视觉方向、品牌约束、交付物和默认项后，才开始资料综合与逐页规划。后续发现实质矛盾时会返回该确认门。

## 3. 理解三道确认门

完整生产不是一次性黑盒生成，而是三次明确确认：

1. **需求合同确认**：确认完整输入、拟采用的默认项和正式程度；在此之前不开始资料综合、文字稿或视觉制作。
2. **文字内容审批**：检查整套逐页标题、核心信息、证据、视觉计划和叙事顺序。此阶段不会生成 SVG、PNG 或 PPTX。
3. **视觉样稿审批**：文字批准后，只生成最多 3 页有代表性的 SVG 与 PNG。确认字体、色彩、构图、密度和视觉性格后，才制作全套。

如果文字内容发生实质修改，受影响的视觉样稿需要重新确认。沉默不视为批准。

## 4. 质量合同

### 内容丰富但不堆砌

普通内容页默认包含明确结论、必要解释、具体证据或例子，以及影响或下一步。在资料允许时，约三分之二的核心内容页使用真正承担说明作用的图表、图解、表格、流程、矩阵或标注图。

没有可靠数字时使用诚实的概念结构，不虚构百分比、坐标轴、趋势或比较。内容放不下时优先拆页，不通过缩小字号制造“丰富”。

### 字体角色精确一致

设计样稿前先锁定字体角色表。所有普通页面标题共享同一个精确字号、字体、字重和行高；同一页中承担相同层级的标题、标签或数字使用同一个 token。

文字溢出时应改写、换行、扩大区域或调整构图，不单独缩小一个标题。每个可见 SVG `<text>` 都要有语义 `data-role`，全套页面在编译前必须通过严格字体审计。

### 艺术感不等于失去专业度

Skill 不应把所有页面都做成横平竖直、等宽等高的卡片。可以用编辑式不对称、英雄字体、受控叠压、裁切、斜切、弧线、超大数字、前后景层次和少量越过栅格的焦点建立视觉张力。

专业、技术、高管、学术、金融、法律、医疗或审计场合仍默认克制、可信和证据优先，但可保留高级的非对称构图。完整漫画、海报、游戏或强烈活动风格属于可选方向，只有用户在需求合同中明确批准后才使用。

## 5. 交付目录

默认输出结构如下：

```text
pptoutput/
├── slide-content.md
├── sample/
│   ├── slides/
│   └── preview/
├── slides/
├── assets/
├── preview/
├── compilation-report.json
└── final.pptx
```

- `slide-content.md` 是已批准的逐页文字真源。
- `slides/` 中一页一个 SVG，是视觉修改入口。
- `preview/` 用于检查实际渲染结果，不是最终编辑源。
- `final.pptx` 尽可能使用 PowerPoint 原生文本和图形。
- `compilation-report.json` 说明哪些元素原生可编辑、哪些使用整体 SVG 降级、哪些失败。

## 6. 手动运行质量链路

先解析两个绝对路径：

```text
SKILL_ROOT = vectordeckppt Skill 所在目录
DECK_ROOT = 本次演示文稿输出目录
```

以下命令在安装好依赖的 Python 环境中运行：

```bash
# 逐页结构与安全校验
python "<SKILL_ROOT>/scripts/validate_svg.py" "<DECK_ROOT>/slides/slide_01.svg" --json

# 整套字体角色与字号一致性审计
python "<SKILL_ROOT>/scripts/audit_typography.py" "<DECK_ROOT>/slides/" --strict --json

# 重新渲染全部 PNG 预览
python "<SKILL_ROOT>/scripts/render_svg.py" "<DECK_ROOT>/slides/" --output-dir "<DECK_ROOT>/preview/"

# 编译并保留逐页报告
python "<SKILL_ROOT>/scripts/compile_pptx.py" "<DECK_ROOT>/slides/" --output "<DECK_ROOT>/final.pptx" --report "<DECK_ROOT>/compilation-report.json"

# 验证最终 PPTX 包
python "<SKILL_ROOT>/scripts/validate_pptx.py" "<DECK_ROOT>/final.pptx" --json
```

在仓库内也可以在每条命令前使用 `uv run`。在普通 pip 环境中直接使用 `python <脚本路径>`，不要写成 `python -m <脚本路径>`。

## 7. 读懂审计结果

### 字体审计

- `missing_text_role`：可见文字缺少 `data-role`。
- `inconsistent_peer_size`：同一页同一角色出现不同字号。
- `inconsistent_deck_size`：跨页复用角色的字号不一致，通常是普通页标题。
- `inconsistent_deck_title_family` / `inconsistent_deck_title_weight`：普通页标题的字体或字重不一致。

### 编译报告

- `native`：已转换为 PowerPoint 原生对象，可逐项编辑。
- `embedded_svg`：外观通过 Office SVG 保留，但通常只能整体编辑。
- `failed`：内容无法安全保真，必须修复；`failed > 0` 时不能交付。

更具体的错误处理见 [故障排查](../.agents/skills/vectordeckppt/references/troubleshooting.md)。

## 8. 修改已有 Deck

1. 修改 `slide-content.md` 中的文字合同；若叙事或事实变化较大，重新确认文字内容。
2. 修改对应 `slides/slide_XX.svg`，不要把 PNG 或 PPTX 当成新的视觉真源。
3. 重新校验 SVG、运行字体审计并渲染预览。
4. 检查实际 PNG 后重新编译、验证 PPTX，并更新编译报告。
5. 若修改改变了整套视觉系统，先更新代表性样稿并重新确认，再批量应用。

## 9. 验收清单

- 完整需求合同、文字内容和代表性视觉样稿都得到明确批准；
- 页数、顺序、事实、数据和来源正确；
- 普通页标题及同页同级文字精确一致；
- 每页 SVG 校验通过，整套字体审计通过；
- 每张 PNG 已按实际尺寸目视检查；
- `compilation-report.json` 的 `failed` 为 `0`；
- 最终 PPTX 校验通过，所有降级均已向使用者说明。
