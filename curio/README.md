# Ciconia Charms 1.6.0

A physical shop catalogue with 24 perspective cartons. Browse here · Buy in store.
My box — saved favourites. Saved for your visit. Items are not reserved.

Open `CICONIA-CHARMS-v1.6.0.html` in a modern browser. All modules, fonts and assets are embedded; no server, installation or network is required. Local file storage depends on browser policy.

## Development

Use the existing `curio/` directory; do not create another worktree unless explicitly requested.
Node 22+ and Python 3 are sufficient. Run `npm ci`, `npm run dev` (port 3000), or `npm run build` and `npm start` for production. No credentials or backend are needed.

## Interaction and architecture

- `public/rack.js`: original perspective geometry, category sectors, hook openings, swing and browsing inputs. Camera framing prioritizes the complete focal carton over cropping. On narrow screens, the information card moves below the scene.
- `public/product-view.js`: integrated focus controller using the existing camera, renderer and actual carton. Background is rendered through a blur compositor; the selected carton is rendered sharp. No cloned product or second product scene exists.
- Focus phases: zooming → ready → dragging → saving (valid release only) → returning → settling → ready. Leaving reverses camera movement, cancels unfinished gestures and coordinates return. Every completed drag adds one unit synchronously, independent of animation callbacks.
- The exact grabbed point is the moving anchor. Ray/plane projection follows the pointer, shallow forward disengagement frees the slot, and damped rotation swings around that anchor. World transforms survive reparenting. Return targets the original attachment, even while the rack/camera returns.
- `public/boutique.js`: one information card containing the description and one saving area, list/search, My box quantities and latest-action Undo. The smaller adjacent button is the accessible alternative; quantity selection affects only button additions.
- `public/products.js`: stable IDs, integer-pence prices or explicit null prices, numbered product/image/description/price placeholders. No invented shop content.
- `public/bag.js`: safe localStorage quantities; existing `curio-quantities` key retained for compatibility.
- `public/motion-config.js`: centralized 250ms hold, 8px drag threshold, 140ms wheel quiet interval and 380ms settling.

All 3D animations remain enabled under reduced-motion preferences. WebGL unavailability alone uses the image/list alternative with the same card and saving area. No purchasing, checkout, reservations, dashboard, authentication or backend.

## Validation and packaging

```
npm test
npm run typecheck
npm run check
npm run build
python3 tests/browser.py
python3 tests/focus.py
python3 tests/geometry.py
python3 tests/interruptions.py
npm run standalone
python3 tests/standalone.py
python3 scripts/package.py
```

Browser suites require Python Playwright and `/usr/bin/chromium`, plus the running source or production server. `CURIO_TEST_URL` overrides port 3000 where supported. Geometry tests use port 3000. Standalone tests require no server. Screenshots and sampled return diagnostics go to `/tmp/charms-validation`.

The original supplied logo is unchanged. The source ZIP and standalone are delivered directly in chat; a GitHub push was subsequently authorized by the owner; deployment and GitHub releases remain excluded. Original v1.5.0 artifacts are preserved separately in the workspace.

## Design

The redesign uses a white/black/grey foundation, sparse rules, whitespace, local DM Sans and editorial serif headings. It removes coloured gradients, grain overlays, fluting and glass panels. Vitsœ (https://www.vitsoe.com) and Dieter Rams (https://www.dieter-rams.org) were attempted as live minimal-design references; both were blocked by network policy. No live inspection or copied reference assets is claimed.
