#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create a TOB weekly review Markdown skeleton."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# TOB 研发周报 {week}

> 周期：{week}
> 范围：{scope}
> 生成方式：AI 初稿 + 人工确认
> 状态：草稿

## 1. 本周核心结论

- 
- 
- 

## 2. 本周业务进展

| 业务能力 | 本周进展 | 当前状态 | 证据 |
|---|---|---|---|
|  |  |  |  |

## 3. 当前核心后端工作进展

| 模块 / 仓库 / 服务 | 主要变更 | 关联业务 | 证据 |
|---|---|---|---|
|  |  |  |  |

## 4. 跨模块 / 跨仓库依赖

| 依赖项 | 涉及范围 | 当前状态 | 需要谁推进 | 下一步 |
|---|---|---|---|---|
|  |  |  |  |  |

## 5. 风险与阻塞

| 风险 | 影响 | Owner | Action | 截止时间 | 状态 |
|---|---|---|---|---|---|
|  |  |  |  |  | Open |

## 6. 测试与发布关注点

| 关注点 | 说明 | 验证方式 | 状态 |
|---|---|---|---|
|  |  |  |  |

## 7. 上周 action 回看

| 上周 Action | 结果 | 证据 | 后续处理 |
|---|---|---|---|
|  | Done / Carry Over / Dropped |  |  |

## 8. 下周动作

| 优先级 | 动作 | Owner | 预期结果 |
|---|---|---|---|
| P0 |  |  |  |
| P1 |  |  |  |

## 9. 需要沉淀的文档 / 方案 / 复盘

- 需求澄清：
- 技术方案：
- 测试用例：
- 问题复盘：
- Repo Wiki / 模块文档：

## 10. 证据索引

| 类型 | 路径 / 编号 / 链接 | 说明 |
|---|---|---|
| 需求文档 |  |  |
| PR/MR |  |  |
| commit |  |  |
| 测试反馈 |  |  |
| 发布记录 |  |  |

## 11. 人工确认记录

- 已确认：
- 待确认：
- 删除 / 修正的 AI 推断：
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a TOB weekly review Markdown skeleton.")
    parser.add_argument("--week", required=True, help="Week label, e.g. 2026-W13")
    parser.add_argument("--out", required=True, help="Output Markdown path")
    parser.add_argument("--scope", default="TOB 当前核心后端工作及相关业务模块", help="Review scope")
    parser.add_argument("--force", action="store_true", help="Overwrite existing output")
    args = parser.parse_args()

    output = Path(args.out)
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(TEMPLATE.format(week=args.week, scope=args.scope), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
