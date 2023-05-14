# authorization-flow-app
Authorization Flow App

# Installation
To install the project, follow these steps.
1. Clone this repository to your local machine.
2. Install the Docker Desktop on your machine.

# Usage
To use the project, follow these commands:
1. docker-compose build
2. docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py makemigrations"
3. docker-compose run --rm app sh -c "python manage.py migrate"
4. docker-compose up
5. open brower and run "http://127.0.0.1:8000/api/docs/"

# API methods
* /api/signup
  - POST: A user can be signed up with a username, email and password.
    ```json
     {
        "username": "string",
        "email": "user@example.com",
        "password": "string"
     } 
      
* /api/login
  - POST: A user can be logged in with username/email and password
      ```json
      {
        "username": "string",
        "password": "string"
      }
      
* /api/permissions
  - GET: get available permissions
  - POST: create new permission (e.g access, read, delete, etc)
      ```json
      {
        "name": "string"
      }
      
* /api/roles
  - GET: get available roles
  - POST: create a new role (e.g staff, admin, hr, etc)
      ```json
      {
        "name": "string",
        "permissions": [  # not required
            {
              "name": "string" 
            }
        ]
      }
      
* /api/roles/:id/permissions
  - GET: get available permission to a certain role
  - PUT: assign a permission to a role
    ```json
      {
        "name": "string",
        "permissions": [
              {
                "name": "string" # Many=True
              }
         ]
      }
      
* /api/users/:id/roles
  - GET: get list of roles added to the user
  - POST: can add a list of roles to the user
    ```json
      {
        "roles": [
              {
                "name": "string" # Many=True
              }
         ]
      }
      
* /api/users/:id/permissions
  - GET: get list of permissions assigned to a user
