# ADR 0003: OpenAI API as Primary AI Provider

Date: March 2025

## Status

Accepted

Superseded in part by a later ADR that names the specific production models.

## Context

- Need for intelligent, context-aware meal plan generation
- Requirement for structured responses via function calling
- Family-specific customisation and cultural preferences
- Natural language recipe instructions and ingredient lists

### Considered Options

1. OpenAI GPT-4 — leading LLM with function calling capabilities
2. Anthropic Claude — alternative LLM with strong reasoning
3. Local AI models — self-hosted for data privacy
4. Rule-based system — traditional algorithmic approach
5. Multiple provider support — abstract interface with multiple implementations

### Decision Factors

- Quality: output quality for meal planning and nutrition content
- Function calling: structured response format for consistent data
- Cultural knowledge: understanding of diverse cuisines and dietary restrictions
- API stability: reliable service availability and performance
- Cost: token usage costs for typical family meal planning scenarios

## Decision

Use OpenAI API as the primary AI service for meal plan generation, with an
abstraction layer for future provider additions.

### Implementation Notes

- `IChatService` abstraction allows future provider implementations
- HTTP client with Polly for resilience (retry, circuit breaker)
- Secure storage for API keys via platform-specific mechanisms
- Function calling with JSON schemas for structured responses

## Consequences

**Positive**: high-quality contextually relevant meal plans; function calling
enables structured JSON responses; strong understanding of nutrition and
dietary restrictions; reliable API.

**Negative**: dependency on external service; API costs scale with usage; data
privacy considerations; vendor lock-in without abstraction layer.

### Risks Created

Mistral function-calling compatibility remains unverified.

### Review Date

June 2026
