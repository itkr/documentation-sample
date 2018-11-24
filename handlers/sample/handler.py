# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os

from handlers.base import BaseJsonHandler


def _get_schema(file_name):
    path = os.path.join(os.path.dirname(__file__), 'schemas', file_name)
    with open(path, 'r') as f:
        return json.loads(f.read())


class GetSampleHandler(BaseJsonHandler):
    """
    Get Sample
    ==========

    Dataを一つ取得する.

    .. code-block:: python

        # sample code block
        for i in range(10):
            print(i)
    """

    @classmethod
    def response_schema(cls, method=None):
        return _get_schema('get_sample_response.json')

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
    Update Sample
    =============

    Dataを更新する.
    """

    @classmethod
    def request_schema(cls, method=None):
        return _get_schema('update_sample_request.json')

    @classmethod
    def response_schema(cls, method=None):
        return _get_schema('update_sample_response.json')

    def put(self, data_id):
        params = self.request_body
        print(params)
        return {
            'message': 'success',
            'status': 200,
        }
