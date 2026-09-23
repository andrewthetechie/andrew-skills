# andrew-skills

Agent skills for engineering, issue triage, code review, and startup analysis.

## Quickstart

```sh
npx skills@latest add andrewthetechie/andrew-skills
```

Pick the skills you want and which coding agents to install them on.

## Skills

| Skill | Description |
|-------|-------------|
| [code-review](skills/code-review) | Thermonuclear code quality review - checks abstraction, structure, and maintainability since a given base commit or branch |
| [fastapi-pro](skills/fastapi-pro) | Design, implement, review, and diagnose production FastAPI services with Pydantic and SQLAlchemy |
| [industry-standardize](skills/industry-standardize) | Use to review a codebase, proposal, or new feature where home-grown machinery should be replaced with something more industry standard. (Experimental) |
| [issue-decomposer](skills/issue-decomposer) | Decompose PRDs and feature descriptions into implementation-ready issue drafts |
| [issue-triage-loop](skills/issue-triage-loop) | Classify, validate, and prepare incoming issues for implementation |
| [martin-clean-code](skills/martin-clean-code) | Analyze code with Robert C. Martin's Clean Code concepts. (Experimental)Classify, validate, and prepare incoming issues for implementation | 
| [prd-review](skills/prd-review) | Review PRDs and technical proposals against the actual repository |
| [rebase-on-main](skills/rebase-on-main) | Safely rebase the current branch onto main with backups and conflict analysis |
| [request-to-prd](skills/request-to-prd) | Turn a rough bug report or feature request into a self-contained PRD draft |
| [startup-analyst](skills/startup-analyst) | Analyze early-stage startup markets, economics, competition, and strategy |
| [two-axis-review](skills/two-axis-review) | Review code changes along documented standards and spec/issue fit |
| [unslop](skills/unlop) | My take on a skill to "unslop" your LLM writing. Tries to force ASD-STE100 |

### Depredated
| Skill | Description | Replacement |
|-------|-------------|-------------|
| [issue-improver](skills/issue-improver) | Ratchet bug reports and feature requests toward implementation readiness | issue-triage-loop |
| [issue-reviewer](skills/issue-reviewer) | Check issue drafts for context-free completeness before handing to an implementer | issue-triage-loop |
| [issue-triage](skills/issue-triage) | Classify, validate, and prepare incoming issues for implementation | issue-triage-loop |
## License

MIT
