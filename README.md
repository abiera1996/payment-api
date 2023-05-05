# Payment API

## Getting started
To make it easy for you to get started with bitbucket, here's a list of recommended next steps.

### Versions
Payment API runs on Python 3.10.4.


### Virtual Environment
Create and activate the virtual environment, and install the required packages.

- Install virtualenv.
  ```
  pip install virtualenv
  python -m venv env
  ```

- Create the virtual environment.
  ``` 
  python -m venv env
  ```

- Activate the virtual environment.
  - For bash (Linux):
    ```
    source env/bin/activate 
    ```
  - For console (Windows):
    ```
    .\env\Scripts\activate
    ```

- Install the required packages.
  ```
  pip install -r requirements.txt
  ```

- DB Migration
  ```
  sh migrate.sh
  ```

- Run python
  ```
  python manage.py runserver
  ```

### Clean migration file
```
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
pip install --upgrade --force-reinstall  Django==4.2.1
sh migrate.sh
```

> Use short lowercase names at least for the top-level files and folders except
> `LICENSE`, `README.md`