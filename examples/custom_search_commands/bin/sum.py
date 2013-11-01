#!/usr/bin/env python
#
# Copyright 2011-2012 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from splunklib.searchcommands import ReportingCommand, Configuration, Option
from splunklib.searchcommands.validators import Fieldname
import logging as log
import sys


@Configuration(clear_required_fields=True, requires_preop=True)
class SumCommand(ReportingCommand):
    """ Computes the sum of a set of fields

    **Syntax:** sum total=*<fieldname>* [*<fieldname>*]...
    **Description:** The total produced is sum(sum(fieldname, 1, n), 1, N) where
    n = number of fields, N = number of records.

    """
    total = Option(require=True, validate=Fieldname(), doc='''
        **Syntax:** **total=***<fieldname>*
        **Description:** Name of the field that will hold the computed sum''')

    @Configuration(clear_required_fields=False)
    def map(self, records):
        """ Computes sum(fieldname, 1, n) and stores the result in 'total' """
        log.debug('Map.configuration=%s' % self.map.configuration)
        total = 0.0
        for record in records:
            for fieldname in self.fieldnames:
                total += float(record[fieldname])
        yield {self.total: total}

    def reduce(self, events):
        """ Computes sum(total, 1, N) and stores the result in 'total' """
        log.debug('Reduce.configuration=%s' % self.configuration)
        total = 0.0
        for event in events:
            total += float(event[self.total])
        yield {self.total: total}


if __name__ == '__main__':
    try:
        # TODO: Are command multi-use or single-use? The code below indicates
        # they are multi-use
        SumCommand().process(sys.argv, sys.stdin, sys.stdout)
    except:
        import traceback
        log.fatal(traceback.format_exc())