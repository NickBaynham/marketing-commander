// AIP section vocabulary for the UI (SCR-07/08). Mirrors the DEC-02
// section set and order defined authoritatively in the backend
// (apps/api/app/domain/aip.py); kept in sync by the shared golden-path
// E2E in Increment 6.4, which drives real sections through this list.
// Traceability: DEC-02; SCR-07, SCR-08.

export const REQUIRED_SECTIONS = [
  "core_identity",
  "musical_identity",
  "differentiation_hypothesis",
  "artist_personality",
  "brand_voice",
  "audience_hypothesis",
  "visual_direction",
  "narrative_themes",
  "do_and_avoid",
] as const;

export const OPTIONAL_SECTIONS = [
  "origin_and_motivation",
  "influence_map",
  "unknowns_and_assumptions",
] as const;

export const ALL_SECTIONS = [...REQUIRED_SECTIONS, ...OPTIONAL_SECTIONS];

export const SECTION_TITLES: Record<string, string> = {
  core_identity: "Core identity",
  musical_identity: "Musical identity",
  differentiation_hypothesis: "Differentiation hypothesis",
  artist_personality: "Artist personality",
  brand_voice: "Brand voice",
  audience_hypothesis: "Audience hypothesis",
  visual_direction: "Visual direction",
  narrative_themes: "Narrative themes",
  do_and_avoid: "Do and avoid guidance",
  origin_and_motivation: "Origin and motivation",
  influence_map: "Influence map",
  unknowns_and_assumptions: "Unknowns and assumptions",
};

export const OPTIONAL_SET = new Set<string>(OPTIONAL_SECTIONS);

export function percent(value: number): string {
  return `${Math.round(value * 100)}%`;
}
