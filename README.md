OleOle Chat App
===================

OleOle application : Try and run using python 2.7

1. Set up a virtual environment. Run this command in terminal:
`virtualenv venv`</br>
In case you do not have `virtualenv` installed, run `pip install virtualenv`

2. Activate your virtual environment : `source activate venv`

2. To run this application install the requirements in a virtual environment:
`pip install -r requirements.txt`

3. Create a postgres database called chatdb4 : `createdb chatdb4`

4. Export oleoleapp.py as environment variable : `export FLASK_APP=oleoleapp.py`

5. Run the app : `python -m flask run` and visit `http://localhost:5000` in one or more browser tabs.
