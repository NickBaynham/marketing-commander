"""Governance-document validation: links, golden path, required files,
ambiguity rules. This suite is the 'automated validation' part of the
Phase 2 deliverable (plan/plan.md)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

GOVERNANCE_FILES = [
    "CLAUDE.md",
    "AGENT.md",
    "plan/plan.md",
    "docs/product/mvp-product-brief.md",
    "docs/product/domain-model.md",
    "docs/product/ux-specification.md",
    "docs/architecture/technical-design.md",
    "knowledge/glossary.md",
    "knowledge/requirements/requirements.md",
    "knowledge/requirements/user-stories.md",
    "knowledge/requirements/acceptance-criteria.md",
    "knowledge/requirements/traceability-matrix.md",
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(#[^)]*)?\)")
GOLDEN_PATH_RE = re.compile(r"Create workspace\n(?:→ [^\n]+\n)+")

# Phrases banned as requirement language (requirements-quality rules).
BANNED_PHRASES = ["as appropriate", "where appropriate", "satisfactory"]
# Words banned when used as bare quality adjectives; checked word-bounded.
BANNED_WORDS = ["readable", "responsive"]
# (file, needle) pairs that are deliberate: definitions of the replacement
# rule itself, or historical review records quoting a finding.
ALLOWED = [
    ("plan/plan.md", 'The phrase "meaningful behavior" is replaced'),
]


def markdown_files() -> list[Path]:
    return [
        p
        for p in ROOT.rglob("*.md")
        if ".git" not in p.parts
        and ".venv" not in p.parts
        and "node_modules" not in p.parts
    ]


def test_required_governance_files_exist():
    missing = [f for f in GOVERNANCE_FILES if not (ROOT / f).exists()]
    assert not missing, f"missing governance files: {missing}"


def test_all_relative_links_resolve():
    broken = []
    for path in markdown_files():
        text = path.read_text()
        for match in LINK_RE.finditer(text):
            href = match.group(1)
            if href.startswith(("http", "mailto:")):
                continue
            target = (path.parent / href).resolve()
            if not target.exists():
                broken.append(f"{path.relative_to(ROOT)}: {href}")
    assert not broken, f"broken links: {broken}"


def test_canonical_golden_path_identical_everywhere():
    blocks = []
    for path in markdown_files():
        for match in GOLDEN_PATH_RE.finditer(path.read_text()):
            block = match.group(0)
            if block.strip().endswith("→ Export campaign"):
                blocks.append((path.relative_to(ROOT), block))
    assert len(blocks) >= 4, f"expected >=4 golden-path blocks, found {len(blocks)}"
    canonical = blocks[0][1]
    assert canonical.count("\n") == 13, "golden path must have 13 steps"
    mismatched = [str(p) for p, b in blocks if b != canonical]
    assert not mismatched, f"golden path differs in: {mismatched}"


def test_no_ambiguous_requirement_language():
    hits = []
    check_files = [ROOT / f for f in GOVERNANCE_FILES]
    for path in check_files:
        rel = str(path.relative_to(ROOT))
        for i, line in enumerate(path.read_text().splitlines(), 1):
            lowered = line.lower()
            if any(a[0] == rel and a[1].lower() in lowered for a in ALLOWED):
                continue
            for phrase in BANNED_PHRASES:
                if phrase in lowered:
                    hits.append(f"{rel}:{i}: {phrase}")
            for word in BANNED_WORDS:
                if re.search(rf"(?<![\w-]){word}(?![\w-])", lowered):
                    hits.append(f"{rel}:{i}: {word}")
    assert not hits, f"ambiguous requirement language: {hits}"


def test_brief_is_approved_with_immutable_metadata():
    text = (ROOT / "docs/product/mvp-product-brief.md").read_text()
    head = text.split("---", 2)[1]
    assert "status: approved" in head
    assert "approved_by: Nick Baynham" in head
    assert re.search(r"approved_at: \d{4}-\d{2}-\d{2}", head)
