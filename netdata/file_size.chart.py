# -*- coding: utf-8 -*-
# Description: file_size netdata python.d module
# Author: zarak
# SPDX-License-Identifier: GPL-3.0-or-later

from bases.FrameworkServices.SimpleService import SimpleService
import os

ORDER = [
    'file_size',
]

CHARTS = {
    'file_size': {
        'options': [None, 'File size', 'kb', 'file_size',
                    'file_size', 'line'],
        'lines': [
            ['file_size']
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.path = self.configuration.get('path', None)

    def _get_data(self):
        try:
            raw = os.path.getsize(self.path)
            return {'file_size': raw / 1024}
        except:
            return None
