from django.urls import re_path

from .views import ServeReactView

from .conf import DJANGO_PATHS

match_expresion = f'^(?!{"|".join(DJANGO_PATHS)}).*'

urlpatterns = [
    re_path(r"{0}".format(match_expresion), ServeReactView.as_view(),name="serve_react_view")
]
