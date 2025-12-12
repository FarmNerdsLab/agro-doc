# LLM (Large Language Model) Text Refinement Component

## Overview

Refines raw OCR output into clean, readable text by correcting errors and improving formatting.

## Example

**OCR Output:** `Pl4nted c0rn t0day in f1eld B`  
**LLM Refined:** `Planted corn today in field B`

## Key Functions

- Correct OCR errors
- Improve formatting
- Apply agricultural domain knowledge
- Standardize terminology

## Supported Backends
**HASN'T YET BEEN IMPLEMENTED**

### Local LLM: Phi-3-mini-128k-instruct
- **Type:** Local
- Can be configured for CPU or GPU depending on host

## Data Flow

```
OCR → LLM → Refined Text → Database (both versions) → Display
```

## Integration

Integrates with `backend.py` blueprint to process OCR output before storage.

## Cost Management

- Cache results to avoid reprocessing
- Track API usage
- Set usage limits

## Next Steps

- **[OCR Documentation](./ocr.md)** - Input source
- **[Backend Documentation](./backend.md)** - Integration

---

**Related Files:**
- `flaskr/backend.py`
- `flaskr/llm/` (if exists)
