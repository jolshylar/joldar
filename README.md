![Logo](./static/images/logo.png)

# Joldar
~ leave reviews about road quality in your place

---

# For developers
Before setting up, make sure that you have `Python 3.8+` installed

### Using a Virtual Environment
Virtual Environments can come in handy your project packages in a certain space.

    virtualenv venv
    venv\Scripts\activate

### Installing Requirements
In `requirements.txt` you can notice essential packages the project needs to run, including `Django`

    pip install -r requirements.txt

### Almost done!
Now you need to apply database migrations (this project uses `SQLite3`)

    python manage.py makemigrations
    python manage.py migrate

### Running the App
If you want a clean database you may need to delete the current instance and run migrations, if you don't:

    python manage.py runserver
