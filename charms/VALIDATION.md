# Validation — Ciconia Charms 1.6.1

## Executed checks

- `npm ci --cache /tmp/ciconia-npm-cache`: passed from the renamed `charms/` source directory. Dependency resolutions match 1.6.0; only package release versions changed.
- `npm test`: five mechanics/storage tests passed, including legacy quantity migration and current-key precedence.
- `npm run check`, `npm run typecheck`, `npm run build`: passed. Syntax covers the application controllers; the repository typecheck covers catalogue, bag and motion modules.
- `tests/browser.py`: Chromium at 390, 768 and 1440px passed. Includes actual snap positions, front/card/category consistency, fixed browsing camera, pointer drag, stationary hold, movement after hold, wheel quiet settling and keyboard input.
- `tests/geometry.py`: passed actual hook/rail contact, slot/attachment clearance, no carton intersections at shared swing extremes, and complete browsing-carton bounds at all three widths.
- `tests/focus.py`: Chromium source and production workflows passed at all three widths. Tests cover integrated same-card saving, no old modal or browsing saving controls, full jewellery/toy bounds, precise grabbed point, same carton UUID/reattachment, repeated one-unit saves, cancellation, quantity button/Undo, exact exit angle, refresh persistence and exact list identity. The final production run additionally checks focused bounds at ±0.14 radians for both packaging shapes at every width. Reduced-motion emulation retains animations.
- `tests/interruptions.py`: passed reversing unfinished zoom, actual-carton selection, keyboard suggestion identity, invalid drop, resizing during drag, completed-save preservation on exit and grouped My box editing.
- `tests/save-sequence.py`: passed frame-sampled disappearance/reappearance and zero-scale relocation checks, same object UUID, exact grabbed-point constraint, no visible travel home during disappearance, busy-button blocking, one completed addition, latest-action Undo, and Escape during dragging, disappearance, reappearance and invalid return. Recovery checks require original attachment, unit scale, visibility, exact saved angle/camera and the same UUID. Diagnostics confirm 23 other blur groups and a sharp selected hook.
- `tests/catalogue.py`: passed combined search/category/name/price controls, counts, unknown-price notice, reset/no-results, exact selected identity, same-card fallback saving, quantity cap, Undo of the actual added amount, unavailable saved rows and unavailable-storage operation.
- `tests/standalone.py`: passed embedded HTML with Chromium networking disabled and zero HTTP(S) requests; 24 WebGL cartons, focus, two-unit button save, Undo and Back. WebGL-unavailable fallback passed using the same card and saving area.
- Direct `file://` navigation was attempted and blocked by `ERR_BLOCKED_BY_ADMINISTRATOR`. Double-click opening is not claimed as tested. The offline embedded test runs the actual generated HTML independently of a server.
- Screenshots inspected at 390, 768 and 1440px, including browsing, jewellery/toy focus and dragging above the target. Fresh final desktop/mobile captures verify removal of bright blur fringes. The blur uses full drawing-buffer resolution, a 17-tap Gaussian per axis, actual-depth masking and correct premultiplied coverage/color conversion; no coarse downsampling. Rail, spokes, pole and selected hook/carton remain sharp. Time samples are saved to `/tmp/charms-validation/save-sequence.json`.
- Supplied brand/font/vendor assets and all prior release HTML/ZIP files were compared byte-for-byte against the verified Git version and remain unchanged. The uploaded 1.6.0 ZIP matches the preserved repository ZIP.
- Source ZIP integrity and embedded standalone matching are checked after packaging. The archive uses `charms/` and includes the editable source, lockfile, docs and all test suites, without dependency/build caches.

## Remaining limitations

Only automated Chromium/SwiftShader testing is claimed. Physical touchscreen/trackpad, Safari, Firefox and low-powered hardware performance were not tested. Very short mobile viewports may require scrolling to reach the saving target. Hook release remains restrained geometric animation rather than a collision simulation. Browser policy determines local-file storage and opening.

Live Vitsœ and Dieter Rams reference requests returned network-policy 403 responses. No live inspection is claimed. Applied principles are monochrome restraint, purposeful spacing, sparse borders, consistent alignment and clear product/drag hierarchy. No borrowed brand assets were used.

The GitHub releases API returned 403, but the public repository releases page was successfully checked and reported no releases; remote main remained at the last verified commit before this work. Chat reports the actual final commit/push verification. No deployment or GitHub release creation is performed.
