# Validation — Ciconia Charms 1.6.0

## Executed

- `npm ci`: lockfile-based dependency installation; no dependency upgrades.
- `npm test`: all four mechanics/storage tests passed.
- `npm run typecheck`, `npm run check`, `npm run build`: passed.
- `tests/browser.py`: Chromium at 390, 768 and 1440px; fixed browsing camera, category/front-card matching, keyboard selection, free drag, hold-stop/resume and wheel settling passed.
- `tests/geometry.py`: hook/rail clearance, real slot attachment, category finishes and no carton intersections at shared swing extremes passed. Whole browsing-carton bounds fit at all three widths and both permitted swing extremes.
- `tests/focus.py`: source-server checks passed at all widths. Production-server checks also passed at all three widths, including repeated saves and pointer cancellation. Checks include full focused carton bounds for jewellery and toys, same-card single target, no old modal, no browsing saving controls, reduced-motion rendering, precise grabbed-point constraint, actual carton identity/attachment after return, button quantity/Undo, valid and cancelled saves, exact exit angle, refresh persistence and list search/reset.
- `tests/interruptions.py`: reversing zoom-in, clicking the actual carton, exact keyboard search selection, invalid drop, resizing during drag, leaving during return while preserving the completed save, and My box editing passed.
- `tests/standalone.py`: embedded HTML with networking disabled passed, with 24 cartons, focus, multi-unit saving, Undo and Back. WebGL-unavailable mode passed using the same information/saving card. No HTTP(S) requests or JavaScript errors.
- Direct `file://` opening was attempted and blocked by the environment's `ERR_BLOCKED_BY_ADMINISTRATOR` policy. Double-click opening is not claimed as tested.
- Screenshots inspected at all three widths, including both category packaging shapes, blur, complete carton framing and dragging over the target. Time-sampled return diagnostics track the same carton UUID, bounds and attachment state.
- Brand files compared byte-for-byte against the supplied original ZIP. Catalogue, bag/storage module and centralized motion settings are also unchanged.

## Not tested / limitations

Physical touchscreen/trackpad feel, Safari, Firefox, and low-powered device performance have not been tested. Browser-local persistence can be unavailable for file URLs. Very short viewports may require scrolling to expose the target; button saving remains available. Hook release is a restrained geometric animation, not a collision-solver simulation.

Live design-reference requests to https://www.vitsoe.com and https://www.dieter-rams.org were denied by network policy (HTTP 403). No live inspection is claimed. The applied visual principles are a restrained monochrome palette, sparse rules, whitespace, a clear type hierarchy and separation of primary drag interaction from secondary button controls.
