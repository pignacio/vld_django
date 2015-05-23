#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import logging

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class ExceptionLoggingMiddleware(object):
    def process_exception(self, request, exception):
        logging.exception('Whoops@%s', request.path)
