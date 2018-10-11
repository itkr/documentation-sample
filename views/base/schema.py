# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


def make_error_response_schema():
    return {
        'type': 'object',
        'properties': {
            'status': {
                'type': 'integer',
                'multipleOf': 1,
                'minimum': 300,
                'maximum': 600,
                'exclusiveMaximum': True,
                'examples': [404],
            },
            'message': {
                'type': 'string',
                'examples': ['Not Found'],
            },
        },
        'required': ['status', 'message']
    }
