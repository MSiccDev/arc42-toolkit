# ADR 0012: Cloud Platform Selection — Azure

Date: June 2026

## Status

Accepted

## Context

An earlier open question identified Azure as the strongly preferred cloud
platform but left the decision unconfirmed. The async plan generation design,
established in an earlier architectural decision, requires an API host, job
queue, background worker, and persistent job state store — all of which need
a concrete infrastructure target. The platform specification intentionally
stays cloud-neutral at requirement level; this ADR owns the infrastructure
decision.

### Considered Options

1. AWS (ECS + RDS + SQS) — technically viable; weaker .NET integration story;
   no Managed Identity equivalent
2. Google Cloud Run + Cloud SQL — viable for containers; fewer first-party
   .NET SDK integrations
3. Azure App Service (instead of Container Apps) — simpler but no native KEDA
   queue-based scaling for the worker
4. Azure Service Bus (instead of Storage Queue) — advanced routing and
   ordering guarantees not needed for single-consumer sequential jobs; higher
   cost
5. Cosmos DB (instead of Azure SQL) — document scale not needed; relational
   model fits the data better
6. Azure OpenAI Service (instead of direct HTTP) — adds EU data residency;
   introduces deployment overhead; deferred until regulatory requirement
   arises

### Decision Factors

- .NET 10 / ASP.NET Core / EF Core has first-class Azure integration (Managed
  Identity, Azure SDK, `dotnet publish` targets)
- Container Apps + KEDA provides native queue-triggered autoscaling with
  scale-to-zero at no extra configuration cost
- Azure SQL serverless auto-pauses during pre-MVP development, minimising
  cost; switches to provisioned tier before launch
- Entra External ID free tier covers the entire pre-MVP user base
- Storage Queue is sufficient and cheaper than Service Bus for this workload
  shape

## Decision

Azure is confirmed as the production cloud platform. The following service
mapping applies:

| Infrastructure need | Azure service | Rationale |
|---|---|---|
| API host | Azure Container Apps (Consumption plan) | Stateless, scales to zero, satisfies the statelessness requirement; no cluster management overhead |
| Job queue | Azure Storage Queue | Simple FIFO, at-least-once delivery; sufficient for single-consumer sequential workload |
| Background worker | Azure Container Apps Job (event-driven) | KEDA queue-based trigger; runs to completion and exits; no hard timeout |
| Persistent storage | Azure SQL + EF Core (General Purpose, serverless pre-MVP) | Relational model fits family profiles and job state; EF Core already targets SQL Server |
| Auth / identity | Microsoft Entra External ID | MAU-based pricing; first 50,000 MAU free; supports social login for future iOS path |
| AI providers | Direct HTTP to OpenAI / Mistral | No Azure AI wrapper; provider adapters already implemented; data residency not a current requirement |

### Implementation Notes

Web portal hosting target (Azure Static Web Apps vs Container Apps vs CDN) is
deferred to the portal implementation phase — see
[0014](0014-web-portal-technology-react-spa.md) and the related open question
on portal technology.

## Consequences

**Positive**: lowest-friction deployment for the .NET stack; Managed Identity
removes credential management; scale-to-zero on both API and worker keeps
pre-MVP costs near zero.

**Negative**: Azure-specific tooling required for infrastructure provisioning
(Bicep / Azure CLI); portability to other clouds requires re-mapping the
service layer.

### Known Limitations (revisit triggers)

- If EU data residency is required for AI calls → evaluate Azure OpenAI
  Service as a proxy
- If throughput outgrows Storage Queue limits → evaluate Azure Service Bus
  Premium
- If multi-region deployment is required → revisit Azure SQL geo-replication
  and Container Apps multi-region environments

### Risks Created

None — the earlier risk of an unfinalised cloud platform is now resolved by
this decision.

### Review Date

December 2027 — reassess service tiers, pricing, and web portal hosting
target after [0014](0014-web-portal-technology-react-spa.md)'s sub-decisions
are resolved.
