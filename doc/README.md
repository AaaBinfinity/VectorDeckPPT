# VectorDeckPPT 文档

这里汇总 VectorDeckPPT 的产品规范、Agent 工作流、设计方法、编译器边界和版本记录。第一次使用建议先阅读根目录 [README](../README.md)，再按角色进入对应文档。

## 按角色阅读

### 我想直接生成 PPT

1. 阅读 [快速开始](../README.md#quick-start)；
2. 根据 [使用指南](usage-guide.md) 选择仓库内或全局安装方式；
3. 复制或修改 [提示词示例](prompt-examples.md)；
4. 了解 [完整 Skill 工作流](../.agents/skills/vectordeckppt/references/workflow.md)；
5. 从 [项目介绍示例](../examples/project-intro-deck/) 查看源 SVG、PPTX 和编译报告。

### 我想调整视觉质量

- [艺术方向](../.agents/skills/vectordeckppt/references/art-direction.md)：从受众、目标和证据定义视觉命题；
- [设计系统](../.agents/skills/vectordeckppt/references/design-system.md)：字体、空间、色彩、图像和几何规则；
- [页面设计](../.agents/skills/vectordeckppt/references/slide-design.md)：信息层级、构图和内容密度；
- [视觉方向参考](../.agents/skills/vectordeckppt/references/style-templates.md)：九套内置视觉语法及可检查的 SVG 源文件；
- [视觉复审](../.agents/skills/vectordeckppt/references/visual-review.md)：逐页 PNG 与最终 PPTX 检查方法。

### 我想保证字体和内容质量

- [设计系统](../.agents/skills/vectordeckppt/references/design-system.md)：先把字号范围收敛为精确的角色 token；
- [页面设计](../.agents/skills/vectordeckppt/references/slide-design.md)：使用结论、解释、证据和行动组成信息丰富页面；
- [字体审计脚本](../.agents/skills/vectordeckppt/scripts/audit_typography.py)：检查普通页标题与同页同级文字是否使用一致字号；
- [故障排查](../.agents/skills/vectordeckppt/references/troubleshooting.md#typography-audit-fails)：根据审计错误修改 SVG，而不是临时缩小单个文本框。

### 我想理解 SVG → PPTX 编译器

- [SVG 作者指南](../.agents/skills/vectordeckppt/references/svg-authoring.md)；
- [SVG → PPTX 映射](../.agents/skills/vectordeckppt/references/svg-to-pptx.md)；
- [故障排查](../.agents/skills/vectordeckppt/references/troubleshooting.md)；
- [确定性脚本](../.agents/skills/vectordeckppt/scripts/)。

### 我想维护项目

- [贡献指南](../CONTRIBUTING.md)；
- [产品需求文档](PRD.md)；
- [仓库开发规范](../AGENTS.md)；
- [变更记录](../CHANGELOG.md)；
- [V1.1.0 发布说明](releases/v1.1.0.md)。

## 架构不变量

- VectorDeckPPT 是 Agent Skill，不是 AI Provider API 应用；
- 宿主 Agent 负责阅读、叙事、艺术方向和视觉判断；
- 确定性脚本只负责校验、渲染、编译和包验证；
- 一页一份 SVG，SVG 是视觉真源；
- PowerPoint 原生对象优先，其次是显式 Office SVG 降级；
- 可见内容不能被静默丢失；
- 开始资料综合前必须先补齐并明确确认完整需求合同；
- 普通页标题必须共享一个精确字体 token，同页同级标题必须完全一致；
- 普通内容页默认同时包含结论、解释、具体证据或例子，以及影响或行动；
- 专业不等于横平竖直的卡片集合；构图可以通过英雄字体、编辑式不对称、裁切、叠压、弧线或斜线建立受控艺术感；
- 完整制作前必须分别通过文字内容和视觉样稿审批。

## 示例产物

| 示例 | 页数 | 源 SVG | 可编辑 PPTX | 编译报告 |
|---|---:|---|---|---|
| Basic Deck | 5 | [查看](../examples/basic-deck/) | [下载](../examples/basic-deck/example.pptx) | [查看](../examples/basic-deck/compilation-report.json) |
| Project Intro | 10 | [查看](../examples/project-intro-deck/slides/) | [下载](../examples/project-intro-deck/project-intro.pptx) | [查看](../examples/project-intro-deck/compilation-report.json) |

## 文档维护原则

- README 负责产品定位、效果展示和快速开始；
- `doc/usage-guide.md` 负责面向使用者的安装、请求、质量链路和验收方法；
- `CONTRIBUTING.md` 负责面向维护者的环境、同步矩阵、测试和发布检查；
- `SKILL.md` 与 `references/` 定义 Agent 的规范行为；
- `doc/PRD.md` 记录产品边界和规范性要求；
- 示例文档只使用真实能力、真实产物和可复现命令；
- Agent 行为、模板库或质量门变化时，同步更新 README、PRD、提示词示例、Skill references 和 Changelog；
- 编译器行为变化时，同步更新测试、映射文档、示例 PPTX 和编译报告。
