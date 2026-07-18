# Mock LLM Response Corpus

Location for mock-provider responses and recorded (redacted) provider
fixtures per the
[AI testing strategy](../../../docs/testing/ai-testing-strategy.md)
(Layers 1 and 2).

Populated from Phase 9: one subdirectory per prompt contract, each response
file named for its fault mode (`valid.json`, `malformed.json`,
`timeout.json`, ...) with the prompt version and model recorded alongside
each capture. Empty until then; do not invent fixtures before the contracts
exist.
