# Backend Component

## Overview

The backend is the server-side component of Agro-Doc, built with Flask. It handles all business logic, user authentication, database operations, and coordinates the OCR and LLM processing pipeline.

## Key Files

```
webapp/flaskr/
├── __init__.py      # Application factory and initialization
├── auth.py          # User authentication (login, register, logout)
├── blog.py          # Blog post management (CRUD operations)
├── db.py            # Database connection and utilities
├── gcp.py           # Image upload and OCR processing
└── schema.sql       # Database schema definition
```

## Architecture Patterns

### Application Factory Pattern

The app uses Flask's application factory pattern in `__init__.py`, which allows:
- Multiple app instances for testing
- Modular blueprint registration
- Clean configuration management

### Blueprint Architecture

The application is organized into three main blueprints:

| Blueprint | Route Prefix | Purpose |
|-----------|-------------|---------|
| `auth.py` | `/auth` | User registration, login, logout |
| `blog.py` | `/` | Blog post CRUD operations |
| `gcp.py` | `/gcp` | Image upload and OCR processing |

Each blueprint handles a distinct area of functionality, making the codebase modular and maintainable.

## Core Responsibilities

### Authentication (`auth.py`)
- User registration and validation
- Login with password verification
- Session management
- Password hashing for security

### Blog Management (`blog.py`)
- Display all posts
- Create new posts
- Edit/delete own posts
- Authorization checks

### Image Processing (`gcp.py`)
- Handle file uploads
- Coordinate OCR processing
- Optional LLM refinement
- Store and display results

### Database Interface (`db.py`)
- Manage database connections per request
- Initialize database from schema
- Provide CLI commands for database operations

## Request Flow

```
Browser → Flask Route → View Function → Database/Services → Template → Browser
```

**Typical flow for creating a post:**
1. User submits form → POST request to `/create`
2. Backend validates input
3. Backend inserts into database
4. Backend redirects to index page
5. User sees updated post list

## Configuration

Application configuration is managed through:
- `app.config` dictionary in `__init__.py`
- Environment variables for secrets
- Instance-specific config files (optional)

Common config values:
- `SECRET_KEY` - Session encryption
- `DATABASE` - SQLite file path
- `MAX_CONTENT_LENGTH` - Upload size limit

## Security Features

- **Password hashing** using Werkzeug
- **SQL injection prevention** via parameterized queries
- **Session-based authentication**
- **CSRF protection** on forms
- **File upload validation**

## Testing

Tests are located in the `tests/` directory and use pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py
```

## Next Steps

- **[Frontend Documentation](./frontend.md)** - How templates display data
- **[Database Documentation](./database.md)** - Data model and queries
- **[OCR Documentation](./ocr.md)** - Image processing pipeline
- **[Development Workflow](../development-workflow.md)** - Coding best practices

---

**Related Files:**
- `flaskr/__init__.py` - Application factory
- `flaskr/auth.py` - Authentication blueprint
- `flaskr/blog.py` - Blog blueprint
- `flaskr/gcp.py` - Image processing blueprint
- `flaskr/db.py` - Database utilities

