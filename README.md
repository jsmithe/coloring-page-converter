# Coloring Page Converter

A local Python tool for converting existing illustrations into black-and-white coloring pages.

**Goal:** preserve the source composition, characters, objects, and details while removing color and shading. This first version uses deterministic computer vision; it does not require ComfyUI, ControlNet, a generative model, a GPU, or cloud hosting.

> **Status: experimental prototype.** Edge extraction is a baseline, not a guarantee of ColorBliss-level fidelity. Complex scenes, gradients, watercolor textures, low-contrast boundaries, and overlaps need further tuning.

## Requirements
- Python 3.10+
- No GPU required

## Install

```bash
git clone https://github.com/jsmithe/coloring-page-converter.git
cd coloring-page-converter
python -m venv .venv
```

Activate with `\.venv\Scripts\Activate.ps1` on Windows PowerShell or `source .venv/bin/activate` on macOS/Linux.

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Convert an image

```bash
coloring-page path/to/illustration.jpg --output output/coloring-page.png
```

Or:

```bash
python -m coloring_page_converter.cli path/to/illustration.jpg -o output/coloring-page.png
```

Useful options:
- `--max-dimension 0` keeps original dimensions.
- `--line-thickness 0` disables line thickening.
- `--color-edges` detects chromatic boundaries too, but may add texture.
- `--no-small-details` disables the small dark-feature preservation pass.

## Tests

```bash
python -m pytest
```

## Current limitations

This method detects edges; it does not semantically understand images. It may miss low-contrast color boundaries, extract texture as unwanted lines, lose interior shapes, or turn large dark regions into contours. Defaults must be evaluated against a representative benchmark set.

Do not commit user-provided benchmark images unless redistribution rights are clear.

## Roadmap
1. Improve deterministic extraction and cleanup against a fixed benchmark set.
2. Add repeatable quality evaluation.
3. Expose the converter through an HTTP API.
4. Add optional AI refinement only if necessary to meet fidelity goals.
5. Connect the API to ChatGPT through MCP or another supported integration.

MIT licensed. See [LICENSE](LICENSE).
