import os

from django.http import HttpResponse, Http404
from django.utils.http import http_date
from django.views.generic import View


class StaticFileView(View):
    http_method_names = ['get']
    dir = None
    file_name = None

    def get(self, request, *args, **kwargs):
        module_dir = os.path.dirname(__file__)
        path = os.path.join(module_dir, self.dir, self.file_name)
        if not os.path.exists(path):
            raise Http404('"%s" does not exist' % path)
        stat = os.stat(path)
        response = HttpResponse(open(path, 'rb').read())
        response['Last-Modified'] = http_date(stat.st_mtime)
        response['Content-Length'] = stat.st_size
        return response
