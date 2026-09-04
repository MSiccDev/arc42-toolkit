# ADR-0001: Extract the AI Evaluation Prototype into a Distributable .NET CLI Tool

**Status:** Proposed

## Context

During a personal learning exercise on `Microsoft.Extensions.AI.Evaluation`, an
`AdrCompletenessEvaluator` was built — an LLM-as-judge custom `IEvaluator` that
scores Architecture Decision Records against a four-criterion rubric (context,
decision, consequences, alternatives considered). It runs against a golden
dataset of real and synthetic ADR fixtures with calibrated expected-score bands,
and judges via a locally hosted Ollama model through the standard
`IChatClient` abstraction. The evaluator currently lives entirely inside
`tests/arc42Toolkit.Evaluations` as an xUnit test project — an internal
quality-regression harness, not something toolkit consumers can invoke.

Separately, arc42-toolkit already ships `arc42-lint`: a markdown skill that
wraps `scripts/arc42-lint.py`, checking whether the script is present, running
it if so, and falling back to applying the same rules manually and
conversationally if the script is absent. This establishes a working precedent
for delivering non-markdown capabilities to consumers of a toolkit that is
otherwise entirely markdown-based, without requiring a runtime dependency for
the base experience.

The repository's `dotnet-tools.json` already references Microsoft's own
evaluation reporting CLI (`microsoft.extensions.ai.evaluation.console` /
`aieval`), so a distributable .NET companion tool is not a foreign concept in
this codebase's existing tooling story.

arc42-toolkit's core positioning is provider-agnostic: skills are markdown
files invoked as slash commands, usable from any AI coding tool capable of
reading markdown (Claude Code, GitHub Copilot, Cursor, Codex, and others), with
no runtime dependency required for most of the toolkit's functionality.

Given these three facts together — a validated evaluator, a proven
script-plus-fallback distribution pattern, and a provider-agnostic design
constraint the tool must respect — there is a genuine opportunity: a
consumer-facing evaluation engine, backed by a real distributable .NET tool,
following the same two-layer pattern already proven by `arc42-lint`.

ADR completeness is the first evaluator, not the only one. arc42-toolkit
already documents ten other sections beyond ADRs, each with its own notion of
"good" — Section 10 quality scenarios need measurable, non-vague criteria;
Section 5 building block descriptions need to stay consistent with the actual
source structure; Section 3 context diagrams need every documented interface
to have a corresponding real integration. Each of these is a plausible future
evaluator with its own rubric, in the same shape as `AdrCompletenessEvaluator`.
The tool is being built to grow into that suite over time, evaluator by
evaluator, as each section's quality criteria are worth automating.

## Decision

Extract the evaluation logic out of `tests/` into a standalone library (e.g.
`src/Arc42Toolkit.Evaluation`) plus a CLI entry point, packaged and distributed
as a dotnet tool — consistent with the precedent already set by Microsoft's own
`aieval` tool referenced in this repository.

The existing `IChatClient`-based judge configuration will be exposed as
user-facing configuration (environment variables or a config file), supporting
multiple providers — OpenAI, Azure OpenAI, Anthropic, and local
OpenAI-compatible endpoints such as LM Studio — preserving the toolkit's
provider-agnostic positioning without requiring a redesign of the underlying
abstraction.

The CLI will be wrapped in a markdown skill (e.g. `arc42-eval-adr`) that
mirrors `arc42-lint`'s check-run-fallback pattern: check whether the tool is
installed, run it if present, and fall back to a manual conversational rubric
pass if absent — so the base skill experience continues to require no runtime
dependency.

A registry or plugin system for selecting between multiple evaluator types
will **not** be built in this first iteration — not because a growing suite of
evaluators isn't the goal, but because only one evaluator (ADR completeness)
currently exists, which is insufficient signal to design a good extension
point. `Microsoft.Extensions.AI.Evaluation` already supports composing
multiple evaluators as a plain list passed into a `ReportingConfiguration`;
that composition mechanism is sufficient for a second and third evaluator
without any bespoke registry of our own. A dedicated selection mechanism
(CLI flags to choose which evaluator(s) to run, evaluator discovery, per-scope
defaults) will be designed once at least two real evaluators exist to compare
— so the abstraction reflects actual variation between evaluator types instead
of a guess made from a single example.

This work is scoped as a separate initiative from the current learning
exercise, to begin after the DevDay session at which this prototype is
presented, not before.

## Consequences

**Positive:**
- Reuses an already-validated two-layer distribution pattern (`arc42-lint`),
  minimizing new architectural risk.
- The existing `IChatClient` abstraction already satisfies the
  provider-agnostic requirement with minimal additional work — no fundamental
  redesign is needed for judge configuration, only user-facing exposure of an
  existing seam.
- Gives toolkit consumers a genuinely new, high-value capability — automated
  ADR quality regression checking today, with a clear path to per-section
  quality checks across the rest of arc42 documentation — consistent with the
  toolkit's existing quality-tooling story (`arc42-lint`, `arc42-review`).
- Growing the evaluator suite incrementally, one real evaluator at a time,
  avoids locking in an extension design before enough evaluators exist to
  know what actually needs to vary between them.
- Demonstrates the toolkit evaluating its own architecture decisions with its
  own tooling.

**Negative / risks:**
- Introduces a new maintenance surface: a distributable dotnet tool requires
  versioning, packaging, and release discipline beyond what a markdown-only
  skill requires.
- Multi-provider judge configuration increases support burden — credential
  handling, endpoint validation, and differing model capabilities across
  providers all need to be accounted for.
- Deferring the selection/registry mechanism means each new evaluator added
  before that mechanism exists requires a small amount of manual wiring
  (adding it to the composed evaluator list, adding its fixtures) rather than
  a plug-and-play extension point. This is an accepted, temporary cost while
  the suite is still small.
- Adds a runtime dependency (a distributable dotnet tool and its configured
  LLM judge) to a toolkit that has otherwise been entirely markdown-based and
  dependency-light. The check-run-fallback pattern must be implemented
  faithfully to preserve the toolkit's core positioning, not treated as
  optional polish.

## Alternatives Considered

**Keep the evaluator permanently internal (status quo).** Rejected — leaves a
validated, reusable capability unused by consumers, and does not build on the
precedent that already justifies productizing it.

**Ship a static, read-only rubric checklist instead of a live LLM-judged
tool.** Rejected — loses the actual quality signal an LLM judge provides over
a self-applied checklist, and would functionally duplicate what
`arc42-review`'s manual fallback already offers.

**Build the full evaluator registry/plugin system immediately, alongside the
CLI.** Rejected for now, not permanently — premature abstraction with only one
real evaluator implemented so far; risks over-engineering extension points
before understanding what actually varies across evaluator types. Revisit once
a second evaluator (e.g. a Section 10 quality-scenario checker) exists.

**Hardcode the tool to a single LLM provider (e.g. OpenAI only) rather than
building pluggable configuration.** Rejected — directly conflicts with the
toolkit's provider-agnostic positioning, a foundational design constraint that
applies across every skill in the toolkit.