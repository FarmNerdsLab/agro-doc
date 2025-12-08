# System Architecture Overview

## Introduction

Agro-Doc is designed as a modular web application with distinct components that work together to digitize and process agricultural documentation. This document provides a high-level overview of the system architecture.

## System Architecture

![Container Diagram](<Powisset System Architecture Diagram - Container Diagram.jpg>)
## Component Overview

The Agro-Doc system consists of five primary components:

### 1. **Backend** (Flask Web Framework)
The server-side application that handles all OCR and routing.

**Technology:** Python with Flask  
**Responsibilities:**
- HTTP request/response handling
- User authentication and authorization
- Database operations
- File upload management
- Coordination of OCR and LLM services

**Learn more:** [Backend Documentation](./components/backend.md)

---

### 2. **Frontend** (HTML/CSS)
The user interface that runs in the browser.

**Technology:** Jinja2 templates, HTML, CSS  
**Responsibilities:**
- Rendering pages dynamically
- Form submission and validation
- Displaying processed results
- User interaction handling


**Later on**, the Frontend will be transitioned to be JavaScript/React.js.

**Learn more:** [Frontend Documentation](./components/frontend.md)

---

### 3. **Database** (SQLite)
Persistent storage for all application data.

**Technology:** SQLite  
**Responsibilities:**
- User account storage
- Blog post content
- Session management
- Upload metadata

**Learn more:** [Database Documentation](./components/database.md)

---

### 4. **OCR Handwriting Recognition**
Converts handwritten documents into digital text. This is all done through API calls.

**Technology:** PaddleOCR  
**Responsibilities:**
- Image preprocessing
- Handwriting detection
- Text extraction
- Confidence scoring

**Learn more:** [OCR Documentation](./components/ocr.md)

---

### 5. **LLM Text Refinement**
Improves OCR output quality using language models.

**Technology:** [Phi-3-mini-128k-instruct](https://huggingface.co/microsoft/phi-3-mini-128k-instruct)  
**Responsibilities:**
- Context-based word correction
- Agricultural terminology recognition
- Formatting improvement

**Learn more:** [LLM Documentation](./components/llm.md)

---

## Data Flow

### Typical User Journey: Uploading a Handwritten Document

```
1. User uploads image → Frontend
2. Frontend sends POST request → Backend (gcp.py)
3. Backend saves image → File system
4. Backend sends image → OCR Engine
5. OCR extracts text → Returns to Backend
6. Backend sends OCR text → LLM
7. LLM refines text → Returns to Backend
8. Backend saves result → Database
9. Backend renders result → Frontend
10. Frontend displays to → User
```

### Authentication Flow

```
1. User submits login form → Frontend
2. Frontend sends credentials → Backend (auth.py)
3. Backend queries → Database (users table)
4. Backend verifies password hash
5. Backend creates session → Database (sessions table)
6. Backend sets cookie → Frontend
7. Frontend stores cookie → Browser
```

## Key Design Patterns

### Application Factory Pattern

The app uses Flask's application factory pattern (`create_app()`), which:
- Allows multiple instances with different configurations
- Enables easier testing
- Supports modular blueprint registration

### Blueprint Architecture

The application is divided into logical blueprints:

| Blueprint | Route Prefix | Purpose |
|-----------|-------------|---------|
| `auth` | `/auth` | User registration, login, logout |
| `blog` | `/` | Blog post CRUD operations |
| `gcp` | `/gcp` | Image upload and OCR processing |

### Database Connection Management

Uses Flask's `g` object to maintain a single database connection per request:
```python
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(...)
    return g.db
```

### Template Inheritance

Templates extend `base.html` for consistent layout:
```html
{% extends "base.html" %}
{% block content %}
  <!-- Page-specific content -->
{% endblock %}
```

## Deployment Architecture

[TODO: Add deployment architecture when available]

### Development Environment
- Local dev containers with Docker
- SQLite database (file-based)
- Debug mode enabled
- Hot reload on code changes

### Production Environment
- [TODO: Specify production platform - Google App Engine?]
- [TODO: Production database - Cloud SQL?]
- [TODO: Static file hosting - Cloud Storage?]
- [TODO: OCR/LLM service endpoints]

## Configuration

Configuration is managed through:

1. **`app.config`** - Flask configuration
2. **Environment variables** - Secrets and API keys
3. **`config.py`** - Environment-specific settings
4. **`.env` files** - Local development overrides

## Security Considerations

### Authentication
- Passwords hashed using Werkzeug's `generate_password_hash()`
- Session-based authentication
- CSRF protection on forms

### File Uploads
- File type validation
- Size limits
- Secure filename generation
- Isolated upload directory

### Database
- Parameterized queries (SQL injection prevention)
- Input validation
- User permission checks

## Scalability Considerations

### Current Limitations
- SQLite is single-writer (suitable for small-scale)
- File uploads stored on local disk
- Synchronous request handling

### Future Improvements
[TODO: Add scalability roadmap]
- Migrate to PostgreSQL or Cloud SQL
- Use object storage (S3/GCS) for uploads
- Implement async task queue (Celery)
- Add caching layer (Redis)
- Containerize services separately

## Development Workflow

```
1. Developer makes changes → Local dev container
2. Flask auto-reloads → Changes visible immediately
3. Developer tests → Browser
4. Developer commits → Git
5. CI/CD pipeline runs → [TODO: Add CI/CD details]
6. Deploy to staging → Test environment
7. Deploy to production → Live environment
```

## Component Naming Conventions

To maintain clarity in discussions and documentation, we use these terms:

| Official Name | What It Does | Where to Find It |
|--------------|--------------|------------------|
| **Backend** | Flask server logic | `flaskr/*.py` |
| **Frontend** | User interface | `templates/`, `static/` |
| **Database** | Data persistence | `instance/flaskr.sqlite` |
| **OCR Engine** | Handwriting recognition | `flaskr/handwriting_reader/` |
| **LLM Service** | Text refinement | [TODO: Add location] |

## Tech Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| **Language** | Python | 3.12 |
| **Web Framework** | Flask | [TODO: Add version] |
| **Database** | SQLite | 3.x |
| **OCR** | [TODO: Specify] | [TODO: Version] |
| **LLM** | [TODO: Specify] | [TODO: Version] |
| **Containerization** | Docker | [TODO: Version] |
| **Development** | VS Code + Dev Containers | Latest |

## Next Steps

Now that you understand the overall architecture:

1. **Dive into component details:**
   - [Backend Documentation](./components/backend.md)
   - [Frontend Documentation](./components/frontend.md)
   - [Database Documentation](./components/database.md)
   - [OCR Documentation](./components/ocr.md)
   - [LLM Documentation](./components/llm.md)

2. **Learn the development workflow:**
   - [Development Workflow Guide](./development-workflow.md)

3. **Explore the codebase:**
   - Start with `flaskr/__init__.py`
   - Read through each blueprint
   - Examine templates and static files

## Questions to Consider

As you explore the codebase, think about:

1. Why is the application divided into blueprints?
2. How does the OCR pipeline handle errors?
3. What happens if the LLM service is unavailable?
4. How are user permissions enforced?
5. What would be required to add a new feature?

---

**Related Documentation:**
- [Tutorial 2: Running Locally](./tutorial-2-running-locally.md)
- [API Reference](./api-reference.md)
- [Troubleshooting Guide](./troubleshooting.md)
