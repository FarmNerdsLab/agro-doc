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
# GOOD
db.execute('SELECT * FROM user WHERE username = ?', (username,))

# BAD - SQL injection vulnerability!
db.execute(f'SELECT * FROM user WHERE username = "{username}"')
```

✅ **Hash passwords:**

```python
from werkzeug.security import generate_password_hash, check_password_hash

hashed = generate_password_hash(password)
```

### Performance

- Use JOINs instead of multiple queries (avoid N+1 problem)
- Add indexes for frequently queried columns
- Commit only when necessary

## Database Tools

### SQLite CLI

```bash
# Open database
sqlite3 instance/flaskr.sqlite

# Common commands
.tables              # List tables
.schema user         # Show table structure
SELECT * FROM user;  # Query data
.quit                # Exit
```

### Backup

```bash
# Full backup
sqlite3 instance/flaskr.sqlite .dump > backup.sql

# Restore
sqlite3 instance/flaskr.sqlite < backup.sql
```

## Troubleshooting

**Database locked:** Ensure connections are closed properly  
**Table already exists:** Delete database file and reinitialize  
**Foreign key violations:** Delete related records first or use CASCADE

## Scaling Considerations

SQLite limitations:
- Single writer at a time
- Not ideal for high-concurrency

When outgrowing SQLite, consider migrating to PostgreSQL or MySQL. Flask code changes will be minimal.

## Next Steps

- **[Backend Documentation](./backend.md)** - How database is used in routes
- **[Development Workflow](../development-workflow.md)** - Testing practices

---

**Related Files:**
- `flaskr/db.py` - Database utilities
- `flaskr/schema.sql` - Schema definition
- `instance/flaskr.sqlite` - Database file (generated)


**Indexes:**
- Primary key on `id`
- Unique constraint on `username`

**Example Data:**

| id | username | password |
|----|----------|----------|
| 1 | alice | pbkdf2:sha256:... |
| 2 | bob | pbkdf2:sha256:... |

---

### Post Table

**Purpose:** Store blog post content

**Schema:**

```sql
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
```

**Fields:**

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique post identifier |
| `author_id` | INTEGER | NOT NULL, FOREIGN KEY | References `user.id` |
| `created` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Post creation time |
| `title` | TEXT | NOT NULL | Post title |
| `body` | TEXT | NOT NULL | Post content |

**Relationships:**
- `author_id` → `user.id` (many-to-one)

**Example Data:**

| id | author_id | created | title | body |
|----|-----------|---------|-------|------|
| 1 | 1 | 2024-01-15 10:30 | First Post | Hello world! |
| 2 | 1 | 2024-01-16 14:20 | My Farm | Today we planted... |
| 3 | 2 | 2024-01-17 09:15 | Harvest Notes | The corn is ready... |

---

### GCP Upload Table (TODO)

[TODO: Document the GCP/image upload table structure]

**Expected Fields:**
- `id` - Unique identifier
- `user_id` - Who uploaded it
- `filename` - Original filename
- `filepath` - Storage location
- `uploaded_at` - Upload timestamp
- `ocr_text` - Raw OCR output
- `refined_text` - LLM-refined output
- `status` - Processing status

---

## Database Operations

### Initialization

Create the database and tables:

```bash
flask --app flaskr init-db
```

This executes `schema.sql` and creates `instance/flaskr.sqlite`.

### Connection Management

**Get connection:**

```python
from flaskr.db import get_db

db = get_db()
```

**Automatic cleanup:**

Connections are automatically closed after each request via the `close_db()` teardown function.

---

## Common Queries

### User Operations

#### Create User

```python
db = get_db()
db.execute(
    'INSERT INTO user (username, password) VALUES (?, ?)',
    (username, hashed_password)
)
db.commit()
```

#### Find User by Username

```python
user = db.execute(
    'SELECT * FROM user WHERE username = ?',
    (username,)
).fetchone()
```

#### Find User by ID

```python
user = db.execute(
    'SELECT * FROM user WHERE id = ?',
    (user_id,)
).fetchone()
```

---

### Post Operations

#### Create Post

```python
db = get_db()
db.execute(
    'INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)',
    (title, body, g.user['id'])
)
db.commit()
```

#### Get All Posts (with Author Info)

```python
posts = db.execute(
    'SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' ORDER BY created DESC'
).fetchall()
```

#### Get Single Post

```python
post = db.execute(
    'SELECT p.id, title, body, created, author_id, username'
    ' FROM post p JOIN user u ON p.author_id = u.id'
    ' WHERE p.id = ?',
    (id,)
).fetchone()
```

#### Update Post

```python
db = get_db()
db.execute(
    'UPDATE post SET title = ?, body = ? WHERE id = ?',
    (title, body, id)
)
db.commit()
```

#### Delete Post

```python
db = get_db()
db.execute('DELETE FROM post WHERE id = ?', (id,))
db.commit()
```

---

## SQLite Row Objects

Flask configures SQLite to return `sqlite3.Row` objects, which behave like dictionaries:

```python
user = db.execute('SELECT * FROM user WHERE id = ?', (1,)).fetchone()

# Access by column name
print(user['username'])  # 'alice'
print(user['id'])        # 1

# Or by index
print(user[0])  # 1
print(user[1])  # 'alice'
```

---

## Database Utilities (`db.py`)

### Core Functions

```python
def get_db():
    """Get database connection for current request"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close database connection at end of request"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database with schema.sql"""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    """Register database functions with Flask app"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
```

---

## Best Practices

### Security

✅ **Always use parameterized queries:**

```python
# GOOD (parameterized)
db.execute('SELECT * FROM user WHERE username = ?', (username,))

# BAD (SQL injection vulnerability!)
db.execute(f'SELECT * FROM user WHERE username = "{username}"')
```

✅ **Hash passwords:**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Storing password
hashed = generate_password_hash(password)
db.execute('INSERT INTO user (username, password) VALUES (?, ?)', 
           (username, hashed))

# Verifying password
if check_password_hash(user['password'], password):
    # Login successful
```

✅ **Validate input:**

```python
if not username or not password:
    error = 'Username and password are required'
```

### Performance

✅ **Use joins instead of multiple queries:**

```python
# GOOD (single query with join)
posts = db.execute(
    'SELECT p.*, u.username FROM post p JOIN user u ON p.author_id = u.id'
).fetchall()

# BAD (N+1 query problem)
posts = db.execute('SELECT * FROM post').fetchall()
for post in posts:
    user = db.execute('SELECT username FROM user WHERE id = ?', 
                     (post['author_id'],)).fetchone()
```

✅ **Commit only when necessary:**

```python
# Multiple inserts in one transaction
db.execute('INSERT INTO post ...')
db.execute('INSERT INTO post ...')
db.commit()  # Commit once
```

✅ **Use indexes for frequently queried columns:**

```sql
CREATE INDEX idx_post_author ON post(author_id);
CREATE INDEX idx_post_created ON post(created);
```

---

## Schema Migrations

### Current Approach

Currently, schema changes require manual steps:

1. Modify `schema.sql`
2. Drop and recreate database
3. Reload data

**Commands:**

```bash
# Backup data
sqlite3 instance/flaskr.sqlite .dump > backup.sql

# Reinitialize
rm instance/flaskr.sqlite
flask --app flaskr init-db

# Restore data (if compatible)
sqlite3 instance/flaskr.sqlite < backup.sql
```

### Future: Migration Tools

[TODO: Consider adding Alembic for migrations]

---

## Querying the Database Directly

### Using SQLite CLI

```bash
# Open database
sqlite3 instance/flaskr.sqlite

# Common commands
.tables              # List tables
.schema user         # Show table structure
SELECT * FROM user;  # Query data
.quit                # Exit
```

### Using Python

```python
import sqlite3

conn = sqlite3.connect('instance/flaskr.sqlite')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Query
cursor.execute('SELECT * FROM user')
users = cursor.fetchall()

for user in users:
    print(user['username'])

conn.close()
```

---

## Testing with Database

### Test Database Setup

```python
import pytest
from flaskr.db import get_db

def test_get_db(app):
    """Test database connection"""
    with app.app_context():
        db = get_db()
        assert db is get_db()  # Same connection within context

def test_init_db_command(runner):
    """Test init-db CLI command"""
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
```

### Using Test Fixtures

```python
@pytest.fixture
def app():
    """Create app with test config"""
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:',  # Use in-memory database
    })
    
    with app.app_context():
        init_db()
        
    yield app

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()
```

---

## Backup and Restore

### Backup

```bash
# Full backup
sqlite3 instance/flaskr.sqlite .dump > backup.sql

# Backup specific table
sqlite3 instance/flaskr.sqlite "SELECT * FROM user;" > users_backup.csv
```

### Restore

```bash
# Restore full database
sqlite3 instance/flaskr.sqlite < backup.sql
```

---

## Troubleshooting

### Database Locked

**Problem:** `database is locked` error

**Causes:**
- Multiple processes accessing database
- Long-running transaction
- Uncommitted changes

**Solutions:**
```python
# Ensure commits are called
db.commit()

# Close connections properly
close_db()

# Increase timeout
conn = sqlite3.connect('db.sqlite', timeout=10.0)
```

### Table Already Exists

**Problem:** `table already exists` error during init-db

**Solution:**
```bash
rm instance/flaskr.sqlite
flask --app flaskr init-db
```

### Foreign Key Violations

**Problem:** Cannot delete user with posts

**Solution:**
```sql
-- Either cascade deletes (modify schema)
FOREIGN KEY (author_id) REFERENCES user (id) ON DELETE CASCADE

-- Or delete posts first
DELETE FROM post WHERE author_id = ?;
DELETE FROM user WHERE id = ?;
```

---

## Scaling Considerations

### SQLite Limitations

- Single writer at a time
- Not ideal for high-concurrency web apps
- File-based (not distributed)

### Migration Path

When outgrowing SQLite, consider:

1. **PostgreSQL** - Full-featured, scalable
2. **MySQL** - Widely supported
3. **Cloud SQL** - Managed database service

### Code Changes Needed

Minimal! Flask abstracts most SQL:

```python
# Works with SQLite, PostgreSQL, MySQL
db.execute('SELECT * FROM user WHERE id = ?', (user_id,))
```

Only database-specific features need changes.

---

## Next Steps

- **[Backend Documentation](./backend.md)** - See how database is used in routes
- **[Development Workflow](../development-workflow.md)** - Learn testing practices
- **[API Reference](../api-reference.md)** - Explore all endpoints

---

## Questions to Explore

1. Why use parameterized queries instead of string formatting?
2. What's the difference between `fetchone()` and `fetchall()`?
3. When should you call `db.commit()`?
4. How do foreign keys maintain data integrity?
5. What are the trade-offs of using SQLite vs PostgreSQL?

---

**Related Files:**
- `flaskr/db.py`
- `flaskr/schema.sql`
- `instance/flaskr.sqlite` (generated)
