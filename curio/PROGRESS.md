# Progress — Ciconia Charms 1.6.0

## Implemented

Recovered the editable source from the supplied v1.5.0 ZIP into the existing empty ciconiacharms checkout. The original release HTML and supplied ZIP are preserved. All supplied brand assets remain byte-identical. Package name/version changed without upgrading dependencies; lockfile dependency resolutions remain intact.

Replaced the obsolete product dialog and cloned scene with an integrated controller for the actual rack carton, existing perspective camera and renderer. The information card transforms in place. Per the owner's later correction, its description and single drag-saving area are now in the SAME card. The drag instruction is primary and the Add button is smaller and secondary, next to its quantity selector. Browsing has no saving controls.

Background cartons/rack blur progressively during focus, while the selected carton remains sharp. A compositing quad handles blur; it contains no duplicate product geometry. The same renderer extends across the card for dragging and return. The exact hit point remains the moving pivot, with shallow forward hook disengagement, restrained swing and damping. World transforms remain continuous during detachment/reparenting and return. Valid release adds one synchronously; cancellation and invalid drops add none. Return and settling block overlapping saves. Back reverses an unfinished camera transition, cancels unfinished gestures, preserves completed saves and restores the saved browsing angle without a new settle.

The monochrome redesign removes old gradients, grain overlays, fluting, glass effects and conflicting CSS. Near-horizontal perspective, responsive whole-carton framing, cropped desktop rack, full-width mobile rack and lower mobile information card replace the old composition. No reduced-motion setting disables animation or activates fallback.

Preserved 24 products, category-specific paperboard geometry, real slots/hooks, separate half-circle category sectors, indexed snapping, 250/8/140/380 input settings, independent list filtering/sorting, keyboard suggestions, My box editing, unknown-price semantics and safe local storage. The fallback uses the same information card and saving area with an image.

## Validation

See VALIDATION.md for executed checks. Chromium screenshots cover 390, 768 and 1440px; return diagnostics sample the same carton UUID and attachment state through the animation. The suites exercise reduced-motion emulation without disabling focus animations. Original logo files are byte-identical to the uploaded ZIP.

## Remaining limits

No physical touchscreen/trackpad, Safari or Firefox testing is claimed. Local-file persistence remains subject to browser policy. This environment blocks direct file:// navigation with ERR_BLOCKED_BY_ADMINISTRATOR; offline embedded-document and WebGL-fallback tests are used separately. Product data remains owner placeholders. Dragging on a very short viewport may require page scrolling to expose the target; the accessible button remains available. The hook-release motion is a geometric approximation, not a rigid-body collision simulation.

Live Vitsœ and Dieter Rams reference requests were blocked by network policy. No inspection or copying of those sites is claimed.

## Delivery and repository

CICONIA-CHARMS-v1.6.0.html and CICONIA-CHARMS-v1.6.0.zip are the renamed release artifacts. The owner's later instruction authorizes a commit and push to heliumhuhu/ciconiacharms. No deployment or GitHub release is authorized or performed. Actual push evidence is reported in chat after completion.
