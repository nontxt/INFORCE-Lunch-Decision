# INFORCE-Lunch-Decision

## Steps to run the application from the docker:
1. Clone this repository
2. Go ahead in the project directory
3. Run `docker-compose up`


## Steps to run the application from the command line:
1. Clone this repository
2. Go ahead in the project directory
   * If you have pipenv, in your command line:
     1. Run `pipenv shell`
     2. Run `pipenv install` 
   * If you use virtualenv:
     1. Activate the virtualenv
     2. Run `pip install -r requirements.txt` in your command line
3. Run `python manage.py makemigrations`
4. Run `python manage.py migrate`
5. Run `python manage.py test` for run unittests
6. Run `python manage.py runscript seput` to populate databases
7. Run `python manage.py runserver`


## Edpoints:
### Auth:
| Endpoint              | Method | Parameters             | Description                          |
|-----------------------|--------|------------------------|--------------------------------------|
| `auth/users/`         | POST   | _username_, _password_ | Create new user                      |
| `auth/token/`         | POST   | _username_, _password_ | Obtain jwt access and refresh tokens |
| `auth/token/refresh/` | POST   | _refresh_              | Obtain new jwt access token          |
| `admin/`              | GET    |                        | Admin site                           |

**Note**: By default admin has **admin** as _username_ and _password_.

### API Account:

| Endpoint                           | Method | Parameters                                   | Description                             |
|------------------------------------|--------|----------------------------------------------|-----------------------------------------|
| `account/employees/`               | POST   |                                              | Assign user to employee group           |
| `account/employees/`               | DELETE |                                              | Remove user from the employee group     |
| `account/owners/`                  | POST   |                                              | Assign user to owner group              |
| `account/owners/`                  | DELETE |                                              | Remove user from the owner group        |

### API Lunch:

| Endpoint                           | Method | Parameters        | Description                       |
|------------------------------------|--------|-------------------|-----------------------------------|
| `lunch/restaurants/`               | GET    |                   | List of restaurants               |
| `lunch/restaurants/`               | POST   | _name_, _address_ | If user owner, create restaurant  |
| `lunch/restaurants/{id}/`          | GET    |                   | Retrieve a restaurant             |
| `lunch/restaurants/{id}/`          | DELETE |                   | If is owner of restaurant, delete |
| `lunch/restaurants/{id}/menu/`     | GET    |                   | Get current menu for restaurants  |
| `lunch/restaurants/{id}/set-menu/` | POST   | _items_           | Set new dayle menu                |
| `lunch/menus/`                     | GET    |                   | List of today menus               |
| `lunch/menus/{id}/`                | GET    |                   | Retrieve menu instance            |
| `lunch/menus/{id}/vote/`           | POST   |                   | Vote for the menu                 |
| `lunch/menus/{id}/unvote/`         | POST   |                   | Unvote form the menu              |
| `lunch/menus/best/`                | GET    |                   | Get best lunch place              |

**Note**: For using this API you must provide token for authenticate.
