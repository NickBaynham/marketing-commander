"""AIP typed schema and completeness engine (DEC-02, Phase 6).

Pure domain module: the twelve-section typed schema (D6-2), placeholder
detection, section weights (D6-4), the DEC-02 weighted completeness
formula, binary approval eligibility, and the DEC-09 size limits.
No transport or persistence imports (layering contract).

Traceability: REQ-006..REQ-011, REQ-045; AC-004; BR-002; DEC-02,
DEC-09; D6-1, D6-2, D6-4.
"""

import re
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

SECTION_MAX_CHARS = 20_000
TOTAL_MAX_CHARS = 200_000
SECTION_MIN_CONTENT_CHARS = 40
MAX_SOURCES = 20
SOURCE_MAX_CHARS = 500

# DEC-02 section order is the render and display order.
REQUIRED_SECTIONS: tuple[str, ...] = (
    "core_identity",
    "musical_identity",
    "differentiation_hypothesis",
    "artist_personality",
    "brand_voice",
    "audience_hypothesis",
    "visual_direction",
    "narrative_themes",
    "do_and_avoid",
)
OPTIONAL_SECTIONS: tuple[str, ...] = (
    "origin_and_motivation",
    "influence_map",
    "unknowns_and_assumptions",
)
ALL_SECTIONS: tuple[str, ...] = REQUIRED_SECTIONS + OPTIONAL_SECTIONS

SECTION_TITLES: dict[str, str] = {
    "core_identity": "Core identity",
    "musical_identity": "Musical identity",
    "differentiation_hypothesis": "Differentiation hypothesis",
    "artist_personality": "Artist personality",
    "brand_voice": "Brand voice",
    "audience_hypothesis": "Audience hypothesis",
    "visual_direction": "Visual direction",
    "narrative_themes": "Narrative themes",
    "do_and_avoid": "Do and avoid guidance",
    "origin_and_motivation": "Origin and motivation",
    "influence_map": "Influence map",
    "unknowns_and_assumptions": "Unknowns and assumptions",
}

# D6-4: equal weights, one constant, validated by tests. Recalibration
# is a recorded change to this module.
SECTION_WEIGHTS: dict[str, float] = {name: 1.0 for name in ALL_SECTIONS}

PLACEHOLDER_PATTERN = re.compile(
    r"\b(todo|tbd|tba|fixme|placeholder|lorem ipsum|xxx)\b", re.IGNORECASE
)


class SectionStatus(StrEnum):
    EMPTY = "empty"
    DRAFT = "draft"
    READY_FOR_REVIEW = "ready_for_review"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Section(BaseModel):
    """Uniform section model (D6-2)."""

    model_config = ConfigDict(extra="forbid")

    content: str = Field(default="", max_length=SECTION_MAX_CHARS)
    status: SectionStatus = SectionStatus.EMPTY
    confidence: Confidence | None = None
    sources: list[Annotated[str, StringConstraints(max_length=SOURCE_MAX_CHARS)]] = (
        Field(default_factory=list, max_length=MAX_SOURCES)
    )
    # Optional sections may be explicitly marked unknown (DEC-02);
    # the schema carries the flag uniformly, eligibility ignores it on
    # required sections.
    unknown: bool = False


class AipSections(BaseModel):
    """The full twelve-section document (D6-1 JSONB shape)."""

    model_config = ConfigDict(extra="forbid")

    core_identity: Section = Field(default_factory=Section)
    musical_identity: Section = Field(default_factory=Section)
    differentiation_hypothesis: Section = Field(default_factory=Section)
    artist_personality: Section = Field(default_factory=Section)
    brand_voice: Section = Field(default_factory=Section)
    audience_hypothesis: Section = Field(default_factory=Section)
    visual_direction: Section = Field(default_factory=Section)
    narrative_themes: Section = Field(default_factory=Section)
    do_and_avoid: Section = Field(default_factory=Section)
    origin_and_motivation: Section = Field(default_factory=Section)
    influence_map: Section = Field(default_factory=Section)
    unknowns_and_assumptions: Section = Field(default_factory=Section)

    def section(self, name: str) -> Section:
        return getattr(self, name)

    def total_content_chars(self) -> int:
        return sum(len(self.section(name).content) for name in ALL_SECTIONS)


def is_placeholder(content: str) -> bool:
    """Placeholder text never counts as complete (DEC-02)."""
    stripped = content.strip()
    if len(stripped) < SECTION_MIN_CONTENT_CHARS:
        return True
    return bool(PLACEHOLDER_PATTERN.search(stripped))


def section_complete(section: Section) -> bool:
    """DEC-02: schema-valid, non-placeholder, ready for review, with
    confidence and source metadata present."""
    return (
        section.status == SectionStatus.READY_FOR_REVIEW
        and not is_placeholder(section.content)
        and section.confidence is not None
        and len(section.sources) > 0
    )


def section_resolved_for_display(name: str, section: Section) -> bool:
    """Display treats an explicitly-unknown optional section as resolved;
    approval eligibility never does."""
    if name in OPTIONAL_SECTIONS and section.unknown:
        return True
    return section_complete(section)


def completeness(sections: AipSections) -> float:
    """DEC-02 formula: completed required weight over total required
    weight. Approval eligibility derives from this value alone."""
    total = sum(SECTION_WEIGHTS[name] for name in REQUIRED_SECTIONS)
    done = sum(
        SECTION_WEIGHTS[name]
        for name in REQUIRED_SECTIONS
        if section_complete(sections.section(name))
    )
    return done / total


def approval_eligible(sections: AipSections) -> bool:
    """Binary (DEC-02): 100% of required sections complete."""
    return completeness(sections) == 1.0


def display_percentage(sections: AipSections) -> float:
    """Broader display value including optional sections (DEC-02)."""
    total = sum(SECTION_WEIGHTS[name] for name in ALL_SECTIONS)
    done = sum(
        SECTION_WEIGHTS[name]
        for name in ALL_SECTIONS
        if section_resolved_for_display(name, sections.section(name))
    )
    return done / total


def size_violations(sections: AipSections) -> list[dict[str, str]]:
    """DEC-09 payload limits as AC-003-shaped detail dicts."""
    violations = [
        {
            "field": f"sections.{name}.content",
            "rule": "max_length",
            "message": (
                f"section exceeds {SECTION_MAX_CHARS} characters"
            ),
        }
        for name in ALL_SECTIONS
        if len(sections.section(name).content) > SECTION_MAX_CHARS
    ]
    if sections.total_content_chars() > TOTAL_MAX_CHARS:
        violations.append(
            {
                "field": "sections",
                "rule": "max_total_length",
                "message": f"profile exceeds {TOTAL_MAX_CHARS} characters in total",
            }
        )
    return violations


def incomplete_required_sections(sections: AipSections) -> list[str]:
    """The exact blocking list SCR-08 and approval errors show."""
    return [
        name
        for name in REQUIRED_SECTIONS
        if not section_complete(sections.section(name))
    ]


def _yaml_scalar(value: str) -> str:
    """Double-quote and escape a YAML scalar so untrusted section-derived
    values (the artist name) cannot break out of the front matter."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\n", " ").replace("\r", " ")
    return f'"{escaped}"'


def render_markdown(artist_name: str, sections: AipSections) -> str:
    """Render the draft as Markdown with YAML front matter (AC-005).

    One `##` heading per DEC-02 section in canonical order; no required
    section is omitted. Front-matter scalars are escaped; section bodies
    are the artist's own text, rendered verbatim under their heading (a
    draft preview, not sanitized HTML — the body is never executed).
    """
    eligible = approval_eligible(sections)
    percent = round(completeness(sections) * 100)
    lines = [
        "---",
        f"title: {_yaml_scalar(f'Artist Identity Profile — {artist_name}')}",
        f"artist: {_yaml_scalar(artist_name)}",
        f"completeness_percent: {percent}",
        f"approval_eligible: {str(eligible).lower()}",
        "kind: aip-draft-preview",
        "---",
        "",
    ]
    for name in ALL_SECTIONS:
        section = sections.section(name)
        lines.append(f"## {SECTION_TITLES[name]}")
        lines.append("")
        if name in OPTIONAL_SECTIONS and section.unknown:
            lines.append("_Marked unknown._")
        elif section.content.strip():
            lines.append(section.content.strip())
        else:
            lines.append("_Not yet provided._")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
