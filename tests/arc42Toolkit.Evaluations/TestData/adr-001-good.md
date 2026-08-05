# Use PostgreSQL as the Primary Datastore

## Status

Accepted

## Context

The team is building a multi-tenant SaaS backend that needs to support
complex relational queries across tenants, strong transactional guarantees
for billing data, and a mature ecosystem of tooling for migrations,
backups, and observability. The current prototype uses an in-memory
store, which does not survive restarts and cannot be used beyond a demo.
We evaluated the problem against expected data volume (low millions of
rows per tenant within the first two years) and a small team with limited
capacity to operate exotic infrastructure.

Three options were evaluated. MongoDB was considered, since some team
members had prior experience with it, but the domain model is highly
relational (accounts, invoices, line items, audit trails) and using it
would have meant reimplementing transactional guarantees and joins in
application code. A separate database per tenant was considered as the
simplest isolation model, but the operational overhead of running and
migrating hundreds of individual databases was judged too high for a
two-person infrastructure team. DynamoDB was considered for its managed
scaling story, but its access-pattern-first modeling would have required
redesigning the domain model around denormalized views, and the team has
no prior operational experience with it.

## Decision

We will use PostgreSQL (managed via a cloud provider's RDS-equivalent
offering) as the primary datastore for all transactional application
data. Schema migrations will be managed through a version-controlled
migration tool, and each tenant's data will be isolated using row-level
security rather than separate databases per tenant.

## Consequences

Strong ACID guarantees simplify reasoning about billing and account
state changes, and mature tooling (migrations, connection pooling,
backup/restore, point-in-time recovery) reduces operational risk for a
small team. Row-level security lets us keep a single schema and single
connection pool while still enforcing tenant isolation at the database
layer, and team members already have production experience with
PostgreSQL, reducing onboarding time.

On the other hand, vertical scaling limits mean we will need to plan for
read replicas or sharding if a single tenant grows far beyond initial
projections. Row-level security policies add complexity to every query
path and must be covered by tests to avoid accidental cross-tenant data
leaks. We also take on a dependency on the cloud provider's managed
PostgreSQL offering, which affects portability if we ever need to
migrate providers — a cost we accepted in exchange for avoiding the
per-tenant operational burden of the rejected alternatives above.
