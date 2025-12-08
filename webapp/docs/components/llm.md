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

### OpenAI GPT
- **Type:** Cloud-based
- **Best for:** High-quality refinement
- **Trade-off:** API costs

### Anthropic Claude
- **Type:** Cloud-based
- **Best for:** Long documents
- **Trade-off:** API costs

### Local LLM (Llama, Mistral)
- **Type:** Local
- **Best for:** Privacy-sensitive deployments
- **Trade-off:** Requires GPU, lower quality

## Data Flow

```
OCR → LLM → Refined Text → Database (both versions) → Display
```

## Configuration

```bash
LLM_BACKEND=openai  # or 'claude', 'local'
OPENAI_API_KEY=sk-...
```

## Integration

Integrates with `gcp.py` blueprint to process OCR output before storage.

## Cost Management

- Cache results to avoid reprocessing
- Track API usage
- Set usage limits

## Next Steps

- **[OCR Documentation](./ocr.md)** - Input source
- **[Backend Documentation](./backend.md)** - Integration

---

**Related Files:**
- `flaskr/gcp.py`
- `flaskr/llm/` (if exists)
- Receives OCR output
- Sends to configured LLM backend
- Returns refined text
- Handles errors and timeouts

## Configuration

LLM backend selection managed through environment variables:

```bash
LLM_BACKEND=openai  # or 'claude', 'local'
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.3
```

## Prompt Engineering

Effective prompts should:
- Specify the task clearly (correct OCR errors)
- Provide context (agricultural documentation)
- Set constraints (preserve numbers and dates)
- Include examples if needed (few-shot learning)

## Error Handling

Common issues to handle:
- API rate limits
- Timeouts
- Invalid responses
- Service unavailability

**Strategy:** Fall back to raw OCR text if LLM processing fails.

## Cost Management

For cloud-based LLMs:
- Track API costs per request
- Cache results to avoid reprocessing
- Set usage limits
- Consider batch processing

## Performance Optimization

- **Caching:** Store refined text to avoid redundant API calls
- **Async processing:** Use background jobs for non-urgent refinements
- **Validation:** Ensure refined text is reasonable before saving

## Testing

Test LLM refinement with sample OCR outputs to verify:
- Error correction accuracy
- Format improvements
- Preservation of important data (numbers, dates)
- Cost per request

## User Experience

Display both versions to users:
- Show original OCR output
- Show refined text
- Highlight changes made
- Allow manual editing of refined text

## Next Steps

- **[OCR Documentation](./ocr.md)** - Understand what LLM is refining
- **[Backend Documentation](./backend.md)** - Integration with Flask
- **[Development Workflow](../development-workflow.md)** - Testing practices

---

**Related Files:**
- `flaskr/gcp.py` - OCR and LLM coordination
- `flaskr/llm/` - LLM service wrapper (if exists)


**Cons:**
- API costs per request
- Requires internet connection
- Data sent to OpenAI

**Usage:**

```python
import openai

def refine_with_openai(ocr_text: str) -> str:
    """Refine OCR text using OpenAI"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a text correction assistant specializing in agricultural documentation. Correct OCR errors while preserving the original meaning."
            },
            {
                "role": "user",
                "content": f"Correct this OCR text from a farm document:\n\n{ocr_text}"
            }
        ],
        temperature=0.3,  # Lower = more consistent
        max_tokens=500
    )
    
    return response.choices[0].message.content
```

---

### 2. Anthropic Claude

**Type:** Cloud-based, commercial  
**Best for:** Complex reasoning and long documents  
**Pros:**
- Large context window
- Strong reasoning
- Good at following instructions

**Cons:**
- API costs
- Requires internet

**Usage:**

```python
import anthropic

def refine_with_claude(ocr_text: str) -> str:
    """Refine OCR text using Claude"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are correcting OCR text from handwritten farm documentation.
                
Fix spelling errors, formatting issues, and improve readability while preserving the original meaning.

OCR Text:
{ocr_text}

Corrected Text:"""
            }
        ]
    )
    
    return message.content[0].text
```

---

### 3. Local LLM (Llama, Mistral)

**Type:** Local, open-source  
**Best for:** Privacy-sensitive deployments  
**Pros:**
- No API costs
- Data stays local
- No internet required

**Cons:**
- Requires powerful hardware (GPU)
- Slower inference
- Lower quality than GPT-4

[TODO: Add implementation if using local LLM]

---

## Integration Architecture

### Data Flow

```
1. OCR extracts text → Raw OCR text
2. Backend sends to → LLM service
3. LLM processes → Refined text
4. Backend receives → Corrected output
5. Backend stores → Database (both versions)
6. Frontend displays → User sees comparison
```

### Code Structure

```
webapp/
├── flaskr/
│   ├── gcp.py              # Coordinates OCR → LLM flow
│   └── llm/                # LLM service wrapper
│       ├── __init__.py
│       ├── openai_service.py
│       ├── claude_service.py
│       └── local_service.py
```

---

## Implementation

### LLM Service Wrapper

```python
# flaskr/llm/__init__.py

class LLMService:
    """Abstract base class for LLM implementations"""
    
    def refine_text(self, ocr_text: str, context: dict = None) -> dict:
        """
        Refine OCR text using LLM.
        
        Args:
            ocr_text: Raw OCR output
            context: Optional context (date, field name, crop type, etc.)
            
        Returns:
            dict with keys:
                - refined_text: Corrected text
                - confidence: Model confidence (0-1)
                - changes: List of corrections made
                - cost: API cost in USD (if applicable)
        """
        raise NotImplementedError
```

### OpenAI Implementation

```python
# flaskr/llm/openai_service.py

import openai
import os

class OpenAIService(LLMService):
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"
    
    def refine_text(self, ocr_text: str, context: dict = None) -> dict:
        # Build prompt with context
        system_prompt = self._build_system_prompt(context)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": self._build_user_prompt(ocr_text)}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            refined_text = response.choices[0].message.content
            
            return {
                'refined_text': refined_text,
                'confidence': 0.9,  # OpenAI doesn't provide confidence
                'changes': self._detect_changes(ocr_text, refined_text),
                'cost': self._calculate_cost(response.usage)
            }
        
        except Exception as e:
            return {
                'refined_text': ocr_text,  # Return original on error
                'confidence': 0.0,
                'changes': [],
                'cost': 0.0,
                'error': str(e)
            }
    
    def _build_system_prompt(self, context):
        """Build context-aware system prompt"""
        prompt = """You are a text correction assistant specializing in agricultural documentation.
        
Your task:
- Correct OCR errors (misrecognized characters)
- Fix formatting and punctuation
- Preserve the original meaning and intent
- Use agricultural terminology correctly
- Keep the same structure and organization"""
        
        if context:
            if 'crop_type' in context:
                prompt += f"\n- The document is about {context['crop_type']}"
            if 'date' in context:
                prompt += f"\n- The document date is {context['date']}"
        
        return prompt
    
    def _build_user_prompt(self, ocr_text):
        """Build user prompt with OCR text"""
        return f"""Correct this OCR text from a farm document:

{ocr_text}

Return only the corrected text without explanations."""
    
    def _detect_changes(self, original, refined):
        """Detect what changes were made"""
        # Simple word-level diff
        orig_words = original.split()
        refined_words = refined.split()
        
        changes = []
        for i, (orig, ref) in enumerate(zip(orig_words, refined_words)):
            if orig != ref:
                changes.append(f"'{orig}' → '{ref}'")
        
        return changes
    
    def _calculate_cost(self, usage):
        """Calculate API cost"""
        # GPT-3.5-turbo pricing (as of 2024)
        input_cost = 0.0015 / 1000  # per token
        output_cost = 0.002 / 1000  # per token
        
        cost = (usage.prompt_tokens * input_cost + 
                usage.completion_tokens * output_cost)
        
        return round(cost, 6)
```

---

## Prompt Engineering

### System Prompt Best Practices

✅ **Be specific about the task:**
```python
"You are correcting OCR errors in handwritten farm documentation."
```

✅ **Provide examples (few-shot learning):**
```python
"""Examples:
Input: "Pl4nted c0rn"
Output: "Planted corn"

Input: "Tem9erature 75F"
Output: "Temperature: 75°F"
"""
```

✅ **Set constraints:**
```python
"Preserve all dates, numbers, and field names exactly as written."
```

✅ **Add domain knowledge:**
```python
"Common agricultural terms: fertilizer, irrigation, harvest, yield, etc."
```

---

## Configuration

### Environment Variables

```bash
# .env file
LLM_BACKEND=openai  # or 'claude', 'local'
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...
LLM_MODEL=gpt-3.5-turbo
LLM_MAX_TOKENS=500
LLM_TEMPERATURE=0.3
```

### Flask Config

```python
app.config.update(
    LLM_ENABLED=True,
    LLM_TIMEOUT=30,  # seconds
    LLM_RETRY_COUNT=3
)
```

---

## Integration with GCP Blueprint

```python
# In flaskr/gcp.py

from flaskr.llm import get_llm_service

@bp.route('/gcp/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        # ... file upload and OCR processing ...
        
        ocr_text = ocr_service.process_image(image_path)['text']
        
        # Refine with LLM (if enabled)
        if current_app.config.get('LLM_ENABLED'):
            llm_service = get_llm_service()
            result = llm_service.refine_text(
                ocr_text,
                context={
                    'crop_type': request.form.get('crop_type'),
                    'date': request.form.get('date')
                }
            )
            refined_text = result['refined_text']
        else:
            refined_text = ocr_text
        
        # Save both versions
        db.execute(
            'INSERT INTO gcp_upload (user_id, filename, ocr_text, refined_text)'
            ' VALUES (?, ?, ?, ?)',
            (g.user['id'], filename, ocr_text, refined_text)
        )
        db.commit()
        
        return redirect(url_for('gcp.index'))
```

---

## Error Handling

### Common Issues

**1. API Rate Limits**

```python
import time

def refine_with_retry(ocr_text, max_retries=3):
    """Retry with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return llm_service.refine_text(ocr_text)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise
```

**2. Timeout**

```python
import signal

def refine_with_timeout(ocr_text, timeout=30):
    """Set timeout for LLM call"""
    def handler(signum, frame):
        raise TimeoutError("LLM processing timeout")
    
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    
    try:
        result = llm_service.refine_text(ocr_text)
    finally:
        signal.alarm(0)  # Cancel alarm
    
    return result
```

**3. Invalid Response**

```python
def validate_refinement(original, refined):
    """Ensure refinement is reasonable"""
    # Check length hasn't changed drastically
    if len(refined) > len(original) * 2:
        return original  # LLM added too much
    
    # Check not empty
    if not refined.strip():
        return original
    
    return refined
```

---

## Cost Management

### Tracking Costs

```python
class CostTracker:
    """Track LLM API costs"""
    
    def __init__(self):
        self.total_cost = 0.0
        self.request_count = 0
    
    def log_request(self, cost):
        """Log a request cost"""
        self.total_cost += cost
        self.request_count += 1
        
        # Store in database
        db.execute(
            'INSERT INTO llm_usage (cost, timestamp) VALUES (?, ?)',
            (cost, datetime.now())
        )
        db.commit()
    
    def get_monthly_cost(self):
        """Get current month's cost"""
        result = db.execute(
            'SELECT SUM(cost) FROM llm_usage WHERE timestamp > ?',
            (datetime.now().replace(day=1),)
        ).fetchone()
        
        return result[0] or 0.0
```

### Cost Optimization

```python
# Cache results to avoid reprocessing
def get_cached_refinement(ocr_text):
    """Check if we've processed this text before"""
    text_hash = hashlib.md5(ocr_text.encode()).hexdigest()
    
    cached = db.execute(
        'SELECT refined_text FROM llm_cache WHERE text_hash = ?',
        (text_hash,)
    ).fetchone()
    
    if cached:
        return cached['refined_text']
    
    # Process and cache
    result = llm_service.refine_text(ocr_text)
    db.execute(
        'INSERT INTO llm_cache (text_hash, ocr_text, refined_text) VALUES (?, ?, ?)',
        (text_hash, ocr_text, result['refined_text'])
    )
    db.commit()
    
    return result['refined_text']
```

---

## Testing

### Unit Tests

```python
def test_llm_refinement():
    """Test basic refinement"""
    service = OpenAIService()
    
    ocr_text = "Pl4nted c0rn t0day"
    result = service.refine_text(ocr_text)
    
    assert result['refined_text']
    assert 'corn' in result['refined_text'].lower()
    assert result['confidence'] > 0

def test_llm_preserves_numbers():
    """Ensure numbers aren't changed"""
    service = OpenAIService()
    
    ocr_text = "Field 42, Temp 75F, 100 bushels"
    result = service.refine_text(ocr_text)
    
    assert '42' in result['refined_text']
    assert '75' in result['refined_text']
    assert '100' in result['refined_text']
```

### Manual Testing

```bash
# Test with sample OCR output
python -c "
from flaskr.llm import get_llm_service

ocr_text = 'Pl4nted c0rn in f1eld B. Tem9erature 75F.'
service = get_llm_service()
result = service.refine_text(ocr_text)

print('Original:', ocr_text)
print('Refined:', result['refined_text'])
print('Changes:', result['changes'])
print('Cost:', f\"\${result['cost']:.6f}\")
"
```

---

## Displaying Results to Users

### Side-by-Side Comparison

```html
<!-- In template -->
<div class="ocr-comparison">
  <div class="ocr-original">
    <h3>Original OCR Output</h3>
    <pre>{{ ocr_text }}</pre>
  </div>
  
  <div class="ocr-refined">
    <h3>AI-Refined Text</h3>
    <pre>{{ refined_text }}</pre>
  </div>
</div>

<div class="ocr-changes">
  <h4>Changes Made:</h4>
  <ul>
    {% for change in changes %}
      <li>{{ change }}</li>
    {% endfor %}
  </ul>
</div>
```

### Editable Output

```html
<!-- Allow users to edit refined text -->
<form method="post" action="{{ url_for('gcp.update', id=upload.id) }}">
  <label for="refined_text">Refined Text (editable)</label>
  <textarea name="refined_text" id="refined_text" rows="10">{{ refined_text }}</textarea>
  <button type="submit">Save Edits</button>
</form>
```

---

## Future Enhancements

[TODO: Add roadmap]

- [ ] Custom fine-tuned model for agricultural terms
- [ ] Confidence scoring for each correction
- [ ] User feedback loop to improve prompts
- [ ] Batch processing for multiple documents
- [ ] Export to structured formats (JSON, CSV)
- [ ] Integration with agricultural databases (crop types, etc.)

---

## Next Steps

- **[OCR Documentation](./ocr.md)** - Understand what LLM is refining
- **[Backend Documentation](./backend.md)** - See full integration
- **[Development Workflow](../development-workflow.md)** - Testing practices

---

## Questions to Explore

1. How do you balance cost vs. quality with different LLM models?
2. What prompt engineering techniques improve accuracy?
3. How can you prevent the LLM from hallucinating information?
4. What metrics measure refinement quality?
5. How would you fine-tune a model for agricultural terminology?

---

**Related Files:**
- `flaskr/gcp.py`
- `flaskr/llm/` (if exists)
- [TODO: Add any LLM-related scripts]
