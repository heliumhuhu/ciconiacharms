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

# CICONIA CHARMS — 1.6.1

The owner's cumulative brief and naming correction supersede all earlier briefs. The current editable source directory is `charms/`. Preserve all previous release files and the supplied main logo unchanged. Retain the 24 stable products with linked numbered placeholders and null unknown prices. No checkout, payment, delivery, orders, reservations, authentication, dashboard or backend.

Retain “Browse here · Buy in store”, “My box — saved favourites” and “Saved for your visit. Items are not reserved.” Use My box consistently.

## Superseded requirements

- Replace the large intentional desktop left crop with a smaller perspective rack centred inside its left panel.
- The single drag target belongs inside the SAME information card as the description; a separate target is obsolete.
- A successful save disappears at the target and reappears on the original hook. A visible successful fly-back is obsolete. Invalid/cancelled drops may return continuously.

## Experience

Browsing shows the perspective rack and a compact picture/name/price card only. Carton, picture, search and list selection all enter the same integrated focus controller. Approach the actual existing carton with the existing camera, pause rotation, transform the existing card, and reveal its description and one saving area. No detached product modal, duplicate carton, separate product scene or quick-add interfaces.

Keep complete focal-carton bounds, including tag and bottom edge, inside the canvas at 390, 768 and 1440px, for both category shapes and permitted swing. Peripheral structure may crop. Keep Back in a reserved row above the canvas. Mobile card goes below the rack. Browsing camera stays fixed during normal rotation.

Blur only other cartons and their hooks. Keep infrastructure, selected hook and selected carton sharp. Use full-resolution premultiplied Gaussian rendering and actual scene-depth masking; blend with focus progress. Keep the dragged actual carton above the saving card.

The exact grabbed point follows the pointer and is the damped swing pivot. Leave the hook on the rail and no stationary duplicate on the rack. A valid release adds one synchronously, then disappears, relocates only at zero scale/invisibility, and reappears on its original attachment. Block additional dragging/button saves until ready. Invalid/cancelled gestures add nothing. Back/Escape can reverse zoom and safely resolve every gesture/animation while preserving completed saves and the original browsing angle/camera.

The target says “Drag here to add to My box” or “Release to add to My box” over its real bounds. Drag is primary. A small secondary button adds its adjacent quantity (1–99), independently of one-unit dragging. Show saved quantity, confirmation, Undo and aggregate header quantity. Undo removes only the actual latest addition, preserving older units. Maintain grouped editing, unavailable rows and safe persistent storage; migrate legacy saved boxes.

Preserve real perspective packaging, radial fronts, opposite category sectors, hook openings, shallow category shapes, matte paper texture, seams and spacing. Retain centralized 250ms hold, 8px threshold, 140ms wheel quiet and 380ms settling. Keep all 3D animations under reduced-motion preferences. Only unavailable WebGL enables the same-card fallback.

Maintain keyboard controls, focus indication, exact product identity, independent description/name search, filters, name/featured/price sorting, unknown-price handling, resets and no-results states. Deliver matching offline HTML and editable source ZIP. A tested commit/push to main is authorized; deployment and GitHub release creation are excluded.
