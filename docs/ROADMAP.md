# Roadmap

The single purpose is to convert an existing image into a clean, structure-preserving black-and-white coloring page. User-facing style choices are out of scope.

## 0.1 — Deterministic prototype
- [x] Load common raster formats with OpenCV.
- [x] Composite transparency onto white.
- [x] Apply edge-preserving smoothing.
- [x] Detect luminance edges; optionally detect color edges.
- [x] Preserve small dark details where possible.
- [x] Export strict binary black-and-white output.
- [x] Add CLI, tests, and GitHub Actions.

## 0.2 — Quality improvement
- [ ] Build a permission-safe benchmark set.
- [ ] Compare extraction strategies on identical images.
- [ ] Reduce background texture without erasing meaningful details.
- [ ] Improve line continuity and remove speckles.
- [ ] Add automated output/noise measurements.

## 0.3 — Reusable service
- [ ] Add HTTP API with upload and size limits.
- [ ] Add temporary storage and cleanup.
- [ ] Return stable conversion errors.

## 0.4 — ChatGPT integration
- [ ] Expose conversion through MCP.
- [ ] Add a Skill enforcing the single default conversion objective.
- [ ] Return transformed images to chat.

## Later: optional AI refinement
Only investigate ComfyUI/ControlNet if deterministic processing cannot meet the fidelity target. Evaluate any AI stage for unwanted changes to composition, characters, text, and details.
