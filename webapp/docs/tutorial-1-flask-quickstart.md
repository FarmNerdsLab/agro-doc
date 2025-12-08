# Tutorial 1: Flask Quickstart

## Overview

Since much of the overall architecture of the codebase is adapted from the Flask quickstart guide tutorial, it'll be incredibly helpful to walk through it.

## Learning Objectives

By completing this tutorial, you will:

1. **Understand information flow in a web application**  
   Learn how data moves between the browser, server, and database in a blog-post webapp.

2. **Recognize file purposes and structure**  
   Understand what each file does and why we organize code this way:
   - `.py` files contain Python backend logic
   - `.html` files serve content to users
   - `.sql` files define database schemas
   - `.css` files style the appearance

3. **Learn Flask architecture patterns**  
   Understand blueprints, templates, routing, and how they fit together.

4. **Build confidence for extending the codebase**  
   See how you might develop new features on top of this architecture.

## The Tutorial

Follow the official Flask Tutorial from start to finish:

🔗 **[Flask Tutorial: Make Your Project Installable](https://flask.palletsprojects.com/en/stable/tutorial/)**

### What You'll Build

You'll create a basic blog application called "Flaskr" where users can:
- Register and log in
- Create, edit, and delete blog posts
- View all posts from all users

### Important Sections to Focus On

1. **Application Setup** - Understanding the application factory pattern
2. **Database** - How Flask interacts with SQLite
3. **Blueprints and Views** - Organizing routes and view functions
4. **Templates** - Using Jinja2 to render HTML dynamically
5. **Static Files** - Serving CSS, JavaScript, and images

## Connecting to Agro-Doc

Once you've completed the Flask tutorial, you'll notice that Agro-Doc follows a similar structure:

| Flask Tutorial | Agro-Doc Equivalent |
|---------------|---------------------|
| `flaskr/__init__.py` | `flaskr/__init__.py` |
| `auth.py` blueprint | `auth.py` blueprint |
| `blog.py` blueprint | `blog.py` + `gcp.py` blueprints |
| `db.py` database helpers | `db.py` database helpers |
| `templates/` folder | `templates/` folder |
| `static/` folder | `static/` folder |

The main difference is that Agro-Doc adds:
- **Image upload and processing** (`gcp.py`)
- **OCR handwriting recognition** (coming in Tutorial 2)
- **LLM text refinement** (planned for a future tutorial)

## Next Steps

Once you've completed the Flask tutorial and feel comfortable with the concepts, proceed to:

**[Tutorial 2: Running Agro-Doc Locally](./tutorial-2-running-locally.md)**

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
