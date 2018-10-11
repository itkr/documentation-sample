# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from webapp2 import Route

from .handlers import GetSampleHandler, UpdateSampleHandler


routes = (
    Route('/<data_id>', GetSampleHandler, methods=['GET']),
    Route('/<data_id>', UpdateSampleHandler, methods=['PUT']),
)
