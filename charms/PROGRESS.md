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

## Recovery and delivery

Recovered from GitHub main 30f2eafbf23ebb3af7e27646f2197b20bad544b2 in the existing checkout. No surviving v1.6.3 work was present. Remote tags and the releases page contained no newer release. The uploaded v1.6.2 ZIP matches the preserved repository archive byte for byte. No dependencies were upgraded. Current validation is recorded in VALIDATION.md.

## Archived earlier release notes (superseded by the specification above)

# CICONIA CHARMS 1.6.2 update

The latest request supersedes the blur and camera requirements below: all blur/compositing is removed, browsing camera distance is 7.2 (previously 8.6), focus distance is 3.5 (previously 3.9), with responsive clearance limits retained. The product-list disclosure is above the rack, immediately discoverable. Saving and recovery mechanics are retained.

## Historical 1.6.1 record (superseded where noted above)

# Progress — CICONIA CHARMS 1.6.1

## Recovery and scope

Started from the verified GitHub main commit `4cfc704f8693a7fedd8fc24a0eb709b676063237`. Remote HEAD was unchanged; the GitHub releases page reported no releases. The uploaded 1.6.0 ZIP is byte-identical to the repository copy. No surviving 1.6.1 work was found. Prior HTML/ZIP releases are preserved.

The owner's cumulative brief retains the working 1.6.0 integrated architecture. Current source directory, diagnostics and test URL variable now use Charms. Storage migrates earlier saved boxes to the new Charms key without losing prior quantities.

## Implemented

- Smaller normal rack centred in its left panel, with perspective framing and no horizontal camera crop. The camera remains fixed during browsing rotation; focus smoothly approaches the existing carton.
- Replaced coarse half-resolution background blur with full-resolution separable Gaussian compositing. Actual scene-depth masks isolate other cartons and hooks. Premultiplied coverage avoids dark fringes and smooths thin hooks and silhouettes. Rail, pole, spokes, selected hook and selected carton remain sharp.
- Successful releases add one synchronously, shrink the same carton out at the target, relocate only at zero scale/invisibility, and grow it back on its original hook. Explicit disappearing/reappearing phases block overlapping saves. Invalid/cancelled releases retain continuous return and settling with no addition. Escape resolves each stage, preserves completed additions, restores layers/transforms and returns to the saved camera/angle.
- Reserved Back row above the canvas for desktop/mobile; it does not overlap carton, hook or card. Combined redundant responsive CSS blocks into one mobile system.
- Retained exact pointer pivot, same-card saving, secondary quantity button, saved count, confirmation, Undo, list/search, grouped editing, fallback and animations under reduced motion. Updated server identity to CICONIA CHARMS.
- Added frame-sampled save/interruption tests and combined catalogue/fallback/storage boundary tests. Package contains all editable source, lockfile, docs, tests and matching standalone.

## Validation and limitations

See VALIDATION.md. Physical touchscreen/trackpad, Safari/Firefox and low-powered device performance are not tested. File navigation can be blocked by this environment, and local-file storage remains browser-dependent. Very short mobile viewports may need scrolling to reach the saving target. Hook disengagement remains geometric animation rather than collision simulation. Design-reference requests were blocked; no live inspection is claimed.

Commit/push is authorized after tests. No deployment or GitHub release is requested. Chat reports the actual final push result; publication is never inferred from local packaging.
