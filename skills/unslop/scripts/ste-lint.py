#!/usr/bin/env python3
"""Deterministic linter for selected structural STE patterns.

Checks only selected patterns that are useful without ASD's dictionary. It is
a heuristic, not an STE parser or a compliance checker. Modal perfect forms
such as "may not have failed" are protected because confidence is content.

Usage:
    ste-lint.py FILE [FILE ...]
    echo "text" | ste-lint.py [--json]
    ste-lint.py --baseline 5 FILE      # pass unless hard violations exceed 5
    ste-lint.py --disable passive-voice,present-perfect FILE
    ste-lint.py --max-words 20 FILE
    ste-lint.py --selftest

Exit 1 when hard ("advisory-free") violations exceed the baseline (default 0).
Advisory findings (passive voice, compound tenses) never fail the run.
"""
import argparse
import json
import re
import sys

# These regular expressions are heuristics, not a parser. A noun-cluster rule
# needs part-of-speech tagging to avoid frequent false positives.
# No ellipsis rule by owner's choice: technical writing sometimes earns one.
RULES = [
    ("semicolon", "advisory-free",
     re.compile(r";"),
     "STE bans the semicolon (Rule 8.1). Split into separate sentences."),
    ("phrasal-verb", "advisory-free",
     re.compile(r"\b(spin(?:ning|s)? up|spun up|reach(?:ing|es|ed)? out|div(?:e|es|ing|ed) into|dove into|kick(?:ing|s|ed)? off|circl(?:e|es|ing|ed) back|touch(?:ing|es|ed)? base|tak(?:e|es|ing|en) off|took off)\b", re.I),
     "Selected phrasal-verb pattern. Use a single plain verb when it preserves the meaning."),
    ("marketing-adjective", "advisory-free",
     re.compile(r"\b(seamless(?:ly)?|robust(?:ly)?|powerful(?:ly)?|cutting-edge|effortless(?:ly)?|blazing[- ]fast|world-class|state-of-the-art|game-chang(?:ing|er))\b", re.I),
     "Selected marketing-word pattern. Delete it, or give the measurement that supports the claim."),
    ("nominalization", "advisory-free",
     re.compile(r"\b(perform|performs|performed|conduct|conducts|conducted|carry out|carries out|carried out)\s+(?:a|an|the)\s+\w+(?:tion|sion|ment|ance|ence|ysis)\b", re.I),
     "Action frozen into a noun. Use the verb (analyze, not perform an analysis of)."),
    ("passive-voice", "advisory",
     re.compile(r"\b(is|are|was|were|been|being)\s+(\w+ed|given|taken|made|done|found|seen|known|shown|written|built|sent|set|run|read|kept|held|left|put)\b(?!\s+(?:to|for|by)\s+\w+ing)", re.I),
     "Possible passive voice. Name the actor and use an active verb, unless the actor is unknown or irrelevant."),
    ("present-perfect", "advisory",
     # modal + perfect infinitive ("may have failed") is a protected hedge, not present perfect
     re.compile(r"(?<!\bmay )(?<!\bmight )(?<!\bcould )(?<!\bshould )(?<!\bwould )(?<!\bmust )\b(has|have|had)\s+(?:been\s+)?\w+(?:ed|en)\b", re.I),
     "Compound tense. Use simple past/present unless current relevance is the point (then keep and flag)."),
]

PROTECTED_MODAL_PERFECT = re.compile(
    r"\b(?:may|might|could|should|would|must)\b"
    r"(?:\s+(?:not|never|possibly|probably|perhaps|still|already|really|just))*\s*$",
    re.I,
)

# One word, one meaning: groups of verbs commonly rotated for the same action.
# Include only pairs whose members are usually interchangeable.
# Error, fault, and failure are distinct concepts, so this list omits them.
SYNONYM_GROUPS = [
    ("check", "verify", "confirm", "validate"),
    ("delete", "remove", "erase"),
    ("start", "launch", "begin", "initiate"),
    ("stop", "halt", "terminate"),
    ("show", "display"),
    ("use", "utilize", "employ"),
    ("fix", "repair", "correct"),
    ("send", "transmit"),
    ("get", "retrieve", "fetch", "obtain"),
    ("change", "modify", "alter"),
]

DEFAULT_MAX_WORDS = 25
SUPPORTED_MAX_WORDS = (20, 25)

FENCE_START = re.compile(
    r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$"
)
LIST_ITEM_START = re.compile(
    r"^(?P<indent> *)(?P<marker>[-*+]|[0-9]+[.)])"
    r"(?P<gap> +)(?P<body>.*)$"
)
CONJUNCTION_END = re.compile(r"\b(?:and|or)\s*$", re.I)
TABLE_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(?P<body>.*)$")
SENTENCE_ABBREVIATIONS = (
    "e.g.", "i.e.", "etc.", "vs.", "mr.", "mrs.", "ms.", "dr.",
    "prof.", "sr.", "jr.", "fig.", "no.",
)


def _word_re(base):
    return re.compile(r"\b" + base + r"(?:s|es|ed|d|ing)?\b", re.I)


def _strip_blockquote_prefix(line):
    """Return content, source offset, and quote depth."""
    offset = 0
    depth = 0
    while offset < len(line):
        start = offset
        spaces = 0
        while offset < len(line) and line[offset] == " " and spaces < 3:
            offset += 1
            spaces += 1
        if offset >= len(line) or line[offset] != ">":
            offset = start
            break
        offset += 1
        if offset < len(line) and line[offset] in " \t":
            offset += 1
        depth += 1
    return line[offset:], offset, depth


def _list_item_info(line):
    content, quote_offset, quote_depth = _strip_blockquote_prefix(line)
    match = LIST_ITEM_START.match(content)
    if not match:
        return None
    indent = len(match.group("indent").expandtabs(4))
    content_indent = indent + len(match.group("marker"))
    content_indent += len(match.group("gap").expandtabs(4))
    return {
        "body": match.group("body"),
        "body_start": quote_offset + match.start("body"),
        "content_indent": content_indent,
        "indent": indent,
        "marker_start": quote_offset + match.start("marker"),
        "quote_depth": quote_depth,
    }


def _fence_start(line):
    content, _, quote_depth = _strip_blockquote_prefix(line)
    match = FENCE_START.match(content)
    if not match:
        return None
    fence = match.group("fence")
    info = match.group("info")
    if fence[0] == "`" and "`" in info:
        return None
    return fence[0], len(fence), quote_depth


def _is_fence_end(line, fence):
    content, _, quote_depth = _strip_blockquote_prefix(line)
    character, minimum_length, opening_quote_depth = fence
    if quote_depth != opening_quote_depth:
        return False
    pattern = rf"^ {{0,3}}{re.escape(character)}{{{minimum_length},}}[ \t]*$"
    return bool(re.match(pattern, content))


def _fenced_lines(lines):
    ignored = set()
    fence = None
    for index, line in enumerate(lines):
        if fence is None:
            fence = _fence_start(line)
            if fence is not None:
                ignored.add(index)
        else:
            ignored.add(index)
            if _is_fence_end(line, fence):
                fence = None
    return ignored


def _mask_range(characters, start, end):
    for index in range(start, end):
        characters[index] = " "


def _is_escaped(text, index):
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def _mask_inline_code(text, placeholder=False):
    """Mask CommonMark-style code spans without changing string length."""
    characters = list(text)
    index = 0
    while index < len(text):
        if text[index] != "`" or _is_escaped(text, index):
            index += 1
            continue
        opening_end = index
        while opening_end < len(text) and text[opening_end] == "`":
            opening_end += 1
        opening_length = opening_end - index
        search = opening_end
        closing_end = None
        while search < len(text):
            closing_start = text.find("`", search)
            if closing_start < 0:
                break
            candidate_end = closing_start
            while candidate_end < len(text) and text[candidate_end] == "`":
                candidate_end += 1
            if candidate_end - closing_start == opening_length:
                closing_end = candidate_end
                break
            search = candidate_end
        if closing_end is None:
            index = opening_end
            continue
        _mask_range(characters, index, closing_end)
        if placeholder:
            characters[index] = "X"
        index = closing_end
    return "".join(characters)


def _matching_label_start(text, closing_bracket):
    depth = 1
    for index in range(closing_bracket - 1, -1, -1):
        if _is_escaped(text, index):
            continue
        if text[index] == "]":
            depth += 1
        elif text[index] == "[":
            depth -= 1
            if depth == 0:
                return index
    return None


def _matching_destination_end(text, opening_parenthesis):
    depth = 1
    index = opening_parenthesis + 1
    while index < len(text):
        if _is_escaped(text, index):
            index += 2
            continue
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return None


def _mask_link_destinations(text, placeholder=False):
    """Keep link labels, but mask Markdown destinations and syntax."""
    characters = list(text)
    index = 0
    while index < len(text) - 1:
        if (text[index:index + 2] != "](" or _is_escaped(text, index)):
            index += 1
            continue
        label_start = _matching_label_start(text, index)
        destination_end = _matching_destination_end(text, index + 1)
        if label_start is None or destination_end is None:
            index += 2
            continue
        characters[label_start] = " "
        if label_start > 0 and text[label_start - 1] == "!":
            characters[label_start - 1] = " "
        _mask_range(characters, index, destination_end + 1)
        index = destination_end + 1
    for match in re.finditer(r"<(?:https?://|mailto:)[^>\s]+>", text,
                             re.I):
        _mask_range(characters, match.start(), match.end())
        if placeholder:
            characters[match.start()] = "X"
    return "".join(characters)


def _mask_markdown_inline(text, code_placeholder=False):
    return _mask_link_destinations(
        _mask_inline_code(text, placeholder=code_placeholder),
        placeholder=code_placeholder,
    )


def _trimmed_masked_fragment(text):
    masked = _mask_markdown_inline(text)
    left = len(masked) - len(masked.lstrip())
    right = len(masked.rstrip())
    return masked[left:right], left


def _markdown_structure(lines):
    """Find fenced code, indented code, and valid Markdown list items."""
    fenced = _fenced_lines(lines)
    indented = set()
    list_items = {}
    list_stacks = {}
    in_indented_code = {}

    for index, line in enumerate(lines):
        if index in fenced:
            continue
        content, _, quote_depth = _strip_blockquote_prefix(line)
        if not content.strip():
            continue

        stack = list_stacks.setdefault(quote_depth, [])
        item = _list_item_info(line)
        if item is not None:
            is_root = item["indent"] <= 3
            has_parent = any(
                parent["indent"] < item["indent"] for parent in stack
            )
            if is_root or has_parent:
                while stack and stack[-1]["indent"] >= item["indent"]:
                    stack.pop()
                stack.append(item)
                list_items[index] = item
                in_indented_code[quote_depth] = False
                continue

        indent = len(content) - len(content.lstrip(" \t"))
        indent = len(content[:indent].expandtabs(4))
        parent = stack[-1] if stack else None
        is_list_continuation = bool(
            parent and indent >= parent["content_indent"]
        )
        is_list_code = bool(
            parent and indent >= parent["content_indent"] + 4
        )
        if is_list_code or (
                indent >= 4
                and (in_indented_code.get(quote_depth, False)
                     or not is_list_continuation)):
            indented.add(index)
            in_indented_code[quote_depth] = True
            continue

        in_indented_code[quote_depth] = False
        if not is_list_continuation:
            stack.clear()

    return fenced, indented, list_items


def _split_table_row(line):
    """Return trimmed table cells and their zero-based source columns.

    A pipe must separate at least two cells. Escaped pipes stay in their cell.
    This implements only the ordinary Markdown table shape. It is
    enough to distinguish a table from prose that happens to contain a pipe.
    """
    left = len(line) - len(line.lstrip())
    right = len(line.rstrip())
    content = line[left:right]
    if "|" not in content:
        return None
    if content.startswith("|"):
        content = content[1:]
        left += 1
    if content.endswith("|"):
        content = content[:-1]
    raw_cells = re.split(r"(?<!\\)\|", content)
    if len(raw_cells) < 2:
        return None

    cells = []
    column = left
    for raw_cell in raw_cells:
        leading = len(raw_cell) - len(raw_cell.lstrip())
        cells.append((raw_cell.strip(), column + leading))
        column += len(raw_cell) + 1
    return cells


def _markdown_table_cells(lines):
    """Map ordinary Markdown table rows to their prose cells.

    The separator row anchors detection, so pipe-containing prose is not
    treated as a table. Both leading-pipe and no-leading-pipe table styles are
    accepted when their header and body use the same number of cells.
    """
    table_cells = {}
    index = 1
    while index < len(lines):
        separator = _split_table_row(lines[index])
        header = _split_table_row(lines[index - 1])
        if (not separator or not header or len(separator) != len(header)
                or not all(TABLE_SEPARATOR_CELL.fullmatch(cell)
                           for cell, _ in separator)):
            index += 1
            continue

        table_cells[index - 1] = header
        table_cells[index] = []
        index += 1
        while index < len(lines):
            row = _split_table_row(lines[index])
            if not row or len(row) != len(separator):
                break
            table_cells[index] = row
            index += 1
    return table_cells


def _prose_blocks(lines, table_cells, ignored_lines, list_items):
    """Return prose blocks while joining soft-wrapped Markdown lines."""
    blocks = []
    current = []
    in_frontmatter = False

    def flush():
        nonlocal current
        if current:
            blocks.append(current)
            current = []

    for index, raw_line in enumerate(lines):
        stripped = raw_line.strip()
        if index in ignored_lines:
            flush()
            continue
        if index == 0 and stripped == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == "---":
                in_frontmatter = False
                continue
            text, left = _trimmed_masked_fragment(raw_line)
            if text:
                blocks.append([(text, index + 1, left + 1)])
            continue
        if index in table_cells:
            flush()
            for cell, source_column in table_cells[index]:
                text, left = _trimmed_masked_fragment(cell)
                if text:
                    blocks.append([(text, index + 1,
                                    source_column + left + 1)])
            continue
        if not stripped:
            flush()
            continue
        if stripped in ("---", "***", "___"):
            flush()
            continue

        content, quote_offset, _ = _strip_blockquote_prefix(raw_line)
        heading = HEADING.match(content)
        if heading:
            flush()
            text, left = _trimmed_masked_fragment(heading.group("body"))
            if text:
                blocks.append([(text, index + 1,
                                quote_offset + heading.start("body")
                                + left + 1)])
            continue

        list_item = list_items.get(index)
        if list_item is not None:
            flush()
            text, left = _trimmed_masked_fragment(list_item["body"])
            if text:
                current.append((text, index + 1,
                                list_item["body_start"] + left + 1))
            continue

        text, left = _trimmed_masked_fragment(content)
        if text:
            current.append((text, index + 1,
                            quote_offset + left + 1))

    flush()
    return blocks


def _source_position(fragments, offset):
    cursor = 0
    for text, line, column in fragments:
        end = cursor + len(text)
        if offset < end:
            return line, column + offset - cursor
        cursor = end + 1
    _, line, column = fragments[-1]
    return line, column


def _sentence_boundaries(block):
    boundaries = []
    for boundary in re.finditer(r"(?<=[.!?])\s+", block):
        prefix = block[:boundary.start()].rstrip().lower()
        if prefix.endswith(SENTENCE_ABBREVIATIONS):
            continue
        boundaries.append(boundary)
    return boundaries


def _long_sentence_findings(lines, table_cells, filename, max_words,
                            ignored_lines, list_items):
    findings = []
    for fragments in _prose_blocks(
            lines, table_cells, ignored_lines, list_items):
        block = " ".join(text for text, _, _ in fragments)
        sentence_start = 0
        boundaries = _sentence_boundaries(block)
        for boundary in boundaries + [None]:
            sentence_end = boundary.start() if boundary else len(block)
            sentence = block[sentence_start:sentence_end]
            leading = len(sentence) - len(sentence.lstrip())
            stripped = sentence.strip()
            if stripped:
                word_count = len(stripped.split())
                if word_count > max_words:
                    offset = sentence_start + leading
                    line, column = _source_position(fragments, offset)
                    findings.append({
                        "file": filename,
                        "line": line,
                        "col": column,
                        "rule": "long-sentence",
                        "level": "advisory-free",
                        "match": f"{word_count} words",
                        "message": (
                            f"Sentence has {word_count} words "
                            f"(cap {max_words}). Split it."
                        ),
                    })
            if boundary is None:
                break
            sentence_start = boundary.end()
    return findings


def _is_protected_modal_perfect(line, match_start):
    return bool(PROTECTED_MODAL_PERFECT.search(line[:match_start]))


def _dangling_conjunction_findings(lines, filename, ignored_lines,
                                   list_items):
    findings = []
    for index, item in sorted(list_items.items()):
        body = _mask_markdown_inline(
            item["body"], code_placeholder=True
        )
        item_lines = [(index, body, item["body_start"] + 1)]
        next_index = index + 1
        while next_index < len(lines):
            if next_index in ignored_lines:
                next_index += 1
                continue
            if next_index in list_items:
                break
            candidate, quote_offset, quote_depth = _strip_blockquote_prefix(
                lines[next_index]
            )
            if not candidate.strip():
                next_index += 1
                continue
            indent_chars = len(candidate) - len(candidate.lstrip(" \t"))
            indent = len(candidate[:indent_chars].expandtabs(4))
            if (quote_depth != item["quote_depth"]
                    or indent < item["content_indent"]):
                break
            masked = _mask_markdown_inline(
                candidate, code_placeholder=True
            )
            left = len(masked) - len(masked.lstrip())
            item_lines.append((next_index, masked.strip(),
                               quote_offset + left + 1))
            next_index += 1

        meaningful = []
        for line_index, item_line, source_column in item_lines:
            cleaned = item_line.strip()
            if cleaned:
                meaningful.append((line_index, cleaned, source_column))
        if meaningful:
            end_line_index, end_line, source_column = meaningful[-1]
            conjunction = CONJUNCTION_END.search(end_line)
        else:
            end_line_index, end_line = None, None
            source_column, conjunction = None, None
        if conjunction:
            if end_line_index == index:
                finding_line = index + 1
                finding_col = item["marker_start"] + 1
            else:
                finding_line = end_line_index + 1
                finding_col = source_column + conjunction.start()
            findings.append({
                "file": filename,
                "line": finding_line,
                "col": finding_col,
                "rule": "dangling-conjunction",
                "level": "advisory-free",
                "match": end_line,
                "message": "List item ends with a coordinating conjunction. Complete the item or join it with the next item.",
            })
    return findings


def lint(text, filename="<stdin>", max_words=DEFAULT_MAX_WORDS):
    findings = []
    words_total = 0
    lines = text.splitlines()
    table_cells = _markdown_table_cells(lines)
    fenced_lines, indented_code_lines, list_items = _markdown_structure(lines)
    ignored_lines = fenced_lines | indented_code_lines
    # first occurrence of each synonym-group member: (group_idx, base) -> (line, col, match)
    seen_synonyms = {}
    for lineno, raw_line in enumerate(lines, 1):
        if lineno - 1 in ignored_lines:
            continue
        segments = table_cells.get(lineno - 1, [(raw_line, 0)])
        for segment, source_column in segments:
            line = _mask_markdown_inline(segment)
            words_total += len(line.split())
            for rule_id, level, pattern, msg in RULES:
                for m in pattern.finditer(line):
                    if (rule_id == "present-perfect"
                            and _is_protected_modal_perfect(line, m.start())):
                        continue
                    findings.append({"file": filename, "line": lineno,
                                     "col": source_column + m.start() + 1,
                                     "rule": rule_id, "level": level,
                                     "match": m.group(0), "message": msg})
            for gi, group in enumerate(SYNONYM_GROUPS):
                for base in group:
                    if (gi, base) in seen_synonyms:
                        continue
                    m = _word_re(base).search(line)
                    if m:
                        seen_synonyms[(gi, base)] = (
                            lineno, source_column + m.start() + 1, m.group(0)
                        )
    # synonym rotation: flag each member after the first, at its first occurrence
    for gi, group in enumerate(SYNONYM_GROUPS):
        present = [(seen_synonyms[(gi, b)], b) for b in group if (gi, b) in seen_synonyms]
        if len(present) > 1:
            present.sort()  # document order
            first_base = present[0][1]
            for (lineno, col, match), base in present[1:]:
                findings.append({"file": filename, "line": lineno, "col": col,
                                 "rule": "synonym-rotation", "level": "advisory",
                                 "match": match,
                                 "message": f"'{base}' and '{first_base}' may name the same action. Check the context, then use one term for one action."})
    findings.extend(_long_sentence_findings(
        lines, table_cells, filename, max_words, ignored_lines, list_items
    ))
    findings.extend(_dangling_conjunction_findings(
        lines, filename, ignored_lines, list_items
    ))
    findings.sort(key=lambda f: (f["line"], f["col"]))
    return findings, words_total


def report(findings, words_total, as_json, hard_count, baseline, max_words):
    rate = round(len(findings) * 100 / words_total, 1) if words_total else 0.0
    if as_json:
        print(json.dumps({"violations": findings, "count": len(findings),
                          "hard_count": hard_count, "baseline": baseline,
                          "max_words": max_words,
                          "words": words_total, "per_100_words": rate}, indent=2))
        return
    for f in findings:
        print(f"{f['file']}:{f['line']}:{f['col']} {f['rule']}: {f['message']} [{f['match']}]")
    print(f"\n{len(findings)} violations ({hard_count} hard, baseline {baseline}), "
          f"{words_total} words, cap {max_words}, {rate} per 100 words")
    print("Modal perfect forms are not tense findings: confidence is content.")


def selftest():
    bad = ("The panel is removed; spin up the job. Take off the cover. "
           "Perform an analysis of the seamless, powerful log. "
           "We have received the report.")
    findings, _ = lint(bad)
    rules = {f["rule"] for f in findings}
    for expected in ("semicolon", "phrasal-verb", "nominalization",
                     "marketing-adjective", "passive-voice", "present-perfect"):
        assert expected in rules, expected
    matches = {f["match"].lower() for f in findings}
    assert "take off" in matches, matches
    assert "powerful" in matches, matches
    # Modal perfect forms must not be tense findings, including negation.
    findings, _ = lint("The request may have failed. It could be a timeout. "
                       "The disk might have filled. "
                       "The request may not have failed. "
                       "The disk could really have filled.")
    assert findings == [], findings
    # Fenced and indented Markdown code blocks are skipped.
    findings, _ = lint("```\nx = a; y = b\n```")
    assert findings == []
    findings, words_total = lint(
        "    The powerful panel is removed; take off the cover."
    )
    assert findings == [], findings
    assert words_total == 0, words_total
    findings, _ = lint(
        "````python\n"
        "The powerful panel is removed; take off the cover.\n"
        "```\n"
        "The code fence is still open; powerful.\n"
        "````\n"
        "The final panel is powerful."
    )
    marketing = [
        f for f in findings if f["rule"] == "marketing-adjective"
    ]
    assert len(marketing) == 1 and marketing[0]["line"] == 6, findings
    # all supported list markers, case variants, and trailing whitespace
    findings, _ = lint(
        "- Confirm the target and\n"
        "* Record the result OR  \n"
        "+ Close the panel\n"
        "1. Start the task and\n"
        "2) Stop the task OR"
    )
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 4, dangling
    assert [f["line"] for f in dangling] == [1, 2, 4, 5], dangling
    assert [f["col"] for f in dangling] == [1, 1, 1, 1], dangling
    assert all(f["level"] == "advisory-free" for f in dangling), dangling

    # valid continuation lines and standalone four-space code are ignored
    findings, _ = lint("  - Confirm the target and\n    record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Confirm the target\n  and")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 2, dangling
    assert dangling[0]["col"] == 3, dangling
    findings, _ = lint("    - code and")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("> - Confirm the target and\n> - Record the result or")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert [f["line"] for f in dangling] == [1, 2], dangling
    assert [f["col"] for f in dangling] == [3, 3], dangling
    findings, _ = lint("- Do this and\n~~~\ncode and\n~~~")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 1, dangling
    findings, _ = lint("```text\n- code and\n```")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)

    # one- and three-space markers and ordered continuation width
    findings, _ = lint(" - Start the task and\n   record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("-  Start the task and\n   record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("-\tStart the task and")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("   - Start the task and", filename="fixture.md")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["col"] == 4, dangling
    assert dangling[0]["file"] == "fixture.md"
    assert dangling[0]["match"].endswith("and")
    assert "Complete the item" in dangling[0]["message"]
    findings, _ = lint("100. Start the task and\n  unrelated text")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1, dangling
    findings, _ = lint("- Start the task and.\n- Stop the task or,")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Start the task and\n\n  record the result.")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Parent item and\n  - Nested item or")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert [f["line"] for f in dangling] == [1, 2], dangling
    findings, _ = lint("- Parent item\n    - Deep nested item and")
    dangling = [f for f in findings if f["rule"] == "dangling-conjunction"]
    assert len(dangling) == 1 and dangling[0]["line"] == 2, dangling
    assert dangling[0]["col"] == 5, dangling

    # ordinary prose, inline code, and fenced code are ignored
    findings, _ = lint("The process may include steps and")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Use `and` as a label")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint("- Combine `left` and `right`")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings), findings
    inline = "Read ``powerful; `take off` `` before the powerful result."
    findings, _ = lint(inline)
    marketing = [
        f for f in findings if f["rule"] == "marketing-adjective"
    ]
    assert len(marketing) == 1, findings
    assert marketing[0]["col"] == inline.rfind("powerful") + 1, marketing
    assert not any(f["rule"] in ("semicolon", "phrasal-verb")
                   for f in findings), findings
    link = (
        "Read [the docs](https://example.test/a;b \"take off powerful\") "
        "before the powerful result."
    )
    findings, _ = lint(link)
    marketing = [
        f for f in findings if f["rule"] == "marketing-adjective"
    ]
    assert len(marketing) == 1, findings
    assert marketing[0]["col"] == link.rfind("powerful") + 1, marketing
    assert not any(f["rule"] in ("semicolon", "phrasal-verb")
                   for f in findings), findings
    findings, _ = lint("~~~\n- code and\n~~~")
    assert not any(f["rule"] == "dangling-conjunction" for f in findings)
    findings, _ = lint(("word " * 30).strip() + ".")
    assert any(f["rule"] == "long-sentence" for f in findings)
    # Soft-wrapped Markdown prose is one sentence for the length check.
    wrapped = (
        "This sentence has enough words to exceed the configured limit when "
        "the linter joins\n"
        "its two physical Markdown lines before it counts all of the words."
    )
    findings, _ = lint(wrapped)
    long_sentences = [f for f in findings if f["rule"] == "long-sentence"]
    assert len(long_sentences) == 1, long_sentences
    assert long_sentences[0]["line"] == 1, long_sentences
    # Common abbreviations do not split a sentence for the word cap.
    for abbreviation in ("e.g.", "i.e."):
        abbreviated = (
            " ".join(f"left{number}" for number in range(1, 14))
            + f" {abbreviation} "
            + " ".join(f"right{number}" for number in range(1, 14))
            + "."
        )
        findings, _ = lint(abbreviated)
        long_sentences = [
            f for f in findings if f["rule"] == "long-sentence"
        ]
        assert len(long_sentences) == 1, long_sentences
        assert long_sentences[0]["match"] == "27 words", long_sentences
    # Instructions can use the 20-word cap while descriptions use 25.
    bounded = " ".join(f"word{number}" for number in range(1, 24)) + "."
    findings, _ = lint(bounded, max_words=20)
    assert any(f["rule"] == "long-sentence" for f in findings), findings
    findings, _ = lint(bounded, max_words=25)
    assert not any(f["rule"] == "long-sentence" for f in findings), findings
    # Markdown table syntax is layout, not prose. Each cell stays lintable.
    short_cell = " ".join(f"term{number}" for number in range(1, 25)) + "."
    for table in (
            "| Label | Detail |\n"
            "| --- | --- |\n"
            f"| Clear | {short_cell} |",
            "Label | Detail\n"
            "--- | ---\n"
            f"Clear | {short_cell}"):
        findings, words_total = lint(table)
        assert not any(f["rule"] == "long-sentence" for f in findings), findings
        assert words_total == 27, words_total
    long_cell = " ".join(f"term{number}" for number in range(1, 27)) + "."
    findings, _ = lint(
        "| Label | Detail |\n"
        "| --- | --- |\n"
        f"| Clear | {long_cell} |"
    )
    long_sentences = [f for f in findings if f["rule"] == "long-sentence"]
    assert len(long_sentences) == 1, long_sentences
    assert long_sentences[0]["match"] == "26 words", long_sentences
    # synonym rotation: second member flagged, first named as the keeper
    findings, _ = lint("Check the config file. Then verify the output. Verify twice.")
    rot = [f for f in findings if f["rule"] == "synonym-rotation"]
    assert len(rot) == 1 and "'verify' and 'check'" in rot[0]["message"], rot
    assert rot[0]["level"] == "advisory", rot
    # single consistent term: no flag
    findings, _ = lint("Check the config. Check the output.")
    assert not any(f["rule"] == "synonym-rotation" for f in findings)
    # per-file labels
    findings, _ = lint("a; b", filename="x.md")
    assert findings[0]["file"] == "x.md"
    print("selftest OK")


def _nonnegative_int(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def build_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Lint selected, mechanically detectable STE writing patterns. "
            "Read UTF-8 files, or read standard input when no file is given."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("files", nargs="*", metavar="FILE",
                        help="UTF-8 text or Markdown file. Use - for stdin")
    parser.add_argument("--json", action="store_true",
                        help="write structured JSON findings")
    parser.add_argument("--baseline", type=_nonnegative_int, default=0,
                        metavar="N",
                        help="allow N hard findings before exit status 1")
    parser.add_argument("--disable", action="append", default=[],
                        metavar="RULE[,RULE...]",
                        help="disable one or more rule IDs. This option is repeatable")
    parser.add_argument("--max-words", type=int,
                        choices=SUPPORTED_MAX_WORDS,
                        default=DEFAULT_MAX_WORDS,
                        help="sentence cap: 20 for instructions, 25 for prose")
    parser.add_argument("--selftest", action="store_true",
                        help="run the embedded regression tests and exit")
    return parser


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.selftest:
        if args.files:
            parser.error("--selftest does not accept files")
        selftest()
        return 0

    disabled = {
        rule.strip()
        for value in args.disable
        for rule in value.split(",")
        if rule.strip()
    }
    known_rules = {rule_id for rule_id, _, _, _ in RULES}
    known_rules.update({
        "dangling-conjunction", "long-sentence", "synonym-rotation"
    })
    unknown_rules = sorted(disabled - known_rules)
    if unknown_rules:
        parser.error("unknown rule ID(s): " + ", ".join(unknown_rules))

    findings, words_total = [], 0
    paths = args.files or ["-"]
    for path in paths:
        if path == "-":
            source = sys.stdin.read()
            filename = "<stdin>"
        else:
            try:
                with open(path, encoding="utf-8") as source_file:
                    source = source_file.read()
            except (OSError, UnicodeError) as exc:
                parser.error(f"cannot read {path!r}: {exc}")
            filename = path
        file_findings, file_words = lint(
            source, filename=filename, max_words=args.max_words
        )
        findings.extend(file_findings)
        words_total += file_words

    findings = [f for f in findings if f["rule"] not in disabled]
    hard_count = sum(1 for f in findings if f["level"] == "advisory-free")
    report(findings, words_total, args.json, hard_count, args.baseline,
           args.max_words)
    return 1 if hard_count > args.baseline else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
