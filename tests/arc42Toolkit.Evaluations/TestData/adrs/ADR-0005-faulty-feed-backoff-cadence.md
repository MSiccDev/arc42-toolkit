# ADR-0005: Faulty-Feed Backoff Cadence

- Status: Accepted
- Date: 2026-03-13

## Context

The application already defines when a feed becomes visibly faulty, but the retry cadence after repeated failures is still open.

Without an explicit policy, refresh behavior, feed-health state, and future background refresh design remain underspecified.

## Decision

The application owns a stepped retry policy for transient feed refresh failures.

- Only `transport failure` and `parse failure` count toward the transient failure ladder.
- `invalid payload` and `unsupported feed` mark a feed faulty immediately, do not increment the transient failure counter, and are retried only by explicit manual action.
- Manual refresh bypasses backoff once for the targeted feed or feeds, but only a successful refresh clears faulty state and resets counters.
- The retry ladder is 15 minutes after the first counted failure, 1 hour after the second, 6 hours after the third, and 24 hours after the fourth and later counted failures.
- A feed becomes visibly faulty after the third consecutive counted failure and remains on the capped retry interval until a successful refresh resets it.

## Consequences

Positive:

- Feed-health behavior is predictable and easy to document.
- Transient failures are handled differently from known-bad content.
- Manual recovery stays available without weakening automatic retry policy.

Negative:

- Refresh metadata now needs more explicit state and timing coverage.
- Later background refresh work must align with the documented cadence rather than inventing a new policy.

Follow-up:

- Keep runtime examples, operational metadata details, and remaining background refresh questions in arc42 instead of expanding this ADR.
