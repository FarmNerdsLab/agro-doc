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
├── gcp.py                  # Upload & OCR coordination
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
- `flaskr/gcp.py`
- `test-trocr.py`, `test-gcp.py`
- `finetune-trocr.py`

### Best Practices

Before OCR processing:
- Validate file type and size
- Ensure image quality
- Consider preprocessing (grayscale, contrast adjustment)
- Resize if too large

### Error Handling

Common issues to handle:
- Unreadable handwriting
- No text detected
- API rate limits
- Large file sizes
- Network errors (for cloud services)

## Testing

Manual testing scripts are available:

```bash
# Test with TrOCR
python test-trocr.py path/to/image.jpg

# Test with Google Cloud Vision
python test-gcp.py path/to/image.jpg

# Test bounding boxes
python test-gcp-bounds.py path/to/image.jpg
```

## Configuration

OCR backend selection and API keys should be managed through environment variables:

```bash
OCR_BACKEND=google_vision  # or 'trocr', 'paddle'
GOOGLE_CLOUD_API_KEY=your-api-key-here
```

## Performance Considerations

- **Caching:** Store OCR results to avoid reprocessing
- **Async processing:** Consider background jobs for large uploads
- **Cost management:** Monitor API usage for cloud services
- **Image optimization:** Resize large images before processing

## Fine-tuning

The `finetune-trocr.py` script enables training TrOCR on custom agricultural handwriting samples to improve accuracy.

## Next Steps

- **[LLM Documentation](./llm.md)** - How OCR output is refined
- **[Backend Documentation](./backend.md)** - Integration with Flask routes
- **[Development Workflow](../development-workflow.md)** - Testing practices

---

**Related Files:**
- `flaskr/gcp.py` - Upload and OCR coordination
- `flaskr/handwriting_reader/` - OCR service wrapper
- `test-trocr.py` - TrOCR testing
- `test-gcp.py` - Google Vision testing
- `finetune-trocr.py` - Model fine-tuning


### 3. Google Cloud Vision API

**Type:** Cloud-based, commercial  
**Best for:** Production deployments  
**Pros:**
- Excellent accuracy
- Highly scalable
- No local compute required
- Handles multiple languages

**Cons:**
- API costs per request
- Requires internet connection
- Data sent to Google

**Location:** `flaskr/gcp.py`, `test-gcp.py`, `test-gcp-bounds.py`

---

## Integration Architecture

### Data Flow

```
1. User uploads image → Frontend form
2. Image saved to disk → static/uploads/images/
3. Image path passed to → OCR service
4. OCR processes image → Extracts text
5. Text returned to → Backend
6. Optional: Text sent to → LLM for refinement
7. Results stored in → Database
8. Results displayed to → User
```

### Code Structure

```
webapp/
├── flaskr/
│   ├── gcp.py                      # Image upload and OCR coordination
│   └── handwriting_reader/         # OCR service wrapper
│       └── [TODO: Add structure]
└── static/uploads/images/          # Uploaded images
```

---

## Implementation Details

### Image Upload Handler

**Location:** `flaskr/gcp.py`

[TODO: Document current implementation]

**Expected flow:**

```python
@bp.route('/gcp/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        # Get uploaded file
        file = request.files['image']
        
        # Validate file
        if not allowed_file(file.filename):
            flash('Invalid file type')
            return redirect(request.url)
        
        # Save securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process with OCR
        ocr_text = process_image_ocr(filepath)
        
        # Optional: Refine with LLM
        refined_text = refine_text_llm(ocr_text)
        
        # Save to database
        db = get_db()
        db.execute(
            'INSERT INTO gcp_upload (user_id, filename, ocr_text, refined_text)'
            ' VALUES (?, ?, ?, ?)',
            (g.user['id'], filename, ocr_text, refined_text)
        )
        db.commit()
        
        return redirect(url_for('gcp.index'))
    
    return render_template('gcp/create.html')
```

---

## OCR Service Wrapper

[TODO: Document the OCR service wrapper implementation]

### Expected Interface

```python
class OCRService:
    """Abstract base class for OCR implementations"""
    
    def process_image(self, image_path: str) -> dict:
        """
        Process an image and extract text.
        
        Args:
            image_path: Path to image file
            
        Returns:
            dict with keys:
                - text: Extracted text
                - confidence: Confidence score (0-1)
                - bounding_boxes: Optional coordinate data
                - processing_time: Time taken (seconds)
        """
        raise NotImplementedError
```

### TrOCR Implementation

```python
class TrOCRService(OCRService):
    def __init__(self):
        # Load model
        self.processor = TrOCRProcessor.from_pretrained(...)
        self.model = VisionEncoderDecoderModel.from_pretrained(...)
    
    def process_image(self, image_path: str) -> dict:
        # Load image
        image = Image.open(image_path).convert("RGB")
        
        # Process
        pixel_values = self.processor(image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return {
            'text': text,
            'confidence': 0.95,  # [TODO: Calculate actual confidence]
            'processing_time': 0.5
        }
```

### Google Cloud Vision Implementation

```python
class GoogleVisionService(OCRService):
    def __init__(self, api_key: str):
        from google.cloud import vision
        self.client = vision.ImageAnnotatorClient()
    
    def process_image(self, image_path: str) -> dict:
        # Read image
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        
        # Call API
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            return {
                'text': texts[0].description,
                'confidence': texts[0].score if hasattr(texts[0], 'score') else 0.9,
                'bounding_boxes': [self._extract_bounds(text) for text in texts[1:]],
                'processing_time': 0.3
            }
        
        return {'text': '', 'confidence': 0, 'processing_time': 0.3}
```

---

## Configuration

### Environment Variables

```bash
# .env file
OCR_BACKEND=google_vision  # or 'trocr', 'paddle'
GOOGLE_CLOUD_API_KEY=your-api-key-here
TROCR_MODEL_PATH=/path/to/model
```

### Flask Config

```python
app.config.update(
    UPLOAD_FOLDER='static/uploads/images',
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
)
```

---

## Image Preprocessing

### Best Practices

Before sending to OCR, consider preprocessing:

```python
from PIL import Image, ImageEnhance

def preprocess_image(image_path):
    """Enhance image for better OCR results"""
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    # Resize if too large
    max_size = 2048
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size))
    
    # Save preprocessed version
    preprocessed_path = image_path.replace('.jpg', '_preprocessed.jpg')
    img.save(preprocessed_path)
    
    return preprocessed_path
```

---

## Error Handling

### Common Issues

**1. Unreadable Handwriting**

```python
if result['confidence'] < 0.5:
    flash('Low confidence. Please upload a clearer image.')
```

**2. No Text Detected**

```python
if not result['text']:
    flash('No text found in image. Please try another image.')
```

**3. API Rate Limits**

```python
try:
    result = ocr_service.process_image(image_path)
except RateLimitError:
    flash('Service temporarily unavailable. Please try again later.')
```

**4. Large File Sizes**

```python
if file.size > app.config['MAX_CONTENT_LENGTH']:
    flash('File too large. Maximum size is 16MB.')
```

---

## Performance Optimization

### Caching

Cache OCR results to avoid reprocessing:

```python
import hashlib

def get_image_hash(image_path):
    """Generate hash of image content"""
    with open(image_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def process_with_cache(image_path):
    """Check cache before OCR"""
    image_hash = get_image_hash(image_path)
    
    # Check database for existing result
    cached = db.execute(
        'SELECT ocr_text FROM gcp_upload WHERE image_hash = ?',
        (image_hash,)
    ).fetchone()
    
    if cached:
        return cached['ocr_text']
    
    # Process if not cached
    return ocr_service.process_image(image_path)
```

### Async Processing

For production, consider async task queue:

```python
# Using Celery (example)
@celery.task
def process_image_async(image_path, upload_id):
    """Process image in background"""
    result = ocr_service.process_image(image_path)
    
    # Update database with result
    db.execute(
        'UPDATE gcp_upload SET ocr_text = ?, status = ? WHERE id = ?',
        (result['text'], 'completed', upload_id)
    )
    db.commit()
```

---

## Testing OCR

### Test Files

**Location:** `attachments/Powisset-Documents/` (if available)

### Manual Testing

```bash
# Test with TrOCR
python test-trocr.py path/to/image.jpg

# Test with Google Cloud Vision
python test-gcp.py path/to/image.jpg

# Test bounding boxes
python test-gcp-bounds.py path/to/image.jpg
```

### Unit Tests

```python
def test_ocr_service():
    """Test OCR on sample image"""
    service = TrOCRService()
    result = service.process_image('tests/sample_handwriting.jpg')
    
    assert result['text']
    assert result['confidence'] > 0.7
    assert result['processing_time'] < 2.0
```

---

## Accuracy Improvement

### Fine-tuning TrOCR

**Script:** `finetune-trocr.py`

[TODO: Document fine-tuning process]

### Data Augmentation

Improve model with more training data:

- Collect real farm documentation
- Vary handwriting styles
- Include different lighting conditions
- Add noise and artifacts

---

## Cost Considerations

### Google Cloud Vision Pricing

[TODO: Add current pricing]

**Estimates:**
- First 1,000 requests/month: Free
- After that: $1.50 per 1,000 requests

### Cost Optimization

```python
# Resize images before sending to API
def resize_for_api(image_path, max_dimension=1024):
    """Reduce image size to minimize costs"""
    img = Image.open(image_path)
    
    if max(img.size) > max_dimension:
        ratio = max_dimension / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.LANCZOS)
        img.save(image_path)
```

---

## Switching OCR Backends

### Configuration-based Switching

```python
# In flaskr/__init__.py or gcp.py
def get_ocr_service():
    """Factory function to get OCR service"""
    backend = os.getenv('OCR_BACKEND', 'trocr')
    
    if backend == 'google_vision':
        api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
        return GoogleVisionService(api_key)
    elif backend == 'trocr':
        model_path = os.getenv('TROCR_MODEL_PATH')
        return TrOCRService(model_path)
    elif backend == 'paddle':
        return PaddleOCRService()
    else:
        raise ValueError(f'Unknown OCR backend: {backend}')
```

### Usage

```python
# In view function
ocr_service = get_ocr_service()
result = ocr_service.process_image(image_path)
```

---

## Future Enhancements

[TODO: Add roadmap]

- [ ] Support for table extraction from images
- [ ] Multi-page document processing
- [ ] Batch upload capability
- [ ] Real-time preview during upload
- [ ] Confidence visualization
- [ ] Manual correction interface
- [ ] Export to various formats (PDF, DOCX)

---

## Next Steps

- **[LLM Documentation](./llm.md)** - Learn how OCR output is refined
- **[Backend Documentation](./backend.md)** - See how OCR integrates with routes
- **[Development Workflow](../development-workflow.md)** - Testing practices

---

## Questions to Explore

1. What preprocessing steps improve OCR accuracy?
2. How do you handle low-confidence results?
3. What's the trade-off between local and cloud OCR?
4. How would you implement batch processing?
5. How can you visualize bounding boxes on the original image?

---

**Related Files:**
- `flaskr/gcp.py`
- `flaskr/handwriting_reader/`
- `test-trocr.py`
- `test-gcp.py`
- `test-gcp-bounds.py`
- `finetune-trocr.py`
