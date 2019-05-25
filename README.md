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

  ```
  python manage.py createsuperuser
  ```

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

 

* To run development server use

  `python manage.py runserver`

  Open browser and go `localhost:8000`
***

### How to Use:

* #### Admin Access

  Use superuser information `userid: DB0001 and password: ********` to access admin panel in `localhost:8000/admin` or just login on the app using these information and click on `Admin Panel`.

  * ##### Create FoodItem

    Click on `FoodItem` and go to the food item control page and create new food item with necessary information

  * ##### Create Staff

    Click on `Account` and then select any of the user from the list and open the user information page and click on `is_staff` to make access on admin site and branch dashboard.

  * ##### Create CafeBrach

    Click on `CafeBranch` and add a new branch with necessary information. The manager should be a staff user.
    
  * ##### Create Group:
  
    Group is a collection of permission to access the admin panel. Make a group with some permission and add staff user on the group to access those.