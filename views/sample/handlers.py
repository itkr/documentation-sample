# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from views.base import BaseJsonHandler


class GetSampleHandler(BaseJsonHandler):
    """
    Get
    ===

    Dataを一つ取得する.
    """

    @classmethod
    def response_schema(cls, method=None):
        return {
            'type': 'object',
            'properties': {
                'status': {
                    'type': 'integer',
                },
                'message': {
                    'type': 'string',
                },
                'result': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'string',
                        },
                        'value': {
                            'type': 'string',
                        }
                    },
                    'required': ['id', 'value'],
                    'additionalProperties': False,
                },
            },
            'required': ['status', 'message', 'result'],
            'additionalProperties': False,
        }

    def get(self, data_id):
        return {
            'message': 'success',
            'status': 200,
            'result': {
                'id': data_id,
                'value': 42,
            },
        }


class UpdateSampleHandler(BaseJsonHandler):
    """
    Update
    ======

    Dataを更新する.
    """

    @classmethod
    def request_schema(cls, method=None):
        return {
            'type': 'object',
            'properties': {
                'value': {
                    'type': 'string',
                },
            },
            'required': ['value'],
            'additionalProperties': False,
        }

    @classmethod
    def response_schema(cls, method=None):
        return {
            'type': 'object',
            'properties': {
                'status': {
                    'type': 'integer',
                },
                'message': {
                    'type': 'string',
                },
            },
            'required': ['status', 'message'],
            'additionalProperties': False,
        }

    def put(self, data_id):
        params = self.request_body
        print(params)
        return {
            'message': 'success',
            'status': 200,
        }
