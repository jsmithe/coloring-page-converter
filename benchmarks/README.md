# Coloring-page quality benchmarks

This benchmark set evaluates how faithfully the converter turns a full-color children's illustration into printable black-and-white line art.

## Original test cases

| File | Primary challenge |
| --- | --- |
| fox-standing.png | Facial details, character silhouettes, and foreground/background separation |
| fox-rabbit-hug.png | Overlapping characters, facial expressions, and interior boundaries |
| woodland-birthday.png | Dense multi-character scene, decorations, and small objects |
| storybook-cover.png | Composition, decorative borders, and a blank title banner |
| character-infographic.png | Panel borders, arrows, icons, and enclosed shapes |

The five source PNGs were generated for this project. Keep them under `benchmarks/sources/` and do not overwrite them with conversion results.

## Reference comparison

A ColorBliss conversion of `fox-rabbit-hug.png` was supplied for visual comparison. The reference demonstrates:
- Clear primary character silhouettes and expressive facial details
- Mostly white interiors suitable for coloring
- Heavier foreground lines and lighter background detail
- Preservation of the original pose and composition

Store our own outputs under `benchmarks/outputs/`. If we publish third-party reference outputs under `benchmarks/references/`, first check their applicable redistribution terms and identify the generating service. A free conversion does not by itself grant redistribution rights.

## Manual benchmark procedure

1. Run `coloring-page benchmarks/sources/fox-rabbit-hug.png --output benchmarks/outputs/fox-rabbit-hug.png`.
2. Compare the source, our output, and the ColorBliss reference at identical dimensions.
3. Evaluate silhouette fidelity, overlapping limbs, eyes/noses/mouths, white fill, background noise, line hierarchy, and printability.
4. Record specific defects before changing the algorithm.
5. Repeat for the other four test cases.

No claim is made yet that the current OpenCV implementation matches ColorBliss quality.

## Asset status

This README documents the benchmark design. Binary PNG files are maintained separately and must be explicitly uploaded to the repository; this document alone does not add those files.
