from django.conf import settings


REACT_BUILD_DIR = getattr(settings, 'REACT_BUILD_DIR')
REACT_ROOT_FILES = getattr(settings, 'REACT_ROOT_FILES',['favicon.png', 'manifest.json', 'robots.txt'])

DJANGO_PATHS = getattr(settings,'DJANGO_PATHS',['api','admin','media','static'])
