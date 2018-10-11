# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import traceback

import jinja2
import webapp2
from jsonschema import ValidationError, validate
from webob import exc

from consts import ROOT_DIR

from .schema import make_error_response_schema


class JsonSchemaMixin(object):

    @staticmethod
    def _is_error_response(response):
        if not isinstance(response, dict):
            return False
        try:
            validate(response, make_error_response_schema())
        except ValidationError:
            return False
        return True

    @staticmethod
    def _to_json_string(dictionary):
        return json.dumps(dictionary, indent=2, separators=(',', ': '))

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
        validate(request_body, self.request_schema(self.request.method))
        return request_body


class BaseJsonHandler(webapp2.RequestHandler, JsonSchemaMixin):

    def write_json_response(self, response):
        self.response.headers[str('Content-Type')] = str('application/json')
        self.response.write(json.dumps(response))

    def make_error_response(self, msg='error', **kwargs):
        code = int(kwargs.get(str('code'), 400))
        self.error(code)
        return {
            'status': code,
            'message': msg
        }

    def _get_valid_response_or_error(self, response):
        if response is None:
            return
        _response = response
        try:
            validate(response, self.response_schema(self.request.method))
        except ValidationError as e:
            if self._is_error_response(response):
                self.write_json_response(response)
                return
            response = self.make_error_response(
                '{}: {}'.format(e.__class__.__name__, e.message), code=500)
            response['response'] = _response
        return response

    def dispatch(self):
        response = super(BaseJsonHandler, self).dispatch()
        response = self._get_valid_response_or_error(response)
        if response:
            self.write_json_response(response)

    def handle_exception(self, exception, debug):
        if isinstance(exception, ValidationError):
            response = self.make_error_response(code=400, msg=exception.message)
            response.update({
                'validator': exception.validator,
                'instance': exception.instance,
                # 'schema': exception.schema,
            })
            return response
        if isinstance(exception, exc.HTTPError):
            return self.make_error_response(
                code=exception.code,
                msg='{} ({})'.format(exception.title, exception.detail or ''))
        if not debug:
            error_trace = traceback.format_exception_only(
                type(exception), exception)
            return self.make_error_response('{}: {}'.format(type(exception).__name__, error_trace))
        return super(BaseJsonHandler, self).handle_exception(exception, debug)


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
