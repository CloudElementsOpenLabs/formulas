# Formulas
Cloud Elements has created a community of custom made formulas that can be viewed, downloaded, and shared. This is an independent catalog of formulas and formula samples created by customers, partners and Cloud Elements developers. Additionally, this community supports our partners leveraging CloudElements technology.

## Contributing
To contribute we ask that you create a folder for the formula, using pascal casing for the folder name (ex. MyContactSync). The folder should contain the formula template JSON as well as a short README file with a description of what you built.
## WorkFlow Charts
If you would like a visual understanding of the workflows for a project, you can run:

bin/generate_flowchart.py <formula JSON file>
Which will generate workflow.png in the same directory as the formula. If you have multiple formulas in the same directory, you may want to rename the generated file.

You will need to install node, phantomjs, and mermaid first:

~~~~ brew install node
npm install -g phantomjs
npm install -g mermaid ~~~~
