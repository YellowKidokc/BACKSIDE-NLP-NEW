# Architecture

This repo separates two views:

## Internal Schema

The internal schema is the station graph behind the NLP/model layer.

```text
Intake -> Transform -> Validate -> Route -> Signals
```

This is for builders and AI partners.

## Consumer Front End

The consumer front end should stay simple:

- Drop something in.
- See what it became.
- Review what needs a decision.
- See what is ready.
- See where it went.
- See what the system needs next.

Consumer-facing workflows should expose folders and scripts, not the whole machine room.
