# ADR 0014: Web Portal Technology — React SPA

Date: June 2026

## Status

Accepted

Resolves the open question on web portal technology.

## Context

The web portal technology question was previously framed as a choice between
Blazor rendering models (WASM, Web App Auto, Server). That framing was
incorrect — it assumed a Blazor-first approach that was never agreed to. The
actual open question was the web portal technology, and React is the stated
preference.

The backend is a stateless ASP.NET Core API, established in an earlier
architectural decision. The portal is a separate client application that
calls this API over HTTP and consumes SSE streams for plan generation
progress, as introduced in another earlier decision. The portal technology
does not affect the backend in any way — the API is framework-agnostic by
design.

### Considered Options

1. **React SPA** — industry-standard, large ecosystem, framework-agnostic API
   consumption, strong SSE and MSAL.js support, straightforward Azure Static
   Web Apps deployment
2. Blazor — not evaluated; no agreement to use it was reached
3. Vue or Angular — viable alternatives to React; not evaluated

### Decision Factors

- React is the stated preference for the web portal
- SSE (`EventSource` API) is natively supported in all modern browsers; React
  integrates without additional libraries
- MSAL.js (`@azure/msal-react`) provides first-class Entra External ID
  integration for token acquisition
- The stateless API design aligns naturally with an SPA model — no
  server-side rendering is required

## Decision

The web portal is a React single-page application (SPA).

### Deferred Sub-Decisions (resolve before portal implementation begins)

- **Meta-framework**: plain React + Vite, or Next.js (static export mode)?
  Decide based on SEO requirements and deployment model.
- **Auth library**: `@azure/msal-react` (most direct Entra External ID
  integration) vs a third-party auth wrapper
- **Azure hosting target**: Azure Static Web Apps (free tier, built-in
  routing, GitHub Actions integration) vs Azure CDN + Blob Storage vs served
  from Container Apps — assess before provisioning infrastructure

## Consequences

**Positive**: clear technology choice enables portal implementation to start;
React ecosystem provides component libraries, routing, and state management
options; no Blazor runtime overhead.

**Negative**: introduces a JavaScript/TypeScript codebase alongside the .NET
backend — separate toolchain, separate CI job; the team must be comfortable
with both stacks.

### Risks Created

None.

### Review Date

June 2027 — reassess hosting target and meta-framework choice once portal
implementation is underway.
