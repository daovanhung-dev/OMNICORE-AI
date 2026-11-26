# UI elements, markers and state matrix

## Marker mapping

Screen ID must be unique, e.g. `UI-001`. Number visible elements left-to-right, top-to-bottom with stable marker `#n`; `#n → UI-001-EL-001`. For repeated cards of same behavior, group unless individually different.

`EL ID | Marker | Type | Label | Data source | Visible condition | Enable condition | Event | Screen state`.

- A “clean” screenshot and numbered variant represent one **visual state**, not the full state machine.
- If real screenshot/HTML/asset provenance missing, record `NO_VISUAL_SOURCE`; do not fabricate visual evidence.
- For each page/dialog/tab, define states as relevant: `INIT → LOADING → SUCCESS | EMPTY | ERROR | UNAUTHORIZED | OFFLINE`; mutation states `IDLE → SUBMITTING → SUCCESS/ERROR`.
- Accessibility: keyboard, focus, alt text, aria semantics, touch target; responsive layout at defined breakpoints where project rules exist.
- Disabled/gated actions must explain why. Do not show fictitious saved-state or unread counts.
