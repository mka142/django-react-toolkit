# django-react-toolkit
Set of tools that gives you easy start with ReactJS integration


# Setup
`pip install django-react-toolkit`
After installig add configuration to `settings.py`:
    
    INSTALLED_APPS=[
        ...
        'djnago_react_toolkit',
    ]
    DJ_REACT_PROXY_RULE=[
        #example data
        ('127.0.0.1',8080,['/api','/admin','/static'])
        ('127.0.0.1',3000,['.*']),
    ]
#### DJ_REACT_PROXY_RULE
It's list that conatains 3 element touples: `(host,port,endpoints_list)`. 
**host** - proxy IP address (default 127.0.0.1)
**port** - port on which proxy will be served
**endpoints_list** - list of valid python regex expressions that should match your route. 
*You need to know that proxy rules are iterated and there is choosed first match, so if you put `['.*']` as an element of first tuple and `['/api']` in secend element, you would never reach `/api` endpoint. It would look like this:*

    DJ_REACT_PROXY_RULE=[
        ('127.0.0.1',3000,['.*']),
        ('127.0.0.1',8080,['/api','/admin','/static']) #this can't be reached
        ]`


# Functionalities:
- ### `manage.py runtkserver`
  Commad that starts reverse proxy server based on our configuration `DJ_REACT_PROXY_RULE`. It's used for serving react dev server and django dev server from same domain.
  `manage.py runtkserver [--host (127.0.0.1)] [--port (8080)]`
  For example: `manage.py runtkserver --host 192.168.80.2 --port 8098` and then you should reach your server based on proxy rules defined in settings above at: `192.168.80.2:8098`.
    
