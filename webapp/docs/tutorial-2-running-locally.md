# Tutorial 2: Running Agro-Doc Locally

## Overview

Now that you understand Flask fundamentals, it's time to run the Agro-Doc webapp locally. You'll set up a development environment using Docker containers (abstracted through VS Code), run the application, and make your first modifications.

## Learning Objectives

By the end of this tutorial, you will be able to:

1. Clone and set up the Agro-Doc repository
2. Use VSCode Dev Containers for isolated development
3. Run the webapp locally and interact with it
4. Make frontend changes (HTML/CSS) and see results
5. Make backend changes (Python) and test functionality
6. Understand the development workflow

## Prerequisites

Ensure you have the following installed:

- **Linux** (or WSL2 on Windows, or macOS)
- **Visual Studio Code** - [Download here](https://code.visualstudio.com/)
- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download here](https://git-scm.com/)
- **VS Code Dev Containers Extension** - [Install from marketplace](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## Step 1: Clone the Repository

Open a terminal and run:

```bash
# Navigate to your projects directory
cd ~/projects  # or wherever you keep your code

# Clone the repository
git clone https://github.com/FarmNerds/agro-doc.git

# Navigate into the webapp directory
cd agro-doc/webapp
```

## Step 2: Understanding Dev Containers

### What is a Dev Container?

A **dev container** is a Docker container specifically configured for development. It provides:

- **Consistent environment** - Everyone uses the same Python version, dependencies, and tools
- **Isolated setup** - Doesn't interfere with your system's Python installation
- **Easy onboarding** - New developers can start quickly without manual setup
- **Pre-configured tools** - VS Code extensions and settings are automatically installed

### Our Dev Container Setup

Look at `.devcontainer/devcontainer.json`:

```json
{
  "name": "FSec Flask",
  "build": {
    "dockerfile": "./Dockerfile",
    "context": ".."
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "esbenp.prettier-vscode"
      ]
    }
  },
  "forwardPorts": [5000],
  "remoteUser": "vscode"
}
```

**Key parts:**
- `dockerfile` - Specifies what's installed in the container
- `extensions` - VS Code extensions automatically installed
- `forwardPorts` - Port 5000 is forwarded so you can access the webapp
- `remoteUser` - Runs as the `vscode` user (not root)

## Step 3: Open in Dev Container

### Using VS Code Command Palette

1. **Open the project in VS Code:**
   ```bash
   code ~/projects/agro-doc/webapp
   ```

2. **Open the Command Palette:**
   - Press `Ctrl+Shift+P` (Windows/Linux)
   - Or press `Cmd+Shift+P` (macOS)

3. **Type and select:**
   ```
   Dev Containers: Reopen in Container
   ```

4. **Wait for the container to build** (first time may take a few minutes)
   - You'll see build progress in the terminal
   - VS Code will reload once complete

5. **Verify you're in the container:**
   - Look at the bottom-left corner of VS Code
   - Should show: **"Dev Container: FSec Flask"**

## Step 4: Set Up the Database

The webapp needs a database to store user accounts and posts. Let's initialize it:

```bash
# Make sure you're in the /workspaces/agro-doc/webapp directory

# Initialize the database
flask --app flaskr init-db
```

**Expected output:**
```
Initialized the database.
```

This creates a SQLite database file at `instance/flaskr.sqlite`.

## Step 5: Run the Application

Start the Flask development server:

```bash
flask --app flaskr run --host=0.0.0.0 --port=5000 --debug
```

**Command breakdown:**
- `flask` - The Flask CLI tool
- `--app flaskr` - Tells Flask where your app is
- `run` - Starts the development server
- `--host=0.0.0.0` - Makes the app accessible outside the container
- `--port=5000` - Runs on port 5000
- `--debug` - Enables debug mode (auto-reload on file changes)

**Expected output:**
```
 * Serving Flask app 'flaskr'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

## Step 6: Explore the Application

Open your browser and navigate to: **http://localhost:5000**

### Tour of the Interface

1. **Homepage** - Shows the latest posts/documents
2. **Register** - Create a new user account
3. **Login** - Sign in with your credentials
4. **Create Post** - Add new content
5. **GCP Upload** - Upload images for OCR processing

### Exercise: Navigate the App

Try the following:

1. Register a new account
2. Log in with your account
3. Create a blog post
4. Edit your post
5. Delete your post
6. Log out

**Pay attention to:**
- What URLs change as you navigate
- What database tables are being used
- How the app redirects after actions

## Step 7: Make a Frontend Change (HTML)

Let's modify the homepage to add a custom welcome message.

### Choose a Template

```bash
# Open the index template
code templates/blog/index.html
```

### Make Your Edit

Find this section (around line 10):

```html
{% block header %}
  <h1>{% block title %}Posts{% endblock %}</h1>
  {% if g.user %}
    <a class="action" href="{{ url_for('blog.create') }}">New</a>
  {% endif %}
{% endblock %}
```

**Change it to:**

```html
{% block header %}
  <h1>{% block title %}Posts{% endblock %}</h1>
  <p class="welcome-message">Welcome to Agro-Doc! Your digital farming notebook.</p>
  {% if g.user %}
    <a class="action" href="{{ url_for('blog.create') }}">New</a>
  {% endif %}
{% endblock %}
```

### See Your Changes

1. Save the file (`Ctrl+S`)
2. Refresh your browser (Flask auto-reloads with `--debug`)
3. You should see the welcome message on the homepage!

## Step 8: Make a Backend Change (Python)

Now let's modify the backend to change how posts are displayed.

### Scenario: Show Post Character Count

Let's add a character count to each post.

### Edit the Blog Blueprint

```bash
# Open the blog view
code flaskr/blog.py
```

Find the `index()` function:

```python
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
```

### Modify the Template

Open `templates/blog/index.html` and find where posts are displayed:

```html
<article class="post">
  <header>
    <div>
      <h1>{{ post['title'] }}</h1>
      <div class="about">by {{ post['username'] }} on {{ post['created'].strftime('%Y-%m-%d') }}</div>
    </div>
  </header>
  <p class="body">{{ post['body'] }}</p>
</article>
```

**Add character count:**

```html
<article class="post">
  <header>
    <div>
      <h1>{{ post['title'] }}</h1>
      <div class="about">
        by {{ post['username'] }} on {{ post['created'].strftime('%Y-%m-%d') }}
        • {{ post['body']|length }} characters
      </div>
    </div>
  </header>
  <p class="body">{{ post['body'] }}</p>
</article>
```

### Test Your Change

1. Save the file
2. Refresh your browser
3. You should see character counts next to each post!

## Understanding the Development Workflow

### The Edit-Save-Refresh Cycle

1. **Edit** code in VS Code
2. **Save** the file (`Ctrl+S`)
3. **Refresh** browser (Flask auto-reloads)
4. **Check** for errors in the terminal

### Debugging Tips

**If the server crashes:**
- Check the terminal for error messages
- Look for Python tracebacks
- Fix the error and the server will auto-restart

**If changes don't appear:**
- Hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R`)
- Check if you saved the file
- Verify you edited the correct file

**If you see "Working outside of application context":**
- This means you're trying to use Flask features outside a request
- Review Tutorial 1 on application context

## Stopping the Application

To stop the Flask server:

1. Go to the terminal where Flask is running
2. Press `Ctrl+C`

To exit the dev container:

1. Open Command Palette (`Ctrl+Shift+P`)
2. Select: `Dev Containers: Reopen Folder Locally`

## Summary

Congratulations! You've:

- Set up a development environment with Docker containers  
- Run the Agro-Doc webapp locally  
- Made frontend changes (HTML/CSS)  
- Made backend changes (Python)  
- Understand the development workflow

## Next Steps

Now that you can run and modify the application, dive deeper into the system architecture:

👉 **[System Architecture Overview](./architecture-overview.md)**

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find and kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Database locked error:**
```bash
# Remove the database and reinitialize
rm instance/flaskr.sqlite
flask --app flaskr init-db
```

**Module not found errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Docker build fails:**
- Ensure Docker Desktop is running
- Try rebuilding: `Dev Containers: Rebuild Container`
