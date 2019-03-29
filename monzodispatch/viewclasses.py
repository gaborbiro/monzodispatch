import os

from django.http import HttpResponse, Http404
from django.utils.http import http_date
from django.views.generic import View
import mimetypes


class StaticFileView(View):
    http_method_names = ['get']
    dir = None
    file_name = None

    def get(self, request, *args, **kwargs):
        module_dir = os.path.dirname(__file__)
        path = os.path.join(module_dir, self.dir, self.file_name)
        mimetype, encoding = mimetypes.guess_type(path)
        mimetype = mimetype or 'application/octet-stream'
        if not os.path.exists(path):
            raise Http404('"%s" does not exist' % path)
        stat = os.stat(path)
        response = HttpResponse(open(path, 'rb').read(), content_type=mimetype)
        response['Last-Modified'] = http_date(stat.st_mtime)
        response['Content-Length'] = stat.st_size
        return response
