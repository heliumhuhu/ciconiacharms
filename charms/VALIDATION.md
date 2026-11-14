# CICONIA CHARMS v1.6.4 validation

Production build, JavaScript syntax, TypeScript and five unit tests pass. Targeted Chromium/SwiftShader tests cover 390/768/1440px: padded rack outline rejects background wheel events; frame samples confirm continued momentum after input ends and eventual settling; dropdown opening and closing animate; complete enlarged carton bounds fit; product media height is at least 280px; five plus presses save five, minus decrements, Undo preserves earlier units, zero disables minus, and no horizontal overflow or uncaught errors occur. Screenshots are inspected.

Offline standalone and fallback tests pass with networking disabled and zero HTTP(S) requests. Twenty rapid plus clicks produce exactly twenty units and rewards with one reusable feedback element. Direct file opening remains blocked by ERR_BLOCKED_BY_ADMINISTRATOR. Frame-sampled drag/save recovery and Escape interruption tests pass with the new counter and larger layout.

Tests use in-browser frame sampling rather than fixed automation delays for short animations. Earlier fixed-delay probes could miss completed animations; disclosure completion is read after the finish event. No physical mouse/trackpad hardware, Safari, Firefox or physical mobile testing was performed. Device feel is validated with synthetic wheel events, not a physical two-finger gesture. Other previous-release checks below were not rerun unless listed above.

## Previous release evidence (v1.6.3)

# CICONIA CHARMS v1.6.3 validation

Production build, JavaScript syntax and TypeScript checks passed; five mechanics/storage unit tests passed. Chromium uses the installed browser and SwiftShader; no physical device, Safari or Firefox testing is claimed.

The targeted focus suite exercises 390, 768 and 1440px, both packaging shapes and swing extremes: five clicks from zero show/store five, Undo retains four, refresh retains four, valid drags add one, repeated additions preserve identity, cancellation adds nothing, Escape restores the saved angle, independent list selection/search works, and page width does not overflow. Focus diagnostics require zero visible surrounding meshes. Screenshots are inspected at each width.

Frame-sampled save-sequence tests check exact grabbed-point anchoring, zero-scale relocation, stationary disappearance, reattachment on the original hook, unchanged UUID, blocked overlapping saves, latest-only Undo and Escape during dragging/disappearance/reappearance/invalid return. Reward calls are counted: one per completed addition and none for cancelled/invalid drops. Offline tests exercise twenty synchronous button clicks with twenty rewards, exactly twenty units, one reusable reward element, no overlapping reward animations and no deferred quantity mutation.

Interruption tests cover unfinished zoom, carton selection, keyboard suggestions, resize cancellation, invalid drops and My box editing. The older test's cached pre-scroll hit coordinates were corrected to query the current carton position. Geometry checks pass hook/rail attachment and clearance, collision checks and responsive bounds. Catalogue/fallback checks pass filtering, sorting, unknown prices, unavailable saved products, quantity cap and unavailable storage.

Offline standalone tests run the generated HTML with networking disabled, with zero HTTP(S) requests and no uncaught page errors, including WebGL-unavailable same-card saving. Direct file:// navigation is attempted separately; this environment blocks it with ERR_BLOCKED_BY_ADMINISTRATOR. Double-click local opening is not claimed as tested. Local-file persistence remains browser-dependent.

Screenshot inspection exposed mobile compositing clipping from an unnecessarily oversized idle canvas. The renderer now expands only while dragging or recovering, preserving the overlay while keeping idle focus inside a scene-sized canvas. A fresh mobile screenshot confirms the entire tag and bottom edge. Focus/save-sequence/offline checks are rerun after this correction.

The restoration regression passes exact original mesh visibility/material identity after exit and verifies a scene-sized idle canvas.

The old quantity-to-add selector and all prior blur requirements are superseded. Historical validation belongs to older releases; current results above describe this release only. Browser interaction suites not listed here were not rerun. No deployment or GitHub release is created. Prior release files and supplied assets remain unchanged.
