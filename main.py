#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import webapp2
from paste import httpserver
from webapp2 import Route, abort
from webapp2_extras.routes import PathPrefixRoute

from handlers.base import BaseTemplateHandler
from handlers.sample import routes as sample_routes
from models.document import Document, DocumentDoesNotExist


class DocumentListHandler(BaseTemplateHandler):

    template_name = 'templates/documents/list.html'

    def get(self):
        global _api_routes
        documents = [doc.to_dict()
                     for doc in Document.get_documents(_api_routes)]
        try:
            # methodが定義されているがルーティングが許可されていないものが存在する場合methodsが空になりIndexエラーになる
            documents = sorted(documents, key=lambda x: x['methods'][0])
        except IndexError:
            pass
        documents = sorted(documents, key=lambda x: x['template'])
        return {'documents': documents}


class DocumentDetailHandler(BaseTemplateHandler):

    template_name = 'templates/documents/detail.html'

    def get(self):
        global _api_routes
        try:
            document = Document.get_document(
                _api_routes,
                self.request.get('template'),
                method=self.request.get('method'))
        except DocumentDoesNotExist:
            abort(404)
            return
        return {'document': document.to_dict()}


# Documentation
_routes = [
    Route('/', webapp2.RedirectHandler, defaults={'_uri': '/docs/'}),
    PathPrefixRoute('/docs', [
        Route('/detail', DocumentDetailHandler),
        Route('/', DocumentListHandler),
    ]),
]

# REST API
_api_routes = [
    PathPrefixRoute('/v1', [
        PathPrefixRoute('/sample', sample_routes),
    ]),
]

_routes.extend(_api_routes)

app = webapp2.WSGIApplication(_routes, debug=True)


def main():
    httpserver.serve(app, host='127.0.0.1', port='8000')


if __name__ == '__main__':
    main()
