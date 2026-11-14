# CICONIA CHARMS v1.6.3 validation

Production build, JavaScript syntax and TypeScript checks passed; five mechanics/storage unit tests passed. Chromium uses the installed browser and SwiftShader; no physical device, Safari or Firefox testing is claimed.

The targeted focus suite exercises 390, 768 and 1440px, both packaging shapes and swing extremes: five clicks from zero show/store five, Undo retains four, refresh retains four, valid drags add one, repeated additions preserve identity, cancellation adds nothing, Escape restores the saved angle, independent list selection/search works, and page width does not overflow. Focus diagnostics require zero visible surrounding meshes. Screenshots are inspected at each width.

Frame-sampled save-sequence tests check exact grabbed-point anchoring, zero-scale relocation, stationary disappearance, reattachment on the original hook, unchanged UUID, blocked overlapping saves, latest-only Undo and Escape during dragging/disappearance/reappearance/invalid return. Reward calls are counted: one per completed addition and none for cancelled/invalid drops. Offline tests exercise twenty synchronous button clicks with twenty rewards, exactly twenty units, one reusable reward element, no overlapping reward animations and no deferred quantity mutation.

Interruption tests cover unfinished zoom, carton selection, keyboard suggestions, resize cancellation, invalid drops and My box editing. The older test's cached pre-scroll hit coordinates were corrected to query the current carton position. Geometry checks pass hook/rail attachment and clearance, collision checks and responsive bounds. Catalogue/fallback checks pass filtering, sorting, unknown prices, unavailable saved products, quantity cap and unavailable storage.

Offline standalone tests run the generated HTML with networking disabled, with zero HTTP(S) requests and no uncaught page errors, including WebGL-unavailable same-card saving. Direct file:// navigation is attempted separately; this environment blocks it with ERR_BLOCKED_BY_ADMINISTRATOR. Double-click local opening is not claimed as tested. Local-file persistence remains browser-dependent.

Screenshot inspection exposed mobile compositing clipping from an unnecessarily oversized idle canvas. The renderer now expands only while dragging or recovering, preserving the overlay while keeping idle focus inside a scene-sized canvas. A fresh mobile screenshot confirms the entire tag and bottom edge. Focus/save-sequence/offline checks are rerun after this correction.

The restoration regression passes exact original mesh visibility/material identity after exit and verifies a scene-sized idle canvas.

The old quantity-to-add selector and all prior blur requirements are superseded. Historical validation belongs to older releases; current results above describe this release only. Browser interaction suites not listed here were not rerun. No deployment or GitHub release is created. Prior release files and supplied assets remain unchanged.
