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

## Styling

Global styles are in `static/style.css`. The CSS provides:
- Layout structure
- Form styling
- Navigation design
- Flash message appearance

## User Interaction

### Flash Messages

Display one-time feedback to users:

```html
{% for message in get_flashed_messages() %}
  <div class="flash">{{ message }}</div>
{% endfor %}
```

### Form Validation

- HTML5 validation attributes (`required`, `minlength`, etc.)
- Backend validation with error messages
- Error display in templates

### Conditional Rendering

Show/hide elements based on user state:

```html
{% if g.user %}
  <a href="{{ url_for('auth.logout') }}">Log Out</a>
{% else %}
  <a href="{{ url_for('auth.login') }}">Log In</a>
{% endif %}
```

## Best Practices

- Use semantic HTML (`<nav>`, `<article>`, `<section>`)
- Associate labels with form inputs
- Provide alt text for images
- Ensure keyboard accessibility
- Maintain color contrast for readability

## Next Steps

- **[Backend Documentation](./backend.md)** - How data flows to templates
- **[Database Documentation](./database.md)** - What data is available
- **[Development Workflow](../development-workflow.md)** - Making changes

---

**Related Files:**
- `flaskr/templates/` - All template files
- `flaskr/static/style.css` - Global styles
- `flaskr/static/uploads/` - Uploaded files

```
<body>
  <nav>
    <!-- Navigation links -->
  </nav>
  
  <section class="content">
    <header>
      {% block header %}{% endblock %}
    </header>
    
    {% for message in get_flashed_messages() %}
      <div class="flash">{{ message }}</div>
    {% endfor %}
    
    {% block content %}{% endblock %}
  </section>
</body>
</html>
```

### Template Inheritance

Child templates extend and customize the base:

```html
{% extends 'base.html' %}

{% block title %}My Page{% endblock %}

{% block header %}
  <h1>My Page Title</h1>
{% endblock %}

{% block content %}
  <p>My page content goes here.</p>
{% endblock %}
```