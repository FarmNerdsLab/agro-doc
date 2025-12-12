# Database Component

## Overview

SQLite database storing user accounts, blog posts, and image metadata.

## Key Files

```
webapp/
├── instance/flaskr.sqlite    # Database file
└── flaskr/
    ├── db.py                 # Database utilities
    └── schema.sql            # Schema definition
```

## Schema

**Tables:**
- `user` - User accounts and credentials
- `post` - Blog posts (linked to users via foreign key)

Additional tables for image uploads will be added as the project evolves.

## Usage

Initialize database:
```bash
flask --app flaskr init-db
```

## Key Concepts

- Connections managed per-request using Flask's `g` object
- Use parameterized queries for security
- Password hashing via Werkzeug
- JOINs for related data (e.g., posts with author info)

## Scaling

SQLite works well for development and small deployments. For production at scale, consider PostgreSQL or MySQL.

## Next Steps

- **[Backend Documentation](./backend.md)** - How database is used
- **[Development Workflow](../development-workflow.md)** - Testing practices

---

**Related Files:**
- `flaskr/db.py`
- `flaskr/schema.sql`
- `instance/flaskr.sqlite` (generated)
