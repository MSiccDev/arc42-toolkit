# Use Redis for Session Storage

## Status

Accepted

## Context

The application currently stores user session state in memory on each
application server instance. This breaks horizontal scaling because a
user's session is pinned to whichever server first handled their login,
and it loses all sessions on every deploy. We need a shared, external
store for session data that all application instances can read from and
write to, with low latency since session lookups happen on nearly every
request.

## Decision

We will use Redis as a shared session store. Each application instance
will read and write session data to a single Redis cluster over the
internal network, with session keys expiring automatically via Redis
TTLs to match our session timeout policy.

## Consequences

Sessions survive application deploys and restarts, since they no longer
live in per-instance memory. Any application instance can serve any
user's request, which removes the need for sticky sessions at the load
balancer. Redis's built-in key expiry maps directly onto our session
timeout requirement without extra cleanup jobs.

The application now has a hard runtime dependency on Redis being
available; a Redis outage means users cannot stay logged in. We must
operate and monitor an additional piece of infrastructure. Session data
is no longer colocated with the process handling the request, adding a
small amount of latency to every request.
