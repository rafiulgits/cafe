# cafe

### Requirements and Setup:
  * Environment : 
      * Python 3.6.2 (recommended) or upper version
      * To install all dependencies open command window in project root directory and make this command 
        > `pip3 install -r requirements.txt`
  * Database : 
      * If MySQL want to use then make a database such `cafe_db` and make a change in `cafe/settings.py`. Change the `USER` and `PASSWORD` if necessary
    ```py
      DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'cafe_db',
          'HOST': '127.0.0.1',
          'PORT': '3306',
          'USER': 'root',
          'PASSWORD': '',
      }}
    ```
      * If want to use SQLite3 then use
      ```py
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.sqlite3',
              'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
          }
      }
      
      ```
      
      
  * Model sync with DB:
    * Open command window in project root directory and make these commands (Linux)
     ```
     python3 manage.py makemigrations user
     python3 manage.py makemigrations home
     python3 manage.py migrate
     ```
    
    * Windows
    ```
    python manage.py makemigrations user
    python manage.py makemigrations home
    python manage.py migrate
    ```
  
  * Create a superuser
  > python manage.py createsuperuser
    ```
    Userid: DB0001
    Name: Mr. User
    Phone: XXXXXXXXX
    Email: example@mail.com
    Gender: M
    Card: 12321431231
    Password:********
    Password (again): ********
    This password is too common.
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.
    ```
