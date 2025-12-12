# OCR (Optical Character Recognition) Component

## Overview

Converts handwritten text in images into digital text.

## Key Files

```
Root directory:
├── finetune-trocr.py       # TrOCR fine-tuning
├── test-trocr.py           # TrOCR testing
├── test-gcp.py             # Google Vision testing
└── test-gcp-bounds.py      # Bounding box testing

webapp/flaskr/
├── backend.py                  # Upload & OCR coordination
└── handwriting_reader/     # OCR service wrapper
```

## Supported Engines

### TrOCR
- **Type:** Local, open-source
- **Best for:** Handwritten text
- **Trade-off:** No costs but requires GPU

### PaddleOCR
- **Type:** Local, open-source
- **Best for:** Printed and handwritten text
- **Trade-off:** Fast but moderate accuracy on messy handwriting

### Google Cloud Vision
- **Type:** Cloud-based, commercial
- **Best for:** Production deployments
- **Trade-off:** Excellent accuracy but API costs

## Data Flow

```
Upload → Save → OCR → (Optional: LLM) → Database → Display
```

## Configuration
    NOTE: Google Cloud Vision has been removed from the devcontainer.

Set OCR backend via environment variables:
```bash
OCR_BACKEND=google_vision  # or 'trocr', 'paddle'
GOOGLE_CLOUD_API_KEY=your-key
```

## Testing

```bash
python test-trocr.py path/to/image.jpg
python test-gcp.py path/to/image.jpg
```

## Next Steps

- **[LLM Documentation](./llm.md)** - Text refinement
- **[Backend Documentation](./backend.md)** - Integration

---

**Related Files:**
- `flaskr/backend.py`
- `test-trocr.py`, `test-gcp.py`
- `finetune-trocr.py`
