# Job Description Summaries
A simple web app that takes an formatted Excel file and uses  ChatGPT 4o to summarize extracted data from the file. Files can be previewed on the app or  downloaded.

## Technical Details
The Web app is written as a Single Page App (SPA) using Typescript + React + Vite and served as static files with Flask, using APIs to communicate between the SPA and Flask which handles all the data and does all the processing.


## Creating a new user
As requested, a new user can not be created on the web app, it has to be created from the backend (python) using a simple script. To do this, simply run the interactive script aptly named `create_new_user` and follow the steps to create a new user. This script expects the Python Web App to be fully running to create a new user. If the site/app is live then it running and you can create a new user.

1. `cd` to the app directory

```bash
cd hippolyte-summaries
```

2. Activate virtual environment

```bash
source bin/activate
```

3. Run the script to create a new user. Follow the instruction from the script

```bash
python -m src/create_new_user
```
That's all.


## Notes for the End User
- Ensure that the First and Second columns (General Question and Specific Questions respectively) are available as headers in the excel sheet. It is used as a strong pivot point/header for the rest of the document. The remaining columns can be dynamic.
    - Currently supported Titles are General Question, Specific Questions.
    - The default worksheet, Sheet1. You don't have to do anything for this. 
- ChatGPT (LLMs in general) may fail to follow System Prompts and produce unrelated or useless information
