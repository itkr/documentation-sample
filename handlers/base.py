# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os

import jinja2
import webapp2
from jsonschema import ValidationError, validate

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


class BaseJsonHandler(webapp2.RequestHandler):

    @staticmethod
    def _to_json_string(dictionary):
        return json.dumps(
            dictionary, indent=2, separators=(',', ': '), sort_keys=True)

    @classmethod
    def _make_sample(cls, obj):
        # TODO: 必要になったものから継ぎ足していっているので質の高いライブラリなどを利用したい。
        sample = {}
        for key, value in obj.items():
            if isinstance(value, basestring):
                continue
            if isinstance(value.get('anyOf'), list) and len(value.get('anyOf')) > 0:
                sample[key] = cls._make_sample({'_': value['anyOf'][0]})['_']
                continue
            if isinstance(value.get('oneOf'), list) and len(value.get('oneOf')) > 0:
                sample[key] = cls._make_sample({'_': value['oneOf'][0]})['_']
                continue
            if value.get('type') == 'object':
                sample[key] = cls._make_sample(value.get('properties', {}))
                continue
            if value.get('type') == 'array':
                sample[key] = [cls._make_sample(
                    {'_': value.get('items')})['_']]
                continue
            if isinstance(value.get('examples'), list) and len(value['examples']) > 0:
                sample[key] = value.get('examples')[0]
                continue
            if value.get('default') is not None:
                sample[key] = value['default']
            sample[key] = {
                'string': '',
                'integer': 0,
                'boolean': False,
            }.get(value.get('type'), None)
        return sample

    @classmethod
    def response_sample(cls, method=None):
        return cls._make_sample({'_': cls.response_schema(method)})['_'] or {}

    @classmethod
    def response_sample_json(cls, method=None):
        return cls._to_json_string(cls.response_sample(method))

    @classmethod
    def response_schema_json(cls, method=None):
        return cls._to_json_string(cls.response_schema(method))

    @classmethod
    def request_sample(cls, method=None):
        return cls._make_sample({'_': cls.request_schema(method)})['_'] or {}

    @classmethod
    def request_sample_json(cls, method=None):
        return cls._to_json_string(cls.request_sample(method))

    @classmethod
    def request_schema_json(cls, method=None):
        return cls._to_json_string(cls.request_schema(method))

    @classmethod
    def response_schema(cls, method=None):
        raise NotImplementedError

    @classmethod
    def request_schema(cls, method=None):
        if method in ('get', 'delete', 'GET', 'DELETE') or method is None:
            return {}
        raise NotImplementedError

    @classmethod
    def request_header_sample(cls):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
        }

    @classmethod
    def request_header_sample_json(cls):
        return cls._to_json_string(cls.request_header_sample())

    @property
    def request_body(self):
        return self.validate_request_body()

    def parse_json_request(self):
        return json.loads(self.request.body, encoding='utf-8')

    def validate_request_body(self):
        request_body = self.parse_json_request()
        try:
            validate(request_body, self.request_schema(self.request.method))
        except ValidationError as e:
            self.abort(400, e)
        return request_body

    def write_json_response(self, response):
        self.response.headers[str('Content-Type')] = str('application/json')
        self.response.write(json.dumps(response))

    def _get_valid_response_or_error(self, response):
        # 不正な値ならValidationErrorが発生
        validate(response, self.response_schema(self.request.method))
        return response

    def dispatch(self):
        response = super(BaseJsonHandler, self).dispatch()
        response = self._get_valid_response_or_error(response)
        self.write_json_response(response)


class BaseTemplateHandler(webapp2.RequestHandler):

    JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(ROOT_DIR),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

    @property
    def template_name(self):
        raise NotImplemented

    def get_template(self):
        return self.JINJA_ENVIRONMENT.get_template(self.template_name)

    def write_template_response(self, response):
        self.response.headers[str('Content-Type')] = str('text/html')
        self.response.write(self.get_template().render(response))

    def dispatch(self):
        response = super(BaseTemplateHandler, self).dispatch()
        if response:
            self.write_template_response(response)
