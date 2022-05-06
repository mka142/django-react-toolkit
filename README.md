# django-react-toolkit
Set of tools that gives you easy start with ReactJS integration

# About
Main goal of this project is to make django-react apps development and deployment easy in the most easiest way without much interfering to django and react internal project code.

# Getting Started
Add `django_react_toolkit` to your installed apps:
```
INSTALLED_APPS=[
    ...
    'djnago_react_toolkit',
]
```


# Functionalities:

## 1. Reverse Proxy server - `manage.py runtkserver` 
#### ⚠️ If you are working with **create-react-app** to add `proxy: django_server` to your `package.json` file and skip this option.
It's django-admin command used to start proxy server that sholud forward django and react traffic to one domain.
#### Setup
- Add proxy rule configuration to `settings.py`
```
DJ_REACT_PROXY_RULE=[
    #example configuration
    ('127.0.0.1',8000,['/api','/admin','/static']), # for django dev server
    ('127.0.0.1',3000,['.*']),                      # for react server
]
```

- Start django and react dev servers:
```
$ ./manage.py runserver
$ npm start
```
- Start proxy server:
```
$ ./manage.py runtkserver
```
Since our proxy is running default on port 8080. We can now access our django `/api`, `/admin` and `/static` and react `/*` from `localhost:8080`. 
    
## 2. ServeReactView - `django_react_toolkit.views.ServeReactView`
Django view that serve us react production build files
#### Setup
Add configuration to `settings.py`:
```

# path to folder where you built your react app
REACT_BUILD_DIR = "/your_react_build_folder/build"

# files that should be served from root path like exmaple.com/favicon.ico
REACT_ROOT_FILES = ['favicon.ico', 'manifest.json', 'robots.txt'] # <= that is default value

# set of paths reserved for django
DJANGO_PATHS = ['api','admin','media','static'])


STATICFILES_DIRS = [
    ...
    REACT_BUILD_DIR / 'static'
]
```
Include `django_react_toolkit` urls in `urls.py`:
```
urlpatterns = [
    ...
    include('django_react_toolkit.urls`)
]
```
`django_react_toolkit` will take every request that does not match your `DJANGO_PATHS` and serve instead `index.html` or one of `REACT_ROOT_FILES`.

If you want some custom urls just import `ServeReactView` directly:
```
from django_react_toolkit.views import ServeReactView
...
urlpatters = [
    re_path(r'/react_app/.*',ServeReactView.as_view(),name="serve_react_view")
]
```
#### 🖋️ If you have some static files (images,fonts,etc.) in react that are in public directory, you can also move them to `public/static` and after build they will be collected as well as `js and css` by django `collectstatic`.

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
- #### REACT_BUILD_DIR
  Path to react build
- #### REACT_ROOT_FILES
  List of filenames that should be served from root url. It means all files that directly under `build/` dir
- #### DJANGO_PATHS
  List of paths that will be reserved for djngo. E.g. api or admin panel etc.
### Commands:
- #### `manage.py runtkserver`
  Commad that starts reverse proxy server based on our configuration `DJ_REACT_PROXY_RULE`. It's used for serving react dev server and django dev server from same domain.
  `manage.py runtkserver [--host (127.0.0.1)] [--port (8080)]`
  For example: `manage.py runtkserver --host 192.168.80.2 --port 8098` and then you should reach your server based on proxy rules defined in settings above at: `192.168.80.2:8098`.
    
# To Do:
- [ ] django base viewset for session and JWT authentication
- [ ] helper js functions for authentication in react
- [ ] manage.py command that stats reverse proxy server and development server at the same time
