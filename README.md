# django-react-toolkit
Set of tools that gives you easy start with ReactJS integration

# What it all is about?
Main goal of this project is to make django-react apps development easy in the most easiest way without much interfering to django and react internal project code.

# Functionalities:

## 1. Reverse Proxy server - `manage.py runtkserver`
It's django-admin command used to start proxy server and work on django-react app on one domain.

### Setup from scratch
- Make root folder and create django and react projects:
    ```   
    mkdir example
    cd example
    ```
    django:
    ```
    python -m venv env <- create your own virtual environment
    source env/bin/activate
    pip install django==3.2 <- choose your version
    django-admin startproject backend
    ```
    react (create-react-app):
    ```
    npm init
    npm install create-react-app
    npx create-react-app frontend
    rm -r package.json package-lock.json node_modules/
    ```
    So at the end we've got two 3 folders:
    ```
    backend
    env
    frontend
    ```
- Then we should install `django-react-toolkit` and add some configuration to our django project `settings.py`

    Make sure you've got activated virtual env!!
    ```
    pip install django-react-toolkit
    ```
    backend/backend/settings.py
    
    ```
    INSTALLED_APPS=[
        ...
        'djnago_react_toolkit',
    ]
    DJ_REACT_PROXY_RULE=[
        #example configuration
        ('127.0.0.1',8000,['/api','/admin','/static']), # for django dev server
        ('127.0.0.1',3000,['.*']),                      # for react server
    ]
    ```
    `DJ_REACT_PROXY_RULE` is varible that contains all of our proxy configuration. So later on url: `/admin`,proxy should redirect our request to server working on `127.0.0.1:8000` (django dev server) - so we should see django admin panel.
- At the and let's start all services and see in browser our proxy in work:
    
    **frontend/**
    
    Start react development server
    ```npm run start```
    
    **backend/**
    
    Apply django migrations and run django development server
    ```
    python manage.py migrate
    python mange.py runserver
    ```
    
    **backend/ (in separete terminal window)**
    
    Firslty activate virtual environment and then run toolkit server (reverse proxy):
    ```
    source ../env/bin/acitivate
    python manage.py runtkserver
    ```
    
At this stage all work is done. We can now access our react and django server from one domain on `127.0.0.1:8080` - default proxy address (more in spec). django on urls `/api`,`/admin`,`/static` and react on other that don't match django urls.
    
# 2. ----
# 3. ----

## Spec:

### Varibles:
- #### DJ_REACT_PROXY_RULE
  It's list that conatains 3 element touples: `(host,port,endpoints_list)`. 
  **host** - proxy IP address (default 127.0.0.1)
  **port** - port on which proxy will be served
  **endpoints_list** - list of valid python regex expressions that should match your route. 
  *You need to know that proxy rules are iterated and there is choosed first match, so if you put `['.*']` as an element of first tuple and `['/api']` in secend element, you would never reach `/api` endpoint. It would look like this:*
    ```
    DJ_REACT_PROXY_RULE=[
        ('127.0.0.1',3000,['.*']),
        ('127.0.0.1',8000,['/api','/admin','/static']) #this can't be reached
        ]
    ```
### Commands:
- #### `manage.py runtkserver`
  Commad that starts reverse proxy server based on our configuration `DJ_REACT_PROXY_RULE`. It's used for serving react dev server and django dev server from same domain.
  `manage.py runtkserver [--host (127.0.0.1)] [--port (8080)]`
  For example: `manage.py runtkserver --host 192.168.80.2 --port 8098` and then you should reach your server based on proxy rules defined in settings above at: `192.168.80.2:8098`.
    
# To Do:
- [ ] django base viewset for session and JWT authentication
- [ ] helper js functions for authentication in react
- [ ] manage.py command that stats reverse proxy server and development server at the same time
