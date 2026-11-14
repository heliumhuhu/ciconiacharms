# CICONIA CHARMS v1.6.5

Restores v1.6.3 rack scroll physics: direct wheel movement, 140ms wheel quiet, then the original 380ms settling to the nearest actual product. The v1.6.4 artificial coast/velocity logic is removed. The padded rack-shaped wheel region, larger focus/media layout and saved −/+ counter remain.

Expanding Explore as a product list now sends a staggered fade/lift ripple diagonally through the actual product grid. Delay follows row plus column so it adapts to two- and four-column layouts. Closing cancels card entrance animations while retaining the animated height collapse. Rapid reversal cancels existing effects before starting a new ripple. No extra products, dependencies or persistent animation elements are created.

## Prior release record (superseded where noted above)

# CICONIA CHARMS v1.6.4

The latest interaction request supersedes previous Add-button and quantity-editing restrictions. The saving area now has a clean − / saved number / + counter. Plus saves one with existing reward feedback; minus removes one, stops at zero and clears stale Undo. Valid dragging still saves one. Storage compatibility and aggregate My box totals remain unchanged.

Wheel input now continues with velocity-based, exponentially damped momentum after the 140ms quiet interval, then settles to an actual product. Holding still stops motion. The wheel interaction region follows a convex outline of projected carton bounds with 28px padding; empty scene corners allow normal page scrolling. No device-type guessing is needed for mouse or trackpad wheel events.

Focused cartons are larger using the existing perspective camera (minimum focus distance 2.95, previously 3.5). Mobile focus has 540px scene height. The same information card provides a 280px desktop / 300px mobile proportion-preserving product image and unrestricted description height. Product assets and placeholders are unchanged.

The product-list disclosure animates height on both expansion and collapse, retaining native summary keyboard activation. Quick repeated toggles reverse from the current height. No dependencies were upgraded; earlier releases are preserved.

## Previous release record (superseded above)

# CICONIA CHARMS v1.6.3

This release supersedes all historical quantity-to-add selector and blur requirements. The focus card displays the stored product quantity starting at zero. Every button click and valid drag saves exactly one; only My box edits quantities. Undo removes the latest completed unit. The aggregate header and compatible persistent storage are retained.

Successful saves synchronously update storage and trigger a count bounce, monochrome target pulse and one reusable floating check/+1. Animation callbacks never change quantities. New feedback cancels the prior effects without adding DOM elements. Invalid/cancelled drops do not trigger rewards. Existing zero-scale disappearance/relocation/reappearance and recovery blocking remain unchanged.

The existing perspective camera approaches the actual carton. Other cartons and infrastructure fade using isolated material copies, becoming invisible at full focus. The selected carton and hook remain intact. Exit reverses the fade and restores original materials, visibility and browsing pose. No blur, cloned geometry or second product scene is introduced. Existing responsive full-carton framing and normal browsing camera are retained.

## Archived earlier release notes (superseded by the specification above)

# CICONIA CHARMS 1.6.2 update

The latest request supersedes the blur and camera requirements below: all blur/compositing is removed, browsing camera distance is 7.2 (previously 8.6), focus distance is 3.5 (previously 3.9), with responsive clearance limits retained. The product-list disclosure is above the rack, immediately discoverable. Saving and recovery mechanics are retained.

## Historical 1.6.1 record (superseded where noted above)

# CICONIA CHARMS 1.6.1

Physical jewellery and toy shop catalogue with 24 perspective cartons.
Browse here · Buy in store. My box — saved favourites.
Saved for your visit. Items are not reserved.

Open `CICONIA-CHARMS-v1.6.5.html` in a modern browser. Scripts, fonts and required assets are embedded; no installation, server or network is required. Browser policy can restrict local-file opening or storage.

## Development

Use the existing `charms/` checkout directory. Each cloud task is already isolated; do not create a worktree unless explicitly requested.
Node 22+ and Python 3 are sufficient for the application. From `charms/`:

```sh
npm ci --cache /tmp/ciconia-npm-cache
npm run dev
```

Development serves port 3000. Production: `npm run build`, then `npm start`. `PORT` and `HOST` override the defaults. No credentials, database or backend are needed. Dependencies and lockfile resolutions are unchanged from 1.6.0.

## Interaction and architecture

- `public/rack.js`: perspective geometry, actual snap positions, opposite category sectors, hook openings, swing and browsing input. A centred camera fits the full focal carton; a separate nearer focus pose provides the approach.
- `public/product-view.js`: one actual carton, existing scene/camera/renderer, exact grabbed-point pivot, pointer capture and safe cancellation. The existing scene renders directly with no blur, postprocessing buffers or compositor. All geometry retains natural depth and occlusion. No cloned product or second product scene exists; only the same dragged carton extends above the information card.
- Focus: zooming → ready → dragging → disappearing → reappearing → ready. Invalid/cancelled gestures instead use returning → settling → ready. Leaving reverses camera progress and waits for safe carton recovery. A valid release adds exactly one before animation callbacks. Successful relocation occurs only at zero scale while invisible; no visible trip back occurs. The same object UUID is retained.
- `public/boutique.js`: one transforming information card, one drag target, secondary quantity/button, saved counts, confirmation, latest-action Undo, list/search and grouped My box management. Both saving methods keep focus open.
- `public/bag.js`: `ciconia-charms-quantities` storage with read-only migration from earlier releases. Current saved data takes precedence, including an intentionally empty box. Malformed or unavailable storage remains safe.
- `public/products.js`: stable IDs and linked numbered placeholders; integer pence when supplied, explicit null prices otherwise. No invented shop content.
- `public/motion-config.js`: centralized 250ms hold, 8px drag threshold, 140ms wheel quiet and 380ms settling.
- `charmsState()` and `charmsGeometry()` expose non-secret diagnostics for browser tests.

The source folder and current diagnostics/test configuration now use Charms. Legacy storage aliases exist solely to preserve previously saved boxes. Earlier release files remain unchanged. The former left crop, separate saving panel and successful fly-back are superseded by BRIEF.md.

All 3D animation stays enabled with reduced-motion preferences. Unavailable WebGL uses the same card and saving structure with an image. No online purchasing, reservations, dashboard or authentication.

## Validation and packaging

```sh
npm test
npm run typecheck
npm run check
npm run build
python3 tests/browser.py
python3 tests/geometry.py
python3 tests/focus.py
python3 tests/interruptions.py
python3 tests/save-sequence.py
python3 tests/catalogue.py
python3 tests/restoration.py
npm run standalone
python3 tests/standalone.py
python3 scripts/package.py
```

Browser suites require Python Playwright and `/usr/bin/chromium` with a running source or production server. `CHARMS_TEST_URL` overrides the default URL where supported; geometry and interruptions use port 3000. Standalone tests need no server. Screenshots and frame diagnostics go to `/tmp/charms-validation`.

See VALIDATION.md for executed outcomes and limits. `scripts/package.py` creates the matching editable `charms/` source archive and includes the standalone HTML.

## Visual references

Live requests to [Vitsœ](https://www.vitsoe.com) and [Dieter Rams](https://www.dieter-rams.org) returned network-policy 403 responses in this environment. No live inspection or copying is claimed. The applied principles are monochrome contrast, sparse borders, purposeful whitespace, consistent alignment and a clear hierarchy favouring products and dragging. Supplied branding and packaging assets are preserved.
