# Frontend Component

## Overview

User-facing web interface built with Jinja2 templates, HTML, CSS, and minimal JavaScript.

## Key Files

```
webapp/flaskr/
├── templates/          # Jinja2 templates
│   ├── base.html       # Base layout
│   ├── auth/           # Login, register
│   ├── blog/           # Post index, create, update
│   └── gcp/            # Image upload & results
└── static/
    ├── style.css       # Global styles
    └── uploads/images/ # User uploads
```

## Architecture

### Template Inheritance

All pages extend `base.html` for consistent structure:

```html
{% extends 'base.html' %}
{% block title %}My Page{% endblock %}
{% block content %}<p>Content</p>{% endblock %}
```

### Jinja2 Essentials

**Variables:** `{{ post.title }}`  
**Filters:** `{{ username|upper }}`  
**Loops:** `{% for item in items %}`  
**Conditionals:** `{% if g.user %}`  
**URLs:** `{{ url_for('blog.index') }}`

## Page Groups

- **auth/** - Login, registration
- **blog/** - Post display and management
- **gcp/** - Image upload and OCR results

## User Interaction

- Flash messages for feedback
- Form validation (HTML5 + backend)
- Conditional rendering based on auth state

## Next Steps

- **[Backend Documentation](./backend.md)** - Data flow
- **[Development Workflow](../development-workflow.md)** - Making changes

---

**Related Files:**
- `flaskr/templates/`
- `flaskr/static/style.css`
