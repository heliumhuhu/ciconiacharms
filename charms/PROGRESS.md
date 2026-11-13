# Progress — Ciconia Charms 1.6.1

## Recovery and scope

Started from the verified GitHub main commit `4cfc704f8693a7fedd8fc24a0eb709b676063237`. Remote HEAD was unchanged; the GitHub releases page reported no releases. The uploaded 1.6.0 ZIP is byte-identical to the repository copy. No surviving 1.6.1 work was found. Prior HTML/ZIP releases are preserved.

The owner's cumulative brief retains the working 1.6.0 integrated architecture. Current source directory, diagnostics and test URL variable now use Charms. Storage migrates earlier saved boxes to the new Charms key without losing prior quantities.

## Implemented

- Smaller normal rack centred in its left panel, with perspective framing and no horizontal camera crop. The camera remains fixed during browsing rotation; focus smoothly approaches the existing carton.
- Replaced coarse half-resolution background blur with full-resolution separable Gaussian compositing. Actual scene-depth masks isolate other cartons and hooks. Premultiplied coverage avoids dark fringes and smooths thin hooks and silhouettes. Rail, pole, spokes, selected hook and selected carton remain sharp.
- Successful releases add one synchronously, shrink the same carton out at the target, relocate only at zero scale/invisibility, and grow it back on its original hook. Explicit disappearing/reappearing phases block overlapping saves. Invalid/cancelled releases retain continuous return and settling with no addition. Escape resolves each stage, preserves completed additions, restores layers/transforms and returns to the saved camera/angle.
- Reserved Back row above the canvas for desktop/mobile; it does not overlap carton, hook or card. Combined redundant responsive CSS blocks into one mobile system.
- Retained exact pointer pivot, same-card saving, secondary quantity button, saved count, confirmation, Undo, list/search, grouped editing, fallback and animations under reduced motion. Updated server identity to Ciconia Charms.
- Added frame-sampled save/interruption tests and combined catalogue/fallback/storage boundary tests. Package contains all editable source, lockfile, docs, tests and matching standalone.

## Validation and limitations

See VALIDATION.md. Physical touchscreen/trackpad, Safari/Firefox and low-powered device performance are not tested. File navigation can be blocked by this environment, and local-file storage remains browser-dependent. Very short mobile viewports may need scrolling to reach the saving target. Hook disengagement remains geometric animation rather than collision simulation. Design-reference requests were blocked; no live inspection is claimed.

Commit/push is authorized after tests. No deployment or GitHub release is requested. Chat reports the actual final push result; publication is never inferred from local packaging.
