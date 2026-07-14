---
name: git-add-new-business-code
description: Use when implementation is complete, before wrapping up, code review, verification, or branch finishing, and there may be newly created untracked business code, test code, or frontend business code that should be placed under git management. Use this whenever the task is to stage only newly added business files with git add, while avoiding docs, configs, generated files, assets, and other non-business additions. This skill stages qualifying new files only. Never commit or push.
---

# Git Add New Business Code

## Overview

After code implementation is complete, inspect git for newly added untracked files.
Only stage new business code, test code, and frontend business code.
Do not commit.
Do not push.
Do not stage tracked modifications.
Do not stage non-business additions.

Announce at start:
"我将使用 git-add-new-business-code skill，只把新增且符合范围的业务代码加入 git 管理，不做 commit 或 push。"

## Core Rule

Only handle untracked files.
In git status output, this means entries equivalent to `??`.
Ignore modified, deleted, renamed, or already staged files.

Prefer this file listing command over parsing directory summaries:

```bash
git ls-files --others --exclude-standard
```

If there are no untracked files, report that clearly and stop.

If the current directory is not a git repository, or the listing command fails, stop and report the reason clearly.
Do not guess from filesystem listings.
Do not use directory scans as a fallback to simulate git status.

## Classification

Stage a file only if it is clearly one of the following.
When uncertain, prefer not to stage automatically and report it as ambiguous.

### 1. Backend Business Classes

Usually includes new source files under backend application modules, for example:

- `back/*/src/main/java/**`
- `back/*/src/main/kotlin/**`

Typical business-class signals:

- Path segment contains `controller`, `service`, `repository`, `manager`, `facade`, `domain`, `entity`, `model`, `dto`, `vo`, `assembler`, `convert`, `mapper`
- Or filename ends with `Controller`, `Service`, `ServiceImpl`, `Repository`, `Manager`, `Facade`, `Entity`, `DO`, `DTO`, `VO`, `Mapper`

Default exclusions even if they are source files:

- `config`, `constant`, `constants`, `annotation`, `annotations`, `enum`, `enums`, `util`, `utils`, `exception`, `exceptions`, `sdk`, `generated`
- SQL, YAML, properties, XML, Markdown, OpenAPI, static assets, scripts

Conservative judgment rule:

- If a backend source file is obviously supporting business flow, stage it.
- If it looks like infrastructure or generic support code, do not auto-stage it.

### 2. Test Code

Stage new test source files, for example:

- `**/src/test/java/**`
- `**/src/test/kotlin/**`
- `**/*.test.ts`
- `**/*.test.tsx`
- `**/*.spec.ts`
- `**/*.spec.tsx`
- `**/*.test.js`
- `**/*.test.jsx`
- `**/*.spec.js`
- `**/*.spec.jsx`

Only stage test source files themselves.
Do not stage snapshots, reports, coverage output, screenshots, temporary fixtures, or generated test artifacts unless the user explicitly asked for them.

### 3. Frontend Business Code

Stage new frontend files that are clearly business-facing application code, especially:

- `front/src/pages/**`
- `front/src/pages/**/components/**`
- `front/src/pages/**/hooks/**`
- `front/src/pages/**/store/**`
- `front/src/pages/**/service*`
- `front/src/pages/**/types*`
- `front/src/pages/**/constants*`
- `front/src/pages/**/utils/**`
- `front/src/components/**` except obvious UI primitives such as `front/src/components/ui/**`

Good signals for frontend business code:

- Page entry files
- Page-scoped modal, drawer, panel, card, table, form, store, service, hook, or type files
- Components tightly coupled to product workflow or domain concepts

Do not auto-stage:

- Generic UI primitives
- Pure styling files unless they are part of a new business page/component that is also being staged
- Generated API clients
- Build config
- Public assets
- Docs

### 4. Non-Standard Repository Layouts

Some repositories do not use `back/*` and `front/src/pages/**`.
For example, they may use layouts such as:

- `services/**`
- `apps/**`
- `packages/**`
- `modules/**`
- `features/**`

In these repositories, keep the same conservative rule:

- Stage only files whose path and filename together clearly indicate business code or test code.
- If a file lives in a shared, platform, infra, generated, tooling, or generic UI area, do not auto-stage it.
- If the repository layout is unfamiliar and the file is not clearly business-facing, classify it as `ambiguous` instead of staging it.

Examples that are often ambiguous unless the path makes the business role obvious:

- `apps/web/src/features/**`
- `packages/shared/**`
- `services/common/**`
- `modules/platform/**`

## Required Process

1. Run `git ls-files --others --exclude-standard`.
2. Review only the untracked file list.
3. Classify each file into one of these buckets:
   - `stage`: clearly new business code / test code / frontend business code
   - `skip`: clearly outside scope
   - `ambiguous`: maybe business-related, but not clear enough to auto-stage
4. Stage only the `stage` bucket with `git add`.
5. Do not commit.
6. Do not push.
7. Report the result.

If the command fails because the current directory is not a git repository:

- Do not run `git add`
- Report that the skill could not proceed because no git repository was detected
- Ask the user to switch to the correct repository root or confirm another target path

## Staging Rules

- Use exact paths with proper shell quoting.
- If a path contains spaces or non-ASCII characters, quote it correctly and retry if needed.
- Prefer staging files one by one or in a tightly scoped command, not broad directory adds.
- Never use `git add .`, `git add -A`, or similar broad staging commands for this skill.

## Output Format

Use a concise result summary:

```text
新增未跟踪文件已检查完毕。

已 git add:
- <path>
- <path>

已跳过:
- <path> - 非业务新增
- <path> - 文档/配置/产物

待确认:
- <path> - 可能是业务代码，但判定不够明确
```

If nothing qualified:

```text
已检查新增未跟踪文件，没有需要纳入 git 管理的新增业务代码或测试代码；未执行 git add。
```

## Red Flags

Never do any of the following:

- Commit
- Push
- Stage tracked modifications together with new files
- Stage docs, specs, screenshots, logs, SQL, config, generated code, or assets just because they are new
- Use broad staging commands
- Pretend a file is business code when the path does not support that conclusion
- Continue when git listing failed or no repository was detected

## Practical Guidance

When this skill is used at the end of an implementation task:

- Run it after coding is done and before the final wrap-up.
- If verification created reports or temporary files, exclude them.
- If both a business component file and its adjacent style file are newly created, the style file may be staged together only when it is clearly part of that same new business component/page.
- If ambiguity remains, do not auto-stage the ambiguous file. Surface it explicitly.
- In monorepos or unfamiliar layouts, bias toward `ambiguous` rather than optimistic staging.
