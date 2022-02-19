# EcommerceUniversityProject
## Introduction
This is a university project that is meant to teach us how to create a fully functioning web application with the use of Django and React.
## Main frameworks and tools used in this project
- Django (as the backend - server side) to handle interactions with the database
- React (as frontend - UI side) to handle the creation of the UI
- Django REST Framework - helps building API's 
- React-bootstrap - helps organizing the page structure and provides useful functionality for managing the UI
- Redux - used as a state management tool in React, it helps the React components retrieve required states from a centralized point called the store
- Axios - used in the frontend to make calls to get/receive data from the database or manage the certain API call
- Swagger UI - serves as the documentation of the API calls that have been created by Django REST Framework

## How to start the project
Requirements:
You should have Python and NodeJS installed

### Cloning/downloading repository
The first step is to locally clone the repository to a new folder.

### Installing and creating virtual environment

1. Open command line and navigate to the folder in which you have your repository.
2. Install virtualenv library
```
pip install virtualenv
```
3. After a successful installation create a new virtual env folder (commands many vary depending on the python interpreter version)
```
python venv env
```
4. Now we need to activate our virtual environment
```
env\Scripts\activate
```

### Preparing backend for launch (Django)

1. We need to install all the required packages that are provided in the requirements.txt file
```
cd EcommerceUniversityProject && pip install -r requirements.txt
```
2. If everything is successful run the following command to start the django backend server
```
python manage.py runserver
```

### Preparing frontend for launch (React)

(Best practices is to do this in a seperate command line terminal)

1. Navigate to the folder frontend
```
cd frontend
```
2. Assuming that NodeJS is installed you can run
```
npm install
```
3. After a successful installation, the last step is to run start the React frontend
```
npm start
```

After this step you should access to the web application via browser, the website is available under the link: localhost:3000/


## Viewing documentation (Swagger)

The swagger API documentation is available under the link: localhost:8000/swagger/
(assuming you have the django server running).

To test most of the API calls we must be an authenticated user, so firstly in the Swagger UI we must navigate to the api/users/login and provide a valid username and password to receive a token.
After this step, we can copy the long line (token) and navigate to the top to find the *Authorize* button (lock symbol). After we click on it we will have the possibility to paste our token in the Value field.
The Value field *MUST* be filled in like given:
```
Bearer *copied_token*
```
