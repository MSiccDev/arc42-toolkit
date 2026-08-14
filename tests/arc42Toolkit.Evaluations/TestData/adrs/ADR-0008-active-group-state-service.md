---
title: "ADR-0008: Active Group State Service"
status: "Accepted"
date: "2026-06-06"
tags: ["architecture", "decision", "application-layer", "state"]
supersedes: ""
superseded_by: ""
---

# ADR-0008: Active Group State Service

## Status

Accepted

## Context

The group navigation feature requires the main feed list view model to know which group is currently active and to update that identity when the user switches groups via previous/next controls.

The group-activation refresh and app-resume refresh features also need the active group identity — and they need it from the application lifecycle layer, not from the view model. An earlier architectural decision explicitly states that presentation decides which group is active, and application decides staleness and eligibility. For that split to hold, the active group identity must be accessible to the application layer without coupling it to a specific view model instance.

Storing the active group identity only in the view model would mean refresh trigger logic in those features must reach into the UI layer to read it — a Clean Architecture violation. Passing it as a navigation parameter on every switch is workable for the view, but provides no stable reference point for application-layer refresh decisions.

## Decision

The application introduces a thin singleton application-layer service, `IActiveGroupState`, that holds the currently active group identity.

- `IActiveGroupState` is defined in the Application layer as a port.
- It exposes a single `Guid? ActiveGroupId` property and a changed notification.
- The view model writes to it when the active group changes (on navigation, on switch).
- The group-activation refresh and app-resume refresh features read from it to determine the active group scope without touching the UI layer.
- The service holds no business logic — it is a lightweight shared state holder only.
- It is registered as a singleton in the DI container.

## Consequences

### Positive

- **POS-001**: Refresh trigger logic in the group-activation and app-resume refresh features can read active group identity without coupling to any view model.
- **POS-002**: Preserves the earlier decision's split: presentation owns which group is active; application owns eligibility and staleness decisions.
- **POS-003**: The view model stays thin — it delegates active-group tracking to the service rather than managing it as private state.
- **POS-004**: The service is easy to test in isolation; both the view model and refresh trigger logic can substitute it via the port.

### Negative

- **NEG-001**: Introduces shared mutable singleton state — requires discipline to keep it thin and prevent it from growing into a god object.
- **NEG-002**: One more DI registration and port interface to maintain.
- **NEG-003**: Changed notification wiring must be handled carefully to avoid memory leaks in long-lived view models.

## Alternatives Considered

### View Model Property Only (Option 1)

- **ALT-001**: **Description**: `ActiveGroupId` is a property on the main feed list view model, set from navigation parameters and updated on switch.
- **ALT-002**: **Rejection Reason**: The group-activation and app-resume refresh features need active group identity from the application layer. Accessing it from the view model would couple refresh trigger logic to the UI layer, violating Clean Architecture boundaries.

### Navigation Parameter Only (Option 3)

- **ALT-003**: **Description**: Active group identity is always passed as a navigation parameter; no state is held between navigations.
- **ALT-004**: **Rejection Reason**: Stateless for the view, but provides no stable reference for the refresh features to read between navigation events. Becomes increasingly awkward as more lifecycle-aware refresh triggers are added.

## Implementation Notes

- **IMP-001**: Define `IActiveGroupState` in `Application/Ports/` alongside the repository ports.
- **IMP-002**: Keep the interface minimal: `Guid? ActiveGroupId { get; set; }` plus a changed event or observable. Do not add methods or business logic.
- **IMP-003**: Register the concrete implementation as a singleton in the app's startup composition root; the interface is the only thing the view model and application layer should reference.
- **IMP-004**: The group-activation and app-resume refresh features should read `IActiveGroupState.ActiveGroupId` via constructor injection — not from any view model directly.

## References

- **REF-001**: An earlier architectural decision on the refresh trigger model and background refresh, which defines the presentation/application split for trigger ownership
- **REF-002**: The group-switching use case documentation
- **REF-003**: The implementation backlog entries for group-activation refresh and app-resume refresh
