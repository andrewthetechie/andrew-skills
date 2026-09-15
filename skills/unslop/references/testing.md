# Testing unslop

Read this file when changing the skill or linter. Run commands from the directory that contains `SKILL.md`.

## Mechanical checks

Run the original self-test and the regression suite:

```bash
python3 -B scripts/ste-lint.py --selftest
python3 -B -m unittest discover -s tests -v
```

Lint the skill and its references at both sentence limits:

```bash
python3 -B scripts/ste-lint.py --max-words 20 SKILL.md references/asd-ste100.md references/testing.md
python3 -B scripts/ste-lint.py --max-words 25 SKILL.md references/asd-ste100.md references/testing.md
```

Review every finding using the completion criteria in `SKILL.md`. Parser tests cover quoted spans, inline code, line wrapping, source positions, and exit status.

## Rewrite checks

Use [the rewrite cases](../tests/rewrite-cases.json) to evaluate the skill's behavior. Each case gives a request, required properties, and one acceptable response.

1. Apply the skill to each case's request. Record the actual response before comparing it with the example.
2. Check every required property. Accept other wording when it preserves meaning and follows the skill.
3. Rewrite the actual response once more with the same audience and constraints. Check that acceptable prose stays unchanged.
4. Record failures, retained fidelity exceptions, and the evaluation method.

For explanations of edits, apply the second pass to the revised prose only. Preserve the original column as quoted source text.

Treat technical terms in these cases as familiar to the specified audience. A lint pass alone does not establish rewrite quality.

A review by the same agent is a manual check. Report independent model evaluations separately, including the model and number of runs.

## Parser limits

The linter protects paired quotation marks, recognized code, and Markdown link destinations. It still reviews prose inside Markdown blockquotes.

Treat findings against exact source blockquotes as inapplicable. Review other unrecognized protected spans manually.

The word count uses placeholders for quoted text and code spans. It does not implement all ASD-STE100 counting rules.

