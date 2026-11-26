# Ví dụ minh họa — UI-DEMO-001: list notes (hypothetical)

**Status:** DESIGN_ONLY; no screenshot or API implementation claimed.

| Element | Type | UI state | Event | Data origin |
|---|---|---|---|---|
| UI-DEMO-EL-001 | Search input | editable, disabled during submit if approved | UI-DEMO-EV-001 | local input |
| UI-DEMO-EL-002 | Note row | visible on success | UI-DEMO-EV-002 | API-DEMO-001 response |
| UI-DEMO-EL-003 | Retry button | visible only on network error | UI-DEMO-EV-003 | local error state |

## Event

`EV-001`: input changed → optional trim/debounce **if specified** → query → loading → data/empty/error; ignoring older responses on rapid input.

`EV-002`: row click → check route parameter → navigate to approved detail path, otherwise gate until destination confirmed.

`EV-003`: explicit retry → call same contract, show failure copy without inventing data.

## Test mapping

`EL-001 → EV-001 → API-DEMO-001 → TC-001 (success), TC-002 (error), TC-003 (stale)`.

No `screen-clean.png` or `screen-numbered.png` exists for this invented example. In actual DD, use real images with provenance or document `NO_VISUAL_SOURCE`.
