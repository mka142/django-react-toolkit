from django.views.generic import View
from django.http import HttpResponse, FileResponse
import os

from .conf import REACT_ROOT_FILES, REACT_BUILD_DIR


class ServeReactView(View):
    def get(self, request):
        file_name = 'index.html'
        url = request.path.strip('/')
        try:
            if url in REACT_ROOT_FILES:
                file_name = url
                file = open(os.path.join(REACT_BUILD_DIR, file_name), 'rb')
                return FileResponse(file)

            with open(os.path.join(REACT_BUILD_DIR, file_name)) as file:
                return HttpResponse(file.read())
        except:
            return HttpResponse(
                """
            {} not found!
            """.format(request.path), status=501)
