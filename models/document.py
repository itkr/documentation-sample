# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect

from docutils.core import publish_string
from docutils.writers.html4css1 import HTMLTranslator, Writer


class DocumentDoesNotExist(Exception):
    pass


class _FakeList(list):

    def extend(self, *args, **kwargs):
        pass

    def append(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass


class NoHeaderHTMLTranslator(HTMLTranslator, object):

    def __init__(self, document):
        super(NoHeaderHTMLTranslator, self).__init__(document)
        self.head_prefix = _FakeList()
        self.body_prefix = _FakeList('<div>')
        self.body_suffix = _FakeList('</div>')
        self.stylesheet = _FakeList()
        self.head = _FakeList()
        self.meta = _FakeList()


class Document(object):

    def __init__(self, route, method=None, translator_class=NoHeaderHTMLTranslator):
        self.route = route
        self.method = method
        self.translator_class = translator_class
        self._writer = Writer()
        self._writer.translator_class = translator_class

    @classmethod
    def get_documents(cls, routes):
        documents = []
        for route in routes:
            if hasattr(route, 'get_children'):
                documents.extend([cls(child)
                                  for child in route.get_children()])
                continue
            documents.append(cls(route))
        return documents

    @classmethod
    def get_document(cls, routes, template, method):
        documents = cls.get_documents(routes)
        for document in documents:
            methods = document.get_request_method_names()
            if document.route.template == template and method in methods:
                return cls(document.route, method, document.translator_class)
        raise DocumentDoesNotExist

    @property
    def doc_html(self):
        settings = {'output_encoding': 'unicode'}
        return publish_string(self.doc_raw,
                              writer=self._writer,
                              settings_overrides=settings).strip()

    @property
    def doc_raw(self):
        return inspect.getdoc(self.route.handler) or ''

    def get_response_type(self):
        if hasattr(self.route.handler, 'write_json_response'):
            return 'application/json'
        if hasattr(self.route.handler, 'write_template_response'):
            return 'text/html'
        return 'Unknown'

    def get_request_method_names(self):
        methods = []
        allowed_methods = ('get', 'post', 'put', 'delete', 'patch')
        for method in allowed_methods:
            # 対象のメソッドが定義されていない
            if not hasattr(self.route.handler, method):
                continue
            # 定義されているが許可されていない
            if self.route.methods and method.upper() not in self.route.methods:
                continue
            methods.append(method.upper())
        if self.route.handler_method and (
                self.route.handler_method not in allowed_methods):
            methods.append('Unknown')
        return methods

    def to_dict(self):
        return {
            'name': self.route.name,
            'template': self.route.template,
            'doc_html': self.doc_html,
            'response_type': self.get_response_type(),
            'method': self.method,
            'methods': self.get_request_method_names(),
            'module': '.'.join([self.route.handler.__module__,
                                self.route.handler.__name__]),
            'response_schema': self.route.handler.response_schema_json(self.method),
            'response_sample': self.route.handler.response_sample_json(self.method),
            'request_schema': self.route.handler.request_schema_json(self.method),
            'request_sample': self.route.handler.request_sample_json(self.method),
            'request_header_sample': self.route.handler.request_header_sample_json(),
        }
