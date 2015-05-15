from __future__ import absolute_import, unicode_literals

import six

from .constants import XERO_REPORTS_URL
from .manager import Manager


class ReportsManager(Manager):
    DATE_FIELDS = (
        'date',
        'fromDate',
        'toDate'
    )

    BOOLEAN_FIELDS = (
        'standardLayout',
        'paymentsOnly'
    )

    def __init__(self, name, credentials):
        super(ReportsManager, self).__init__(name, credentials)
        self.base_url = self.base_url + XERO_REPORTS_URL

    def _get_results(self, data):
        response = data.get('Response')

        if response.get('Status') == 'OK':
            reports = response.get('Reports')

            if len(reports) > 1:
                return reports
            elif len(reports) == 1:
                return reports[0]

    def _filter(self, **kwargs):
        params = self.extra_params.copy()
        headers = None
        uri = '/'.join([self.base_url, self.name])

        for key, value in six.iteritems(kwargs):
            if key in self.BOOLEAN_FIELDS:
                value = ('true' if value is True else 'false'
                         if value is False else '')
            elif key in self.DATE_FIELDS:
                value = value.isoformat()

            params[key] = value

        return uri, params, 'get', None, headers, False
