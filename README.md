![Logo](./static/images/logo.png)

# Joldar
Leave reviews about road quality in your place

---

# For developers
Before setting up, make sure that you have `Python 3.8+` installed

### Using a Virtual Environment
Virtual Environments can come in handy your project packages in a certain space.

    virtualenv venv
    venv\Scripts\activate.bat

### Installing Requirements
In `requirements.txt` you can notice essential packages the project needs to run, including `Django`

    pip install -r requirements.txt

### Running the App
If you want a clean database you may need to delete the current instance and run migrations, if you don't:

    python manage.py runserver