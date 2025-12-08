# Agro-Doc Documentation

Welcome to the Agro-Doc documentation! This guide will help you understand, run, and contribute to the Agro-Doc project.

## About This Project

Agro-Doc is a web application designed to help the farmers at Powisset Farm in Dover, MA streamline their documentation workflows. When we were working at Powisset Farm and co-designing with the head farmers, we learned that a big struggle of theirs was recording their field notes and harvest metrics digitally in their Excel spreadsheets. 

Each week, the farmers would fill out a whiteboard with relevant information throughout the week, such as a grid of harvests for each day, contamination information, to-dos throughout the week, etc.

![image of Powisset Whiteboard](/webapp/flaskr/static/uploads/images/pow_whiteboard.jpg)

The workflow they adopted over time was to take a picture of the whiteboard as everyone was heading out Friday afternoon, and then come in on the weekends and manually enter in the values by zooming into the picture on their phone to read each cell.

**Our goal is to streamline this process by using modern technology such as Optical Character Recognition (OCR) with AI models to digitally translate their handwriting and automatically populate their spreadsheets.**

## Prerequisites

Before getting started, you should have:
- Completed a first-year programming course (familiarity with Python)
- Basic understanding of Git and version control
- Linux environment (or WSL on Windows)
- [Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) installed
- [DevContainers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in VSCode

## Onboarding To-Do List

### Getting Started
Before jumping into making new features and committing code to this project, complete the onboarding tutorials.

1. **[Tutorial 1: Flask Quickstart](./tutorial-1-flask-quickstart.md)**  
   Learn Flask fundamentals by completing the official Flask quickstart. By the end of this tutorial, you will have a foundation to understand this webapp architecture as it is (currently) heavily adapted from the quickstart.

2. **[Tutorial 2: Running Agro-Doc Locally](./tutorial-2-running-locally.md)**  
   Set up your development environment, run the webapp using *DevContainers*, and make your first modifications.

### Understanding the System
To understand the overall system, see these documents linked below:

3. **[System Architecture Overview](./architecture-overview.md)**  
   High-level overview of how all the components work together.

4. **[Component Documentation](./components/)**  
    Documentation for each system component:
   - [Backend (Flask)](./components/backend.md)
   - [Frontend (HTML/CSS Templates)](./components/frontend.md)
   - [Database (SQLite)](./components/database.md)
   - [OCR Handwriting Recognition](./components/ocr.md)
   - [LLM Text Refinement](./components/llm.md)

### Development Guides
5. **[Development Workflow](./development-workflow.md)**  
   Best practices for developing and testing changes.

6. **[Deployment Guide](./deployment.md)**  
   How to deploy the application to production.

### Reference
7. **[API Reference](./api-reference.md)**  
   Detailed API endpoints and usage.

8. **[Troubleshooting](./troubleshooting.md)**  
   Common issues and solutions.

## Quick Start

If you just want to get the app running quickly:

```bash
# Clone the repository
git clone https://github.com/FarmNerds/agro-doc.git
cd agro-doc/webapp

# Open in VS Code
code .

# Open Command Palette (Ctrl+Shift+P) and select:
# "Dev Containers: Reopen in Container"

# Once in the container, run:
pip install -r requirements.txt
flask --app flaskr init-db
flask --app flaskr run --host=0.0.0.0 --port=5000 --debug
```

Visit `http://localhost:5000` in your browser.

## Contributing

To make contributions, please do so in the form of a Pull Request to main.
## Support

Contact Eddy, Arianne, or Alessandra with any questions (epan2@olin.edu, afong@olin.edu, aferzoco@olin.edu)