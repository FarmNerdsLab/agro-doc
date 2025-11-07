# agro-doc
AgroDoc is an app that helps farmers input handwritten data into spreadsheets automatically.

[Notion Page for testing](https://www.notion.so/forthebirds/TrOCR-Testing-4a11aaf524f947c3b0069833b4bb462a)



## Launching the Webapp locally
For local launching, here's the workflow I've used so far:

After cloning the repository, `cd` into the `webapp` directory and run 
```
code .
```
to launch it in VSCode. With the Microsoft Dev Containers extension, hit `Ctrl+Shit+P` to open the Command Palette, and type in `Reopen in Devcontainer`.

After the IDE has relaunched, pull up the terminal in the devcontainer. Now run the following two commands:
```
flask --app flaskr init-db
```

After you see "Database initialized", now run:
```
flask --app flaskr run
```
to launch the app. 

## Notes
This prototype was adapted using the framework provided by the Flask quickstart, [Flaskr](https://flask.palletsprojects.com/en/stable/tutorial/database/)
