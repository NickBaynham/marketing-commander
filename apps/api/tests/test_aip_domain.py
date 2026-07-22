"""AIP schema and completeness engine unit tests (DEC-02).

Fixtures per the Test Data Strategy: minimal valid, complete valid,
incomplete, adversarial (files) and oversized (factory, to keep a 20k+
character blob out of the repository).

Traceability: REQ-006..REQ-011, REQ-045; AC-004; BR-002; DEC-02,
DEC-09; D6-1, D6-2, D6-4.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.domain.aip import (
    ALL_SECTIONS,
    OPTIONAL_SECTIONS,
    REQUIRED_SECTIONS,
    SECTION_MAX_CHARS,
    SECTION_WEIGHTS,
    AipSections,
    Confidence,
    Section,
    SectionStatus,
    approval_eligible,
    completeness,
    display_percentage,
    incomplete_required_sections,
    is_placeholder,
    section_complete,
    size_violations,
)

FIXTURES = Path(__file__).parent / "fixtures"


def load(name: str) -> AipSections:
    return AipSections.model_validate(
        json.loads((FIXTURES / f"{name}.json").read_text())
    )


def complete_section() -> Section:
    return Section(
        content="Long enough real content describing the artist in detail here.",
        status=SectionStatus.READY_FOR_REVIEW,
        confidence=Confidence.MEDIUM,
        sources=["artist interview"],
    )


def oversized_sections() -> AipSections:
    """Oversized fixture (factory): one section over the per-section cap
    is impossible to construct through the schema, so the factory builds
    a schema-valid document that breaches the TOTAL cap instead."""
    block = "x" * SECTION_MAX_CHARS
    return AipSections.model_validate(
        {
            name: {
                "content": block,
                "status": "ready_for_review",
                "confidence": "low",
                "sources": ["s"],
            }
            for name in ALL_SECTIONS
        }
    )


# Schema (D6-2)


def test_section_lists_match_dec02():
    assert len(REQUIRED_SECTIONS) == 9
    assert len(OPTIONAL_SECTIONS) == 3
    assert set(ALL_SECTIONS) == set(AipSections.model_fields)


def test_fixtures_parse():
    for name in ("aip_minimal_valid", "aip_complete_valid", "aip_incomplete"):
        assert isinstance(load(name), AipSections)


def test_adversarial_fixture_is_plain_data():
    sections = load("aip_adversarial")
    assert "<script>" in sections.core_identity.content
    assert sections.core_identity.status == SectionStatus.READY_FOR_REVIEW


def test_unknown_fields_rejected():
    with pytest.raises(ValidationError):
        AipSections.model_validate({"core_identity": {"content": "x", "extra": 1}})
    with pytest.raises(ValidationError):
        AipSections.model_validate({"not_a_section": {}})


def test_section_content_cap_enforced_by_schema():
    with pytest.raises(ValidationError):
        Section(content="x" * (SECTION_MAX_CHARS + 1))


def test_source_caps():
    with pytest.raises(ValidationError):
        Section(sources=["x" * 501])
    with pytest.raises(ValidationError):
        Section(sources=["s"] * 21)


# Placeholder detection (DEC-02)


@pytest.mark.parametrize(
    "content",
    [
        "",
        "   ",
        "short",
        "TODO: write the core identity section for this artist later",
        "This is tbd until the manager decides on final positioning.",
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do.",
        "Section pending XXX final review from the whole creative team.",
    ],
)
def test_placeholder_content(content):
    assert is_placeholder(content) is True


def test_real_content_is_not_placeholder():
    assert is_placeholder(complete_section().content) is False


# Section completeness (DEC-02 legs)


def test_complete_section_passes():
    assert section_complete(complete_section()) is True


@pytest.mark.parametrize(
    "mutation",
    [
        {"status": SectionStatus.DRAFT},
        {"content": "TODO fill this in with something meaningful for the artist"},
        {"confidence": None},
        {"sources": []},
    ],
)
def test_each_incomplete_leg_fails(mutation):
    section = complete_section().model_copy(update=mutation)
    assert section_complete(section) is False


# Completeness, eligibility, display (DEC-02 formula; D6-4 weights)


def test_weights_cover_all_sections_positively():
    assert set(SECTION_WEIGHTS) == set(ALL_SECTIONS)
    assert all(weight > 0 for weight in SECTION_WEIGHTS.values())


def test_empty_draft_scores_zero_and_ineligible():
    sections = AipSections()
    assert completeness(sections) == 0.0
    assert approval_eligible(sections) is False
    assert incomplete_required_sections(sections) == list(REQUIRED_SECTIONS)


def test_minimal_valid_is_eligible():
    sections = load("aip_minimal_valid")
    assert completeness(sections) == 1.0
    assert approval_eligible(sections) is True
    assert incomplete_required_sections(sections) == []


def test_incomplete_fixture_scores_fraction_and_names_blockers():
    sections = load("aip_incomplete")
    assert completeness(sections) == pytest.approx(6 / 9)
    assert approval_eligible(sections) is False
    assert incomplete_required_sections(sections) == [
        "visual_direction",
        "narrative_themes",
        "do_and_avoid",
    ]


def test_eligibility_is_binary_not_threshold():
    sections = load("aip_minimal_valid")
    sections.do_and_avoid.status = SectionStatus.DRAFT
    assert completeness(sections) == pytest.approx(8 / 9)
    assert approval_eligible(sections) is False


def test_optional_sections_do_not_affect_eligibility():
    sections = load("aip_minimal_valid")
    assert sections.influence_map.status == SectionStatus.EMPTY
    assert approval_eligible(sections) is True


def test_display_includes_optional_and_unknown_counts_as_resolved():
    minimal = load("aip_minimal_valid")
    assert display_percentage(minimal) == pytest.approx(9 / 12)
    complete = load("aip_complete_valid")
    assert complete.unknowns_and_assumptions.unknown is True
    assert display_percentage(complete) == 1.0


def test_unknown_on_required_section_does_not_count():
    sections = AipSections()
    sections.core_identity.unknown = True
    assert completeness(sections) == 0.0
    assert display_percentage(sections) == 0.0


# Size limits (DEC-09, REQ-045)


def test_no_size_violations_on_valid_fixture():
    assert size_violations(load("aip_complete_valid")) == []


def test_total_size_violation_shape():
    violations = size_violations(oversized_sections())
    assert {
        "field": "sections",
        "rule": "max_total_length",
    }.items() <= violations[-1].items()


def test_section_size_violation_shape():
    sections = AipSections()
    # Bypass schema validation deliberately to exercise the guard the
    # API applies before persistence.
    object.__setattr__(
        sections.core_identity, "content", "x" * (SECTION_MAX_CHARS + 1)
    )
    violations = size_violations(sections)
    assert violations[0]["field"] == "sections.core_identity.content"
    assert violations[0]["rule"] == "max_length"
